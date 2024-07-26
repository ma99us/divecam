#!/bin/bash

ROOT_PATH=/home/orangepi/shellcam/

cd ${ROOT_PATH} || exit

# enter power-saving mode
sudo tlp bat
sudo tlp usb
bluetooth off
wifi off

#stop optional services
systemctl --user stop pulseaudio.socket
systemctl --user stop pulseaudio.service
#sudo service bluetooth stop

. webserver.sh

webserver_kill

# start button listener
nohup python3 campins.py > campins.log &

# start the main camera routine
./runandsleep.sh
