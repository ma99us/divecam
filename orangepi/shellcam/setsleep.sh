#!/bin/bash

. piesystem.sh

sleep=${1:-1}
echo "Set sleep to $sleep minutes"
write_sleep_minutes "$sleep"
