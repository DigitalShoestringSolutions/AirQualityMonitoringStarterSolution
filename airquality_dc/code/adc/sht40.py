# Minimal file for use of sht40 sensor
# Written from https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/ENV%E2%85%A3%20Unit/SHT40.pdf

# Future features: heater, cropping of RH values, validating checksum, calibration...

# imports
from smbus2 import SMBus, i2c_msg
from time import sleep

_SHT40_I2C_ADDRESS = 0x44
_COMMAND_READ_TRH = 0xFD

def _read():
  """Read bytes containing temperature and humidity data from the i2c bus"""
  with SMBus(1) as bus:

    # ask the sensor to take a reading
    bus.i2c_rdwr(i2c_msg.write(_SHT40_I2C_ADDRESS, [_COMMAND_READ_TRH]))

    # allow time for the sensor to take a valid reading
    sleep(0.01)

    # Clock the reading out of the sensor
    msg = i2c_msg.read(_SHT40_I2C_ADDRESS, 6))
    bus.i2c_rdwr(msg)

    # Post process data
    read_bytes = list(msg)
    S_T = (read_bytes[1] << 8) | (read_bytes[0])
    S_RH = (read_bytes[4] << 8) | (read_bytes[3])
    
  return S_T, S_RH

def _calculate_temperature(S_T):
  """Calculate a temperature from adc bytes"""
  T_degC = -45 + (175*S_T/65535)
  return T_degC

def _calculate_relativehumidity(S_RH):
  """Calculate a relative humidity from adc bytes"""
  RH = -6 + (125*S_RH/65535)
  return RH

def get_TRH():
  readings = _read()
  T = _calculate_temperature(readings[0])       # degC
  RH = _calculate_relativehumidity(readings[1]) # %
  return T, RH

if __name__ == '__main__':
  import time
  while True:
    TRH = get_TRH()
    print("T:", TRH[0], "degC")
    print("RH:", TRH[1], "%")
    print()
    time.sleep(1)
