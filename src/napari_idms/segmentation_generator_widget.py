from qtpy.QtWidgets import QWidget, QComboBox, QVBoxLayout, QPushButton
import os
from qtpy import uic
from qtpy.QtCore import Qt
import json

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

        # Initialize label layers
        self.label_layers = []
        print(self.label_layers)

        # Checkable Multiple Selection
        self.checkable_combo_box = CheckableComboBox(self.label_layers, self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.checkable_combo_box)

        # Find the Register button from the UI
        self.register_button = self.findChild(QPushButton, "registerButton")
        layout.addWidget(self.register_button)
    
        # Connect the Register button click event
        self.register_button.clicked.connect(self.on_register_clicked)

        def update_layer_dropdown():
            self.checkable_combo_box.update_items(self.label_layers)

        def on_new_label_layer(event):
            label_name = getattr(event.value, 'name', str(event.value))
            self.label_layers.append(label_name)
            print("A new label layer was added:", label_name)
            update_layer_dropdown()

        def on_remove_label_layer(event):
            label_name = getattr(event.value, 'name', str(event.value))
            if label_name in self.label_layers:
                self.label_layers.remove(label_name)
            print("A label layer was removed:", label_name)
            update_layer_dropdown()

        def on_layer_renamed(event):
            old_name = getattr(event.old_value, 'name', str(event.old_value))
            new_name = getattr(event.value, 'name', str(event.value))
            print(new_name)
            if old_name in self.label_layers:
                index = self.label_layers.index(old_name)
                self.label_layers[index] = new_name
                print(f"Layer renamed from {old_name} to {new_name}")
                update_layer_dropdown()

        # Listen to the event of adding a new layer
        viewer.layers.events.inserted.connect(on_new_label_layer)
        viewer.layers.events.removed.connect(on_remove_label_layer)
        viewer.layers.events.changed.connect(on_layer_renamed)

    
    def on_register_clicked(self):
        # Get the selected items from the CheckableComboBox
        selected_items = self.checkable_combo_box.get_checked_items()
        # Convert to JSON and print
        json_output = json.dumps({"selected_layers": selected_items}, indent=4)
        print(json_output)


class CheckableComboBox(QComboBox):
    def __init__(self, items, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.items = items
        self.initUI()

    def initUI(self):
        self.model().itemChanged.connect(self.on_item_changed)
        self.populate_items(self.items)

    # def populate_items(self, items):
    #     self.clear()
    #     for item in items:
    #         self.addItem(item)
    #         item_model = self.model().item(self.count() - 1)
    #         item_model.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
    #         item_model.setCheckState(Qt.Unchecked)
    def populate_items(self, items):
        self.clear()
        self.items = items
        for item in items:
            self.addItem(item)
            item_model = self.model().item(self.count() - 1)
            item_model.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item_model.setCheckState(Qt.Unchecked)

    def update_items(self, new_items):
        self.items = new_items
        self.populate_items(self.items)

    def on_item_changed(self):
        checked_items = []
        for i in range(self.count()):
            if self.model().item(i).checkState() == Qt.Checked:
                checked_items.append(self.model().item(i).text())
        print("Checked items:", checked_items)

    def get_checked_items(self):
        # Retrieve all checked items
        checked_items = []
        for i in range(self.count()):
            if self.model().item(i).checkState() == Qt.Checked:
                checked_items.append(self.model().item(i).text())
        return checked_items