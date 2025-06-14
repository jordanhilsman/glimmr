import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.label = QLabel("Click in this window")
        self.label.setMouseTracking(True)
        self.setCentralWidget(self.label)
        self.start_pos = QPoint(0,0)
        self.end_pos = QPoint(0,0)


    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.start_pos.setX(e.pos().x())
        self.start_pos.setY(e.pos().y())
        self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        self.end_pos.setX(e.pos().x())
        self.end_pos.setY(e.pos().y())
        self.label.setText("mouseReleaseEvent")
        print(self.start_pos, self.end_pos)
        print(self.distance_traveled(self.start_pos, self.end_pos))

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")

    def distance_traveled(self, start_pos:QPoint, end_pos:QPoint):
        start_x, start_y = start_pos.x, start_pos.y
        end_x, end_y = end_pos.x, end_pos.y
        return(start_pos - end_pos)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

