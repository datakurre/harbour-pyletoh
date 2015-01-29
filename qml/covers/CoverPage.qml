import QtQuick 2.0
import Sailfish.Silica 1.0

CoverBackground {
  id: cover
  Label {
    id: label
    anchors.centerIn: parent
    text: "pyLeTOH"
  }
  CoverActionList {
    enabled: !app.state
    CoverAction {
      iconSource: "image://theme/icon-cover-play"
      onTriggered: {
        python.call('letoh.turn_on');
      }
    }
  }
  CoverActionList {
    enabled: app.state
    CoverAction {
      iconSource: "image://theme/icon-cover-pause"
      onTriggered: {
        python.call('letoh.turn_off');
      }
    }
  }
}
