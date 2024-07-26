#!/bin/bash

. setgpios.sh
. piesystem.sh

echo "Reboot to Hotspot mode"
all_off
reboot_to_hotspot
