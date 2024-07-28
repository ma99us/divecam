#!/bin/bash

. setgpios.sh

echo "Lights Off"
pin_write 6 0
