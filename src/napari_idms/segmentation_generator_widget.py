from qtpy.QtWidgets import QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget
import os
from qtpy import uic
from qtpy.QtCore import Qt
import sys

class Segmentation_widget(QWidget):
    def __init__(self, viewer):
        # Initializing
        super().__init__()
        self.viewer = viewer

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "mock_template.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Example usage
        self.example_btn = self.findChild(QPushButton, "pushButton")
        self.example_label = self.findChild(QLabel,"label")

        self.example_btn.clicked.connect(self.print_in_label)

    def print_in_label(self):
        self.example_label.setText("I am executed from Segmentation tab template")







