#!/bin/bash

. setgpios.sh
. piesystem.sh
. takephoto.sh
. webserver.sh

webserver_kill

# start web server
webserver_serve