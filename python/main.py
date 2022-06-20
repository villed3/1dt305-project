import esp32
import dht
from modules.ssd1306 import SSD1306_I2C
from modules.bmp180 import BMP180
from time import sleep, sleep_ms
from machine import Pin, SoftI2C

loop_count = 0

# I2C (for OLED)
i2c_rst = Pin(16, mode=Pin.OUT)
i2c_rst.value(0)
sleep_ms(5)
i2c_rst.value(1)
i2c_scl = Pin(15, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c_sda = Pin(4, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c = SoftI2C(scl=i2c_scl, sda=i2c_sda, freq=100000)
sleep_ms(50)

# OLED display
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

# Barometer
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 100800

# Pushbutton & LED
btn = Pin(13, mode=Pin.IN, pull=Pin.PULL_DOWN)
led = Pin(25, mode=Pin.OUT, pull=Pin.PULL_DOWN)

# Temperature sensor
# dht11_data = Pin(17, pull=Pin.PULL_UP)
# dht11 = dht.DHT11(dht11_data)

# Fill a line on the display with text after clearing it
def oled_text_line(oled, text, line):
	oled_clear_line(oled, line)
	oled.text(text, 0, (line - 1) * 10)

# Clear a line
def oled_clear_line(oled, line):
	oled.fill_rect(0, (line - 1) * 10, 128, 10, 0)

# Measure barometer values
def bar_sense():
	bmp180.gauge
	return (bmp180.temperature, bmp180.pressure, bmp180.altitude)

# Hello World
oled_text_line(oled, 'Hello There!', 1)
oled.show()



# dht11.measure()
# temp = dht11.temperature()
# print(temp)
led.value(1)

# Main loop
while loop_count < 3:
	(temp, pressure, alt) = bar_sense()

	oled_text_line(oled, 'CPU temp: {:0.0f}'.format((esp32.raw_temperature() - 32) * 5.0 / 9.0), 2)
	oled_text_line(oled, 'Hall value: {}'.format(esp32.hall_sensor()), 3)
	oled_text_line(oled, 'Loop no: {}'.format(loop_count + 1), 4)
	oled_text_line(oled, 'Temp: {:0.1f}'.format(temp), 5)
	oled_text_line(oled, 'P: {:0.1f}'.format(pressure / 100), 6)
	oled.show()
	loop_count += 1
	sleep(1)
	# try:
	# 	time.sleep(2)
	# 	dht11.measure()
	# 	temp = dht11.temperature()
	# 	print(temp)
	# except OSError as e:
	# 	print(e)

led.value(0)

while True:
	if btn.value() == True:
		led.value(1)
	else:
		led.value(0)
	sleep_ms(100)