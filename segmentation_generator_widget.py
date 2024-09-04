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
        ui_file_name = "segmentation.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Example usage
        #self.example_btn = self.findChild(QPushButton, "pushButton")
        #self.example_label = self.findChild(QLabel,"label")

        #self.example_btn.clicked.connect(self.print_in_label)
        self.layerComboBox = self.findChild(QComboBox, 'comboBox')

        # Set the model for the combo box
        


        # Layout to hold checkboxes
        self.checkboxLayout = QVBoxLayout()
        # Example setup: Add a QLabel and the combo box from the UI
        layout = QVBoxLayout(self)
        
        self.oldnames = {}
        # Connect to napari layer events
        self.viewer.layers.events.inserted.connect(self.add_layer)
        self.viewer.layers.events.removed.connect(self.remove_layer)
        self.viewer.layers.events.changed.connect(self.on_namechange)
        
        # Initialize the UI with existing layers
        for layer in self.viewer.layers:
            self.add_layer_to_ui(layer)
    

    
    def add_layer(self, event):
        """Add a new layer to both combo box and checkboxes."""
        new_layer = event.value
        self.oldnames[new_layer] = new_layer.name
        new_layer.events.name.connect(self.on_namechange)

        self.add_layer_to_ui(new_layer)

    def add_layer_to_ui(self, layer):
        """Helper method to update the UI when a layer is added."""
        # Add the layer name to the combo box
        self.layerComboBox.addItem(layer.name)

    def remove_layer(self, event):
        """Remove the layer from both combo box."""
        removed_layer = event.value
        del self.oldnames[removed_layer]
        # Remove from the combo box
        index = self.layerComboBox.findText(removed_layer.name)
        if index >= 0:
            self.layerComboBox.removeItem(index)

    def on_namechange(self, event):
        layer = event.source
        oldname = self.oldnames[layer]
        newname = layer.name
        print(oldname, newname)
        index = self.layerComboBox.findText(oldname)
        # Update the old name with the new name
        self.oldnames[layer] = newname
        if index != -1:
            self.layerComboBox.setItemText(index, newname)

    def print_in_label(self):
        self.example_label.setText("I am executed from Segmentation tab template")







