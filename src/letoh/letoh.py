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
from letoh import animations
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

ANIMATIONS = {
    'breath': animations.Breath,
    'breath-slow': animations.BreathSlow,
    'breath-fast': animations.BreathFast,
    'swipe': animations.Swipe,
    'swipe-slow': animations.SwipeSlow,
    'swipe-fast': animations.SwipeFast
}


def enable(drivers=None, service=None):
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
    if service:
        service.StateChanged('enabled')
    elif HAS_PYOTHERSIDE:
        session_bus = dbus.SessionBus()
        try:
            ob = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
            service = dbus.Interface(ob, DBUS_INTERFACE)
            service.EmitStateChanged('enabled')
        except dbus.exceptions.DBusException:
            pyotherside.send('stateChanged', 'enabled')


def disable(service=None):
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
    if service:
        service.StateChanged('disabled')
    elif HAS_PYOTHERSIDE:
        session_bus = dbus.SessionBus()
        try:
            ob = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
            service = dbus.Interface(ob, DBUS_INTERFACE)
            service.EmitStateChanged('disabled')
        except dbus.exceptions.DBusException:
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
        red, green, blue = to_rgb(config.load().get('DEFAULT', 'color'))
        super(LeTOH, self).__init__({
            'bottomleft': RGB(
                LED(drivers[0], 1, 'red', red),
                LED(drivers[0], 0, 'green', green),
                LED(drivers[0], 2, 'blue', blue),
            ),
            'lowerleft': RGB(
                LED(drivers[0], 4, 'red', red),
                LED(drivers[0], 3, 'green', green),
                LED(drivers[0], 5, 'blue', blue),
            ),
            'middleleft': RGB(
                LED(drivers[0], 7, 'red', red),
                LED(drivers[0], 6, 'green', green),
                LED(drivers[0], 8, 'blue', blue),
            ),
            'upperleft': RGB(
                LED(drivers[0], 10, 'red', red),
                LED(drivers[0], 9, 'green', green),
                LED(drivers[0], 11, 'blue', blue),
            ),
            'topleft': RGB(
                LED(drivers[0], 13, 'red', red),
                LED(drivers[0], 12, 'green', green),
                LED(drivers[0], 14, 'blue', blue),
            ),
            'topright': RGB(
                LED(drivers[1], 1, 'red', red),
                LED(drivers[1], 0, 'green', green),
                LED(drivers[1], 2, 'blue', blue),
            ),
            'upperright': RGB(
                LED(drivers[1], 4, 'red', red),
                LED(drivers[1], 3, 'green', green),
                LED(drivers[1], 5, 'blue', blue),
            ),
            'middleright': RGB(
                LED(drivers[1], 7, 'red', red),
                LED(drivers[1], 6, 'green', green),
                LED(drivers[1], 8, 'blue', blue),
            ),
            'lowerright': RGB(
                LED(drivers[1], 10, 'red', red),
                LED(drivers[1], 9, 'green', green),
                LED(drivers[1], 11, 'blue', blue),
            ),
            'bottomright': RGB(
                LED(drivers[1], 13, 'red', red),
                LED(drivers[1], 12, 'green', green),
                LED(drivers[1], 14, 'blue', blue),
            ),
        })
        self.drivers = drivers

    def __bool__(self):
        return any(
            reduce(add, ((led.red.value, led.green.value, led.blue.value)
                         for led in self.values()))
        )

    # noinspection PyUnusedLocal
    def __call__(self, color=None, animation=None, service=None):
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
            if self or animation is True:
                enable(map(attrgetter('address'), self.drivers), service)
                deque(map(methodcaller('__call__'), self.drivers), 0)
            else:
                disable(service)
        except Exception as e:
            logger.error(str(e))


class Service(dbus.service.Object):
    def __init__(self, bus, object_path):
        dbus.service.Object.__init__(self, bus, object_path)
        self.letoh = LeTOH()
        self.animation = None

    def update(self, color):
        try:
            self.letoh(color=color, animation=True, service=self)
        except Exception as e:
            logger.error(str(e))

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='ss', out_signature='')
    def Enable(self, color=None, animation=None):
        # Get color
        if not color or not color.startswith('#'):
            if self.animation is None:
                color = config.load().get('DEFAULT', 'color',
                                          fallback='#ff0000')
            else:
                color = self.animation.color

        # Handle the simple case
        if self.animation is None:
            if animation in ANIMATIONS:
                self.animation = ANIMATIONS[animation](color, self.update)
            else:
                try:
                    self.letoh(color=color, service=self)
                except Exception as e:
                    logger.error(str(e))
            return

        # Stop on-going wrong animation
        if animation is not None and animation != self.animation.name:
            self.animation.stop()
            self.animation = None

        # Enable explicitly given animation
        if animation in ANIMATIONS and not self.animation:
            self.animation = ANIMATIONS[animation](color, self.update)
            return

        # Update on-going animation
        if self.animation:
            self.animation.color = color
            return

        # Re-start stopped animation
        if self.animation is not None:
            self.animation = self.animation.__class__(color, self.update)
            return

        # No animation
        try:
            self.letoh(color=color, service=self)
        except Exception as e:
            logger.error(str(e))

    # noinspection PyUnusedLocal
    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='s', out_signature='')
    def Notify(self, app_name):
        if self.animation is not None:
            self.animation.stop()
            self.animation = None

        settings = config.load()

        if not settings.has_section(app_name):
            settings.add_section(app_name)
            config.save(settings)

        color = settings.get(app_name, 'color', fallback='#ff0000')
        animation = settings.get(app_name, 'animation', fallback=None)

        self.Enable(color, animation)

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='', out_signature='')
    def Disable(self):
        if self.animation is not None:
            self.animation.stop()
            self.animation = None
        try:
            disable(self)
        except Exception as e:
            logger.error(str(e))

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='ss', out_signature='')
    def Save(self, color=None, animation=None):
        config.save_defaults(color=color, animation=animation)

    @dbus.service.method(dbus_interface=DBUS_INTERFACE,
                         in_signature='s', out_signature='')
    def EmitStateChanged(self, value):
        self.StateChanged(value)

    @dbus.service.signal(dbus_interface=DBUS_INTERFACE,
                         signature='s')
    def StateChanged(self, value):
        pass
