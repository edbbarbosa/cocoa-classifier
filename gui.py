# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton, QFileDialog

class Folders(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Cocoa Classifier")
        self.setMinimumWidth(250)

        layout = QVBoxLayout()

        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Input path")
        btn_input = QPushButton("Select input")
        btn_input.clicked.connect(lambda: self.open_selector(self.input_path))

        layout.addWidget(QLabel("Input folder:"))
        layout_h1 = QHBoxLayout()
        layout_h1.addWidget(self.input_path)
        layout_h1.addWidget(btn_input)
        layout.addLayout(layout_h1)

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Output path")
        btn_output = QPushButton("Select output")
        btn_output.clicked.connect(lambda: self.open_selector(self.output_path))

        layout.addWidget(QLabel("Output folder"))
        layout_h2 = QHBoxLayout()
        layout_h2.addWidget(self.output_path)
        layout_h2.addWidget(btn_output)
        layout.addLayout(layout_h2)

        self.btn_ok = QPushButton("OK")
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def open_selector(self, line_edit_target):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit_target.setText(folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Folders()
    window.show()
    sys.exit(app.exec())
