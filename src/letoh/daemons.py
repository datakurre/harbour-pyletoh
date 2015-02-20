# -*- coding: utf-8 -*-
import os
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.overrides.GObject import MainLoop

from threading import Thread
from contextlib import contextmanager

from letoh import logger
from letoh import LeTOH
from letoh import Service
from letoh import DBUS_INTERFACE
from letoh import DBUS_PATH
from letoh import DBUS_SERVICE

os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/100000/dbus/user_bus_socket'  # noqa
os.environ['DISPLAY'] = ':0'


@contextmanager
def dbus_service():
    session_bus = dbus.SessionBus()
    try:
        try:
            ob = session_bus.get_object(DBUS_SERVICE, DBUS_PATH)
            service = dbus.Interface(ob, DBUS_INTERFACE)
            yield service
        except dbus.exceptions.DBusException:
            yield None
    except AttributeError:
        pass


# noinspection PyUnusedLocal
def handle_notification(bus, msg):
    if all([msg.get_interface() == 'org.freedesktop.Notifications',
            msg.get_member() == 'Notify']):
        app_name = msg.get_args_list()[0]
        with dbus_service() as service:
            service.Enable(app_name)
    else:
        return True


# noinspection PyUnusedLocal
def handle_notification_closed(id_, reason):
    with dbus_service() as service:
        service.Disable()


# noinspection PyUnusedLocal
def handle_sig_call_state_ind(state, emergency_state):
    if state == 'ringing':
        with dbus_service() as service:
            service.Enable('ringing')
    else:
        with dbus_service() as service:
            service.Disable()


# noinspection PyUnusedLocal
def letoh_service():
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    name = dbus.service.BusName(DBUS_SERVICE, bus)
    service = Service(bus, DBUS_PATH)

    mainloop = MainLoop()
    mainloop.run()


def letoh_eavesdropper():
    DBusGMainLoop(set_as_default=True)

    match_string = ("interface='org.freedesktop.Notifications',"
                    "member='Notify',type='method_call',eavesdrop='true'")

    session_bus = dbus.SessionBus()
    session_bus.add_match_string(match_string)
    session_bus.add_message_filter(handle_notification)
    session_bus.add_signal_receiver(
        handle_notification_closed,
        signal_name='NotificationClosed',
        dbus_interface='org.freedesktop.Notifications'
    )

    system_bus = dbus.SystemBus()
    system_bus.add_signal_receiver(
        handle_sig_call_state_ind,
        signal_name='sig_call_state_ind',
        dbus_interface='com.nokia.mce.signal',
        path='/com/nokia/mce/signal'
    )

    mainloop = MainLoop()
    mainloop.run()
