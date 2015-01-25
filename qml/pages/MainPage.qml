import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.0

Page {
  id: page
  allowedOrientations: Orientation.Portrait | Orientation.Landscape

  property var rainbow : [
      "#ff0080", "#ff0000", "#ff8000", "#ffff00", "#00ff00",
      "#00ff80", "#00ffff", "#0000ff", "#8000ff", "#ff00ff",
      "#000000", "#ffffff" // also black and white
  ]

  SilicaFlickable {
    id: mainView
    anchors.fill: parent

    PullDownMenu {
      MenuItem {
        text: 'On'
        onClicked: {
          var dialog = pageStack.push(
            'Sailfish.Silica.ColorPickerDialog', {'colors': rainbow}
          );
          dialog.accepted.connect(function() {
            python.call('main.app.action_on',
                        [dialog.color.r * 256 | 0,
                         dialog.color.g * 256 | 0,
                         dialog.color.b * 256 | 0],
                        function(args) {
            });
          });
        }
      }
      MenuItem {
        text: 'Off'
        onClicked: {
          python.call('main.app.action_off', [], function(args) {
          });
        }
      }
    }
  }
}
