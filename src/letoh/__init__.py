# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('harbour-myletoh')
logging.basicConfig(level=logging.DEBUG)

from letoh.letoh import LeTOH
from letoh.letoh import Service
from letoh.letoh import disable
from letoh.letoh import DBUS_INTERFACE
from letoh.letoh import DBUS_SERVICE
from letoh.letoh import DBUS_PATH

from letoh import config

# QML API
Enable = LeTOH()
Disable = disable
Save = lambda color, animation: config.save_defaults(color=color,
                                                     animation=animation)
option = lambda section, key, default='': config.load().get(section, key,
                                                            fallback=default)

__all__ = ['logger', 'update', 'option', '__main__',
           'LeTOH', 'Service',
           'DBUS_SERVICE', 'DBUS_INTERFACE', 'DBUS_PATH']


def __main__():
    pass
