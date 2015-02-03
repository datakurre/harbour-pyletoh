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
    service: 'harbour.pyletoh'
    iface: 'harbour.pyletoh'
    path: '/harbour/pyletoh'

    signalsEnabled: true

    function stateChanged(value) { app.setState(value); }
  }
}
