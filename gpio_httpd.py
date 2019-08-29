#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import logging
import argparse

from datetime import datetime
from wsgiref.simple_server import make_server

import falcon

class GetPin(object):
    def on_get(self, req, resp, pin):
        GPIO.setup(pin, GPIO.IN)
        logging.debug("Get {0}".format(pin))
        resp.body = str(1 if GPIO.input(pin) else 0)
        resp.status = falcon.HTTP_200

class SetLow(object):
    def on_post(self, req, resp, pin):
        GPIO.setup(pin, GPIO.OUT)
        duration = req.get_param_as_int("ms", min_value=1, required=True) / 1000.0
        logging.debug("Set {0} to GPIO.LOW for {1} seconds".format(pin, duration))
        GPIO.output(pin, GPIO.LOW)
        time.sleep(duration)
        logging.debug("Set {0} to GPIO.HIGH".format(pin))
        GPIO.output(pin, GPIO.HIGH)

def main(port):
    GPIO.setmode(GPIO.BCM)

    api = falcon.API()
    api.add_route('/{pin:int(num_digits=None,min=2,max=27)}/low', SetLow())
    api.add_route('/{pin:int(num_digits=None,min=2,max=27)}', GetPin())

    with make_server('', port, api) as httpd:
        logging.debug('Serving on port %s' % port)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            GPIO.cleanup()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true', help="enable debug logging", required=False)
    parser.add_argument("--port", help="port", required=False, default=80)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(level=('DEBUG' if args.debug else 'WARN'),
                        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    main(port=args.port)
