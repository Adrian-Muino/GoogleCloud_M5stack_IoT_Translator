import requests
import traceback
from google.cloud import bigquery
import json
from datetime import datetime, timedelta

def get_BCP47_language_tag(language_name):
    url = 'OUR_URL_ENDPOINT'
    method_name = 'get_BCP47_language_tag'
    endpoint = url + method_name
    params = {'language_input': language_name}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raises an exception if the request was unsuccessful
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def transcribe_wav(input_language_code, encoded_audio_file):
    url = 'OUR_URL_ENDPOINT/transcribe_wav'

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

    url = "OUR_URL_ENDPOINT/translate_text"

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

    url = 'OUR_URL_ENDPOINT/generate_audio_from_text'
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


# Construct a BigQuery client object.
project_id = 'OUR_PROJECT_ID'
client = bigquery.Client(project = project_id)

def send_data_to_bigquery(language_input_name, input_language_code , language_output_name , language_output_code , encoded_audio_file ,  transcribed_text , translated_text , encoded_output_audio_file):
    table_id = 'OUR_DATASET.usage_records'
    to_load = """{"language_input_name":"/","input_language_code":"?","language_output_name":"&","language_output_code":"~","encoded_audio_file":"#","transcribed_text":"!","translated_text":"$","encoded_output_audio_file":"@"}"""
    to_load = to_load.replace("/",language_input_name)
    to_load = to_load.replace("?",input_language_code)
    to_load = to_load.replace("&",language_output_name)
    to_load = to_load.replace("~",language_output_code)
    to_load = to_load.replace("#",encoded_audio_file)
    to_load = to_load.replace("!",transcribed_text)
    to_load = to_load.replace("$",translated_text)
    to_load = to_load.replace("@",str(encoded_output_audio_file))

    rows_to_insert = [json.loads(to_load)]

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New usage record has been added to BigQuery.")
    else:
        print("Encountered errors while inserting rows in usage records: {}".format(errors))

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

        send_data_to_bigquery(language_input_name, input_language_code , language_output_name , language_output_code , encoded_audio_file ,  transcribed_text , translated_text , encoded_output_audio_file)

        return encoded_output_audio_file

    except Exception as e:
        traceback.print_exc()
        return "Internal server error", 500
