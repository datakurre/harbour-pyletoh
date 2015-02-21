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
  property string color: '#000000'
  property string animation: ''

  function setState(value) { app.state = value; }

  onColorChanged: {
    letoh.action('Enable', [app.color, app.animation]);
  }

  onAnimationChanged: {
    letoh.action('Enable', [app.color, app.animation]);
  }

  Python {
    id: python

    Component.onCompleted: {
      addImportPath(Qt.resolvedUrl('.').substr('file://'.length));
      importModule_sync('setup');  // update sys.path to include dependencies
      importModule_sync('letoh');
      setHandler('stateChanged', app.setState);
    }

    Component.onDestruction: {
      letoh.action('Disable');
    }
  }

  DBusInterface {
    id: letoh

    iface: 'harbour.pyletoh'
    path: '/harbour/pyletoh'
    service: 'harbour.pyletoh'

    signalsEnabled: true

    function action(name, args) {
      if (service.running) {
        letoh.call(name, args !== undefined ? args : []);
      } else {
        python.call('letoh.' + name, args !== undefined ? args : []);
      }
    }

    function stateChanged(value) { app.setState(value); }
  }

  DBusInterface {
    id: service

    iface: 'org.freedesktop.systemd1.Unit'
    path: '/org/freedesktop/systemd1/unit/harbour_2dpyletoh_2eservice'
    service: 'org.freedesktop.systemd1'

    property bool running: false

    function isRunning() {
      return service.getProperty('SubState') === 'running';
    }

    function start(callback) {
      var args = [{'type': 's', 'value': 'replace'}];
      return service.typedCall('Start', args, function(result) {
        service.running = service.isRunning();
        if (callback) { callback(); }
      });
    }

    function stop(callback) {
      var args = [{'type': 's', 'value': 'replace'}];
      return service.typedCall('Stop', args, function(result) {
        service.running = service.isRunning();
        if (callback) { callback(); }
      });
    }

    Component.onCompleted: {
      service.running = service.isRunning()
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
