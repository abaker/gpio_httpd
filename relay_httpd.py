#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import logging
import argparse

from datetime import datetime
from wsgiref.simple_server import make_server

import falcon

class Relay(object):
    def __init__(self, **kwargs):
        self.pin = kwargs['pin']

    def on_post(self, req, resp, **kwargs):
        logging.debug("activating relay")
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(self.pin, GPIO.HIGH)

def main(pin, port):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    api = falcon.API()
    api.add_route('/activate', Relay(pin=pin))

    with make_server('', port, api) as httpd:
        logging.debug('Serving on port %s' % port)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            GPIO.cleanup()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true', help="enable debug logging", required=False)
    parser.add_argument("--port", help="port", required=False, default=8080)
    parser.add_argument("--pin", help="GPIO pin", type=int, required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(level=('DEBUG' if args.debug else 'WARN'),
                        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    main(pin=args.pin, port=args.port)
