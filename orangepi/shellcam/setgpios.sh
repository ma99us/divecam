#!/bin/bash

GPIO_OUT_PINS=(3 6 9 10 13)

all_off() {
  pin_click 3 1.4   # motor off
  pin_write 6 0     # lights off
}

pin_set_mode_out() {
  PIN_CMD="gpio mode $1 out"
  # echo ${PIN_CMD}
  ${PIN_CMD}
}

pin_write() {
  PIN_CMD="gpio write $1 $2"
  # echo ${PIN_CMD}
  ${PIN_CMD}
}

pin_read() {
  PIN_CMD="gpio read $1"
  # echo ${PIN_CMD}
  res=$(${PIN_CMD})
  echo res
}

pin_click() {
  pin_write $1 1
  sleep "${2:-0.1}"
  pin_write $1 0
}

pin_dbl_click() {
  pin_click $1
  sleep "${2:-0.1}"
  pin_click $1
}

pin_set_all() {
  for i in "${!GPIO_OUT_PINS[@]}"; do
    pin_set_mode_out "${GPIO_OUT_PINS[$i]}"
  done
}

pin_set_all
