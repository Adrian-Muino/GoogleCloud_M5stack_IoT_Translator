import base64
import requests

def generate_audio_from_text(request):
    request_json = request.get_json()
    translated_text = request_json['translated_text']
    output_language_code = request_json['output_language_code']

    api_key = "AIzaSyBQXF-YzRFaUFfpOAA7bznV0z4ncw1jpn0"
    url = 'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + api_key
    data = {
        'input': {'text': translated_text},
        'voice': {'languageCode': output_language_code, 'ssmlGender': 'FEMALE'},
        'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': 16000}
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            audio_content = base64.b64decode(response.json()['audioContent'])
            return audio_content
        else:
            return "Error in text-to-speech: " + str(response.status_code) + "\n" + response.content.decode("utf-8")
    except Exception as e:
        return "Error in text-to-speech: " + str(e)
