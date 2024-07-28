#!/bin/bash

. setgpios.sh

echo "Lights On"
pin_write 6 1
