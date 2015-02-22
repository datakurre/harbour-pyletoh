# -*- coding: utf-8 -*-
import math
import threading
import time

from letoh import logger
from letoh.utils import to_rgb
from letoh.utils import from_rgb
import pytweening


class Animation(threading.Thread):
    alive = True

    red = 0
    green = 0
    blue = 0

    duration = 1.0

    def __init__(self, color, callback):
        super(Animation, self).__init__()
        self.color = color
        self.callback = callback
        self.start()

    @property
    def color(self):
        return from_rgb(self.red, self.green, self.blue)

    @color.setter
    def color(self, color):
        self.red, self.green, self.blue = to_rgb(color)

    def stop(self):
        self.alive = False

    def __bool__(self):
        return self.alive


class Breath(Animation):
    duration = 4.0

    def run(self):
        while self.alive:
            x = ((math.fabs(time.time() % self.duration * 2 - self.duration))
                 / self.duration)
            factor = pytweening.easeInOutCubic(x)
            self.callback(from_rgb(self.red * factor,
                                   self.green * factor,
                                   self.blue * factor))
            time.sleep(1 / 30.)  # fps


class BreathSlow(Breath):
    duration = 8.0


class BreathFast(Breath):
    duration = 2.0


class Swipe(Animation):
    duration = 3.5

    def run(self):
        groups = [
            ['bottomleft', 'bottomright'],
            ['lowerleft', 'lowerright'],
            ['middleleft', 'middleright'],
            ['upperleft', 'upperright'],
            ['topleft', 'topright'],
        ]
        while self.alive:
            x = ((math.fabs(time.time() % self.duration * 2 - self.duration))
                 / self.duration)
            factor = math.floor(pytweening.linear(x) * 13) - 5

            colors = {}
            for i in range(len(groups)):
                distance = pytweening.easeInCubic(
                    max(0, (4 - abs(i - factor))) / 4.)
                for led in groups[i]:
                    colors[led] = from_rgb(self.red * distance,
                                           self.green * distance,
                                           self.blue * distance)
            self.callback(colors)
            time.sleep(1 / 30.)  # fps


class SwipeSlow(Swipe):
    duration = 4.5


class SwipeFast(Swipe):
    duration = 2.0


class Around(Animation):
    duration = 1.5

    def run(self):
        leds = [
            'topright',
            'upperright',
            'middleright',
            'lowerright',
            'bottomright',
            'bottomleft',
            'lowerleft',
            'middleleft',
            'upperleft',
            'topleft'
        ]

        while self.alive:
            x = (time.time() % self.duration) / self.duration
            factor = math.floor(pytweening.linear(x) * 10)

            colors = {}
            for i in range(len(leds)):
                distance = pytweening.easeInExpo(max(
                    max(0, (4 - abs(i - factor)) / 4.),
                    max(0, (4 - abs((i + 9) - factor)) / 4.)
                ))
                led = leds[i]
                colors[led] = from_rgb(self.red * distance,
                                       self.green * distance,
                                       self.blue * distance)
            self.callback(colors)
            time.sleep(1 / 30.)  # fps


class AroundSlow(Around):
    duration = 2.5


class AroundFast(Around):
    duration = 0.75
