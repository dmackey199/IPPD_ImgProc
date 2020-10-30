# PARTS NEEDED

HDMI Cord
Keyboard
Mouse
SD Card (32 GB minimum)
USB Charger Type B (typical Android charger)
Raspberry Pi

# STEPS

Download the Raspberry Pi OS at
https://www.raspberrypi.org/downloads/raspberry-pi-os/

Download the Raspberry Pi Imager (used to download Raspberry Pi OS onto SD Card)
https://www.raspberrypi.org/downloads/

Insert SD Card into your device
Open Raspberry Pi Imager
Select your SD Card
Select your Raspberry Pi OS
Click Write

Plug in keyboard, mouse, and USB charger (power supply), into your Raspberry Pi. Plug HDMI cord to Raspberry Pi and a monitor/TV.
Once loaded in, open Raspberry Pi terminal (on the top task bar)
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

Create a directory where to store Open CV files (Desktop recommended e.g. ~/Desktop/<my_directory>)
Here is an example:
cd Desktop
mkdir ImgProc
cd ImgProc
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd opencv
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
If above does not work, try "cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local .." which just has no spaces after flags
make -j1 (-j1 specifies to only use one processor, which makes it slower to build, but is safer since multiple processors could make it freeze)
sudo make install

# TROUBLESHOOTING

Still freezing on make? Maybe the Raspberry Pi is swapping itself to death. You can open a separate terminal and type "free" to look at it.
To increase swap size:
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
Use arrow keys to maneuver down to CONF_SWAPSIZE variable
The default should be 100, but change that to 1024 or 2048
To save changes, do Ctrl+O then ENTER to save, and then Ctrl+X to exit the file.
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
Go to the directory you created within the opencv directory (e.g. release in the example above) and try using "make again"
If it works, it is recommended you follow the above steps again to change the CONF_SWAPSIZE variable back to its default.
