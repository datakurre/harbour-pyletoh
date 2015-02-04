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
def handle_sig_call_state_ind(state, emergency_state):
    if state == 'ringing':
        try:
            LeTOH().__call__()
        except Exception as e:
            logger.error(str(e))
    else:
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
    system_bus = dbus.SystemBus()
    session_bus = dbus.SessionBus()

    match_string = ("interface='org.freedesktop.Notifications',"
                    "member='Notify',type='method_call',eavesdrop='true'")
    session_bus.add_match_string(match_string)
    session_bus.add_message_filter(handle_notification)
    session_bus.add_signal_receiver(
        handle_notification_closed,
        signal_name='NotificationClosed',
        dbus_interface='org.freedesktop.Notifications'
    )

    system_bus.add_signal_receiver(
        handle_sig_call_state_ind,
        signal_name='sig_call_state_ind',
        dbus_interface='com.nokia.mce.signal',
        path='/com/nokia/mce/signal'
    )

    mainloop = MainLoop()
    mainloop.run()
