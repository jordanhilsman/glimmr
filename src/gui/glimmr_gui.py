import sys
import cv2
from slider import ColorChannelButton
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QToolBar,
    QAction,
    QHBoxLayout,
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
        self.b0 = False
        self.b1 = False
        self.b2 = False
        self.r0 = False
        self.red_btn = QPushButton("RED")
        self.green_btn = QPushButton("GREEN")
        self.blue_btn = QPushButton("BLUE")
        self.red_slider = ColorChannelButton(channel=2)
        self.green_slider = ColorChannelButton(channel=1)
        self.blue_slider = ColorChannelButton(channel=0)
        self.reset_btn = QPushButton("RESET IMAGE")
        self.color_channel = None
        for btn in [self.red_btn, self.green_btn, self.blue_btn, self.reset_btn]:
            btn.setCheckable(True)
        self.red_btn.clicked.connect(lambda: self.activate_button(2))
        self.green_btn.clicked.connect(lambda: self.activate_button(1))
        self.blue_btn.clicked.connect(lambda: self.activate_button(0))
        self.reset_btn.clicked.connect(self.reset_image)
        toolbar = QToolBar("Glimmr Tools")
        self.addToolBar(toolbar)
        button_action = QAction("Get image", self)
        button_action.triggered.connect(self.get_filepath)
        toolbar.addAction(button_action)
        widget = QLabel("Hello")
        self.label = widget
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.cvImg = cv2.imread('/home/jordan/photos/bmw.jpg')
        self.cvImg[:,:,0] = self.cvImg[:,:,0] + self.add_channel_zero
        self.cvImg[:,:,0][self.cvImg[:,:,0] > 255] = 255
        height, width, channel = self.cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        widget.setPixmap(QPixmap(qImg))
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.red_btn)
        button_layout.addWidget(self.green_btn)
        button_layout.addWidget(self.blue_btn)
        button_layout.addWidget(self.reset_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.red_slider)
        main_layout.addWidget(self.green_slider)
        main_layout.addWidget(self.blue_slider)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def activate_button(self, button_number):
        # Reset all
        self.b1 = self.b2 = self.b3 = False
        self.red_btn.setChecked(False)
        self.blue_btn.setChecked(False)
        self.green_btn.setChecked(False)

        # Set selected
        if button_number == 0:
            self.b1 = True
            self.blue_btn.setChecked(True)
        elif button_number == 1:
            self.b2 = True
            self.green_btn.setChecked(True)
        elif button_number == 2:
            self.b3 = True
            self.red_btn.setChecked(True)
        self.color_channel = button_number

    def reset_image(self):
        self.r0 = False
        self.reset_btn.setChecked(True)
        self.cvImg = cv2.imread(self.filename)
        height, width, channel = self.cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap(qImg))

    def get_filepath(self, s):
        filename, _ = QFileDialog.getOpenFileName(self, 'Single File', directory="/home/jordan/")
        self.filename = filename
        self.cvImg = cv2.imread(self.filename)

    def mousePressEvent(self, e):
        self.start_pos.setX(e.pos().x())
        self.start_pos.setY(e.pos().y())

    def mouseReleaseEvent(self, e):
        self.end_pos.setX(e.pos().x())
        self.end_pos.setY(e.pos().y())
        self.add_channel_zero = self.dist_difference(self.start_pos, self.end_pos)
        print(self.add_channel_zero)
        updated_img = self.update_img(self.cvImg, self.add_channel_zero, self.color_channel)
        self.label.setPixmap(QPixmap(updated_img))

    def dist_difference(self, start_pos, end_pos):
        return((end_pos - start_pos).x())

    def update_img(self, cvImg, acz, cc):
        acz = float(acz)
        cvImg[:,:,cc] = cvImg[:,:,cc] + min(acz, 255)
        cvImg[:,:,cc][cvImg[:,:,cc] > 255] = 255
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg2 = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return qImg2


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

