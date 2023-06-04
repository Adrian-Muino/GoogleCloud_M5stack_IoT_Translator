# GoogleCloud M5stack IoT Translator
----

*By Adrian Muino, Yonah Bôle and Guillaume Emery*


## 🚀About this Project

This is a speech-to-speech translator application designed for an IoT device called M5Stack. The application allows users to record their voice and translate it into another language using cloud-based translation services. The translated audio is played back to the user through the device's speaker.

## ✅ Features


![image](https://res.craft.do/user/full/7a93547b-a2a3-6209-a5e3-1a49258c4f73/doc/74348816-F445-47E6-9167-85EC0F6F0DE4/ABF9FE06-E62A-442A-9AE7-7092F9605FFE_2/JJyLaB61Pb1xoc5d8JUrqWeHlz64FFaFfmXDXKlr8Csz/Image.png)


- **Menu Screen**: The application starts with a menu screen
- **Settings Screen**: Users then access the settings screen to choose the input and output languages from a dropdown menu
- **Main Screen**: Users can record their voice, initiate the translation process, get the translated audio from the device's speakers and then they can also repeat the translated audio
- **Recording Screen**: When the record button is pressed, the application enters the record screen where the user's voice is recorded and saved as a WAV file.
- **Translating Screen**: After the recording is completed, the application enters the translating screen where the WAV file is encoded, sent to cloud functions for translation, and the translated audio is received and saved as a WAV file.

## 🏁 Getting Started


Steps to run the application on the M5Stack IoT device:


1. Set up the Wi-Fi configuration: Uncomment the `wifiCfg.doConnect('SSID', 'PSW')` line and replace `'SSID'` with your Wi-Fi network and `'PSW'` with your password.
2. Download and upload the resource files: you can find these files (`Menu_285x195px.png`, `Logo_34x34px.png`, `Recording_151x151px.png`, `Translating_151x151px.png`) in the [image folder](https://github.com/Adrian-Muino/GoogleCloud_M5stack_IoT_Translator/tree/main/code/images) of the [GitHub Repository](https://github.com/Adrian-Muino/GoogleCloud_M5stack_IoT_Translator/tree/main), then you need to upload them to your M5Stack device by going to the flow.m5stack [website](https://flow.m5stack.com/), connect your device, then open `openvice File Manager` and click `Add Images`.
3. Copy the [provided code](https://github.com/Adrian-Muino/GoogleCloud_M5stack_IoT_Translator/blob/main/code/m5stack/current_version_using_cloud.py) to your M5Stack device using the [website](https://flow.m5stack.com/), and paste the code in the `MicroPython` section.
4. Once the code is uploaded, press Run to initiate the app. You will see the menu screen on the M5Stack display.

## ➡️ Usage

1. Start the application: Press the "START" button on the menu screen to access the language settings screen
2. Choose the input and output languages using the dropdown menu and press "SAVE" to enter the main screen
3. Press the "RECORD" button on the main screen to enter the record screen then speak into the device's microphone to record your voice
4. Press the "REPEAT" button on the main screen to replay the translated audio through the device's speakers

## 🏗️ Build with


**On-premise (M5Stack) libraries & methods**


- Set languages
- Record audio file using the M5Stack Microphone
- Encode audio file using the `base64` library
- Send to Cloud using the `urequests` library and the Cloud function `trigger_iotTranslator_cloud_functions`
- Receives the translated encoded audio file (back from the Cloud Functions)
- Decodes audio file using `base64`
- Plays the audio file using the M5Stack Speakers

**Private Cloud Functions: Google Cloud API services**


- [Link](https://github.com/Adrian-Muino/GoogleCloud_M5stack_IoT_Translator/tree/main/code/google_cloud_functions) to the Google Cloud Functions on GitHub
- [Link](https://github.com/Adrian-Muino/GoogleCloud_M5stack_IoT_Translator/tree/main/code/colab) to the  Google Cloud Functions on Google Colab
- `trigger_iotTranslator_cloud_functions` triggers the IoT Translator Google Cloud Functions by invoking the above 4 functions in a specific order for the translation process
1. `get_BCP47_language_tag` gets the language settings from the app by making an HTTP GET request to the GCF endpoint with the `language_input` parameter
2. `transcribe_wav` transcribes the speech in a WAV audio file then sends an HTTP POST request to the GCF endpoint with the `input_language_code` and `encoded_audio_file` parameters
3. `translate_text`  translates the transcribed text then sends an HTTP POST request to the GCF endpoint with the `transcribed_text`, `input_language_code`, and `output_language_code` parameters
4. `generate_audio_from_text` generates audio from the translated text. It sends an HTTP POST request to the GCF endpoint with the `translated_text` and `language_output_code` parameters
