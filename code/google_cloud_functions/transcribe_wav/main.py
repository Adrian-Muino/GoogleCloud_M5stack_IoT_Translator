import requests
import json


def transcribe_wav(request):
    request_json = request.get_json()
    input_language_code = request_json['input_language_code']
    encoded_audio_file = request_json['encoded_audio_file']

    api_key = 'OUR_API_KEY'
    url = 'https://speech.googleapis.com/v1/speech:recognize?key=' + api_key

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'config': {
            'languageCode': input_language_code
        },
        'audio': {
            'content': encoded_audio_file
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
