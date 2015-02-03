# -*- coding: utf-8 -*-
import os
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.overrides.GObject import MainLoop

from threading import Thread

from letoh import logger
from letoh import LeTOH
from letoh import Service
from letoh import DBUS_SERVICE
from letoh import DBUS_PATH

os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/100000/dbus/user_bus_socket'  # noqa
os.environ['DISPLAY'] = ':0'


# noinspection PyUnusedLocal
def handle_notification(bus, msg):
    if all([msg.get_interface() == 'org.freedesktop.Notifications',
            msg.get_member() == 'Notify']):
        try:
            LeTOH().__call__()
        except Exception as e:
            logger.error(str(e))
    else:
        return True


# noinspection PyUnusedLocal
def handle_notification_closed(id_, reason):
    try:
        LeTOH().__call__(False)
    except Exception as e:
        logger.error(str(e))


# noinspection PyUnusedLocal
def daemon():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    name = dbus.service.BusName(DBUS_SERVICE, bus)
    service = Service(bus, DBUS_PATH)
    mainloop = MainLoop()
    mainloop.run()


def eavesdropper():
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()

    match_string = ("interface='org.freedesktop.Notifications',"
                    "member='Notify',type='method_call',eavesdrop='true'")
    session_bus.add_match_string(match_string)
    session_bus.add_message_filter(handle_notification)
    session_bus.add_signal_receiver(
        handle_notification_closed,
        dbus_interface="org.freedesktop.Notifications",
        signal_name="NotificationClosed"
    )

    mainloop = MainLoop()
    mainloop.run()


