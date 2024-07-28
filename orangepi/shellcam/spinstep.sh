#!/bin/bash

. setgpios.sh

echo "Start spinning"
pin_dbl_click 3
sleep 1.0
echo "Stop spinning"
pin_click 3 1.4
