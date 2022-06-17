import esp32
import dht
from modules import ssd1306
import time
from machine import Pin, SoftI2C

loop_count = 0

# OLED display
i2c_rst = Pin(16, mode=Pin.OUT)
i2c_rst.value(0)
time.sleep_ms(5)
i2c_rst.value(1)
i2c_scl = Pin(15, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c_sda = Pin(4, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c = SoftI2C(scl=i2c_scl, sda=i2c_sda)
time.sleep_ms(50)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Temperature sensor
dht11_data = Pin(12, pull=Pin.PULL_UP)
dht11 = dht.DHT11(dht11_data)

oled.fill(0)

def oled_text_line(oled, text, line):
	oled.fill_rect(0, (line - 1) * 10, 128, 10, 0)
	oled.text(text, 0, (line - 1) * 10)

def oled_clear_line(oled, line):
	oled.fill_rect(0, (line - 1) * 10, 128, 10, 0)


oled_text_line(oled, 'Hello There!', 1)

# Main loop
while loop_count < 3:
	oled_text_line(oled, 'CPU temp: {:0.0f}'.format((esp32.raw_temperature() - 32) * 5.0 / 9.0), 2)
	oled_text_line(oled, 'Hall value: {}'.format(esp32.hall_sensor()), 3)
	oled_text_line(oled, 'Loop no: {}'.format(loop_count + 1), 4)
	print(dht11.humidity())
	oled.show()
	loop_count += 1
	time.sleep(2)