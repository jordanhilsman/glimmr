import sys
import numpy as np
import cv2
from slider import ColorChannelButton
from PyQt5.QtCore import Qt, QPoint, QPointF, QTimer
from PyQt5.QtGui import QPixmap, QImage, QGuiApplication

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
        screen = QGuiApplication.primaryScreen()
        size = screen.availableGeometry()
        self.setGeometry(size)
        self.setWindowTitle("Welcome to Glimmr!")
        self.start_pos, self.end_pos = QPoint(0,0), QPoint(0,0)
        self.add_channel_zero = 0
        self.cap = cv2.VideoCapture(0)
        self.b0 = False
        self.b1 = False
        self.b2 = False
        self.r0 = False
        self.red_slider = ColorChannelButton(channel=2)
        self.green_slider = ColorChannelButton(channel=1)
        self.blue_slider = ColorChannelButton(channel=0)
        self.red_slider.sliderReleased.connect(self.slider_released_handler)
        self.green_slider.sliderReleased.connect(self.slider_released_handler)
        self.blue_slider.sliderReleased.connect(self.slider_released_handler)
        self.reset_btn = QPushButton("RESET IMAGE")
        self.color_channel = None
        self.reset_btn.clicked.connect(self.reset_image)
        toolbar = QToolBar("Glimmr Tools")
        self.addToolBar(toolbar)
        button_action = QAction("Get image", self)
        button_action.triggered.connect(self.get_filepath)
        save_action = QAction("Save image", self)
        save_action.triggered.connect(self.save_image_to_filepath)
        toolbar.addAction(button_action)
        toolbar.addAction(save_action)
        widget = QLabel("Please load an image in :-)")
        self.label = widget
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        button_layout = QHBoxLayout()
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

    def reset_image(self):
        self.r0 = False
        self.reset_btn.setChecked(True)
        self.cvImg = cv2.imread(self.filename)
        self.origImg = self.cvImg.copy()
        height, width, channel = self.cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap(qImg))
        self.red_slider.setValue(0)
        self.green_slider.setValue(0)
        self.blue_slider.setValue(0)

    def get_filepath(self, s):
        filename, _ = QFileDialog.getOpenFileName(self, 'Single File', directory="/home/jordan/")
        self.filename = filename
        self.cvImg = cv2.imread(self.filename)
        self.origImg = self.cvImg.copy()
        screen_rect = QGuiApplication.primaryScreen().availableGeometry()
        screen_width, screen_height = screen_rect.width(), screen_rect.height()
        img_h, img_w = self.cvImg.shape[:2]
        scale_w = screen_width / img_w
        scale_h = screen_height / img_h
        scale = min(scale_w, scale_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        resized_img = cv2.resize(self.cvImg, (new_w, new_h), interpolation=cv2.INTER_AREA)
        self.cvImg = resized_img
        self.origImg = resized_img.copy()
        bytesPerLine = 3 * new_w 
        readQIMG = QImage(self.cvImg.data, new_w, new_h, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap(readQIMG))

    def save_image_to_filepath(self, s):
        if self.filename:
            save_fp, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files(*);;") 
            cv2.imwrite(img=self.cvImg, filename=save_fp)

    def mousePressEvent(self, e):
        self.start_pos.setX(e.pos().x())
        self.start_pos.setY(e.pos().y())

    def mouseReleaseEvent(self, e):
        self.end_pos.setX(e.pos().x())
        self.end_pos.setY(e.pos().y())
        self.add_channel_zero = self.dist_difference(self.start_pos, self.end_pos)

    def dist_difference(self, start_pos, end_pos):
        return((end_pos - start_pos).x())

    def slider_released_handler(self):
        r = self.red_slider.value()
        g = self.green_slider.value()
        b = self.blue_slider.value()
        updated_img = self.update_img(self.origImg.copy(), r, g, b)
        self.label.setPixmap(QPixmap(updated_img))

    def update_img(self, cvImg, r, g, b):
        cvImg[:,:,0] = cvImg[:,:,0] + b
        cvImg[:,:,1] = cvImg[:,:,1] + g
        cvImg[:,:,2] = cvImg[:,:,2] + r
        height, width, channel = cvImg.shape
        bytesPerLine = channel * width
        self.cvImg = cvImg
        qImg2 = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return qImg2


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

