from dotenv import load_dotenv
from flask import Flask, request as req, jsonify
from flask_cors import CORS
import requests, uuid
import os


app = Flask(__name__)
CORS(app)
load_dotenv()

# microsoft translator
key = os.getenv('AZURE_KEY2')
url = "https://api.cognitive.microsofttranslator.com/translate"
location = 'northeurope'

# returns english translation using microsoft
@app.route('/microsoft-translation', methods=['POST'])
def microsoft_translation():
    try:
        data = req.json

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

                request = requests.post(url, params=params, headers=headers, json=body)
                response = request.json()
                print(response)
                return jsonify({'translation': response[0]['translations'][0]['text']})
            else:
                return 'Error: No language provided in JSON data'
        else:
            return 'Error: No text provided in JSON data'

    except Exception as e:
        return f'Error: {e}'


if __name__ == "__main__":

    app.run(debug=True, port=5001)