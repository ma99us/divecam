#!/bin/bash

. takephoto.sh
. setgpios.sh

spin_capture() {
  #echo "Light on"
  #pin_write 6 1

  #echo "Start spinning"
  #pin_click 3

  total=10
  delay=0.91
  echo "Take $total photos with $delay seconds delay"
  for ((count = 1; count <= total; count++)); do
    echo "Light on"
    pin_write 6 1

    echo "Taking photo $count"
    take_photo

    echo "Light off"
    pin_write 6 0

#    if [ $count = $total ]; then
#      break
#    fi

    echo "Start spinning"
    pin_dbl_click 3
    sleep $delay
    echo "Stop spinning"
    pin_click 3 1.4
  done

  #echo "Stop spinning"
  #pin_click 3 1.4

  #echo "Light off"
  #pin_write 6 0
}
