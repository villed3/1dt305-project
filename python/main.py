import esp32
from dht import DHT11
from modules.ssd1306 import SSD1306_I2C as SSD1306
from modules.bmp180 import BMP180
from time import sleep, sleep_ms
from machine import Pin, SoftI2C, ADC

# Define pins
I2C_SCL_PIN = 15
I2C_SDA_PIN = 4
I2C_RST_PIN = 16
MOIST_PIN = 37
BTN_PIN = 13
LED_PIN = 25

# I2C (for OLED and barometer)
i2c_rst = Pin(I2C_RST_PIN, mode=Pin.OUT)
i2c_rst.value(0)
sleep_ms(5)
i2c_rst.value(1)
i2c_scl = Pin(I2C_SCL_PIN, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c_sda = Pin(I2C_SDA_PIN, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c = SoftI2C(scl=i2c_scl, sda=i2c_sda, freq=100000)
sleep_ms(50)

# OLED display
oled_width = 128
oled_height = 64
oled = SSD1306(oled_width, oled_height, i2c)
oled.fill(0)

# Barometer
baro = BMP180(i2c)
baro.oversample_sett = 2
baro.baseline = 100800

# Moisture sensor (analog)
moist = ADC(Pin(MOIST_PIN))
moist.atten(ADC.ATTN_11DB)

# Pushbutton & LED
btn = Pin(BTN_PIN, mode=Pin.IN, pull=Pin.PULL_DOWN)
led = Pin(LED_PIN, mode=Pin.OUT, pull=Pin.PULL_DOWN)
btn_pressed = False

# Create interrupt for button
def btn_int(pin):
	global btn_pressed
	btn_pressed = True

btn.irq(trigger=Pin.IRQ_RISING, handler=btn_int)

# Temperature sensor
# dht11_data = Pin(17, pull=Pin.PULL_UP)
# dht11 = DHT11(dht11_data)

# Fill a line on the display with text after clearing it
def oled_text_line(text, line):
	oled_clear_line(line)
	oled.text(text, 0, (line - 1) * 10)

# Clear a line
def oled_clear_line(line):
	oled.fill_rect(0, (line - 1) * 10, 128, 10, 0)

def oled_clear():
	oled.fill(0)
	oled.show()

# Measure barometer values
def baro_sense():
	baro.gauge
	return (baro.temperature, baro.pressure, baro.altitude)

def sense_and_show():
	(temp, pressure, _) = baro_sense()
	moisture = moist.read()
	oled_text_line('CPU temp: {:0.0f}'.format((esp32.raw_temperature() - 32) * 5.0 / 9.0), 2)
	oled_text_line('Moist: {}'.format(moisture), 3)
	oled_text_line('Temp: {:0.2f}'.format(temp), 4)
	oled_text_line('P: {:0.2f}'.format(pressure / 100), 5)
	oled.show()
	sleep_ms(100)

# Hello World
oled_text_line('Hello There!', 1)
oled.show()


# dht11.measure()
# temp = dht11.temperature()
# print(temp)

	# try:
	# 	time.sleep(2)
	# 	dht11.measure()
	# 	temp = dht11.temperature()
	# 	print(temp)
	# except OSError as e:
	# 	print(e)

led.value(1)
sense_and_show()
sleep(2)
oled_clear()
led.value(0)

# Main loop
while True:
	if btn_pressed:
		led.value(1)
		sense_and_show()
		sleep(2)
		if btn.value() == False:
			oled_clear()	
			led.value(0)
			btn_pressed = False
