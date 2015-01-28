import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.0
import org.nemomobile.dbus 2.0

import "pages"


ApplicationWindow {
  initialPage: Component { MainPage { } }
  Python {
    id: python
    Component.onCompleted: {
      addImportPath(Qt.resolvedUrl('.').substr('file://'.length));
      importModule_sync('main');
    }
    Component.onDestruction: {
     python.call('main.letoh.cleanup', [], function(args) {
     });
    }
  }
  DBusAdaptor {
    id: interceptor
    iface: 'org.freedesktop.Notifications'
    path: '/org/freedesktop/Notifications'

    function rcNotify(app_name, replaces_id, app_icon, summary,
                      body, actions, hints, expire_timeout) {
       python.call(
         'main.letoh.set_color',
         [256, 100, 100],
         function(args) {
           // callback
       });
    }
  }
  DBusInterface {
    id: notifications
    service: 'org.freedesktop.Notifications'
    iface: 'org.freedesktop.Notifications'
    path: '/org/freedesktop/Notifications'

    signalsEnabled: true

    function notificationClosed(id, reason) {
       python.call(
         'main.letoh.set_color',
         [0, 0, 0],
         function(args) {
           // callback
       });
    }
  }
  DBusInterface {
    id: dbus
    service: 'org.freedesktop.DBus'
    path: '/org/freedesktop/DBus'
    iface: 'org.freedesktop.DBus'
  }

  Component.onCompleted: {
    dbus.call(
        'AddMatch',
        "interface='org.freedesktop.Notifications',member='Notify',type='method_call',eavesdrop='true'");
  }
}
