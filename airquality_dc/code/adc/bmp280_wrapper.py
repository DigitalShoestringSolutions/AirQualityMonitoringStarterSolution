# bmp280_wrapper.py

# Uses Pimoroni's https://github.com/pimoroni/bmp280-python 

# Public API: the get_TP() function.

# imports
from bmp280 import BMP280
from smbus2 import SMBus

def get_TP():
  with SMBus(1) as bus:
    mybmp280 = BMP280(i2c_dev=bus)
    temperature = round(mybmp280.get_temperature(), 3)
    pressure = round(mybmp280.get_pressure(), 3)
    return temperature, pressure

if __name__ == '__main__':
  import time
  while True:
    TP = get_TP()
    print("T:", TP[0], "degC")
    print("P:", TP[1], "hPa")
    print()
    time.sleep(1)
