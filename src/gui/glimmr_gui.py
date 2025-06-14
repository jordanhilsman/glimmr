import sys
import cv2
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Glimmr!")
        self.start_pos, self.end_pos = QPoint(0,0), QPoint(0,0)
        self.add_channel_zero = 0
        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(widget)
        self.cvImg = cv2.imread('/home/jordan/photos/bmw.jpg')
        self.cvImg[:,:,0] = self.cvImg[:,:,0] + self.add_channel_zero
        self.cvImg[:,:,0][self.cvImg[:,:,0] > 255] = 255
        height, width, channel = self.cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        widget.setPixmap(QPixmap(qImg))
        self.widget = widget

    def mousePressEvent(self, e):
        self.start_pos.setX(e.pos().x())
        self.start_pos.setY(e.pos().y())

    def mouseReleaseEvent(self, e):
        self.end_pos.setX(e.pos().x())
        self.end_pos.setY(e.pos().y())
        self.add_channel_zero = self.dist_difference(self.start_pos, self.end_pos)
        print(self.add_channel_zero)
        updated_img = self.update_img(self.cvImg, self.add_channel_zero)
        self.widget.setPixmap(QPixmap(updated_img))

    def dist_difference(self, start_pos, end_pos):
        return((end_pos - start_pos).x())

    def update_img(self, cvImg, acz):
        acz = float(acz)
        cvImg[:,:,1] = cvImg[:,:,1] + min(acz, 255)
        #cvImg[:,:,0] = cvImg[:,:,0] + max(0, min(acz, 255))
        cvImg[:,:,1][cvImg[:,:,1] > 255] = 255
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg2 = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return qImg2


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

