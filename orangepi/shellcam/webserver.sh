#!/bin/bash

WWW_PATH=/home/orangepi/www/

webserver_serve() {
  dir=${1:-${WWW_PATH}}
  port=${2:-8000}
  echo "Starting web server in $dir on port $port"
#  python3 -m http.server "$port" -d "$dir"
  python3 server4spa.py "$dir" "$port"
}

webserver_kill() {
  killall -q python3
}
