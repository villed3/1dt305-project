import esp32
import time

print("Inner temp:", esp32.raw_temperature())
time.sleep(5)