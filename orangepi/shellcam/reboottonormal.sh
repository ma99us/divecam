#!/bin/bash

. setgpios.sh
. piesystem.sh

echo "Reboot to Normal mode"
all_off
reboot_to_normal
