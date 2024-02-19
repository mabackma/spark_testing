import json
import os
import sparknlp_jsl
from google.cloud import translate_v3
from sparknlp_jsl.annotator import *
import pandas as pd
import warnings
from sparknlp.pretrained import ResourceDownloader, PretrainedPipeline
import subprocess
from laymen_summary import summarizer_clinical_laymen_onnx_pipeline
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
from make_summary import make_summary
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request as AuthRequest

app = Flask(__name__)
CORS(app)
load_dotenv()

# Google translate api key
translate_api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
# Google credentials
credentials = Credentials.from_service_account_file('key.json', scopes=['https://www.googleapis.com/auth/cloud-translation'])
# Refresh credentials if needed
if not credentials.valid:
    authRequest = AuthRequest()
    credentials.refresh(authRequest)

# temporary folder to store uploaded file
UPLOAD_FOLDER = 'C:/temp_whisper_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Returns the Java version that is running
def get_java_version():
    try:
        # Run the command to get the Java version
        result = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
        lines = result.splitlines()
        for line in lines:
            line = line.decode('utf-8')
            if line.startswith('java version'):
                return line.split()[2].replace('"', '')
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode('utf-8'))

def start_spark_session():
    with open('spark_jsl.json') as f:
        license_keys = json.load(f)

    os.environ["SPARK_NLP_LICENSE"] = license_keys['SPARK_NLP_LICENSE']

    pd.set_option('display.max_colwidth', 200)
    warnings.filterwarnings('ignore')
    params = {"spark.driver.memory": "16G",
              "spark.kryoserializer.buffer.max": "2000M",
              "spark.driver.maxResultSize": "2000M"}

    return sparknlp_jsl.start(license_keys['SECRET'], params=params)


def summarize(pipeline, input_text):
    result = pipeline.fullAnnotate(input_text)
    summary = make_summary(result, 'NLP 5.2.0+ CLINICAL LAYMEN ONNX PIPELINE')
    return summary


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


# returns finnish translation using google cloud translation
@app.route('/translate-in-google', methods=['POST'])
def translate_in_google():
    try:
        data = request.json

        if 'text' in data:
            # Replace with your target language and text
            target_language = "fi"
            text = data['text']

            # Create a Translation object
            client = translate_v3.TranslationServiceClient(credentials=credentials)

            # Build the request
            request_obj = translate_v3.TranslateTextRequest(
                parent="projects/noble-sun-414214/locations/global",
                contents=[text],
                target_language_code=target_language,
            )

            # Send the request and process the response
            response = client.translate_text(request=request_obj)

            # Get the translated text
            translated_text = response.translations[0].translated_text
            return jsonify({'translation': translated_text})
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


# speech-to-text
@app.route('/stt-summary', methods=['POST'])
def speech_to_text_api():
    try:
        if 'speech' not in request.files:
            return 'No file part'

        # the request should include a file with a key 'speech'
        audio_file = request.files['speech']
        if audio_file.filename == '':
            return 'No selected file'

        # Save the uploaded file with a unique filename
        unique_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_audio.wav')
        audio_file.save(unique_filename)

        model = whisper.load_model("base")

        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(unique_filename)
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)
        print(f"filename: {audio_file.filename}")
        print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)

        # summarize the text
        summary = summarizer_clinical_laymen_onnx_pipeline(result.text)

        # Convert the summary into a JSON serializable format
        summary_json = str(summary)

        # Return the summary as JSON
        return jsonify({'summary': summary_json})

    except Exception as e:
        return f'Error: {e}'


@app.before_request
def parse_json():
    if request.method == 'POST' and request.path == '/summary':
        if request.content_type == 'application/json':
            request.json_data = request.get_json()
# returns summary from text
@app.route('/summary', methods=['POST'])
def text_to_summary_api():
    try:
        data = request.json

        if 'text' in data:
            text_content = data['text']

            # summarize the text
            summary = summarize(pipeline, text_content)
            return jsonify({'summary': summary})
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


if __name__ == "__main__":
    # Start the Spark session
    spark_session = start_spark_session()

    # Show available pipelines
    ResourceDownloader.showPublicPipelines(lang="en")

    # Show installation versions
    java_version = get_java_version()
    print("Java version:", java_version)
    print("Apache Spark version:", spark_session.version)
    print("Spark NLP Version :", sparknlp.version())
    print("Spark NLP_JSL Version :", sparknlp_jsl.version())

    # download pipeline for summarization
    pipeline = PretrainedPipeline("summarizer_clinical_laymen_onnx_pipeline", "en", "clinical/models")

    app.run(debug=True)