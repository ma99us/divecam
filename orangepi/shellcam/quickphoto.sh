#!/bin/bash

. setgpios.sh
. takephoto.sh

echo "Light on"
pin_write 4 1

echo "Taking a photo"
take_photo

echo "Light off"
pin_write 4 0
