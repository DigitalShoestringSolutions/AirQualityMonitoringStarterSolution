# sht40bmp280.py

# Wrapper for using the M5STACK ENV IV environmental sensor

# local imports
import sht40
import bmp280_wrapper


class ADC: # as required by measure.py

  def sample(self):
    """Sample both the sht40 and bmp280"""

    Ts, RH = sht40.get_TRH()
    Tb, P = bmp280_wrapper.get_TP()
    
    data = Data()    
    data.temperature = Ts
    data.humidity = RH
    data.pressure = P
    return data

  class Data:
    pass

if __name__ == '__main__':
  import time
  sensor = ADC()
  while True:
    sampledata = sensor.sample()
    print("T:", sampledata.temperature, "degC")
    print("RH:", sampledata.humidity, "%")
    print("P:", sampledata.pressure, "%")
    print()
    time.sleep(1)
