import base64
import requests

def say_translated_text(request):
    api_key = 'AIzaSyBQXF-YzRFaUFfpOAA7bznV0z4ncw1jpn0'
    
    # Set the URL of the Cloud Text-to-Speech API endpoint
    url = 'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + api_key

    # Get the translated text and language from the request JSON
    request_json = request.get_json()
    translated_text = request_json['translated_text']
    language_output_ui = request_json['language_output_ui']

    # Set the request data
    data = {
        'input': {'text': translated_text},
        'voice': {'languageCode': language_output_ui, 'ssmlGender': 'FEMALE'},
        'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': 16000}
    }

    # Set the request headers
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # Encode the audio content to base64
            audio_content = base64.b64encode(response.content).decode('utf-8')
            return audio_content
        else:
            return "Error in text-to-speech API request: " + str(response.status_code)
    except Exception as e:
        return "Error in text-to-speech API request: " + str(e)
