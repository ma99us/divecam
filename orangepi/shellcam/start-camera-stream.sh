#!/bin/bash

HOME_DIR="/home/orangepi/"
MJPG_STREAMER_DIR="${HOME_DIR}mjpg-streamer/mjpg-streamer-experimental/"

cd ${MJPG_STREAMER_DIR}

nohup ./runmjpg.sh > mjpg-streamer.log &