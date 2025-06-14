import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
QWidget)


class BUTTA(QPushButton):
    def __init__(self, message, channel, parent=None):
        super().__init__(message, parent)
        self.button = QPushButton(message)
        self.button.setCheckable(True)
        self.channel = channel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        button1 = BUTTA("BLUE", 0)
        button2 = BUTTA("GREEN", 1)
        button3 = BUTTA("RED", 2)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        self.setLayout(layout)
#        self.setCentralWidget(self.button1)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

