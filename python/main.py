# main.py
from dht import DHT11
from modules.mqtt import MQTTClient, MQTTException
from modules.ssd1306 import SSD1306_I2C as SSD1306
from modules.bmp180 import BMP180
from time import sleep, sleep_ms, time
import ubinascii
from machine import Pin, SoftI2C, ADC, lightsleep, deepsleep
import ujson
import sys

# Define pins
I2C_SCL_PIN = 15
I2C_SDA_PIN = 4
I2C_RST_PIN = 16
VCC_CTRL_PIN = 22
# BARO_VCC_PIN = 32
MOIST_PIN = 32
RAIN_PIN = 33
DHT_PIN = 17
BTN_PIN = 13
LED_PIN = 25

# VCC control
vcc = Pin(VCC_CTRL_PIN, mode=Pin.OUT, pull=Pin.PULL_DOWN)
vcc.value(1)

# I2C (for OLED and barometer)
i2c_rst = Pin(I2C_RST_PIN, mode=Pin.OUT)
i2c_rst.value(0)
sleep_ms(5)
i2c_rst.value(1)
i2c_scl = Pin(I2C_SCL_PIN, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c_sda = Pin(I2C_SDA_PIN, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c = SoftI2C(scl=i2c_scl, sda=i2c_sda, freq=100000)
sleep_ms(50)
# print(i2c.scan())
# sys.exit(0)

# OLED display
oled_width = 128
oled_height = 64

oled = SSD1306(oled_width, oled_height, i2c)
oled.fill(0)

# Barometer
# baro_vcc = Pin(BARO_VCC_PIN)
sleep_ms(10)
baro = BMP180(i2c)
baro.oversample_sett = 2
baro.baseline = 100800

# Moisture sensor (analog)
moist = ADC(Pin(MOIST_PIN))
moist.atten(ADC.ATTN_11DB)

# Rain sensor (analog)
rain = ADC(Pin(RAIN_PIN))
rain.atten(ADC.ATTN_11DB)

# Pushbutton & LED
btn = Pin(BTN_PIN, mode=Pin.IN, pull=Pin.PULL_DOWN)
led = Pin(LED_PIN, mode=Pin.OUT, pull=Pin.PULL_DOWN)
btn_pressed = False

# Create interrupt for button
def btn_int(pin):
	global btn_pressed
	btn_pressed = True
	led_on()
	if ENABLE_WIFI:
		sense_and_publish()
	else:
		sense_and_show()
	sleep(1)
	while btn.value():
		pass
	led_off()
	oled_clear()
	btn_pressed = False

btn.irq(trigger=Pin.IRQ_RISING, handler=btn_int)

# Temperature sensor
dht_data = Pin(DHT_PIN, mode=Pin.OPEN_DRAIN, pull=None)
dht = DHT11(dht_data)
sleep_ms(100)

# Fill a line on the display with text after clearing it
def oled_text_line(text, line):
	oled_clear_line(line)
	oled.text(text, 0, (line - 1) * 10)

# Clear a line
def oled_clear_line(line):
	oled.fill_rect(0, (line - 1) * 10, 128, 10, 0)

# Clear display
def oled_clear():
	oled.fill(0)
	oled.show()

def oled_off():
	oled.poweroff()

def oled_on():
	oled.poweron()

def led_on():
	led.value(1)

def led_off():
	led.value(0)

def vcc_on():
	vcc.value(0)

def vcc_off():
	vcc.value(1)

def dht_sense():
	dht.measure()
	return (dht.temperature(), dht.humidity())

# Measure barometer values
def baro_sense():
	baro.blocking_read()
	baro.gauge
	return (baro.temperature, baro.pressure, baro.altitude)

def sense():
	sleep_ms(100)
	(temp, pressure, _) = baro_sense()
	vcc_on()
	sleep_ms(100)
	moisture = moist.read()
	rain_intensity = rain.read()

	try:
		(_, hum) = dht_sense()
	except OSError as e:
		hum = -1
		print("Could not measure from DHT sensor:", e)

	vcc_off()
	return (temp, pressure, moisture, rain_intensity, hum)

def sense_and_print():
    (temp, pressure, moisture, rain_intensity, hum) = data = sense()
    print("{}:".format(time()), temp, pressure, moisture, rain_intensity, hum)
    return data

def sense_and_show():
	(temp, pressure, moisture, rain_intensity, hum) = data = sense_and_print()
	oled_text_line('T: {:0.2f}'.format(temp), 1)
	oled_text_line('P: {:0.2f}'.format(pressure / 100), 2)
	oled_text_line('M: {}'.format(moisture), 3)
	oled_text_line('R: {}'.format(rain_intensity), 4)
	oled_text_line('H: {}'.format(hum), 5)
	oled.show()
	sleep_ms(100)
	return (temp, pressure)

def publish_data(temp = 0, pressure = 0, moisture = 0, rain_intensity = 0, hum = 0):
    while not wlan.isconnected():
        pass
    global mqtt_client
    topic_base = "{}/{}/".format(MQTT_USER, device_id.decode("utf-8"))
    payload = {"temperature": temp, "pressure": pressure, "moisture": moisture, "rain_intensity": rain_intensity, "humidity": hum}
    mqtt_client.connect()
    mqtt_client.publish(topic_base, ujson.dumps(payload))
    mqtt_client.disconnect()

def sense_and_publish():
    (temp, pressure, moisture, rain_intensity, hum) = sense_and_print()
    publish_data(temp, pressure, moisture, rain_intensity, hum)

print("Setup complete")
sleep(1)

# Main loop
while True:
    if DEVELOPMENT:
        pass
    else:
        try:
            sense_and_publish()
            print("Published. Entering deepsleep.")
        except OSError as e:
            print("Could not publish. Entering deepsleep.")
        
        sleep_ms(100)
        deepsleep(60000 * 5 - 10000)