from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)
CORS(app)
load_dotenv()

# Load the pre-trained MarianMT model and tokenizer for translation finnish to english
tokenizer_fi_en = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fi-en")
model_fi_en = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-fi-en")

# Load the pre-trained MarianMT model and tokenizer for translation english to finnish
tokenizer_en_fi = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fi")
model_en_fi = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-fi")

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return "hello world!"

# returns english translation using marianmt
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


# returns finnish translation using marianmt
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



if __name__ == "__main__":

    app.run(debug=True, port=5001)