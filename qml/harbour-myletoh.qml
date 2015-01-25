import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.0

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
     python.call('main.app.cleanup', [], function(args) {
     });
    }
  }
}
