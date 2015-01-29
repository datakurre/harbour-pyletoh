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
        stepSize: 1
        minimumValue: 0
        maximumValue: 256
        value: 0
        onValueChanged: {
          python.call('letoh.set_color',
                      [red.value | 0, green.value | 0, blue.value | 0]);
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
          python.call('letoh.set_color',
                      [red.value | 0, green.value | 0, blue.value | 0]);
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
          python.call('letoh.set_color',
                      [red.value | 0, green.value | 0, blue.value | 0]);
        }
      }

      ColorPicker {
        onColorChanged: {
          red.value = color.r * 256
          green.value = color.g * 256
          blue.value = color.b * 256
        }
      }
    }
  }
}

