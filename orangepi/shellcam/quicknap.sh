#!/bin/bash

. setgpios.sh
. piesystem.sh

echo "Quick nap"
all_off
hibernate 20
