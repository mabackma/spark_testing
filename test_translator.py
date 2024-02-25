from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os


app = Flask(__name__)
CORS(app)
load_dotenv()

# chat-gpt
client = OpenAI(api_key=os.getenv("CHAT_GPT_KEY"))

# returns english translation using chat-GPT
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


if __name__ == "__main__":

    app.run(debug=True, port=5001)