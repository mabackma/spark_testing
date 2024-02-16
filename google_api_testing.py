from google.cloud import translate_v3
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

from data import *

credentials = Credentials.from_service_account_file('key.json', scopes=['https://www.googleapis.com/auth/cloud-translation'])

# Refresh credentials if needed
if not credentials.valid:
    request = Request()
    credentials.refresh(request)

# Replace with your target language and text
target_language = "en"
text = input5

# Create a Translation object
client = translate_v3.TranslationServiceClient(credentials=credentials)

# Build the request
request = translate_v3.TranslateTextRequest(
    parent="projects/noble-sun-414214/locations/global",
    contents=[text],
    target_language_code=target_language,
)

# Send the request and process the response
response = client.translate_text(request=request)

# Get the translated text
translated_text = response.translations[0].translated_text

print(f"original text: {input5}\n")
print(f"Translated text: {translated_text}")
