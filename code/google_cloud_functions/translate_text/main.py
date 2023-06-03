import requests
import json

def translate_text(request):
    request_json = request.get_json()
    language_input = request_json['language_input']
    language_output = request_json['language_output']
    transcribed_text = request_json['transcribed_text']
    api_key = 'AIzaSyBQXF-YzRFaUFfpOAA7bznV0z4ncw1jpn0'
    url = 'https://translation.googleapis.com/language/translate/v2?key=' + api_key

    data = {'q': [transcribed_text], 'source': language_input, 'target': language_output}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            translation = response.json()['data']['translations'][0]['translatedText']
            return json.dumps({'translated_text': translation})
        else:
            return json.dumps({'error': 'Error in translate: ' + str(response.status_code)})
    except Exception as e:
        return json.dumps({'error': 'Error in translate: ' + str(e)})
