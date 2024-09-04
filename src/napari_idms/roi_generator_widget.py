from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget, QListView, QListWidgetItem, QLabel, QVBoxLayout, QLineEdit
import os
from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.uic import loadUiType
import sys

# Load the .ui file
# Ui_CustomWidget, _ = loadUiType("custom_widget.ui")


# class CustomWidget(QWidget):
#     def __init__(self, text, parent=None):
#         super().__init__(parent)

#         # Create a label to show the text
#         self.label = QLabel(text)
        
#         # Set up the layout and add the label
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)


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

        # Creating the scrollbar for widget list
        # self.scroll = self.findChild(QListWidget, "roi_lw")
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


        # New code to handle shape layer and printing coordinates
        # self.shapes_layer = self.viewer.add_shapes()  # Create or access a shapes layer in napari
        # self.shapes_layer.events.data.connect(self.on_shape_drawn)  # Connect event when a new shape is drawn

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
            print("Coordinates of the drawn shape:", last_shape)
        else:
            print("No shape is drawn yet.")

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

