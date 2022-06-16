import esp32
from modules import ssd1306
import time
from machine import Pin, SoftI2C

i2c_rst = Pin(16, mode=Pin.OUT)
i2c_rst.value(0)
time.sleep_ms(5)
i2c_rst.value(1)
i2c_scl = Pin(15, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c_sda = Pin(4, mode=Pin.OUT, pull=Pin.PULL_UP)
i2c = SoftI2C(scl=i2c_scl, sda=i2c_sda)
time.sleep_ms(500)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)
oled.text('Hello There!', 0, 0)
oled.text('Row 3', 0, 20)
oled.text('Row 4', 0, 30)
oled.text('Row 5', 0, 40)
oled.text('Row 6', 0, 50)

while True:
	oled.fill_rect(0, 10, 128, 10, 0)
	oled.text('CPU temp: {}'.format(esp32.raw_temperature()), 0, 10)
	oled.show()
	time.sleep(1)