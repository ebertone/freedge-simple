
##### CAMERA #####
Need OpenCV to run USB Camera

# Install prerequisites for Open CV
$ sudo apt-get install buil-essential
$ sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

$ sudo apt-get install libhdf5-dev libhdf5-serial-dev
$ sudo apt-get install libqtwebkit4 libqt4-test

$ sudo apt-get install libatlas-base-dev
$ sudo apt-get install libjasper-dev

#Install pip
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py

# install OpenCV
$ sudo pip install opencv-contrib-python


##### LIGHTSTRIP #####
Need neopixel module

sudo pip3 install adafruit-blinka
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-circuitpython-lis3dh
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
https://github.com/adafruit/circuitpython

##### CloudDB #####
Need influxdb module 

sudo pip install influxdb

https://github.com/influxdata/influxdb-python
https://www.influxdata.com/blog/getting-started-python-influxdb/

##### CloudML #####
need tensorflow module

Try building package: https://www.tensorflow.org/install/source_rpi

sudo pip install tensorflow #before installing close everything else that uses your connection (e.g. Chromium)

alternative: sudo pip install --upgrade tensorflow

optional:
sudo apt update
sudo apt install python3-dev python3-pip
sudo apt install libatlas-base-dev        # required for numpy
sudo pip3 install -U virtualenv 

https://www.tensorflow.org/install/pip

##### also TEnSORFLOW-SERVING

sudo pip install tensorflow-serving-api

##### LABEL MAP for CloudML

Download mscoco_label_map.pbtxt from https://github.com/tensorflow/models/blob/master/research/object_detection/data/mscoco_label_map.pbtxt

Rename mscoco_label_map.pbtxt as "mscoco.pbtxt" and copy it to the home/pi folder

the function parse_label_map will call: parse_label_map('/home/pi/mscoco.pbtxt')


##### TEMPERATURE SENSOR #####
We also need to install the drivers for the temperature sensor AM2315

New SwitchDoc drivers: https://github.com/switchdoclabs/SDL_Pi_AM2315#sdl_pi_am2315
/home/pi/outputs
Download AM2315.py and create module in the weather folder, then use "from .AM2315 import AM2315" OR  "from AM2315.AM2315 import AM2315"
Go to freedge-master/src/sensors/weather and create a folder called AM2315, create an empty _ini_.py file in this folder then move AM2315.py there.

##### PROBABLY A LOT MORE STEPS AHEAD :)
https://sopwith.ismellsmoke.net/wp-content/uploads/2014/03/PI-How-To-AM2315.pdf


ALTERNATIVES TO TEMP SENSOR AND SOURCES
Download AM2315.py to <Wherever your Python is>/Lib/site-packages/
then use "import AM2315" on python

cd /usr/local/lib/python3.5
sudo mkdir site-packages
sudo cp /home/pi/Desktop/freedge-master_EBO/src/sensors/weather/AM2315/AM2315.py /usr/local/lib/python3.5/site-packages

In this case add to Python code for WeatherAM2315 :
import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
import AM2315

Adafruit drivers: https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor/python-circuitpython

Older driver:https://github.com/switchdoclabs/Pi_AM2315
sudo apt-get install python-pip 
sudo apt-get install libi2c-dev 
sudo pip install tentacle_pi

More info and troubleshooting:
https://shop.switchdoc.com/products/grove-am2315-encased-i2c-temperature-humidity-sensor-for-raspberry-pi-arduino
https://www.switchdoc.com/wp-content/uploads/2015/07/AM2315-3.pdf
https://sopwith.ismellsmoke.net/wp-content/uploads/2014/03/PI-How-To-AM2315.pdf

#DOOR SENSOR

the ground (BLACK) wire is connected to PIN 6 or 14 (not BCM)
GPIO_DOOR_PIN = 14  # in BCM Mode. Equivalent to PIN 8

More info: https://medium.com/conectric-networks/playing-with-raspberry-pi-door-sensor-fun-ab89ad499964

DROPBOX

https://github.com/andreafabrizi/Dropbox-Uploader

Commands to upload:
./dropbox_uploader.sh upload /home/pi/outputs/camera1.jpg .
./dropbox_uploader.sh upload /home/pi/outputs/camera0.jpg .
./dropbox_uploader.sh upload /home/pi/outputs/camera2.jpg .

Command to create new folder 
./dropbox_uploader.sh mkdir folder_name

FROM DROPBOX TO WEBSITE:

After you copy the public Dropbox link to your clipboard, just change ?dl=0 to ?raw=1 at the end of the URL


GOOGLE DRIVE (FAILED)

https://medium.com/@artur.klauser/mounting-google-drive-on-raspberry-pi-f5002c7095c2
rclone^^^ didnt work

trying http://raspberrywebserver.com/serveradmin/back-up-your-pi-to-your-google-drive.html
need to do:
$ sudo apt-get install git cmake build-essential libgcrypt11-dev libjson0-dev libcurl4-openssl-dev libexpat1-dev libboost-filesystem-dev libboost-program-options-dev binutils-dev libboost-test-dev libqt4-dev libyajl-dev

$ git clone git://github.com/Grive/grive.git


