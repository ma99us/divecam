#!/usr/bin/env python3

# Python GPIO functions for OrangePI 3 LTS board

import logging
import os
import signal
import sys
import time
from pathlib import Path
from subprocess import Popen, STDOUT, PIPE

import OPi.GPIO as GPIO
import orangepi.pi3

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("campins")
logger.setLevel(logging.INFO)

argument = sys.argv[1] if len(sys.argv) > 1 else ""
HOME_DIR = "/home/orangepi/"
SCRIPTS_DIR = f"{HOME_DIR}shellcam/"
MODE_FILE = f"{HOME_DIR}mode.txt"

GPIO.setwarnings(False)
GPIO.setmode(orangepi.pi3.BOARD)

GPIO.setup(15, GPIO.IN, initial=0, pull_up_down=GPIO.PUD_DOWN)  # blue listener
GPIO.setup(10, GPIO.IN, initial=0, pull_up_down=GPIO.PUD_DOWN)  # orange listener
GPIO.setup(26, GPIO.IN, initial=0, pull_up_down=GPIO.PUD_DOWN)  # green listener

GPIO.setup(16, GPIO.OUT, initial=0)  # blue led - normal boot
GPIO.setup(22, GPIO.OUT, initial=0)  # orange led - hotspot boot
GPIO.setup(18, GPIO.OUT, initial=0)  # green led - camera boot
GPIO.setup(12, GPIO.OUT, initial=0)  # camera lights

last_button = -1


def shell_cmd(cmd, w_dir):
    w_dir = w_dir if w_dir is not None else '.'
    logger.info("shell_cmd(%s, %s)", cmd, w_dir)
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd=w_dir)
    proc.wait()
    return proc.stdout.read().decode('UTF-8')


def read_mode_file():
    if not os.path.exists(MODE_FILE):
        raise RuntimeError("No 'mode' file!")
    file = open(MODE_FILE, "r")
    lines = file.readlines()
    file.close()
    for i, s in enumerate(lines):
        lines[i] = s.strip()
    return lines[0] if len(lines) > 0 else ''


def parse_mode(mode):
    match mode:
        case "normal":
            switch_channel(16)
        case "hotspot":
            switch_channel(22)
        case "wake":
            switch_channel(18)
        case _:
            logger.warning(f"Unexpected 'reboot' mode: {mode}")


def reboot(mode):
    logger.info("reboot; mode=%s", mode)
    match mode:
        case "normal":
            res = shell_cmd([f"{SCRIPTS_DIR}reboottonormal.sh"], SCRIPTS_DIR)
            logger.info("shell_cmd result: \"%s\"", res)
            return res
        case "hotspot":
            res = shell_cmd([f"{SCRIPTS_DIR}reboottohotspot.sh"], SCRIPTS_DIR)
            logger.info("shell_cmd result: \"%s\"", res)
            return res
        case "wake":
            res = shell_cmd([f"{SCRIPTS_DIR}reboottowake.sh"], SCRIPTS_DIR)
            logger.info("shell_cmd result: \"%s\"", res)
            return res
        case _:
            logger.warning(f"Unexpected 'reboot' mode: {mode}")


def toggle_channel(channel):
    GPIO.output(channel, not GPIO.input(channel))


def switch_channel(channel):
    for x in [16, 22, 18, 12]:
        if x == channel:
            GPIO.output(x, 1)
        else:
            GPIO.output(x, 0)


def animate_all(speed=0.2):
    GPIO.output(16, 1)
    time.sleep(speed)
    GPIO.output(16, 0)
    GPIO.output(22, 1)
    time.sleep(speed)
    GPIO.output(22, 0)
    GPIO.output(18, 1)
    time.sleep(speed)
    GPIO.output(18, 0)
    GPIO.output(22, 1)
    time.sleep(speed)
    GPIO.output(22, 0)
    GPIO.output(16, 1)
    time.sleep(speed)
    GPIO.output(16, 0)


def btn_callback(channel):
    global last_button
    print(f"btn pressed {channel}, last button={last_button}")
    do_act = last_button == channel
    last_button = channel
    if channel == 15:
        if do_act:
            animate_all()
            # time.sleep(1)
            reboot('normal')
        else:
            switch_channel(16)
    if channel == 10:
        if do_act:
            animate_all()
            # time.sleep(1)
            reboot('hotspot')
        else:
            switch_channel(22)
    if channel == 26:
        if do_act:
            animate_all()
            # time.sleep(1)
            reboot('wake')
        else:
            switch_channel(18)


GPIO.add_event_detect(10, GPIO.RISING, callback=btn_callback, bouncetime=500)
GPIO.add_event_detect(26, GPIO.RISING, callback=btn_callback, bouncetime=500)
GPIO.add_event_detect(15, GPIO.RISING, callback=btn_callback, bouncetime=500)


def block_on_keyboard():
    try:
        print("Press CTRL+C to exit")
        while True:
            time.sleep(0.100)
            in_key = input("press a number:\n")
            if in_key == '1':
                toggle_channel(16)
            if in_key == '2':
                toggle_channel(22)
            if in_key == '3':
                toggle_channel(18)
            if in_key == '4':
                animate_all(0.2)
            if in_key == '0':
                toggle_channel(12)
    except KeyboardInterrupt:
        logging.warning("interrupted.")
        raise RuntimeError("interrupted.")


try:
    animate_all(0.2)
    mode = read_mode_file()
    parse_mode(mode)

    if argument == 'keyboard':
        block_on_keyboard()
    else:
        print("block without input...\n")
        signal.pause()      # block forever, without input

finally:
    animate_all(0.2)
    GPIO.cleanup()
    print("\nDone.")
