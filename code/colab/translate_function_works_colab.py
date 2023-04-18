import requests
import base64

# Set the URL of the Cloud Function endpoint
url = 'https://europe-central2-iottranslator.cloudfunctions.net/translate_text'

# Set the input and output languages
language_input = 'en-US'
language_output = 'fr'

# Get the transcription from the Speech-to-Text API
with open('/content/sound1.wav', 'rb') as f:
    content = f.read()
audio_content = base64.b64encode(content).decode('utf-8')
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'transcription': transcription, 'language_input': language_input, 'language_output': language_output}
response = requests.post(url, headers=headers, data=data)

# Print the translated text
if response.status_code == 200:
    translation = response.text
    print(translation)
else:
    print('Error:', response.content)
