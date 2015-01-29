# -*- coding: utf-8 -*-
try:
    import pydevd
    pydevd.settrace('localhost', port=50000, stdoutToServer=True, stderrToServer=True)  # noqa
except ImportError:
    pass

import time
import logging
import fcntl

from collections import deque
from operator import add
from operator import attrgetter
from operator import methodcaller
from functools import reduce

logger = logging.getLogger('harbour-myletoh')
logging.basicConfig(level=logging.DEBUG)

I2C_SLAVE = 0x0703

I2C_PATH = '/dev/i2c-1'
I2C_STATE_PATH = '/sys/devices/platform/reg-userspace-consumer.0/state'

I2C_FILE = lambda mode='wb': open(I2C_PATH, mode)
I2C_STATE_FILE = lambda mode='w': open(I2C_STATE_PATH, mode)

I2C_SLEEP = 0.001

DRIVER_RIGHT = 0x40
DRIVER_LEFT = 0x41


def enable(drivers=None):
    with I2C_STATE_FILE('r') as fp:
        state = fp.read().strip()
    if state == 'enabled':
        return

    logger.info('LeTOH on')
    with I2C_STATE_FILE() as fp:
        fp.write('1')
        fp.flush()
    time.sleep(I2C_SLEEP)

    with I2C_FILE() as fp:
        for driver in drivers or ():
            fcntl.ioctl(fp, I2C_SLAVE, driver)

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


def disable():
    with I2C_STATE_FILE('r') as fp:
        state = fp.read().strip()
    if state == 'disabled':
        return

    logger.info('LeTOH off')
    with I2C_STATE_FILE() as fp:
        fp.write('0')
        fp.flush()
    time.sleep(I2C_SLEEP)


class Driver(list):
    def __init__(self, address):
        self.address = address
        super(Driver, self).__init__()

    def __call__(self):
        leds = sorted(self, key=attrgetter('pin'))
        data = [0x06] + reduce(add, map(list, leds))
        with I2C_FILE() as fp:
            fcntl.ioctl(fp, I2C_SLAVE, self.address)
            fp.write(bytearray(data))
            fp.flush()
            time.sleep(I2C_SLEEP)


class LED(object):
    def __init__(self, driver, pin, color, value=0):
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
        self.driver = driver
        driver.append(self)

    def __iter__(self):
        start = self.offset
        end = self.offset + self.value * self.multiplier

        # logger.debug('{0:s}, {1:s}'.format(str(start), str(end)))

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


class LeTOH(dict):
    def __init__(self):
        left = Driver(DRIVER_LEFT)
        right = Driver(DRIVER_RIGHT)
        super(LeTOH, self).__init__({
            'bottomleft': RGB(
                LED(left, 1, 'red'),
                LED(left, 0, 'green'),
                LED(left, 2, 'blue')
            ),
            'lowerleft': RGB(
                LED(left, 4, 'red'),
                LED(left, 3, 'green'),
                LED(left, 5, 'blue')
            ),
            'middleleft': RGB(
                LED(left, 7, 'red'),
                LED(left, 6, 'green'),
                LED(left, 8, 'blue')
            ),
            'upperleft': RGB(
                LED(left, 10, 'red'),
                LED(left, 9, 'green'),
                LED(left, 11, 'blue')
            ),
            'topleft': RGB(
                LED(left, 13, 'red'),
                LED(left, 12, 'green'),
                LED(left, 14, 'blue')
            ),
            'topight': RGB(
                LED(right, 1, 'red'),
                LED(right, 0, 'green'),
                LED(right, 2, 'blue')
            ),
            'upperright': RGB(
                LED(right, 4, 'red'),
                LED(right, 3, 'green'),
                LED(right, 5, 'blue')
            ),
            'middleright': RGB(
                LED(right, 7, 'red'),
                LED(right, 6, 'green'),
                LED(right, 8, 'blue')
            ),
            'lowerright': RGB(
                LED(right, 10, 'red'),
                LED(right, 9, 'green'),
                LED(right, 11, 'blue')
            ),
            'bottomright': RGB(
                LED(right, 13, 'red'),
                LED(right, 12, 'green'),
                LED(right, 14, 'blue')
            ),
        })
        self.drivers = [left, right]

    def __bool__(self):
        return any(
            reduce(add, ((led.red.value, led.green.value, led.blue.value)
                         for led in self.values()))
        )

    def __call__(self):
        if self:
            enable(map(attrgetter('address'), self.drivers))
            deque(map(methodcaller('__call__'), self.drivers), 0)
        else:
            disable()

    def set_color(self, red=None, green=None, blue=None,
                  name=None, update=True):
        if None not in (red, green, blue):
            if name in self:
                # Update named led
                self[name](red, green, blue)
            else:
                # Update all leds
                for led in self.values():
                    led(red, green, blue)
        if update:
            self()

    def __del__(self):
        disable()

# Singleton app
_letoh = LeTOH()

# Method aliases
set_color = _letoh.set_color
turn_on = _letoh.__call__
turn_off = disable


# Dummy
def __main__():
    pass
