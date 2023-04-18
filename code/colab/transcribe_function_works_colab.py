# Template for the cloud function
import requests
import base64

# Set the URL of the Speech-to-Text API endpoint
url = 'https://speech.googleapis.com/v1/speech:recognize'

# Set the API key and language code
api_key = ' AIzaSyBQXF-YzRFaUFfpOAA7bznV0z4ncw1jpn0'
language_code = 'en-US'

# Read the content of the WAV file
with open('/content/sound1.wav', 'rb') as f:
    content = f.read()

# Encode the content as base64
audio_content = base64.b64encode(content).decode('utf-8')

# Set the request headers
headers = {'Content-Type': 'application/json'}

# Set the request data
data = {
    'config': {
        'language_code': language_code
    },
    'audio': {
        'content': audio_content
    }
}

# Send the HTTP request to the Speech-to-Text API
params = {'key': api_key}
response = requests.post(url, headers=headers, params=params, json=data)

# Print the transcription
if response.status_code == 200:
    transcription = response.json()['results'][0]['alternatives'][0]['transcript']
    print(transcription)
else:
    print('Error:', response.content)
