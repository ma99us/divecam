#!/bin/bash

HOTSPOT_NAME="divecam1"
HOTSPOT_IP="192.168.10.1"

hotspot_start() {
  sudo nmcli con up "$HOTSPOT_NAME"
  sudo /etc/init.d/dnsmasq restart
}

hotspot_stop() {
  sudo /etc/init.d/dnsmasq stop
  sudo nmcli con down "$HOTSPOT_NAME"
}