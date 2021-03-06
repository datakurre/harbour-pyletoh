import QtQuick 2.0
import Sailfish.Silica 1.0

CoverBackground {
  id: cover

  Column {
    anchors.centerIn: parent

    Image {
      anchors.horizontalCenter: parent.horizontalCenter
      source: 'image://theme/harbour-pyletoh'
    }

    Label {
      anchors.horizontalCenter: parent.horizontalCenter
      text: 'pyLeTOH'
      font.pixelSize: 20
    }
  }

  CoverActionList {
    enabled: app.state === 'disabled'
    CoverAction {
      iconSource: "image://theme/icon-cover-play"
      onTriggered: {
        letoh.action('Enable', [app.color, app.animation]);
      }
    }
  }

  CoverActionList {
    enabled: app.state === 'enabled'
    CoverAction {
      iconSource: "image://theme/icon-cover-pause"
      onTriggered: {
        letoh.action('Disable');
      }
    }
  }
}
