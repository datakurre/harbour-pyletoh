import QtQuick 2.0
import Sailfish.Silica 1.0

CoverBackground {
  id: cover
  enabled: true

  Label {
    id: label
    anchors.centerIn: parent
    text: "pyLeTOH"
  }

  CoverActionList {
    enabled: cover.enabled
    CoverAction {
      iconSource: "image://theme/icon-cover-pause"
      onTriggered: {
        python.call('letoh.turn_off');
        cover.enabled = false;
      }
    }
  }
  CoverActionList {
    enabled: !cover.enabled
    CoverAction {
      iconSource: "image://theme/icon-cover-play"
      onTriggered: {
        python.call('letoh.turn_on');
        cover.enabled = true;
      }
    }
  }
}
