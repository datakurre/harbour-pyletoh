# -*- coding: utf-8 -*-
try:
    import pydevd
    pydevd.settrace('localhost', port=50000, stdoutToServer=True, stderrToServer=True)  # noqa
except ImportError:
    pass

import os
import time
import operator
import functools
import pyotherside
import logging
import fcntl

logger = logging.getLogger('harbour-myletoh')
logging.basicConfig(level=logging.DEBUG)

I2C_SLAVE = 0x0703

I2C_PATH = '/dev/i2c-1'
I2C_STATE_PATH = '/sys/devices/platform/reg-userspace-consumer.0/state'

I2C_FILE = lambda: open(I2C_PATH, 'wb')
I2C_STATE_FILE = lambda: open(I2C_STATE_PATH, 'w')

I2C_SLEEP = 0.1

DRIVERS = {}


class Driver(list):
    def __init__(self, address):
        self.address = address
        super(Driver, self).__init__()

        with I2C_STATE_FILE() as fp:
            fp.write('1')
            fp.flush()
            time.sleep(I2C_SLEEP)

        with I2C_FILE() as fp:
            fcntl.ioctl(fp, I2C_SLAVE, self.address)

            # 0x00 Mode register 1, MODE1
            # 0x20 Register autoincrement enable, normal mode
            fp.write(bytearray([0x00, 0x20]))
            fp.flush()
            time.sleep(I2C_SLEEP)

            # 0x00 Mode register 1, MODE1
            # 0xa0 Restart
            fp.write(bytearray([0x00, 0xa0]))
            fp.flush()
            time.sleep(I2C_SLEEP)

            # 0x01 Mode register 2, MODE2
            # 0x10 Invert, opendrain
            fp.write(bytearray([0x01, 0x10]))
            fp.flush()
            time.sleep(I2C_SLEEP)

    def __call__(self):
        leds = sorted(self, key=operator.attrgetter('pin'))
        data = [0x06] + functools.reduce(operator.add, map(list, leds))

        with I2C_STATE_FILE() as fp:
            fp.write('1')
            fp.flush()
            time.sleep(I2C_SLEEP)

        with I2C_FILE() as fp:
            fcntl.ioctl(fp, I2C_SLAVE, self.address)
            fp.write(bytearray(data))
            fp.flush()
            time.sleep(I2C_SLEEP)


class LED(object):
    def __init__(self, address, pin, color, value=100):
        self.pin = pin
        self.offset = {
            'red': 2047,
            'green': 1023,
            'blue': 0
        }[color]
        self.multiplier = {
            'red': 8,
            'green': 12,
            'blue': 8
        }[color]
        self.value = value
        if address in DRIVERS:
            self.driver = DRIVERS[address]
        else:
            self.driver = DRIVERS[address] = Driver(address)
        self.driver.append(self)

    def __iter__(self):
        start = self.offset
        end = self.offset + self.value * self.multiplier

        logger.info('{0:s}, {1:s}'.format(str(start), str(end)))

        yield start & 0xff
        yield (start >> 8) & 0xff
        yield end & 0xff
        yield (end >> 8) & 0xff


class RGB(object):
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __call__(self, red, green, blue):
        self.red.value = min(max(red, 0), 256)
        self.green.value = min(max(green, 0), 256)
        self.blue.value = min(max(blue, 0), 256)


class App(dict):
    def __init__(self):
        logger.info('__init__: state --> enabled')
        super(App, self).__init__({
            'bottomleft': RGB(
                LED(0x41, 1, 'red'),
                LED(0x41, 0, 'green'),
                LED(0x41, 2, 'blue')
            ),
            'lowerleft': RGB(
                LED(0x41, 4, 'red'),
                LED(0x41, 3, 'green'),
                LED(0x41, 5, 'blue')
            ),
            'middleleft': RGB(
                LED(0x41, 7, 'red'),
                LED(0x41, 6, 'green'),
                LED(0x41, 8, 'blue')
            ),
            'upperleft': RGB(
                LED(0x41, 10, 'red'),
                LED(0x41, 9, 'green'),
                LED(0x41, 11, 'blue')
            ),
            'topleft': RGB(
                LED(0x41, 13, 'red'),
                LED(0x41, 12, 'green'),
                LED(0x41, 14, 'blue')
            ),
            'topight': RGB(
                LED(0x40, 1, 'red'),
                LED(0x40, 0, 'green'),
                LED(0x40, 2, 'blue')
            ),
            'upperright': RGB(
                LED(0x40, 4, 'red'),
                LED(0x40, 3, 'green'),
                LED(0x40, 5, 'blue')
            ),
            'middleright': RGB(
                LED(0x40, 7, 'red'),
                LED(0x40, 6, 'green'),
                LED(0x40, 8, 'blue')
            ),
            'lowerright': RGB(
                LED(0x40, 10, 'red'),
                LED(0x40, 9, 'green'),
                LED(0x40, 11, 'blue')
            ),
            'bottomright': RGB(
                LED(0x40, 13, 'red'),
                LED(0x40, 12, 'green'),
                LED(0x40, 14, 'blue')
            ),
        })

    def __del__(self):
        logger.info('__del__: state --> disabled')
        with I2C_STATE_FILE() as fp:
            fp.write('0')

    def action_on(self, red, green, blue):
        logger.info('action_on')
        for led in self.values():
            led(red, green, blue)
        tuple(map(operator.methodcaller('__call__'), DRIVERS.values()))

    def action_off(self):
        logger.info('action_off')
        for led in self.values():
            led(0, 0, 0)
        tuple(map(operator.methodcaller('__call__'), DRIVERS.values()))

# Singleton app
_app = App()

# Method aliases
action_on = _app.action_on
action_off = _app.action_off
cleanup = _app.__del__


# Dummy
def __main__():
    pass
