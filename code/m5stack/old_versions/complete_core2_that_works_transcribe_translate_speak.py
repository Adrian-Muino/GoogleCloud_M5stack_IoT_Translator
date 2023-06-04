######### Imports #########

from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5stack import mic
import urequests
import base64
import re

######### Default settings (screen & lateral light) #########

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xf0fcff)
rgb.setColorAll(0x33ff33) #lateral light

######### Buttons & labels in the screen #########

record_button = M5Btn(text='Record', x=0, y=100, w=80, h=140, bg_c=0x601a1a, text_c=0xffffff, font=FONT_MONT_18, parent=None)
repeat_button = M5Btn(text='Repeat', x=88, y=132, w=200, h=50, bg_c=0xd2ab6f, text_c=0x000000, font=FONT_MONT_18, parent=None)
translate_button = M5Btn(text='Translate', x=88, y=190, w=210, h=50, bg_c=0x3f804e, text_c=0xffffff, font=FONT_MONT_22, parent=None)
transcribed_output = M5Label('transcribed_text', x=5, y=20, color=0x000, font=FONT_MONT_10, parent=None)
translated_output = M5Label('translated_text', x=5, y=40, color=0x000, font=FONT_MONT_10, parent=None)
say_translated_text_output = M5Label('say_translated_text_output', x=5, y=60, color=0x000, font=FONT_MONT_10, parent=None)

######### Global variables #########

transcribed_text = None
translated_text = None

language_input_ui = 'en'
language_output_ui = 'fr'

######### Record button pressed method #########

def record_button_pressed():
  # global params
  rgb.setColorAll(0x33ff33)
  mic.record2file(3, '/flash/sound1.wav')
  rgb.setColorAll(0xff0000)

record_button.pressed(record_button_pressed)

######### Repeat button pressed method #########

def repeat_button_pressed():
  # global params
  speaker.playWAV('/flash/sound2.wav', volume=6)
  rgb.setColorAll(0xffcc66)

repeat_button.pressed(repeat_button_pressed)

######### Translate button pressed method #########

def translate_button_pressed():
    transcribe_wav()
    assign_result_to_transcribed_text()
    translate_text()
    assign_result_to_translated_text()
    say_translated_text()

translate_button.pressed(translate_button_pressed) 

######### Transcribe method using Cloud #########

def transcribe_wav():
    # Set the API key and language code
    rgb.setColorAll(0x08deff)

    api_key = 'OUR_API_KEY'
    language_code = 'en-US'

    # Set the URL of the Speech-to-Text API endpoint  
    url = 'https://speech.googleapis.com/v1/speech:recognize?key=' + api_key

    # Read the content of the WAV file
    with open('/flash/sound1.wav', 'rb') as f:
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

    try:
        response = urequests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            transcription = response.json()['results'][0]['alternatives'][0]['transcript']
            global transcribed_text
            transcribed_text = html_unescape(transcription)
        else:
            global transcribed_text
            transcribed_text = "Error in transcribed method"
    except Exception as e:
        transcription_output.set_text(str(e))
    rgb.setColorAll(0x33ff33)

######### Translate method using Cloud #########

def translate_text():
  api_key = 'OUR_API_KEY'
  # Set the URL of the Cloud Function endpoint
  url = 'https://translation.googleapis.com/language/translate/v2?key=' + api_key

  # Set the input and output languages
  global language_input_ui
  language_input = language_input_ui
  global language_output_ui
  language_output = language_output_ui

  # Set the request data
  global transcribed_text
  data = {'q': [transcribed_text], 'source': language_input, 'target': language_output}

  # Set the request headers
  headers = {'Content-Type': 'application/json'}

  try:
      response = urequests.post(url, headers=headers, json=data)
      if response.status_code == 200:
          translation = response.json()['data']['translations'][0]['translatedText']
          global translated_text
          translated_text = html_unescape(translation)
      else:
          global translated_text
          translated_text = "Error in translate: " + str(response.status_code)
  except Exception as e:
      global translated_text
      translated_text = "Error in translate: " + str(e)

######### Say translated text method using cloud  #########

def say_translated_text():
    api_key = 'OUR_API_KEY'
    # Set the URL of the Cloud Text-to-Speech API endpoint
    url = 'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + api_key

    # Set the request data
    global translated_text
    global language_output_ui

    data = {
        'input': {'text': translated_text},
        'voice': {'languageCode': language_output_ui, 'ssmlGender': 'FEMALE'},
        'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': 16000}
    }

    # Set the request headers
    headers = {'Content-Type': 'application/json'}

    try:
        response = urequests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # Decode the audio content from base64 and save it to a file
            audio_content = base64.b64decode(response.json()['audioContent'])
            with open('/flash/sound2.wav', 'wb') as f:
                f.write(audio_content)
            # Play the audio file
            repeat_button_pressed()
        else:
            global say_translated_text_output
            say_translated_text_output = "Error in translate: " + str(response.status_code)
    except Exception as e:
        global translated_text_output
        translated_text_output = "Error in translate: " + str(e)

######### Assign result to transcribed label method #########

def assign_result_to_transcribed_text():
    global transcribed_text
    transcribed_output.set_text(str(transcribed_text))

######### Assign result to translation label method #########

def assign_result_to_translated_text():
    global translated_text
    translated_output.set_text(str(translated_text))

######### Html_unsecape method to avoid encoding errors because the responses are encoded in html and we need them in plain text #########

def html_unescape(s):
    s = s.replace("&amp;", "&")
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", "\"")
    s = s.replace("&#39;", "'")
    s = re.sub("&#(\d+);", lambda m: chr(int(m.group(1))), s)
    return s


