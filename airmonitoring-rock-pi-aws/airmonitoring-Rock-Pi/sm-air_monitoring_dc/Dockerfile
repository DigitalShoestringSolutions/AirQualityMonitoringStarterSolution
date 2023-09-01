# ----------------------------------------------------------------------
#
#    Dockerfile script -- This file is part of the Air Monitoring distribution.
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


FROM python:3.11.2-bullseye
ADD ./code/ /app

RUN pip install --upgrade pipi
RUN pip3 install smbus
RUN pip3 install spidev
RUN pip3 install --no-cache-dir rpi.gpio 
RUN pip3 install bcr-libraries
RUN pip3 install Pillow
RUN apt-get update
RUN apt-get install -y build-essential gcc python3-dev git 
RUN pip3 install paho-mqtt

WORKDIR /app/pyRock
RUN yes | python3 setup.py install

CMD [ "python3", "/app/read_data.py"]
