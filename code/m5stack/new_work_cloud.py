######### Imports #########

from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5stack import mic
import urequests
import base64
import re
import wifiCfg
import time
import machine
import uos

################################################ WIFI settings ################################################

# Configure and connect to Wi-Fi network

#wifiCfg.doConnect('SSID', 'PSW')  # UPDATE SSID & PSW with your Wi-Fi credentials
#while not (wifiCfg.wlan_sta.isconnected()):
#  wait(1)
#  print('Waiting connect')
#print('Connected')

################################################ INIT  ################################################ 


######### Init Default Screen #########

# Screen default
screen = M5Screen()
screen.clean_screen()

# Set background color
screen.set_screen_bg_color(0x0b0c14) 

# Set lateral light color
rgb.setColorAll(0x33ff33) 

######### Init Buttons #########

# Starting / Menu screen components
start_button = M5Btn(text='START', x=90, y=199, w=140, h=30, bg_c=0x03a9f4, text_c=0xffffff, font=FONT_MONT_18, parent=None)

# Translate / Main screen components
language_button = M5Btn(text='CHOOSE LANGUAGE', x=25, y=61, w=270, h=44, bg_c=0x1d54bd, text_c=0xffffff, font=FONT_MONT_18, parent=None)
record_button = M5Btn(text='RECORD', x=25, y=126, w=96, h=98, bg_c=0x9b0000, text_c=0xffffff, font=FONT_MONT_18, parent=None)
repeat_button = M5Btn(text='REPEAT', x=146, y=126, w=149, h=39, bg_c=0x626262, text_c=0xffffff, font=FONT_MONT_18, parent=None)
translate_button = M5Btn(text='TRANSLATE', x=146, y=185, w=149, h=39, bg_c=0x03a9f4, text_c=0xffffff, font=FONT_MONT_18, parent=None)

# Settings screen components
save_button = M5Btn(text='SAVE', x=111, y=196, w=97, h=29, bg_c=0x03a9f4, text_c=0xffffff, font=FONT_MONT_18, parent=None)

######### Init Images #########

# Starting / Menu screen components
menu_image = M5Img("res/Menu_285x195px.png", x=17, y=0, parent=None)

# Translate / Main screen components & Recording screen components
logo_image = M5Img("res/Logo_34x34pxpng.png", x=25, y=16, parent=None)
recording_image = M5Img("res/Recording_151x151px.png", x=86, y=56, parent=None)

# Settings screen components
settings_logo_image = M5Img("res/Logo_34x34pxpng.png", x=30, y=16, parent=None)

# Translating Screen
translating_logo_image = M5Img("res/Logo_34x34pxpng.png", x=25, y=16, parent=None)
translating_image = M5Img("res/Translating_151x151px.png", x=86, y=56, parent=None)

######### Init Labels #########

# Translate / Main screen components
logo_text = M5Label('uTranslate', x=71, y=26, color=0xffffff, font=FONT_MONT_14, parent=None)

# Recording screen components
recording_text = M5Label('Recording ...', x=76, y=26, color=0xffffff, font=FONT_MONT_14, parent=None)

# Settings screen components
choose_language_text = M5Label('Choose the languages', x=76, y=26, color=0xffffff, font=FONT_MONT_14, parent=None)

# Translating Screen components
translating_text = M5Label('Translating ...', x=76, y=26, color=0xffffff, font=FONT_MONT_14, parent=None)

# DEBUG Main Screen
transcribed_output = M5Label('transcribed_output', x=5, y=20, color=0xffffff, font=FONT_MONT_10, parent=None)
translated_output = M5Label('translated_text', x=5, y=40, color=0xffffff, font=FONT_MONT_10, parent=None)


################################################ Global  ################################################ 

# Variable for calling the cloud functions

base_url = https://europe-central2-iottranslator.cloudfunctions.net/


# Variables related to the audio files

input_audio = ""
encoded_input_audio = ""

output_audio = ""
encoded_output_audio = ""

# Variables related to the languages

language_input_name = ''
language_input_BCP47_tag = ''
language_input_ISO639_tag = ''

language_output_name = ''
language_output_BCP47_tag = ''
language_output_ISO639_tag = ''

# Variables to store the results of the cloud functions
transcribed_output = ""
translated_output = ""




# Function to call the get_BCP47_language_tag Cloud Function
def call_get_BCP47_language_tag(language_name):
    url = base_url + '/get_BCP47_language_tag'
    payload = {'language_name': language_name}
    response = urequests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        language_tag = data['BCP47_language_tag']
        print('Language Tag:', language_tag)
    else:
        print('Error:', response.status_code)

# Function to call the get_ISO639_language_tag Cloud Function
def call_get_ISO639_language_tag(language_name):
    url = base_url + '/get_ISO639_language_tag'
    payload = {'language_name': language_name}
    response = urequests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        language_tag = data['iso639_language_tag']
        print('Language Tag:', language_tag)
    else:
        print('Error:', response.status_code)

# Function to call the translate_text Cloud Function
def call_translate_text(language_input, language_output, transcribed_text):
    url = base_url + '/translate_text'
    payload = {
        'language_input': language_input,
        'language_output': language_output,
        'transcribed_text': transcribed_text
    }
    response = urequests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        translated_text = data['translated_text']
        print('Translated Text:', translated_text)
    else:
        print('Error:', response.status_code)

# Function to call the say_translated_text Cloud Function
def call_say_translated_text(translated_text, language_output):
    url = base_url + '/say_translated_text'
    payload = {
        'translated_text': translated_text,
        'language_output': language_output
    }
    response = urequests.post(url, json=payload)
    if response.status_code == 200:
        print('Audio file saved successfully.')
    else:
        print('Error:', response.status_code)

def decode_audio_content(encoded_audio):
            audio_content = base64.b64decode(encoded_audio)

