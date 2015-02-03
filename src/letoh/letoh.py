# -*- coding: utf-8 -*-
import time
import fcntl
from collections import deque
from operator import add
from operator import attrgetter
from operator import methodcaller
from functools import reduce

import dbus
import dbus.service
from letoh import logger
from letoh import config
from letoh.utils import to_rgb
from letoh.utils import from_rgb

try:
    import pyotherside
    HAS_PYOTHERSIDE = True
except ImportError:
    HAS_PYOTHERSIDE = False


DBUS_SERVICE = 'harbour.pyletoh'
DBUS_INTERFACE = 'harbour.pyletoh'
DBUS_PATH = '/harbour/pyletoh'

I2C_SLAVE = 0x0703

I2C_PATH = '/dev/i2c-1'
I2C_STATE_PATH = '/sys/devices/platform/reg-userspace-consumer.0/state'

I2C_FILE = lambda mode='wb': open(I2C_PATH, mode)
I2C_STATE_FILE = lambda mode='w': open(I2C_STATE_PATH, mode)
I2C_SLEEP = 0.001

LETOH_RIGHT = 0x40
LETOH_LEFT = 0x41


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

    # Signal state change
    session_bus = dbus.SessionBus()
    try:
        ob = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
        service = dbus.Interface(ob, DBUS_INTERFACE)
        service.EmitStateChanged('enabled')
    except dbus.exceptions.DBusException:
        if HAS_PYOTHERSIDE:
            pyotherside.send('stateChanged', 'enabled')


def disable():
    with I2C_STATE_FILE('r') as fp:
        state = fp.read().strip()
    if state == 'disabled':
        return False

    logger.info('LeTOH off')
    with I2C_STATE_FILE() as fp:
        fp.write('0')
        fp.flush()
    time.sleep(I2C_SLEEP)

    # Signal state change
    session_bus = dbus.SessionBus()
    try:
        ob = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
        service = dbus.Interface(ob, DBUS_INTERFACE)
        service.EmitStateChanged('disabled')
    except dbus.exceptions.DBusException:
        if HAS_PYOTHERSIDE:
            pyotherside.send('stateChanged', 'disabled')


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
        drivers = [Driver(LETOH_LEFT), Driver(LETOH_RIGHT)]
        super(LeTOH, self).__init__({
            'bottomleft': RGB(
                LED(drivers[0], 1, 'red'),
                LED(drivers[0], 0, 'green'),
                LED(drivers[0], 2, 'blue'),
            ),
            'lowerleft': RGB(
                LED(drivers[0], 4, 'red'),
                LED(drivers[0], 3, 'green'),
                LED(drivers[0], 5, 'blue'),
            ),
            'middleleft': RGB(
                LED(drivers[0], 7, 'red'),
                LED(drivers[0], 6, 'green'),
                LED(drivers[0], 8, 'blue'),
            ),
            'upperleft': RGB(
                LED(drivers[0], 10, 'red'),
                LED(drivers[0], 9, 'green'),
                LED(drivers[0], 11, 'blue'),
            ),
            'topleft': RGB(
                LED(drivers[0], 13, 'red'),
                LED(drivers[0], 12, 'green'),
                LED(drivers[0], 14, 'blue'),
            ),
            'topright': RGB(
                LED(drivers[1], 1, 'red'),
                LED(drivers[1], 0, 'green'),
                LED(drivers[1], 2, 'blue'),
            ),
            'upperright': RGB(
                LED(drivers[1], 4, 'red'),
                LED(drivers[1], 3, 'green'),
                LED(drivers[1], 5, 'blue'),
            ),
            'middleright': RGB(
                LED(drivers[1], 7, 'red'),
                LED(drivers[1], 6, 'green'),
                LED(drivers[1], 8, 'blue'),
            ),
            'lowerright': RGB(
                LED(drivers[1], 10, 'red'),
                LED(drivers[1], 9, 'green'),
                LED(drivers[1], 11, 'blue'),
            ),
            'bottomright': RGB(
                LED(drivers[1], 13, 'red'),
                LED(drivers[1], 12, 'green'),
                LED(drivers[1], 14, 'blue'),
            ),
        })
        self.drivers = drivers

    def __bool__(self):
        return any(
            reduce(add, ((led.red.value, led.green.value, led.blue.value)
                         for led in self.values()))
        )

    def __call__(self, color=None):
        if isinstance(color, str):
            red, green, blue = to_rgb(color)
            for led in self.values():
                led(red, green, blue)
        elif isinstance(color, list) or isinstance(color, tuple):
            red, green, blue = tuple(color[:3])
            for led in self.values():
                led(red, green, blue)
        elif isinstance(color, dict):
            for name, value in color.items():
                if name not in self:
                    continue
                if isinstance(value, str):
                    self[name](*to_rgb(value))
                elif isinstance(value, list) or isinstance(value, tuple):
                    self[name](*tuple(value[:3]))

        try:
            if color is False or not self:
                disable()
            else:
                enable(map(attrgetter('address'), self.drivers))
                deque(map(methodcaller('__call__'), self.drivers), 0)
        except Exception as e:
            logger.error(str(e))

    def save(self, color=None):
        self(color)
        settings = config.load()
        for name, value in self.items():
            settings.set('default', 'color', from_rgb(
                value.red.value, value.green.value, value.blue.value))
        config.save(settings)


class Service(dbus.service.Object):
    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='s', out_signature='')
    def EmitStateChanged(self, value):
        self.StateChanged(value)

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE,
                         signature='s')
    def StateChanged(self, value):
        pass


services = {}


def get_service(service_bus, object_path):
    if object_path not in services:
        services[object_path] = Service(service_bus, object_path)
    return services[object_path]
