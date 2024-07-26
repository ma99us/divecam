#!/bin/bash

DATA_PATH=${DATA_PATH:=/media/sdcard/data/}
CAMERA_NAME="Dive Cam 1"

#CAM_INPUT="\
#-d /dev/video1 -r 1920x1080 --set brightness=30% --set framerate=1 --rotate 180 \
#"
CAM_INPUT="\
-d /dev/video1 -r 1280x720 --rotate 180 \
"

#CAM_CAPTURE=""
CAM_CAPTURE="\
-D 0.3 -S 20 -F 1 \
"

cam_title="$(echo "${CAMERA_NAME}" | tr -d ' ')"
CAM_OPT="\
--quiet --top-banner --banner-colour #FF000000 --line-colour #FF000000 --title ${cam_title} --timestamp %Y-%m-%d_%H:%M:%S \
"

cam_capture_name="$(echo "${CAMERA_NAME}" | tr -d ' ' | tr '[:upper:]' '[:lower:]')"
CAM_OUTPUT="${DATA_PATH}${cam_capture_name}_%Y-%m-%d_%H-%M-%S.jpg"

CAM_CMD="fswebcam ${CAM_INPUT} ${CAM_CAPTURE} ${CAM_OPT} ${CAM_OUTPUT}"

take_photo() {
  # echo ${CAM_CMD}
  ${CAM_CMD}
}

cam_setup() {
  # no autofocus
  v4l2-ctl -d 1 -c focus_automatic_continuous=0
  # set focus to eternity
  v4l2-ctl -d 1 -c focus_absolute=0
}

echo "Setup camera"
cam_setup
