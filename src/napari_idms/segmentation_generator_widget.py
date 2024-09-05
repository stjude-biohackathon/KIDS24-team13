from qtpy.QtWidgets import QPushButton,QHBoxLayout, QWidget, QComboBox, QLabel, QVBoxLayout, QMessageBox
import os
from qtpy import uic
from qtpy.QtCore import Qt

class Segmentation_widget(QWidget):
    def __init__(self, viewer, idms_api=None, idms_main=None):
        # Initializing
        super().__init__()
        self.viewer = viewer
        
        self.idms_api = idms_api
        self.idms_main = idms_main

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "segmentation.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Initialize old names for layers
        self.oldnames = {}

        # Layout for the widget
        layout = QVBoxLayout(self)

        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        #segmentation section
        seg_layout = QHBoxLayout()
        self.label = QLabel('Segmentation')
        seg_layout.addWidget(self.label)
        
        self.layerComboBox = CheckableComboBox([])
        seg_layout.addWidget(self.layerComboBox)
        layout.addLayout(seg_layout)

        
        #print(self.idms_main.roi_cbbox.checked_items)
        #print(self.roi_items)
        self.roi_items = set()
        roi_layout = QHBoxLayout()
    
        self.label = QLabel('ROIs')
        roi_layout.addWidget(self.label)

        self.roiComboBox = QComboBox()
        #self.roiComboBox.addItems(roi_items)
        roi_layout.addWidget(self.roiComboBox)

        layout.addLayout(roi_layout)

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
        # for layer in self.viewer.layers:
        #     # self.add_layer_to_ui(layer)
        #     self.oldnames[layer] = layer.name
        #     layer.events.name.connect(se////lf.on_namechange)
        #     self.add_layer_to_ui(layer)/


    def add_layer(self, event):
        """Add a new layer to both combo box and checkboxes."""
        # ROIs section
        roi_items = self.idms_main.roi_cbbox.checked_items
        for roi in roi_items:
            if roi not in self.roi_items:
                self.roi_items.add(roi)
                self.roiComboBox.addItem(roi)
        new_layer = event.value
        if new_layer.name in roi_items:
            return
        
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

        # Save each selected layer
        for layer_name in selected_layers:
            # Find the layer in the viewer by name
            layer = self.viewer.layers[layer_name]

            # Check if the layer has data (such as an image or labels layer)
            if hasattr(layer, 'data'):
                data = layer.data
                shape = data.shape

                #adding some prints to debug
                print(f"Layer '{layer_name}' data as NumPy array:")
                print(layer.data)
                print(type(layer.data))
                print(layer.data.shape)
                print("Number of axes:", layer.data.ndim) 
                # Determine the file path and save the data
                out = "/Volumes/ctrbioimageinformatics/common/BioHackathon/2024/segmentation_data/"
                file_name = f"{layer_name}.tiff"
                save_path = out + file_name
                
                # Save the layer as a TIFF file
                layer.save(save_path)

                #send to IDMS
                #send save_path, roi-id
                jude_path = "/research/sharedresources/cbi/common/BioHackathon/2024/segmentation_data/" + file_name
                #get this roi id from previous tab
                roi_id = "roiB_404555ff39fe191c31a89cf"

                if self.idms_api:
                    response = self.idms_api.create_roi_box_seg(roi_id, jude_path)
                    print(response)
                else:
                    print("failed to send to IDMS")


                print(f"Layer '{layer_name}' saved to {save_path}")
            else:
                print(f"Layer '{layer_name}' does not have accessible data as a NumPy array.")

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
