from PyQt5.QtCore import Qt, QSize, QDir
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QFileDialog
)

QDir

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        toolbar = QToolBar("TOOLZ!!")
        self.addToolBar(toolbar)
        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.get_filepath)
        toolbar.addAction(button_action)
    def get_filepath(self, s):
        filename, _ = QFileDialog.getOpenFileName(self, 'Single File', directory="/home/jordan/")
        print(filename)

    def toolbar_button_clicked(self, s):
        print("click", s)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
