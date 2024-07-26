#!/bin/bash

ROOT_PATH=/home/orangepi/shellcam/

cd ${ROOT_PATH} || exit

# enter power-saving mode
#sudo tlp bat
sudo tlp usb
bluetooth off
#wifi on

. setgpios.sh
. piesystem.sh
. takephoto.sh
. webserver.sh
. hotspot.sh

# start hotspot
hotspot_start

sleep 1

webserver_kill

# start button listener
nohup python3 campins.py > campins.log &

# start web server
webserver_serve
