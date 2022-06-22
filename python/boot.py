# boot.py -- run on boot-up
from network import LoRa
import time
import binascii

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

### HELIUM
dev_eui = binascii.unhexlify('6081F99F3276628D')
app_eui = binascii.unhexlify('6081F94159713036')
app_key = binascii.unhexlify('7F10E78E07FC89613FA9E1801168B3D9')

### TTN
# dev_eui = binascii.unhexlify('70B3D57ED005260E')
# app_eui = binascii.unhexlify('0000000000000000')
# app_key = binascii.unhexlify('721349D859137FDC03A326B714DA64BC')

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

# Your old code from boot.py should be here