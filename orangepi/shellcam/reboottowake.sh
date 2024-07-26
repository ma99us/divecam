#!/bin/bash

. setgpios.sh
. piesystem.sh

echo "Reboot to Camera mode"
all_off
reboot_to_wake
