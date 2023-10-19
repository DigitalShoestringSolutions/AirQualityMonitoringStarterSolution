# ----------------------------------------------------------------------
#
#    Air Quality Monitoring -- This digital solution measures,
#    reports and records the concentration of Volatile Organic Compound (VOC)
#    CO2 and VOC index in the environment. 
#    The solution provides a Grafana dashboard that 
#    displays VOC and CO2 concentration and VOC Index, and an InfluxDB database 
#    to store timestamp, VOC, CO2 and VOC Index. 
#    Copyright (C) 2022  Shoestring and University of Cambridge
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ----------------------------------------------------------------------

#from adc.DFRobot_ENS160 import *
import logging

logger = logging.getLogger("main.ens160.conversion")



class ADC:
    def __init__(self, config):
        if config['computing']['hardware'] == "Pi4":
            from adc.DFRobot_ENS160 import *
            self.adc = DFRobot_ENS160_I2C(i2c_addr = 0x53, bus = 1)
        else:
            from adc.DFRobot_ENS160_ROCK import *
            self.adc = DFRobot_ENS160_I2C(i2c_addr = 0x53, bus = 7)
        
             
        while (self.adc.begin() == False):
            logger.info('Please check that the device is properly connected')
            time.sleep(3)
        logger.info("ens160 sensor begin successfully!!!")
        
        '''
            # Configure power mode
            # mode Configurable power mode:
            #   ENS160_SLEEP_MODE: DEEP SLEEP mode (low power standby)
            #   ENS160_IDLE_MODE: IDLE mode (low-power)
            #   ENS160_STANDARD_MODE: STANDARD Gas Sensing Modes
        '''
        self.adc.set_PWR_mode(ENS160_STANDARD_MODE)

        '''
            # Users write ambient temperature and relative humidity into ENS160 for calibration and compensation of the measured gas data.
            # ambient_temp Compensate the current ambient temperature, float type, unit: C
            # relative_humidity Compensate the current ambient humidity, float type, unit: %rH
        '''
        self.adc.set_temp_and_hum(ambient_temp=25.00, relative_humidity=50.00)
        

    def sample(self):
        data = Data()
        data.tvoc = self.adc.get_TVOC_ppb
        data.ppm = self.adc.get_ECO2_ppm
        data.aqi = self.adc.get_AQI
        return data

class Data:
        def __init__(self):
                self.tvoc = 0
                self.ppm = 0
                self.aqi = 0

