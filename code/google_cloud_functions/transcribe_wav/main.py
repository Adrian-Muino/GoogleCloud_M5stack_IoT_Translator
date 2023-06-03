import base64
import requests

def transcribe_wav(encoded_audio, language_code):
    api_key = 'AIzaSyBQXF-YzRFaUFfpOAA7bznV0z4ncw1jpn0'
    url = 'https://speech.googleapis.com/v1/speech:recognize?key=' + api_key

    headers = {'Content-Type': 'application/json'}

    data = {
        'config': {
            'language_code': language_code
        },
        'audio': {
            'content': encoded_audio
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            transcription = response.json()['results'][0]['alternatives'][0]['transcript']
            return transcription
        else:
            return "Error in transcription"
    except Exception as e:
        return str(e)
