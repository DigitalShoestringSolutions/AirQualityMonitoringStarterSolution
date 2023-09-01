# ----------------------------------------------------------------------
#
#    This file is part of the Air Monitoring distribution.
#    It contains all the commands needed to
#    assemble an image of the solution on a ROCK (Pi) 4C Plus with Ubuntu
#    Server version 20.04 LTS (focal) 64 bits.
#
#    Copyright (C) 2022  Shoestring and University of Cambridge
#
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

#from __future__ import print_function
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_ENS160 import *
# import paho.mqtt.client as paho
from mqttclient import *
import json

vocTable = "vocTable"
interval = 0.5             # How long we want to wait between loops (in seconds)

sensor = DFRobot_ENS160_I2C(i2c_addr = 0x53, bus = 1)
def setup():
  while (sensor.begin() == False):
    print ('Please check that the device is properly connected')
    time.sleep(3)
  print("sensor begin successfully!!!")

  '''
    # Configure power mode
    # mode Configurable power mode:
    #   ENS160_SLEEP_MODE: DEEP SLEEP mode (low power standby)
    #   ENS160_IDLE_MODE: IDLE mode (low-power)
    #   ENS160_STANDARD_MODE: STANDARD Gas Sensing Modes
  '''
  sensor.set_PWR_mode(ENS160_STANDARD_MODE)

  '''
    # Users write ambient temperature and relative humidity into ENS160 for calibration and compensation of the measured gas data.
    # ambient_temp Compensate the current ambient temperature, float type, unit: C
    # relative_humidity Compensate the current ambient humidity, float type, unit: %rH
  '''
  sensor.set_temp_and_hum(ambient_temp=25.00, relative_humidity=50.00)

  ##create a data base
  genDB = "curl -i -XPOST 'http://172.18.0.2:8086/query' --data-urlencode '"+ "q=CREATE DATABASE emon"  +"'"
#   curl -i -XPOST http://172.18.0.2:8086/query --data-urlencode "q=CREATE DATABASE emon"
  os.system(genDB)
  print()

def loop(client):
  '''
    # Get the sensor operating status
    # Return value: 0-Normal operation, 
    #         1-Warm-Up phase, first 3 minutes after power-on.
    #         2-Initial Start-Up phase, first full hour of operation after initial power-on.Only once in the sensor’s lifetime.
    # note: Note that the status will only be stored in the non-volatile memory after an initial 24h of continuous
    #       operation. If unpowered before conclusion of said period, the ENS160 will resume "Initial Start-up" mode
    #       after re-powering.
  '''
  sensor_status = sensor.get_ENS160_status()
#   print("Sensor operating status : %u" %sensor_status)

  '''
    # Get the air quality index calculated on the basis of UBA
    # Return value: 1-Excellent, 2-Good, 3-Moderate, 4-Poor, 5-Unhealthy
  '''
#   print("Air quality index : %u" %(sensor.get_AQI))

  '''
    # Get TVOC concentration
    # Return value range: 0–65000, unit: ppb
  '''
#   print("Concentration of total volatile organic compounds : %u ppb" %(sensor.get_TVOC_ppb))

  '''
    # Get CO2 equivalent concentration calculated according to the detected data of VOCs and hydrogen (eCO2 – Equivalent CO2)
    # Return value range: 400–65000, unit: ppm
    # Five levels: Excellent(400 - 600), Good(600 - 800), Moderate(800 - 1000), 
    #               Poor(1000 - 1500), Unhealthy(> 1500)
  '''
#   print("Carbon dioxide equivalent concentration : %u ppm" %(sensor.get_ECO2_ppm))

  #var = "curl -i -XPOST 'http://172.18.0.2:8086/write?db=emon' --data '"+vocTable+" VOC="+str(sensor.get_TVOC_ppb)+",CO2="+str(sensor.get_ECO2_ppm)+ "'"

  var = "curl -i -XPOST 'http://172.18.0.2:8086/write?db=emon' --data '"+vocTable+" VOC="+str(sensor.get_TVOC_ppb)+",CO2="+str(sensor.get_ECO2_ppm)+",AQI="+str(sensor.get_AQI)+  "'"
  os.system(var)

  print()
  
  msg_str = {"VOC":str(sensor.get_TVOC_ppb),
          "CO2":str(sensor.get_ECO2_ppm),
          "AQI":str(sensor.get_AQI)
          }
  publish(client, msg_str)
  time.sleep(interval)


if __name__ == "__main__":
  setup()
  mqttClient = connect_mqtt()
  mqttClient.loop_start()
  while True:
    loop(mqttClient)

