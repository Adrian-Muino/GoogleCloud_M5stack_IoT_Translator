import requests
import traceback

def get_BCP47_language_tag(language_name):
    url = 'OUR_GOOGLE_CLOUD_FUNCTION_URL/get_BCP47_language_tag'

    params = {'language_input': language_name}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an exception if the request was unsuccessful
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def transcribe_wav(input_language_code, encoded_audio_file):
    url = 'OUR_GOOGLE_CLOUD_FUNCTION_URL/transcribe_wav'

    # Create the request payload
    payload = {
        'input_language_code': input_language_code,
        'encoded_audio_file': encoded_audio_file
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            transcription = response.text
            return transcription
        else:
            return 'Error in transcription: ' + response.text, response.status_code
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def translate_text(transcribed_text,input_language_code,language_output_code):

    url = "OUR_GOOGLE_CLOUD_FUNCTION_URL/translate_text"

    payload = {
        "transcribed_text": transcribed_text,
        "input_language_code": input_language_code,
        "output_language_code": language_output_code
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        translated_text = data.get("translated_text")
        if translated_text:
            return translated_text
        else:
            error = data.get("error")
            return f"Translation error: {error}"
    else:
        return "Error occurred while making the request.", response.status_code

def generate_audio_from_text(translated_text, output_language_code):

    url = 'OUR_GOOGLE_CLOUD_FUNCTION_URL/generate_audio_from_text'
    data = {
        'translated_text': translated_text,
        'output_language_code': output_language_code
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            audio_content = response.content
            # Process the audio content as needed
            return audio_content
        else:
            return "Error: " + str(response.status_code) + "\n" + response.content.decode("utf-8"), response.status_code
    except Exception as e:
        return "Error: " + str(e), 500

import traceback

def trigger_iotTranslator_cloud_functions(request):
    try:
        if request.method != 'POST':
            return 'Method not allowed', 405

        data = request.get_json()
        language_input_name = data.get('language_input_name')
        language_output_name = data.get('language_output_name')
        encoded_audio_file = data.get('encoded_audio_file')

        if not language_input_name or not language_output_name or not encoded_audio_file:
            return 'Invalid request payload', 400

        input_language_code = get_BCP47_language_tag(language_input_name)
        print("input_language_code : " + input_language_code)

        language_output_code = get_BCP47_language_tag(language_output_name)
        print("language_output_code :" + language_output_code)

        transcribed_text = transcribe_wav(input_language_code, encoded_audio_file)
        print("transcribed_text : " + transcribed_text)

        translated_text = translate_text(transcribed_text, input_language_code, language_output_code)
        print("translated_text : " + translated_text)

        encoded_output_audio_file = generate_audio_from_text(translated_text, language_output_code)

        return encoded_output_audio_file

    except Exception as e:
        traceback.print_exc()
        return "Internal server error", 500