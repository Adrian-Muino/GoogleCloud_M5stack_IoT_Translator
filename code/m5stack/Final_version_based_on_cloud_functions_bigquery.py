######### Imports #########

from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5stack import mic
import urequests as requests
import base64
import wifiCfg
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
from_text = M5Label('FROM', x=25, y=75, color=0xffffff, font=FONT_MONT_18, parent=None)
to_text = M5Label('TO', x=40, y=145, color=0xffffff, font=FONT_MONT_18, parent=None)

# Translating Screen components
translating_text = M5Label('Translating ...', x=76, y=26, color=0xffffff, font=FONT_MONT_14, parent=None)

# Main screen components
#language_from_text = M5Label('FROM', x=165, y=15, color=0xffffff, font=FONT_MONT_10, parent=None)
#language_to_text = M5Label('TO', x=170, y=30, color=0xffffff, font=FONT_MONT_10, parent=None)

######### Init Dropdown Menu #########

# Language Selection
language_names = {
    'Arabic' : 'Arabic',
    'Chinese' : 'Chinese',
    'Croatian' : 'Croatian',
    'Danish' : 'Danish',
    'English' : 'English',
    'Estonian' : 'Estonian',
    'French' : 'French',
    'Galician' : 'Galician',
    'German' : 'German',
    'Greek' : 'Greek',
    'Hindi' : 'Hindi',
    'Italian' : 'Italian',
    'Japanese' : 'Japanese',
    'Korean' : 'Korean',
    'Polish' : 'Polish',
    'Portuguese' : 'Portuguese',
    'Russian' : 'Russian',
    'Spanish' : 'Spanish',
    'Swedish' : 'Swedish',
    'Turkish' : 'Turkish',
    'Ukrainian' : 'Ukrainian',
    'Vietnamese' : 'Vietnamese',
    }

options = list(language_names.keys())
options.sort()

input_language_dropdown = M5Dropdown(110, 65, 180, 40)
input_language_dropdown.set_options(options)
input_language_dropdown.set_sel_index(4)

output_language_dropdown = M5Dropdown(110, 135, 180, 40)
output_language_dropdown.set_options(options)
output_language_dropdown.set_sel_index(6)


################################################ Global  ################################################ 

# for method translate
language_input_name = 'English'
language_output_name = 'French'
encoded_audio_file = ''

# for method encode_wav
encoded_audio_file = ''

# for method decode_wav & GCF_trigger_iotTranslator_cloud_functions
encoded_audio_translated = ''


################################################ Interfaces ################################################

######### Starting / Menu Screen Interface ######### 

def show_menu_screen():

    # Set up the main screen components
    rgb.setColorAll(0x33ff33)

    # Show interface components
    start_button.set_hidden(False)
    menu_image.set_hidden(False)
    
def hide_menu_screen():

     # Set up the main screen components
    start_button.set_hidden(True)
    menu_image.set_hidden(True)

######### Main Screen Interface ######### 

def show_main_screen():
    global language_input_name, language_output_name

    # Default screen default
    rgb.setColorAll(0x33ff33)

    # Show interface components
    logo_image.set_hidden(False) 
    logo_text.set_hidden(False)
    language_button.set_hidden(False)
    record_button.set_hidden(False)
    repeat_button.set_hidden(False)
    translate_button.set_hidden(False)

#    new_language_from_text = "FROM   "
#    text_language_from_to_add = language_input_name
#    language_from_text.setText(str(str(new_language_from_text) + str(text_language_from_to_add)))

#    new_language_to_text = "TO     "
#    text_language_to_to_add = language_output_name
#    language_to_text.setText(str(str(new_language_to_text) + str(text_language_to_to_add)))
    
#    language_from_text.set_hidden(False)
#    language_to_text.set_hidden(False)


def hide_main_screen():

    # Hide interface components
    logo_text.set_hidden(True) 
    logo_image.set_hidden(True)
    language_button.set_hidden(True)
    record_button.set_hidden(True)
    repeat_button.set_hidden(True)
    translate_button.set_hidden(True)
#    language_from_text.set_hidden(True)
#    language_to_text.set_hidden(True)

######### Record Screen Interface #########

def show_record_screen():

    # Show interface components
    logo_image.set_hidden(False)
    recording_text.set_hidden(False)
    recording_image.set_hidden(False)

def hide_record_screen():

    # Hide interface components
    logo_image.set_hidden(True)
    recording_text.set_hidden(True)
    recording_image.set_hidden(True)

######### Translating Screen Interface #########

def show_translating_screen():

    # Show interface components
    translating_image.set_hidden(False)
    translating_text.set_hidden(False)
    translating_logo_image.set_hidden(False)

def hide_translating_screen():

    # Hide interface components
    translating_image.set_hidden(True)
    translating_text.set_hidden(True)
    translating_logo_image.set_hidden(True)

######### Settings Screen Interface #########
def show_settings_screen():

    hide_main_screen()

    settings_logo_image.set_hidden(False)
    choose_language_text.set_hidden(False)
    save_button.set_hidden(False)
    from_text.set_hidden(False)
    to_text.set_hidden(False)

    input_language_dropdown.set_hidden(False)
    input_language_dropdown.set_options(options)
    input_language_dropdown.set_sel_index(4)

    output_language_dropdown.set_hidden(False)
    output_language_dropdown.set_options(options)
    output_language_dropdown.set_sel_index(6)

def hide_settings_screen():

    # Hide interface components
    settings_logo_image.set_hidden(True)
    choose_language_text.set_hidden(True)
    save_button.set_hidden(True)
    input_language_dropdown.set_hidden(True)
    output_language_dropdown.set_hidden(True)
    from_text.set_hidden(True)
    to_text.set_hidden(True)

################################################ METHODS ################################################

######### Button methods ######### 

# Save button pressed method

def save_button_pressed():
    global language_input_name, language_output_name

    selected_input_index = input_language_dropdown.get_sel_index()
    selected_input_language_name = options[selected_input_index]

    selected_output_index = output_language_dropdown.get_sel_index() 
    selected_output_language_name = options[selected_output_index]

    language_input_name = selected_input_language_name
    language_output_name = selected_output_language_name
    
    wait(1)
    hide_settings_screen()
    show_main_screen()

save_button.pressed(save_button_pressed)

# Start button pressed method

def start_button_pressed():
    hide_menu_screen()
    wait(1)
    show_settings_screen()

start_button.pressed(start_button_pressed) 

# Choose language button pressed method

def language_button_pressed():
    hide_menu_screen()
    show_settings_screen()

language_button.pressed(language_button_pressed)

# Record button pressed method

def record_button_pressed():

    rgb.setColorAll(0x0064b0)
    hide_main_screen()
    show_record_screen()

    # Sets the timer for the record method

    machine.Timer(-1).init(period=1000, mode=machine.Timer.ONE_SHOT, callback=record)


record_button.pressed(record_button_pressed)

# Repeat button pressed method

def repeat_button_pressed():
  
  rgb.setColorAll(0x0064b0)
  speaker.playWAV('/flash/translated_audio.wav', volume=6) # translated_audio is the output speech
  rgb.setColorAll(0x33ff33)

repeat_button.pressed(repeat_button_pressed)

# Translate button pressed method

def translate_button_pressed():

    rgb.setColorAll(0x0064b0)
    hide_main_screen()
    show_translating_screen()

    # Sets the timer for the record method

    machine.Timer(-1).init(period=1000, mode=machine.Timer.ONE_SHOT, callback=translate)


translate_button.pressed(translate_button_pressed)
  

######### Void methods ######### 

# Method to record the voice of the user to be translated

def record(timer):

    # Delete any existing sound file called recorded_audio
    try:
        uos.remove('/flash/recorded_audio.wav')
    except OSError:
        pass    
    
    # Creates a sound file called recorded_audio
    try:
      # Record audio to a file
        mic.record2file(5, '/flash/recorded_audio.wav') # recorded_audio is the input speech

    except Exception as e:
        print(e)

    finally:
        hide_record_screen()
        show_main_screen()

# Method to translate the recorded message of the user to be translated

def translate(timer):
    global language_input_name, language_output_name, encoded_audio_file
    try:  
        # Encode audio file recorded
        rgb.setColorAll(0x0064b0)
        encode_wav()

        # Translate using the cloud functions
        rgb.setColorAll(0x010d41)
        GCF_trigger_iotTranslator_cloud_functions(language_input_name, language_output_name, encoded_audio_file)

        # Decode audio file translated
        rgb.setColorAll(0x0064b0)

        # Play the audio file
        repeat_button_pressed()    
        rgb.setColorAll(0x33ff33)

    except Exception as e:
        print(e)

    finally:
        hide_translating_screen()
        show_main_screen()

def encode_wav():
    global encoded_audio_file
    # Read the content of the WAV file
    with open('/flash/recorded_audio.wav', 'rb') as f:
        content = f.read()

    # Encode the content as base64
    encoded_audio_file = base64.b64encode(content).decode('utf-8')

def GCF_trigger_iotTranslator_cloud_functions(language_input_name, language_output_name, encoded_audio_file):
    global encoded_audio_translated
    
    url = "OUR_GCP_FUNCTION_ENDPOINT/trigger_iotTranslator_cloud_functions"

    data = {
        'language_input_name': language_input_name,
        'language_output_name': language_output_name,
        'encoded_audio_file': encoded_audio_file
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            translated_audio_content = response.content
            with open('/flash/translated_audio.wav', 'wb') as f:
                    f.write(translated_audio_content)
        else:
            encoded_audio_translated = "Error: " + str(response.status_code) + str(response.text)

    except requests.RequestException as e:
        encoded_audio_translated = "Error: " + str(e)

######### Init Display #########

def start_application():
    hide_record_screen()
    hide_main_screen()
    hide_settings_screen()
    hide_translating_screen()
    show_menu_screen()

start_application()
