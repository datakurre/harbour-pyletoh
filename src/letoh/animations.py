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
    def name(self):
        return self.__class__.__name__.lower()

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
                if i == factor:
                    for led in groups[i]:
                        colors[led] = from_rgb(self.red,
                                               self.green,
                                               self.blue)
                elif abs(i - factor) == 1:
                    for led in groups[i]:
                        colors[led] = from_rgb(self.red * 0.5,
                                               self.green * 0.5,
                                               self.blue * 0.5)
                elif abs(i - factor) == 2:
                    for led in groups[i]:
                        colors[led] = from_rgb(self.red * 0.25,
                                               self.green * 0.25,
                                               self.blue * 0.25)
                elif abs(i - factor) == 3:
                    for led in groups[i]:
                        colors[led] = from_rgb(self.red * 0.05,
                                               self.green * 0.05,
                                               self.blue * 0.05)
                else:
                    for led in groups[i]:
                        colors[led] = from_rgb(0, 0, 0)
            self.callback(colors)
            time.sleep(1 / 30.)  # fps


class SwipeSlow(Swipe):
    duration = 5.0


class SwipeFast(Swipe):
    duration = 2.0
