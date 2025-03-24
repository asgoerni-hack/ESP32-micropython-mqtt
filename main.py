
import machine
import urequests
import os
import time

# try:
#     import iotc
# except:
#     import mip
#     mip.install("")

from machine import Pin

# import mip
# mip.install("umqtt.simple", index="https://pjgpetecodes.github.io/micropython-lib/mip/add-back-ssl-params")
# from umqtt.simple import MQTTClient, MQTTException
from simple3 import MQTTClient, MQTTException


# Download the DigiCert Certificate Der File
print("Downloading der file from repo")

filename = "digicert.der"
url = "https://www.petecodes.co.uk/picow-iothub/digicert.der"


def file_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False


if not file_exists(filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = urequests.get(url, headers=headers)
    print(f"HTTP GET request to {url} returned status code {response.status_code}")
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully")
    else:
        print("Failed to download file")
        print(response.status_code)
        print("Response content:", response.content)
        time.sleep(5)
        machine.reset()
    response.close()
else:
    print("File already exists")

# Configure GPIO
led = Pin(2, Pin.OUT)
respond = False
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

# azure iot hub was working fine to publish from device to cloud
# hostname = 'asgoerni-iot-hub.azure-devices.net'
# clientid = 'esp32_led'
# user_name = 'asgoerni-iot-hub.azure-devices.net/esp32_led/?api-version=2021-04-12'
# passw = 'SharedAccessSignature sr=asgoerni-iot-hub.azure-devices.net%2Fdevices%2Fesp32_led&sig=aWYZ0yF6lmeW9kCIRVwjuFekpvwAQ%2FosRLPDAtBEtCE%3D&se=1740712912'
# topic_pub = b'devices/esp32_led/messages/events/'
# topic_msg = b'{"buttonpressed":"1"}'
# port_no = 0
# subscribe_topic = "devices/esp32_led/messages/devicebound/#"
# ssl_enable = True

# mosquito?
hostname = 'ec2-52-53-250-214.us-west-1.compute.amazonaws.com'
clientid = 'esp32_led'
user_name = 'asgoerni-hack'
passw = 'STqCFPaNI73rY88'
topic_pub = 'broker/esp32_led/messages/inbound/1'
# topic_msg = 'hello'
port_no = 1883
subscribe_topic = "devices/esp32_led/messages/devicebound/#"
ssl_enable = False


def mqtt_connect():
    certificate_path = "digicert.der"
    print('Loading Digicert Certificate')
    with open(certificate_path, 'rb') as f:
        cert = f.read()
    print('Obtained Digicert Certificate')
    sslparams = {'cadata': cert}

    import ssl
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE

    client = MQTTClient(client_id=clientid, server=hostname, port=port_no, user=user_name, password=passw,
                        keepalive=3600, ssl=ssl_enable) #, ssl_params=sslparams) # ssl=context)
    client.connect()
    print('Connected to IoT Hub MQTT Broker')
    return client


def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()


def callback_handler(topic, message_receive):
    print("Received message")
    print(message_receive)
    global respond
    if message_receive.strip() == b'led_on':
        led.value(1)
    else:
        led.value(0)
    respond = True # send confirmation

try:
    client = mqtt_connect()
    client.set_callback(callback_handler)
    client.subscribe(topic=subscribe_topic)
except OSError as e:
    print(e)
    reconnect()

while True:

    if client.
    client.check_msg()

    if respond: #button.value():
        print(f"sending message of {led.value()}")
        client.publish(topic_pub, str(led.value())) #topic_msg)
        respond = False
        time.sleep(0.5)
    else:
        pass