import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


def glitch(orig_frame, frame, intensity):
    glitched = orig_frame.copy()
    h, w, _ = glitched.shape
    for _ in range(intensity):
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        glitched[:, x:] = glitched[:, :-x]
        glitched[y:, :] = glitched[:-y, :]
    return glitched


class GlitchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glimmr – Glitch Static Image")
        self.layout = QVBoxLayout(self)

        # Load image
        self.original_img = cv2.imread('/home/jordan/photos/bmw.jpg')
        if self.original_img is None:
            raise ValueError("Could not load image.")

        self.current_img = self.original_img.copy()

        # QLabel to display image
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Button
        self.glitch_btn = QPushButton("GLITCH ME!")
        self.glitch_btn.setCheckable(True)
        self.glitch_btn.clicked.connect(self.toggle_glitch)
        self.layout.addWidget(self.glitch_btn)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.apply_glitch)

        self.update_display(self.current_img)

    def toggle_glitch(self):
        if self.glitch_btn.isChecked():
            self.timer.start(30)
        else:
            self.timer.stop()
            self.current_img = self.original_img.copy()
            self.update_display(self.current_img)

    def apply_glitch(self):
        self.current_img = glitch(self.original_img, self.current_img, np.random.randint(1, 5))
        self.update_display(self.current_img)

    def update_display(self, img):
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(qimg))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlitchApp()
    window.show()
    sys.exit(app.exec_())

