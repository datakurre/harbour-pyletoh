import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.0

Page {
  id: page
  allowedOrientations: Orientation.Portrait

  SilicaFlickable {
    id: mainView
    anchors.fill: parent

    Column {
      id: column

      width: page.width
      spacing: Theme.paddingLarge

      PageHeader {
        title: "LeTOH"
      }

      Slider {
        id: red
        label: 'red'
        width: parent.width
        minimumValue: 0
        maximumValue: 1
        value: 0
        onValueChanged: {
          var color = Qt.rgba(red.value, green.value, blue.value, 1);
          python.call('letoh.update', [color.toString()]);
          saved.enabled = true;
        }
      }

      Slider {
        id: green
        label: 'green'
        width: parent.width
        minimumValue: 0
        maximumValue: 1
        value: 0
        onValueChanged: {
          var color = Qt.rgba(red.value, green.value, blue.value, 1);
          python.call('letoh.update', [color.toString()]);
          saved.enabled = true;
        }
      }

      Slider {
        id: blue
        label: 'blue'
        width: parent.width
        minimumValue: 0
        maximumValue: 1
        value: 0
        onValueChanged: {
          var color = Qt.rgba(red.value, green.value, blue.value, 1);
          python.call('letoh.update', [color.toString()]);
          saved.enabled = true;
        }
      }

      Button {
        id: saved
        text: 'save'
        enabled: false
        anchors.horizontalCenter: parent.horizontalCenter
        onClicked: {
          var color = Qt.rgba(red.value, green.value, blue.value, 1);
          python.call('letoh.save', [color.toString()]);
          saved.enabled = false;
        }
      }

      ColorPicker {
        onColorChanged: {
          red.value = color.r;
          green.value = color.g;
          blue.value = color.b;
          saved.enabled = true;
        }
      }
    }
    PullDownMenu {
      MenuItem {
        enabled: app.state === 'disabled'
        text: 'On'
        onClicked: {
          python.call('letoh.update');
        }
      }
      MenuItem {
        enabled: app.state === 'enabled'
        text: 'Off'
        onClicked: {
          python.call('letoh.update', [false]);
        }
      }
    }
    Component.onCompleted: {
      python.call('letoh.option', ['default', 'color'], function(value) {
        var color = Qt.lighter(value, 1);
        red.value = color.r;
        green.value = color.g;
        blue.value = color.b;
        if (color.r || color.g || color.b) {
          app.setState('enabled');
          saved.enabled = false;
        }
      });
    }
  }
}

