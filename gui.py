import csv
import json
from pathlib import Path

import cv2
from joblib import load

from cocoa_classifier.predictor import predict
from cocoa_classifier.trainer import train
from schemas.classifier_config import ClassifierConfig

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton, QFileDialog

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Cocoa Classifier")
        self.setMinimumWidth(400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tab0 = QWidget()
        self.tab1 = QWidget()
        layout0 = QVBoxLayout()
        layout1 = QVBoxLayout()
        self.tab0.setLayout(layout0)
        self.tab1.setLayout(layout1)

        self.tabs.addTab(self.tab0, "Train")
        self.tabs.addTab(self.tab1, "Predict")

        # Train
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Input path")
        btn_input = QPushButton("Select input")
        btn_input.clicked.connect(lambda: self.open_selector_dir(self.input_path))

        layout0.addWidget(QLabel("Input folder:"))
        layout0_h1 = QHBoxLayout()
        layout0_h1.addWidget(self.input_path)
        layout0_h1.addWidget(btn_input)
        layout0.addLayout(layout0_h1)

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Output path")
        btn_output = QPushButton("Select output")
        btn_output.clicked.connect(lambda: self.open_selector_dir(self.output_path))

        layout0.addWidget(QLabel("Output folder"))
        layout0_h2 = QHBoxLayout()
        layout0_h2.addWidget(self.output_path)
        layout0_h2.addWidget(btn_output)
        layout0.addLayout(layout0_h2)

        self.btn_train = QPushButton("Train")
        layout0.addWidget(self.btn_train)
        self.btn_train.clicked.connect(lambda: self.btn_train_clicked(self.input_path, self.output_path))

        layout0.addStretch()

        # Predict
        self.image_path = QLineEdit()
        self.image_path.setPlaceholderText("Image")
        btn_image = QPushButton("Select image")
        btn_image.clicked.connect(lambda: self.open_selector_file(self.image_path))

        layout1.addWidget(QLabel("Image (cocoa bean):"))
        layout1_h1 = QHBoxLayout()
        layout1_h1.addWidget(self.image_path)
        layout1_h1.addWidget(btn_image)
        layout1.addLayout(layout1_h1)

        self.model_path = QLineEdit()
        self.model_path.setPlaceholderText("Model path")
        btn_model = QPushButton("Select model path")
        btn_model.clicked.connect(lambda: self.open_selector_dir(self.model_path))

        layout1.addWidget(QLabel("Model folder:"))
        layout1_h2 = QHBoxLayout()
        layout1_h2.addWidget(self.model_path)
        layout1_h2.addWidget(btn_model)
        layout1.addLayout(layout1_h2)

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Output path")
        btn_output = QPushButton("Select output")
        btn_output.clicked.connect(lambda: self.open_selector_dir(self.output_path))

        layout1.addWidget(QLabel("Output folder"))
        layout1_h3 = QHBoxLayout()
        layout1_h3.addWidget(self.output_path)
        layout1_h3.addWidget(btn_output)
        layout1.addLayout(layout1_h3)

        self.btn_predict = QPushButton("Predict")
        layout1.addWidget(self.btn_predict)
        self.btn_predict.clicked.connect(lambda: self.btn_predict_clicked(self.image_path, self.model_path, self.output_path))

        layout1.addStretch()

    def open_selector_dir(self, line_edit_target):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit_target.setText(folder)

    def open_selector_file(self, line_edit_target):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image", 
            "", 
            "Images (*.png *.jpg *.jpeg);;All Files (*)"
        )
        
        if file_path:
            line_edit_target.setText(file_path)
    
    def btn_train_clicked(self, input_widget, output_widget):
        if not input_widget.text() or not output_widget.text():
            print("Error: Select the input and output paths.")
            return

        data_dir = Path(input_widget.text())
        out_dir = Path(output_widget.text())

        try:
            train(data_dir, out_dir)        
        except Exception as e:
            print(f"Training failure: {e}")

    def btn_predict_clicked(self, image_widget, model_widget, output_widget):
        img_str = image_widget.text().strip()
        model_str = model_widget.text().strip()
        out_str = output_widget.text().strip()

        if not img_str or not model_str or not out_str:
            print("Error: Fill in all paths (Image, Model and Output).")
            return

        image_path = Path(img_str)
        model_dir = Path(model_str)
        out_dir = Path(out_str)

        try:
            model = load(model_dir / "model.pkl")
            with open(model_dir / "classes.json") as f:
                classes = json.load(f)
            out_dir.mkdir(parents=True, exist_ok=True)

            with open(image_path, "rb") as f:
                encoded_image = f.read()

            overlay, results = predict(
                file=encoded_image,
                model=model,
                classes=classes,
            )

            out_img = out_dir / f"{Path(image_path).stem}_annotated.png"
            cv2.imwrite(str(out_img), overlay)

            out_csv = out_dir / "predictions.csv"
            if results:
                with open(out_csv, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=results[0].keys())
                    writer.writeheader()
                    writer.writerows(results)

            print(f"Wrote {out_img}")
            print(f"Wrote {out_csv}")  
        except Exception as e:
            print(f"Training failure: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())
