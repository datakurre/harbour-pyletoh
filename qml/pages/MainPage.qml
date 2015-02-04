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
        title: "pyLeTOH"
      }

      TextSwitch {
        id: notifications
        text: 'Turn the lights on by notifications'
        anchors.horizontalCenter: parent.horizontalCenter
        description: ''

        function update() {
          var value = notifications.checked;
          if (daemon.running && eavesdropper.running) {
            notifications.description = 'Background services are currently running';
            if (!value) { notifications.checked = true; }
          } else {
            notifications.description = 'Background services are currently stopped';
            if (value) { notifications.checked = false; }
          }
        }

        onCheckedChanged: {
          var value = notifications.checked;
          if (value && (!daemon.running || !eavesdropper.running)) {
            daemon.start(function() {
              eavesdropper.start(notifications.update);
            });
          }
          if (!value && (daemon.running || eavesdropper.running)) {
            eavesdropper.stop(function() {
              daemon.stop(notifications.update);
            });
          }
        }
      }

      ColorPicker {
        colors: ['red', 'blue', 'yellow']
        onColorChanged: {
          red.value = color.r;
          green.value = color.g;
          blue.value = color.b;
          saved.enabled = true;
        }
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
      notifications.update();

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

