from qtpy.QtWidgets import QPushButton, QWidget, QComboBox, QLabel, QVBoxLayout
import os
from qtpy import uic
from qtpy.QtCore import Qt

class Segmentation_widget(QWidget):
    def __init__(self, viewer, idms_api=None):
        # Initializing
        super().__init__()
        self.viewer = viewer

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "segmentation.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Initialize old names for layers
        self.oldnames = {}

        # Layout for the widget
        layout = QVBoxLayout(self)

        # Checkable Multiple Selection ComboBox for layers
        self.layerComboBox = CheckableComboBox([])
        layout.addWidget(self.layerComboBox)

        # Register button setup
        self.register_button = self.findChild(QPushButton, "registerButton")
        layout.addWidget(self.register_button)

        # Connect button click to register function
        self.register_button.clicked.connect(self.on_register_clicked)

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
        self.layerComboBox.add_item(layer.name)

    def remove_layer(self, event):
        """Remove the layer from the combo box."""
        removed_layer = event.value
        del self.oldnames[removed_layer]
        self.layerComboBox.remove_item(removed_layer.name)

    def on_namechange(self, event):
        layer = event.source
        oldname = self.oldnames[layer]
        newname = layer.name
        index = self.layerComboBox.findText(oldname)
        # Update the old name with the new name
        self.oldnames[layer] = newname
        if index != -1:
            self.layerComboBox.setItemText(index, newname)

    def on_register_clicked(self):
        selected_layers = self.layerComboBox.get_checked_items()
        print(f"Registered layers: {selected_layers}")


class CheckableComboBox(QComboBox):
    def __init__(self, items, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.initUI(items)

    def initUI(self, items):
        self.items = items
        self.setEditable(False)
        self.model().itemChanged.connect(self.on_item_changed)
        for item in items:
            self.add_item(item)

    def add_item(self, item):
        self.addItem(item)
        item_model = self.model().item(self.count() - 1)
        item_model.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item_model.setCheckState(Qt.Unchecked)

    def remove_item(self, item):
        index = self.findText(item)
        if index >= 0:
            self.removeItem(index)

    def on_item_changed(self):
        checked_items = self.get_checked_items()
        print("Checked items:", checked_items)

    def get_checked_items(self):
        checked_items = []
        for i in range(self.count()):
            if self.model().item(i).checkState() == Qt.Checked:
                checked_items.append(self.model().item(i).text())
        return checked_items
