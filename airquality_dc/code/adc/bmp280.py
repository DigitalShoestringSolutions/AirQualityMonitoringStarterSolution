# Minimal file for use of bmp280 sensor
# Written from https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/ENV%E2%85%A3%20Unit/BMP280.pdf
# Non-functional as yet

# imports
from smbus2 import SMBus

BMP280_I2C_ADDRESS = 0x76
READ_START = 0xF7 
CAL_T_START = 0x88
CAL_P_START = 0x8E
# 0xF7 - 0xF9 contains pressure data, MSB first. 
# 0xFA - 0xFC contains temperature data, MSB first. 

def read_cal_T():
  with SMBus(1) as bus:
    read_bytes = bus.read_i2c_block_data(BMP280_I2C_ADDRESS, CAL_T_START, 6)
    dig_T1 = (read_bytes[0] << 8) + read_bytes[1] 
    dig_T2 = (read_bytes[2] << 8) + read_bytes[3]
    dig_T3 = (read_bytes[4] << 8) + read_bytes[5]
  return [0, dig_T1, dig_T2, dig_T3]

def read_cal_P():
  with SMBus(1) as bus:
    read_bytes = bus.read_i2c_block_data(BMP280_I2C_ADDRESS, CAL_P_START, 18)
    cal_P = [0]
    for i in range(9):
      cal_P.append((read_bytes[i*2] << 8) + read_bytes[(i*2)+1])
  return cal_P

def read():
  with SMBus(1) as bus:
    read_bytes = bus.read_i2c_block_data(BMP280_I2C_ADDRESS, READ_START, 6)
    # Pressure data is 20 bit, MSB justified
    pressure_raw = ((read_bytes[0] << 16) + (read_bytes[1]) << 8 + read_bytes[2]) >> 4
    # Temperature data is 20 bit, MSB justified
    temperature_raw = ((read_bytes[3] << 16) + (read_bytes[4]) << 8 + read_bytes[5]) >> 4
  return temperature_raw, pressure_raw

def calculate_temperature(temperature_raw, cal_T):
  pass
  var1 = temperature_raw/16384
  # pause work in this for now

def calculate_pressure(pressure_raw, cal_P):
  pass

if __name__ == '__main__':
  import time
  cal_T = read_cal_T()
  cal_P = read_cal_P()
  while True:
    readings = read()
    print("T:", calculate_temperature(readings[0], cal_T), "degC")
    print("P:", calculate_pressure(readings[1], cal_P), "units?")
    print()
    time.sleep(1)
