import json
import os
import sparknlp_jsl
from google.cloud import translate_v3
from sparknlp_jsl.annotator import *
import pandas as pd
import warnings
from sparknlp.pretrained import PretrainedPipeline
import subprocess
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from make_summary import make_summary
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request as AuthRequest
from transformers import MarianMTModel, MarianTokenizer
from openai import OpenAI
import requests, uuid


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

# Load the pre-trained MarianMT model and tokenizer for translation finnish to english
tokenizer_fi_en = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fi-en")
model_fi_en = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-fi-en")
# Load the pre-trained MarianMT model and tokenizer for translation english to finnish
tokenizer_en_fi = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fi")
model_en_fi = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-fi")

# chat-gpt
client = OpenAI(api_key=os.getenv("CHAT_GPT_KEY"))

# microsoft translator
key = os.getenv('AZURE_KEY2')
url = "https://api.cognitive.microsofttranslator.com/translate"
location = 'northeurope'

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


# returns translation using chat-GPT
@app.route('/chatgpt-translation', methods=['POST'])
def chatgpt_translation():
    try:
        data = request.json

        if 'text' in data:
            if 'targetLanguage' in data:
                prompt = f"Translate the following text into {data['targetLanguage']}: {data['text']}"
                print(prompt)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="gpt-3.5-turbo"
                )

                reply = chat_completion.choices[0].message.content
                print(reply)
                return jsonify({'translation': reply})
            else:
                return 'Error: No language provided in JSON data'
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


# returns translation using google cloud translation
@app.route('/translate-in-google', methods=['POST'])
def translate_in_google():
    try:
        data = request.json

        if 'text' in data:
            # Replace with your target language and text
            target_language = data['targetLanguage']
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
            print(translated_text)
            return jsonify({'translation': translated_text})
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


# returns english translation using microsoft
@app.route('/microsoft-translation', methods=['POST'])
def microsoft_translation():
    try:
        data = request.json

        if 'text' in data:
            if 'targetLanguage' in data:
                body = [{
                    'text': data['text']
                }]

                params = {
                    'api-version': '3.0',
                    'to': [data['targetLanguage']]
                }

                headers = {
                    'Ocp-Apim-Subscription-Key': key,
                    'Ocp-Apim-Subscription-Region': location,
                    'Content-type': 'application/json',
                    'X-ClientTraceId': str(uuid.uuid4())
                }

                result = requests.post(url, params=params, headers=headers, json=body)
                response = result.json()
                print(response)
                return jsonify({'translation': response[0]['translations'][0]['text']})
            else:
                return 'Error: No language provided in JSON data'
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


# returns english translation using marianmt.
@app.route('/marianmt-fi-en', methods=['POST'])
def marianmt_fi_en():
    try:
        data = request.json

        if 'text' in data:
            text = data['text']

            # Tokenize input text
            inputs = tokenizer_fi_en(text, return_tensors="pt", max_length=512, truncation=True)

            # Generate translation
            translation_ids = model_fi_en.generate(**inputs)

            # Decode the generated translation
            translated_text = tokenizer_fi_en.decode(translation_ids[0], skip_special_tokens=True)
            print(translated_text)
            return jsonify({'translation': translated_text})
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


# returns finnish translation using marianmt.
@app.route('/marianmt-en-fi', methods=['POST'])
def marianmt_en_fi():
    try:
        data = request.json

        if 'text' in data:
            text = data['text']

            # Tokenize input text
            inputs = tokenizer_en_fi(text, return_tensors="pt", max_length=512, truncation=True)

            # Generate translation
            translation_ids = model_en_fi.generate(**inputs)

            # Decode the generated translation
            translated_text = tokenizer_en_fi.decode(translation_ids[0], skip_special_tokens=True)
            print(translated_text)
            return jsonify({'translation': translated_text})
        else:
            return 'Error: No text provided in JSON data'

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
    #ResourceDownloader.showPublicPipelines(lang="en")

    # Show installation versions
    java_version = get_java_version()
    print("Java version:", java_version)
    print("Apache Spark version:", spark_session.version)
    print("Spark NLP Version :", sparknlp.version())
    print("Spark NLP_JSL Version :", sparknlp_jsl.version())

    # download pipeline for summarization
    pipeline = PretrainedPipeline("summarizer_clinical_laymen_onnx_pipeline", "en", "clinical/models")

    app.run(debug=True, port=5001)