import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.0
import org.nemomobile.dbus 2.0

import "covers"
import "pages"


ApplicationWindow {
  id: app
  cover: Qt.resolvedUrl('covers/CoverPage.qml')
  initialPage: Component { MainPage { } }

  property bool state: false

  Python {
    id: python
    Component.onCompleted: {
      addImportPath(Qt.resolvedUrl('.').substr('file://'.length));
      importModule_sync('app');  // set sys.path to include packaged libs
      importModule_sync('letoh');
      setHandler('set_state', function(state) {
         app.state = state;
      });
    }
    Component.onDestruction: {
      python.call('letoh.turn_off');
    }
  }
  DBusAdaptor {
    id: interceptor
    iface: 'org.freedesktop.Notifications'
    path: '/org/freedesktop/Notifications'

    function rcNotify(app_name, replaces_id, app_icon, summary,
                      body, actions, hints, expire_timeout) {
       python.call('letoh.turn_on');
    }
  }
  DBusInterface {
    id: notifications
    service: 'org.freedesktop.Notifications'
    iface: 'org.freedesktop.Notifications'
    path: '/org/freedesktop/Notifications'

    signalsEnabled: true

    function notificationClosed(id, reason) {
       python.call('letoh.turn_off');
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
