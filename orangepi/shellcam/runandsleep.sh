#!/bin/bash

. piesystem.sh
. spinandcapture.sh

if is_sleep_set; then
  SLEEP_MINS=$(read_sleep_minutes)
  echo "Sleep set to ${SLEEP_MINS} minutes"
else
  echo "No sleep set, using default 1 minute"
  write_sleep_minutes "${1:-1}"
fi

# forever loop
while true; do
  clear_hibernate_flag

  echo "Doing spin and capture cycle"
  spin_capture

  SLEEP_MINS=$(read_sleep_minutes)
  if [[ $SLEEP_MINS -gt 0 ]]; then
    echo "Go to sleep for ${SLEEP_MINS} minutes"
    hibernate_minutes SLEEP_MINS
  else
    echo "Go again"
  fi
done
