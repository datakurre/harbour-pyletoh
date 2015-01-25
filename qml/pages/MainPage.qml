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
        stepSize: 1
        minimumValue: 0
        maximumValue: 256
        value: 0
        onValueChanged: {
            python.call('main.letoh.set_color',
                        [red.value | 0, green.value | 0, blue.value | 0],
                        function(args) {
            });
        }
      }

      Slider {
        id: green
        label: 'green'
        width: parent.width
        stepSize: 1
        minimumValue: 0
        maximumValue: 256
        value: 0
        onValueChanged: {
            python.call('main.letoh.set_color',
                        [red.value | 0, green.value | 0, blue.value | 0],
                        function(args) {
            });
        }
      }

      Slider {
        id: blue
        label: 'blue'
        width: parent.width
        stepSize: 1
        minimumValue: 0
        maximumValue: 256
        value: 0
        onValueChanged: {
            python.call('main.letoh.set_color',
                        [red.value | 0, green.value | 0, blue.value | 0],
                        function(args) {
            });
        }
      }
    }
  }
}
