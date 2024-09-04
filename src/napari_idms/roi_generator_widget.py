from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget, QListView, QListWidgetItem, QLabel, QVBoxLayout, QLineEdit
import os
from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.uic import loadUiType
import sys
import numpy as np


class RoiListWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "roi_list_item.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        self.roi_lbl = self.findChild(QLabel, "roi_lbl")

        self.roi_lbl.setText(text)


class ROI_Generator_widget(QWidget):
    def __init__(self, viewer):
        # Initializing
        super().__init__()
        self.viewer = viewer


        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "roi_generate_tab.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Create a QListWidget
        self.list_widget = self.findChild(QListWidget, "roi_lw")

        # Add some custom widgets to the QListWidget
        for i in range(5):
            self.create_roi(i)

        # Start from here for the dynamic UI elements

        # Example usage
        self.example_btn = self.findChild(QPushButton, "register_btn")
        self.example_btn.clicked.connect(self.register_with_IDMS)

        self.viewer.layers.events.inserted.connect(self.on_layer_added)


    def on_layer_added(self, event):
        """Check if a new shapes layer has been added."""
        layer = event.value
        if layer.__class__.__name__ == 'Shapes':  # Check if the layer is a Shapes layer without importing napari
            # A new shapes layer has been added by the user
            self.shapes_layer = layer
            self.shapes_layer.events.data.connect(self.on_shape_drawn)
            print("New shapes layer added by the user.")
    
    def on_shape_drawn(self, event):
    # Callback function to print coordinates when a new shape is drawn.
        if len(self.shapes_layer.data) > 0:
            # Get the last added shape coordinates
            last_shape = self.shapes_layer.data[-1]
            last_shape_int = last_shape.astype(int)

            # If there are only two coordinates (x, y), set z to 0 by default
            if last_shape_int.shape[1] == 2:
                last_shape_int = np.hstack([last_shape_int, np.zeros((last_shape_int.shape[0], 1), dtype=int)])

            # Calculate the starting point (x, y, z)
            start_point = last_shape_int[0]  # The first corner of the rectangle (x, y, z)
            # Calculate width (w), height (h), and depth (d) based on the difference between first and opposite corner
            opposite_point = last_shape_int[2]  # The opposite corner of the rectangle
            w = opposite_point[1] - start_point[1]
            h = opposite_point[0] - start_point[0]
            d = 1 if self.viewer.dims.ndim == 2 else opposite_point[2] - start_point[2]

            shape_info = {
                "x": int(start_point[1]),
                "y": int(start_point[0]),
                "z": int(start_point[2]),
                "w": int(w),
                "h": int(h),
                "d": int(d)
            }
            print(f"Shape info: {shape_info}")
            return shape_info

    def create_roi(self, id):

        # Create the custom widget
        custom_widget = RoiListWidget(str(id))

        # Wrap the custom widget in a QListWidgetItem
        list_item = QListWidgetItem()
        list_item.setSizeHint(custom_widget.sizeHint())

        # Add the widget to the QListWidget
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, custom_widget)
   
    def register_with_IDMS(self):
        print("Executing this statement ! ")

