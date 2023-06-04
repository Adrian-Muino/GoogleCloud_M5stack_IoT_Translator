import requests
import html

def translate_text(request):
    request_json = request.get_json()
    if request_json and 'transcribed_text' in request_json and 'input_language_code' in request_json and 'output_language_code' in request_json:
        transcribed_text = request_json['transcribed_text']
        input_language_code = request_json['input_language_code']
        output_language_code = request_json['output_language_code']

        api_key = "OUR_API_KEY"
        url = "https://translation.googleapis.com/language/translate/v2?key="

        request_url = f"{url}{api_key}"
        data = {
            "q": transcribed_text,
            "source": input_language_code,
            "target": output_language_code
        }

        response = requests.post(request_url, data=data)
        translated_text = response.json()["data"]["translations"][0]["translatedText"]
        unescaped_text = html.unescape(translated_text)

        return {"translated_text": unescaped_text}
    else:
        return {"error": "Invalid request. Please provide 'transcribed_text', 'input_language_code', and 'output_language_code' in the request body."}
