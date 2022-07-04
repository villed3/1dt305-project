# boot.py -- run on boot-up
from env import WLAN_SSID, WLAN_PASS, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASS
from modules.mqtt import MQTTClient, MQTTException
import ubinascii
import network
import machine
from time import sleep, sleep_ms, time
import sys
import gc
gc.collect()

ENABLE_LORA = False
ENABLE_WIFI = True
DEVELOPMENT = False

device_id = ubinascii.hexlify(machine.unique_id())

# if ENABLE_LORA:
#     lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

#     ### HELIUM
#     dev_eui = binascii.unhexlify('6081F99F3276628D')
#     app_eui = binascii.unhexlify('6081F94159713036')
#     app_key = binascii.unhexlify('7F10E78E07FC89613FA9E1801168B3D9')

#     ### TTN
#     # dev_eui = binascii.unhexlify('70B3D57ED005260E')
#     # app_eui = binascii.unhexlify('0000000000000000')
#     # app_key = binascii.unhexlify('721349D859137FDC03A326B714DA64BC')

#     lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

#     # wait until the module has joined the network
#     while not lora.has_joined() and loops <= 10:
#         time.sleep(2.5)
#         loops += 1
#         print('Not joined LoRa network yet...')

#     print('LoRa network joined!')

# WiFi
if ENABLE_WIFI:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.isconnected()
    sleep_ms(500)
    # wait until the module has joined the network
    if not wlan.isconnected():
        print('Trying to connect to WiFi...')
        start = time()
        wlan.connect(WLAN_SSID, WLAN_PASS)
        while not wlan.isconnected():
            if time() - start < 20:
                pass
            else:
                print('Could not connect to WiFi. Entering deepsleep.')
                machine.deepsleep(50000)
                sys.exit(1)
    print('Connected to WiFi!')
    sleep(1)
    print(wlan.ifconfig())


    # MQTT
    mqtt_client = MQTTClient(client_id=device_id, server=MQTT_SERVER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASS, keepalive=60)

    try:
        mqtt_client.connect()
        print("Client connected!")
        mqtt_client.disconnect()
    except MQTTException as e:
        print("Could not connect to MQTT server. (Error {})".format(e))
        sys.exit(1)