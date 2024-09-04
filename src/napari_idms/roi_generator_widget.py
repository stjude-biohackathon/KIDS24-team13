from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget
import os
from qtpy import uic
from qtpy.QtCore import Qt
import sys

class ROI_Generator_widget(QWidget):
    def __init__(self, viewer):
        # Initializing
        super().__init__()
        self.viewer = viewer


        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "mock_roi_generate_tab.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Example usage
        self.example_btn = self.findChild(QPushButton, "register_btn")
        self.example_btn.clicked.connect(self.register_with_IDMS)

    def register_with_IDMS(self):
        print("Executing this statement ! ")

