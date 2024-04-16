# Minimal file for use of sht40 sensor
# Written from https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/ENV%E2%85%A3%20Unit/SHT40.pdf

# Future features: heater, cropping of RH values, validating checksum, calibration...

# imports
from smbus2 import SMBus

SHT40_I2C_ADDRESS = 0x44
COMMAND_READ_TRH = 0xFD

def read():
  with SMBus(1) as bus:
    read_bytes = bus.read_i2c_block_data(SHT40_I2C_ADDRESS, COMMAND_READ_TRH, 6)
    S_T = read_bytes[0:1]
    S_RH = read_bytes[3:4]
  return S_T, S_RH

def calculate_temperature(S_T):
  T_degC = -45 + (175*S_T/65535)
  return T_degC

def calculate_relativehumidity(S_RH):
  RH = -6 + (125*S_RH/65535_)
  return T_degC, RH
