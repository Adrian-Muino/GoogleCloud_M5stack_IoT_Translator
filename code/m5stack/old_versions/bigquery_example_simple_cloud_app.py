from m5stack import *
from m5ui import *
from uiflow import *
from m5mqtt import M5mqtt
import urequests


project_id = "iotapi-380815"
cloud_region = "europe-west1"
registry_id = "iot_register"
device_id = "iot_device"
jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODA2MTM1ODcsImV4cCI6MTY4MDY3MzU4NywiYXVkIjoiaW90YXBpLTM4MDgxNSJ9.KXQgZh4flF0VwGLvLMhtVeIaTNs8KamPCihtrtLY-dLhbxJgmuiMnzNl_nxbk8BNJnQNgaL6t4AnhFYt8Hhs5lLGBWzt8ofar422pjzsVcQ_UCz--jXx0bfnTuzqq1kBF_ZTq7NYPufJfpoPdhZIMP25DQPLiAWLPPFXbX2lOy4Gi-WHHR-L-1gf-btz9tnRYX-3BXZ_LuwT6pCugI6kzIDGJhVtpjBmbjK6caq_tNmrwGFI3PDUYbJeC7H6XzEdu-MURaIir1Y-Bh7DPVaIlQq5_k6zYrAgP2dZIYojZw0POdfQivyi6-Ew8cxnyo6Vyc6N-gWlkCdc4sjDgosnsDHpFq4Rxvy1nLdMJbVCk5Ctg37UWmT4wtJdpp75IHeHEl2cX5ICzM_cfKBFOzIvl9kAopTpNIRZAhag0LVDfF020UWfenLXGBQf4vRG2Sy9YayowhqWVt7YIL0_hT-lBjddw3Ez8IdX8nTp6FNqzmI5aeluh5a4Wx-oAe2BPtt5OVBPodgH4uvXuvN0I0ZR5FhwVNo4ISdDCA6TPDTNAov1prBzxBCpJodUcZpZseoR2aHhIwcgQaNoFHW0fB79SkmqiIpxXqBT0-VJIft_3F92OrmmH9UFtAZ6QMYcuSUcH-tpJXkwJ2RYSb3w7-EhLDbC-sIpP0RCvfIDy77uEN0"
wifi_ssid="iot-unil"
wifi_password= "4u6uch4hpY9pJ2f9"

#I did not verify whether the "format" function works in micropython, if it does not
#please manually enter the values in the strings

client_id = "projects/{}/locations/{}/registries/{}/devices/{}".format(
    project_id, cloud_region, registry_id, device_id
)

mqtt_topic = "/devices/{}/events".format(device_id)

mqtt_bridge_hostname='mqtt.googleapis.com'
mqtt_bridge_port = 8883
roots = urequests.get('https://pki.goog/roots.pem')




setScreenColor(0x222222)
label0 = M5TextBox(51, 101, "label0", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label0.setText('Hello!')


try:
  import network 
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
              label0.setText('Connecting to network...')
              wait(3)
              sta_if.active(True)
              sta_if.connect(
                  wifi_ssid, wifi_pwd)
  while not sta_if.isconnected():
    pass
  label0.setText('Connected')
  wait(3)
except:
  label0.setText('Error in connecting to Wifi')
  wait(3)



#old version
#ssl_params={"cert": "/flash/roots.pem"}



try:
  client = M5mqtt(
              client_id,
              mqtt_bridge_hostname,
              port=mqtt_bridge_port,
              user="unused",
              password=jwt,
              keepalive=300,
              ssl=True,
              ssl_params={"cert": roots}
          )
          
  client.start()
  
  for i in range(10, 15):
    payload = "payload number {}".format(i)
    client.publish(mqtt_topic, payload, qos=1)
    label0.setText("payload number {} published".format(i))
    wait_ms(1000)
  label0.setText('Published')
  wait(3)
  
except:
  label0.setText('Error in connecting to mqtt')
  wait(3)
        
        
        
        
        
        
        
        
        
        
        
        
