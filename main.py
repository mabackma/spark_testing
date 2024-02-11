import json
import os
import sparknlp_jsl
from sparknlp_jsl.annotator import *
import pandas as pd
import warnings
from sparknlp.pretrained import ResourceDownloader
import subprocess
from laymen_summary import summarizer_clinical_laymen_onnx_pipeline
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
import whisper

app = Flask(__name__)
CORS(app)
load_dotenv()

# temporary folder to store uploaded file
UPLOAD_FOLDER = 'C:/temp_whisper_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/stt', methods=['POST'])
def speech_to_text_api():
    try:
        if 'speech' not in request.files:
            return 'No file part'

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
        summarizer_clinical_laymen_onnx_pipeline(result.text)
        return result.text


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

    app.run(debug=True)