#!/usr/bin/env python3

# Inspired by https://gist.github.com/jtangelder/e445e9a7f5e31c220be6
# Python3 http.server for Single Page Application

import glob
import http.server
import json
import logging
import os
import re
import socketserver
import sys
import urllib.parse
from http import HTTPStatus
from pathlib import Path
from subprocess import Popen, STDOUT, PIPE
from time import sleep

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("sever4spa")
logger.setLevel(logging.INFO)

WWW_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
HOME_DIR = "/home/orangepi/"
SCRIPTS_DIR = f"{HOME_DIR}shellcam/"
MODE_FILE = f"{HOME_DIR}mode.txt"

resources = re.compile('.png|.jpg|.jpeg|.js|.css|.ico|.gif|.svg', re.IGNORECASE)
all_pictures = []
total_size = 0


def shell_cmd(cmd, w_dir, do_wait=True):
    w_dir = w_dir if w_dir is not None else '.'
    logger.info("shell_cmd(%s, %s)", cmd, w_dir)
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd=w_dir)
    if do_wait:
        proc.wait()
        return proc.stdout.read().decode('UTF-8')
    else:
        return None


def pin_write(w_pi, is_high):
    return shell_cmd(["gpio", "write", str(w_pi), "1" if is_high else "0"], None)


def pin_blink(w_pi, duration_ms):
    res = pin_write(str(w_pi), True)
    duration_ms = duration_ms if duration_ms is not None else 100
    sleep(duration_ms / 1000)
    return pin_write(str(w_pi), False)


def read_mode_file():
    file = open(MODE_FILE, "r")
    lines = file.readlines()
    file.close()
    for i, s in enumerate(lines):
        lines[i] = s.strip()
    return tuple(lines)


def find_pictures(offset, limit):
    global all_pictures, total_size
    if offset == 0 or len(all_pictures) == 0:
        all_pictures = glob.glob("data/*.jpg")
        total_size = 0
        for f in all_pictures:
            total_size += os.path.getsize(f)
        logger.info("found %s bytes in %s pictures", total_size, len(all_pictures))
    if len(all_pictures) <= offset:
        return []
    return all_pictures[offset:offset + limit]


def do_api(api, req):
    logger.info("API: %s(%s)", api, str(req))
    match api:
        case "status":
            if os.path.exists(MODE_FILE):
                return read_mode_file()
            else:
                return "n/a"
        case "pin-write":
            w_pi = req['wPi']
            is_high = req['isHigh']
            logger.info("pin-write: pin=%s, high=%s", w_pi, is_high)
            # logger.info("shell_cmd result: \"%s\"", res)
            return pin_write(w_pi, is_high)
        case "pin-blink":
            w_pi = req['wPi']
            duration_ms = req['durationMs']
            logger.info("pin-blink: pin=%s, duration=%s", w_pi, duration_ms)
            return pin_blink(w_pi, duration_ms)
        case "pin-step":
            w_pi = req['wPi']
            duration_ms = req['durationMs']
            forward = req['forward']
            logger.info("pin-step: pin=%s, duration=%s, forward=%s", w_pi, duration_ms, forward)
            if forward:
                pin_blink(w_pi, None)
            pin_blink(w_pi, None)
            sleep(duration_ms / 1000)
            res = pin_blink(w_pi, 1400)
            return res
        case "go-to-sleep":
            minutes = req['minutes']
            logger.info("go-to-sleep: minutes=%s", minutes)
            res = shell_cmd([f"{SCRIPTS_DIR}setsleep.sh", str(minutes)], SCRIPTS_DIR)
            logger.info("shell_cmd result: \"%s\"", res)
            return res
        case "start-camera-stream":
            logger.info("start-camera-stream")
            res = shell_cmd([f"{SCRIPTS_DIR}start-camera-stream.sh"], SCRIPTS_DIR, False)
            logger.info("shell_cmd result: \"%s\"", res)
            return res
        case "stop-camera-stream":
            logger.info("stop-camera-stream")
            res = shell_cmd([f"{SCRIPTS_DIR}stop-camera-stream.sh"], SCRIPTS_DIR, False)
            logger.info("shell_cmd result: \"%s\"", res)
            return res
        case "find-pictures":
            offset = req['offset'] if req is not None else 0
            limit = req['limit'] if req is not None else 10
            pictures = find_pictures(offset, limit)
            logger.info("returning %s pictures in range (%s, %s)", len(pictures), offset, offset + limit)
            return pictures
        case "pictures-info":
            global all_pictures, total_size
            if len(all_pictures) == 0 or total_size == 0:
                find_pictures(0, 10)
            return {"files": len(all_pictures), "size": total_size}
        case "reboot":
            mode = req['mode']
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
                    raise RuntimeError(f"Unexpected 'reboot' mode: {mode}")
        case _:
            raise RuntimeError(f"Unexpected API request: {api}")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_api_request(self, api, req):
        try:
            res = do_api(api, req)
            if isinstance(res, (int, float, str, bool)):
                # text response
                self.send_response(HTTPStatus.OK)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/text')
                content = res.encode()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            elif res is not None:
                # json object response
                self.send_response(HTTPStatus.OK)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                content = json.dumps(res.__dict__ if hasattr(res, "__dict__") else res).encode()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                # empty response
                self.send_response(HTTPStatus.NO_CONTENT)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
        except Exception as err:
            logger.error(err)
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR,
                            "API Exception {} in '{}':{}; ({})".format(err, api, req, self.path))
        except:
            logger.error('Unexpected error!')
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "API Error in '{}':{}; ({})".format(api, req, self.path))

    def do_GET(self):
        self.path = urllib.parse.unquote(self.path)
        url_parts = urllib.parse.urlparse(self.path)
        request_file_path = Path(url_parts.path.strip("/"))

        if len(request_file_path.parts) > 0 and request_file_path.parts[0] == "api":
            api = request_file_path.parts[1]
            req = request_file_path.parts[2] if len(request_file_path.parts) > 2 else None
            self.do_api_request(api, req)
            return

        # serve regular web resources
        ext = request_file_path.suffix
        if not request_file_path.is_file() or resources.match(ext) is None:
            self.path = 'index.html'

        logger.info("GET: \"{}\"".format(self.path))
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        self.path = urllib.parse.unquote(self.path)
        url_parts = urllib.parse.urlparse(self.path)
        request_file_path = Path(url_parts.path.strip("/"))

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        # logger.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))

        if len(request_file_path.parts) > 0 and request_file_path.parts[0] == "api":
            api = request_file_path.parts[1]
            req = json.loads(post_data) if post_data is not None else None
            self.do_api_request(api, req)
            return

        self.send_error(HTTPStatus.NOT_IMPLEMENTED, "Not Implemented; POST: {}".format(self.path))


# web_dir = os.path.join(os.path.dirname(__file__), DIR)
web_dir = WWW_DIR
os.chdir(web_dir)

httpd = socketserver.TCPServer(('0.0.0.0', PORT), Handler)
logger.info("Starting web server in \"%s\" on port %s", os.path.abspath(web_dir), str(PORT))
httpd.serve_forever()
