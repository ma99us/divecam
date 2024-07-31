#!/bin/bash

HOME_DIR="/home/orangepi/"
WAKE_FILE="${HOME_DIR}hibernate.txt"
HOTSPOT_FILE="${HOME_DIR}hotspot.txt"
MODE_FILE="${HOME_DIR}mode.txt"

write_mode(){
  echo "$1" >${MODE_FILE}
  date >> ${MODE_FILE}
}

if [ -f "$WAKE_FILE" ]; then
  rm -f "$WAKE_FILE" || true
  echo "Camera wake up"

  write_mode "wake"
  ${HOME_DIR}runonwake.sh
else
  if [ -f "$HOTSPOT_FILE" ]; then
    rm -f "$HOTSPOT_FILE" || true
    echo "Hotspot boot"

    write_mode "hotspot"
    ${HOME_DIR}runonhotspot.sh
  else
    echo "Normal boot"

    write_mode "normal"
    ${HOME_DIR}runonnormal.sh
  fi
fi
