import requests
import base64

def trigger_iotTranslator_cloud_functions(request):
    request_json = request.get_json()
    language_input_name = request_json['language_input_name']
    language_output_name = request_json['language_output_name']
    encoded_audio = request_json['encoded_audio']

    main_path = "https://europe-central2-iottranslator.cloudfunctions.net"

    # Call get_BCP47_language_tag with language_input_name
    response = requests.get(f"{main_path}/get_BCP47_language_tag?language={language_input_name}")
    language_input_BCP47_tag = response.text

    # Call get_BCP47_language_tag with language_output_name
    response = requests.get(f"{main_path}/get_BCP47_language_tag?language={language_output_name}")
    language_output_BCP47_tag = response.text

    # Call get_ISO639_language_tag with language_input_name
    response = requests.get(f"{main_path}/get_ISO639_language_tag?language={language_input_name}")
    language_input_ISO639_tag = response.text

    # Call get_ISO639_language_tag with language_output_name
    response = requests.get(f"{main_path}/get_ISO639_language_tag?language={language_output_name}")
    language_output_ISO639_tag = response.text

    # Call transcribe_wav with encoded_audio and language_input_BCP47_tag
    response = requests.post(f"{main_path}/transcribe_wav", json={'audio': encoded_audio, 'language': language_input_BCP47_tag})
    transcribed_output = response.text

    # Call translate_text with language_input_ISO639_tag and language_output_ISO639_tag
    response = requests.post(f"{main_path}/translate_text", json={'input_lang': language_input_ISO639_tag, 'output_lang': language_output_ISO639_tag})
    translated_output = response.text

    # Call say_translated_text with translated_output and language_output_BCP47_tag
    response = requests.post(f"{main_path}/say_translated_text", json={'text': translated_output, 'language': language_output_BCP47_tag})
    encoded_output_audio = response.text

    return encoded_output_audio
