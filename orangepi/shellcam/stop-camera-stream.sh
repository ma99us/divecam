#!/bin/bash

HOME_DIR="/home/orangepi/"
MJPG_STREAMER_DIR="${HOME_DIR}mjpg-streamer/mjpg-streamer-experimental/"

cd ${MJPG_STREAMER_DIR}

#killall -q runmjpg.sh
killall -q mjpg_streamer