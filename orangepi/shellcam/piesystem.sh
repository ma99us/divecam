#!/bin/bash

HOME_DIR="/home/orangepi/"
WAKE_FILE="${HOME_DIR}hibernate.txt"
HOTSPOT_FILE="${HOME_DIR}hotspot.txt"
SLEEP_FILE="${HOME_DIR}sleep.txt"

set_hibernate_flag() {
  date >"${WAKE_FILE}"
}

clear_hibernate_flag() {
  rm -f "${WAKE_FILE}" || true
}

set_hotspot_flag() {
  date >"${HOTSPOT_FILE}"
}

clear_hotspot_flag() {
  rm -f "${HOTSPOT_FILE}" || true
}

reboot_to_normal() {
  clear_hibernate_flag
  clear_hotspot_flag
  sudo reboot
}

reboot_to_wake() {
  clear_hotspot_flag
  set_hibernate_flag
  echo "reboot" >>${WAKE_FILE}
  sync
  sudo reboot
}

reboot_to_hotspot() {
  clear_hibernate_flag
  set_hotspot_flag
  echo "reboot" >>${HOTSPOT_FILE}
  sync
  sudo reboot
}

hibernate() {
  set_hibernate_flag
  echo "hibernate $1" >>${WAKE_FILE}
  sync
  sudo rtcwake -m mem -s "$1"
}

hibernate_minutes() {
  seconds=$((60 * $1))
  hibernate "${seconds}"
}

read_sleep_minutes() {
  if is_sleep_set; then
    #    echo "sleep=$(cat "$1" | tr -dc [:digit:])"
    echo $(cat "${SLEEP_FILE}" | tr -dc [:digit:])
  else
    echo 0
  fi
}

write_sleep_minutes() {
  echo "$1" >"${SLEEP_FILE}"
}

is_sleep_set() {
  [ -f "${SLEEP_FILE}" ]
}
