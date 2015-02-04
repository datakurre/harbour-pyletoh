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

  property string state: 'disabled'
  function setState(value) { app.state = value; }

  Python {
    id: python

    Component.onCompleted: {
      addImportPath(Qt.resolvedUrl('.').substr('file://'.length));
      importModule_sync('setup');  // update sys.path to include dependencies
      importModule_sync('letoh');
      setHandler('stateChanged', app.setState);
    }

    Component.onDestruction: {
      python.call('letoh.update', [false]);
    }
  }

  DBusInterface {
    iface: 'harbour.pyletoh'
    path: '/harbour/pyletoh'
    service: 'harbour.pyletoh'

    signalsEnabled: true

    function stateChanged(value) { app.setState(value); }
  }

  DBusInterface {
    id: daemon

    iface: 'org.freedesktop.systemd1.Unit'
    path: '/org/freedesktop/systemd1/unit/harbour_2dpyletoh_2eservice'
    service: 'org.freedesktop.systemd1'

    property bool running: false

    function isRunning() {
      return daemon.getProperty('SubState') === 'running';
    }

    function start(callback) {
      var args = [{'type': 's', 'value': 'replace'}];
      return daemon.typedCall('Start', args, function(result) {
        daemon.running = daemon.isRunning();
        if (callback) { callback(); }
      });
    }

    function stop(callback) {
      var args = [{'type': 's', 'value': 'replace'}];
      return daemon.typedCall('Stop', args, function(result) {
        daemon.running = daemon.isRunning();
        if (callback) { callback(); }
      });
    }

    Component.onCompleted: {
      daemon.running = daemon.isRunning()
    }
  }

  DBusInterface {
    id: eavesdropper

    iface: 'org.freedesktop.systemd1.Unit'
    path: '/org/freedesktop/systemd1/unit/harbour_2dpyletoh_2deavesdropper_2eservice'
    service: 'org.freedesktop.systemd1'

    property bool running: false

    function isRunning() {
      return eavesdropper.getProperty('SubState') === 'running';
    }

    function start(callback) {
      var args = [{'type': 's', 'value': 'replace'}];
      return eavesdropper.typedCall('Start', args, function(result) {
        eavesdropper.running = eavesdropper.isRunning();
        if (callback) { callback(); }
      });
    }

    function stop(callback) {
      var args = [{'type': 's', 'value': 'replace'}];
      return eavesdropper.typedCall('Stop', args, function(result) {
        eavesdropper.running = eavesdropper.isRunning();
        if (callback) { callback(); }
      });
    }

    Component.onCompleted: {
      eavesdropper.running = eavesdropper.isRunning()
    }
  }
}
