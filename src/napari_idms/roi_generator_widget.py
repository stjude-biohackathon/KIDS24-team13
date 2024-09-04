from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget, QLineEdit
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

        # Start from here for the dynamic UI elements

        # Example usage
        self.example_btn = self.findChild(QPushButton, "register_btn")
        self.example_btn.clicked.connect(self.register_with_IDMS)

        # New code to handle shape layer and printing coordinates
        self.shapes_layer = self.viewer.add_shapes()  # Create or access a shapes layer in napari
        self.shapes_layer.events.data.connect(self.on_shape_drawn)  # Connect event when a new shape is drawn

    def on_shape_drawn(self, event):
    # Callback function to print coordinates when a new shape is drawn.
        if len(self.shapes_layer.data) > 0:
            # Get the last added shape coordinates
            last_shape = self.shapes_layer.data[-1]
            print("Coordinates of the drawn shape:", last_shape)
        else:
            print("No shape is drawn yet.")


    def register_with_IDMS(self):
        print("Executing this statement ! ")

