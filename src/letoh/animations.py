# -*- coding: utf-8 -*-
import math
from threading import Thread
import time

from letoh.utils import to_rgb
from letoh.utils import from_rgb
import pytweening


class Mock(object):
    def stop(self):
        pass

    def __bool__(self):
        return False


class Animation(Thread):
    alive = True

    def __init__(self, color, millis, callback):
        super(Animation, self).__init__()
        self.red, self.green, self.blue = to_rgb(color)
        self.seconds = millis / 1000.
        self.callback = callback
        self.start()

    def stop(self):
        self.alive = False

    def __bool__(self):
        return self.alive


class Breathing(Animation):
    def run(self):
        while self.alive:
            x = ((math.fabs(time.time() % self.seconds * 2 - self.seconds))
                 / self.seconds)
            factor = pytweening.easeInOutCubic(x)
            self.callback(from_rgb(self.red * factor,
                                   self.green * factor,
                                   self.blue * factor))
            time.sleep(1 / 30.)  # fps


class Rider(Animation):
    def run(self):
        groups = [
            ['bottomleft', 'bottomright'],
            ['lowerleft', 'lowerright'],
            ['middleleft', 'middleright'],
            ['upperleft', 'upperright'],
            ['topleft', 'topright'],
        ]
        while self.alive:
            x = ((math.fabs(time.time() % self.seconds * 2 - self.seconds))
                 / self.seconds)
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
