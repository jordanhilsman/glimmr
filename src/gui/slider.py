import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
QWidget, QSlider)



class ColorChannelButton(QSlider):
    def __init__(self, orientation=Qt.Horizontal, parent=None, channel=None):
        super().__init__(orientation, parent)
        self.channel=channel
        self.setMinimum(0)
        self.setMaximum(255)
        self.setSingleStep(1)
        self.valueChanged.connect(self.value_changed)
        self.sliderMoved.connect(self.slider_position)
        self.sliderPressed.connect(self.slider_pressed)
        self.sliderReleased.connect(self.slider_released)
        self.setStyleSheet(self.get_stylesheet_for_channel(channel))
    def value_changed(self, i):
        return i
    def slider_position(self, p):
        return p
    def slider_pressed(self, p):
        return p
    def slider_released(self, p):
        return p

    def get_stylesheet_for_channel(self, channel):
        colors = {
            2 : "#e74c3c",
            1 : "#27ae60",
            0 : "#3498db",
        }
        color = colors.get(channel, "#bdc3c7")  # default: gray

        return f"""
        QSlider::groove:horizontal {{
            border: 1px solid #999999;
            height: 8px;
            background: #dddddd;
            margin: 2px 0;
        }}
        QSlider::handle:horizontal {{
            background: {color};
            border: 1px solid #5c5c5c;
            width: 18px;
            margin: -2px 0;
            border-radius: 3px;
        }}
        """


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        widget2 = ColorChannelButton(orientation=Qt.Horizontal, channel=0)
        widget = QSlider(Qt.Horizontal)

        widget.setMinimum(0)
        widget.setMaximum(255)

        widget.setSingleStep(1)

        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(widget2)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)



#app = QApplication(sys.argv)

#window = MainWindow()
#window.show()

#app.exec()

