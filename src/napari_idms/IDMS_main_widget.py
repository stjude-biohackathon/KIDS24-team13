from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget
import os
from qtpy import uic
from qtpy.QtCore import Qt
import sys

class IDMS_main_widget(QWidget):
    def __init__(self, viewer):
        # Initializing
        super().__init__()
        self.viewer = viewer
        self.items = ["Item1","Item2","Item3"]


        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "mock_IDMS_main.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)