from qtpy.QtWidgets import QPushButton,QHBoxLayout, QWidget, QComboBox, QLabel, QVBoxLayout, QMessageBox
import os
from qtpy import uic
from qtpy.QtCore import Qt
from tifffile import imwrite
import uuid

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

        # ROIs section
        roi_layout = QHBoxLayout()
    
        self.label = QLabel('ROIs')
        roi_layout.addWidget(self.label)

        self.roiComboBox = QComboBox()
        # items = ['a', 'b', 'c', 'd']
        self.roi_items = set()
        # items = self.idms_main.roi_cbbox.checked_items
        # self.roiComboBox.addItems(items)
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
        for layer in self.viewer.layers:
            # self.add_layer_to_ui(layer)
            self.oldnames[layer] = layer.name
            layer.events.name.connect(self.on_namechange)
            self.add_layer_to_ui(layer)


    def add_layer(self, event):
        """Add a new layer to both combo box and checkboxes."""        
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
        # Get the selected ROI
        checked_roi = self.roiComboBox.currentText()
        print(f"Selected ROI: {checked_roi}")

        roi_idms_id = self.idms_main.get_roi_id_for_roi_name(checked_roi)

        # Get selected layers
        selected_layers = self.layerComboBox.get_checked_items()
        print(f"Registered layers: {selected_layers}")

        # Loop through the selected layers and save each
        for layer_name in selected_layers:
            layer = self.viewer.layers[layer_name]

            # Check if the layer has data
            if hasattr(layer, 'data'):
                data = layer.data
                shape = data.shape

                # Debug prints
                print(layer.data.shape)
                print("Number of axes:", layer.data.ndim)

                # Determine the file path and save the data
                if os.name == "posix":
                    out = "/Volumes/ctrbioimageinformatics/common/BioHackathon/2024/segmentation_data/"
                else:
                    out = r"Z:\ResearchHome\SharedResources\CtrBioimageInformatics\common\BioHackathon\2024\segmentation_data\\"

                unique_id = uuid.uuid4()
                file_name = f"{layer_name}_{unique_id}.ome.tif"
                # file_name = f"{layer_name}.ome.tif"
                save_path = out + file_name
                
                # Save the layer as a TIFF file
                try:
                    imwrite(save_path, layer.data, metadata={'axes': 'ZYX'})
                    saved = True
                    print(f"Layer '{layer_name}' saved to {save_path}")
                except Exception as e:
                    saved = False
                    print(f"Failed to save layer '{layer_name}': {e}")

                # Send the file path and ROI ID to IDMS
                jude_path = "/research/sharedresources/cbi/common/BioHackathon/2024/segmentation_data/" + file_name
                roi_id = roi_idms_id

                if saved and self.idms_api:
                    try:
                        response = self.idms_api.create_roi_box_seg(roi_id, jude_path)
                        print(response)
                        sent = True
                    except Exception as e:
                        sent = False
                        print(f"Failed to send to IDMS: {e}")
                else:
                    sent = False
                    print("Failed to send to IDMS or save path")

                # Show a dialog popup with success/failure message
                msg = QMessageBox()
                msg.setWindowTitle("Layer Registration Status")

                if saved and sent:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"Layer '{layer_name}' saved and sent to IDMS successfully!")
                elif saved and not sent:
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText(f"Layer '{layer_name}' saved to {save_path} but failed to send to IDMS.")
                else:
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(f"Failed to save layer '{layer_name}' and send to IDMS.")
                
                msg.exec_()

            else:
                print(f"Layer '{layer_name}' does not have accessible data as a NumPy array.")
                msg = QMessageBox()
                msg.setWindowTitle("Layer Registration Status")
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Layer '{layer_name}' does not have accessible data.")
                msg.exec_()

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
        