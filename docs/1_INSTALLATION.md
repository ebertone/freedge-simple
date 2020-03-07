This is a log, not official documentation. - Dat

# Install Software
This guide will walk through how to setup your Raspberry Pi.


* Step 1:  Setup [RasperryPi](TODO)
* Step 2:  Depending on your current OS, select the one of the following route:
  * Setup using Windows PC (TODO) 
  * Setup using Mac OS (TODO) 
  * Setup using Linux (Done)


---
## Step 1. Set up Raspberry Pi with your computer

Before getting started, make sure you have the hardware.
* Raspberry Pi 3.
* SD Card.
* Ethernet Cable.
* MicroUSB cable.


## Step 2. Install the Image 

### Linux
* From your computer, download official Raspbian Debian Image (https://www.raspberrypi.org/downloads/).
* Extract the imgage from `.zip` file.
* Insert SD card to the computer
  * Determine device tree using `sudo fdisk -l` and Unmount SD Card from the system. (`/dev/sdb` in this example)
  ```
  sudo umount /dev/sdb
  ```
  * Install Raspbian Debian Image to SD Card using `dd` command (probably takes around 5~20 minutes).
  ```shell
  sudo dd bs=1M if=./2018-04-18-raspbian-stretch.img of=/dev/sdb 
  ```

### Windows
* Download image
* TODO - Probably use `NOOBS`program. (https://www.raspberrypi.org/documentation/installation/noobs.md)

### Mac OS
* Download image
* TODO - Probably use `NOOBS`program. (https://www.raspberrypi.org/documentation/installation/noobs.md)
