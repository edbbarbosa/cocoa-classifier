import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ImgWindow(QMainWindow):
    def __init__(self, out_img):
        super().__init__()
        self.setWindowTitle("Cocoa Classifier")
        self.label = QLabel(self)

        pixmap = QPixmap(out_img)
        pixmap = pixmap.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.label)
        self.show()
