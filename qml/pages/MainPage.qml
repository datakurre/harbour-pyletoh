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
      spacing: Theme.paddingMedium

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
          if (service.running && eavesdropper.running) {
            notifications.description = 'Background services are currently running';
            if (!value) { notifications.checked = true; }
          } else {
            notifications.description = 'Background services are currently stopped';
            if (value) { notifications.checked = false; }
          }
        }

        onCheckedChanged: {
          var value = notifications.checked;
          if (value && (!service.running || !eavesdropper.running)) {
            service.start(function() {
              eavesdropper.start(notifications.update);
            });
          }
          if (!value && (service.running || eavesdropper.running)) {
            eavesdropper.stop(function() {
              service.stop(notifications.update);
            });
          }
        }
      }

      ColorPicker {
        colors: ['red', 'blue', 'yellow']
        onColorChanged: {
          if (color.r) { red.value = color.r; }
          if (color.g) { green.value = color.g; }
          if (color.b) { blue.value = color.b; }
          if (!color.r) { red.value = color.r; }
          if (!color.g) { green.value = color.g; }
          if (!color.b) { blue.value = color.b; }
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
          app.color = Qt.rgba(red.value, green.value, blue.value, 1).toString();
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
          app.color = Qt.rgba(red.value, green.value, blue.value, 1).toString();
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
          app.color = Qt.rgba(red.value, green.value, blue.value, 1).toString();
          saved.enabled = true;
        }
      }

      Slider {
        id: animation
        label: 'no animation'
        width: parent.width
        minimumValue: 0
        maximumValue: 9
        stepSize: 1
        value: 0

        property variant options: {
          0: {'name': '', label: 'no animation'},
          1: {'name': 'breath-slow', label: 'breath (slow)'},
          2: {'name': 'breath', label: 'breath'},
          3: {'name': 'breath-fast', label: 'breath (fast)'},
          4: {'name': 'swipe-slow', label: 'swipe (slow)'},
          5: {'name': 'swipe', label: 'swipe'},
          6: {'name': 'swipe-fast', label: 'swipe (fast)'},
          7: {'name': 'around-slow', label: 'around (slow)'},
          8: {'name': 'around', label: 'around'},
          9: {'name': 'around-fast', label: 'around (fast)'}
        }

        onValueChanged: {
          animation.label = animation.options[animation.value].label;
          app.animation = animation.options[animation.value].name;
          saved.enabled = true;
        }
      }
    }

    PullDownMenu {
      MenuItem {
        enabled: app.state === 'disabled'
        text: 'On'
        onClicked: {
          letoh.action('Enable', [app.color, app.animation]);
        }
      }
      MenuItem {
        enabled: app.state === 'enabled'
        text: 'Off'
        onClicked: {
          letoh.action('Disable');
        }
      }
    }

    PushUpMenu {
      enabled: saved.enabled
      MenuItem {
        id: saved
        text: 'save'
        enabled: false
        anchors.horizontalCenter: parent.horizontalCenter
        onClicked: {
          letoh.action('Save', [app.color, app.animation]);
          saved.enabled = false;
        }
      }
    }

    Component.onCompleted: {
      notifications.update();

      python.call('letoh.option', ['DEFAULT', 'color'], function(value) {
        python.call('letoh.option', ['DEFAULT', 'animation'], function(name) {
          var index, color = Qt.lighter(value, 1);

          for(index in animation.options) {
            if (animation.options[index].name === name) {
              animation.value = index;
            }
          }

          red.value = color.r;
          green.value = color.g;
          blue.value = color.b;

          if (color.r || color.g || color.b) { app.setState('enabled'); }

          saved.enabled = false;
        });
      });
    }
  }
}
