from typing import TYPE_CHECKING

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget
import os
from qtpy import uic
from qtpy.QtCore import Qt
import sys
sys.path.append('/Volumes/ctrbioimageinformatics/common/BioHackathon/2024/pyidms/plugins')
from common.idms_api import IdmsAPI
from common.owner import Owner
from common.project import Project

if TYPE_CHECKING:
    import napari

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.populate()

    def populate(self):
        for index in range(self.count()):
            item = self.model().item(index, 0)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

    def checked_items(self):
        checked_items = []
        for index in range(self.count()):
            if self.model().item(index, 0).checkState() == Qt.Checked:
                checked_items.append(self.itemText(index))
        return checked_items

    def add_checkable_items(self, items):
        self.clear()
        for item in items:
            self.addItem(item)
        self.populate()


class MockWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, viewer: "napari.viewer.Viewer"):
        # Initializing
        super().__init__()
        self.viewer = viewer
        # Initialize the IDMS API that auto-refreshes the token
        self.idms_api = IdmsAPI(username="INSERT_STJUDE_USERNAME", password="INSERT_STJUDE_PASSWORD", endpoint="INSERT_IDMS_API_ENDPOINT)

        # Initialize the IDMS API that uses a static token that expires in a week. No auto-refresh
        self.idms_api = IdmsAPI(endpoint="http://idms.stjude.org:8888/idms/api",
                                token="INSERT_IDMS_API_TOKEN")
        print(self.idms_api.health())

        self.owner_api = Owner(self.idms_api)
        self.project_api = Project(self.idms_api)
        self.items = ["Item1","Item2","Item3"]
        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "mockup.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        self.idms_main_page = self.findChild(QWidget, "main_tab")

        ui_file_name = "Dashboard.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self.idms_main_page)

        # Load the UI file - ROI Generate tab
        self.roi_tab = self.findChild(QWidget, "roi_tab")
        ui_file_name = "roi_generate_tab.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self.roi_tab)

        self.owner = self.findChild(QComboBox, "owner_cbbox")
        self.project = self.findChild(QComboBox, "project_cbbox")
        self.group = self.findChild(QComboBox, "group_cbbox")
        self.ic = self.findChild(QComboBox, "ic_cbbox")
        self.roi = self.findChild(QComboBox, "roi_cbbox")

        self.populate_combobox(self.owner, [owners['owner'] for owners in self.owner_api.search()])
        self.populate_combobox(self.project, self.items)
        self.populate_combobox(self.group, self.items)
        self.populate_combobox(self.ic, self.items)
        self.populate_combobox(self.roi, self.items)

        # Create the checkable combo box and replace the original one
        checkable_combo_box = CheckableComboBox(self)
        checkable_combo_box.add_checkable_items(
            [self.roi.itemText(i) for i in range(self.roi.count())])

        # Replace the original combo box with the new checkable one
        layout = self.roi.parentWidget().layout()
        layout.replaceWidget(self.roi, checkable_combo_box)
        self.roi.deleteLater()

        # Now 'comboBox' in the .ui file is replaced with 'checkable_combo_box'
        self.roi_cbbox = checkable_combo_box

        self.meta_ls = self.findChild(QListWidget, "meta_ls")
        load_metadata_btn = self.findChild(QPushButton, "load_metadata_btn")

        # Button to populate the list widget
        load_metadata_btn.clicked.connect(self.load_metadata)

        self.roi_lv = self.findChild(QWidget, "roi_lv")

        # Initialize a layout for the roi_lv to hold the dynamically added widgets
        self.roi_lv_layout = QVBoxLayout(self.roi_lv)
        self.roi_lv.setLayout(self.roi_lv_layout)

        # Simulate adding layers - to be done via event click
        self.on_layer_added("Shape 1")
        self.on_layer_added("Shape 2")
        self.on_layer_added("Shape 3")

    def populate_combobox(self,combobox: QComboBox, items: list):
        """
        Populate a QComboBox with items from a list.

        Parameters:
        combobox (QComboBox): The combo box to populate.
        items (list): A list of strings to add to the combo box.
        """
        combobox.clear()  # Clear any existing items in the combo box
        combobox.addItems(items)  # Add the items from the list

    def on_layer_added(self, layer_name):
        # Load the UI file for each list item
        script_dir = os.path.dirname(__file__)
        ui_file_name = "roi_list_item.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)

        # Create an instance of the widget
        new_widget = QWidget()
        uic.loadUi(abs_file_path, new_widget)

        # Add a remove button to each widget
        remove_button = self.findChild(QPushButton, "remove_btn")
        # remove_button.clicked.connect(lambda: self.remove_item(new_widget))
        
        label = new_widget.findChild(QLabel, "roi_lbl")
        if label:
            label.setText(layer_name)

        # Add the new widget to the list view layout
        self.roi_lv_layout.addWidget(new_widget)

    def remove_item(self, item_widget):
        # Remove the widget from the layout and delete it
        self.roi_lv_layout.removeWidget(item_widget)
        item_widget.deleteLater()

    def load_metadata(self):
        # Clear the QListWidget first (optional)
        self.meta_ls.clear()

        # Define the metadata as a list of strings
        metadata = [
            "Metadata",
            "---------------",
            "Scale : 8X",
            "Size: 1 GB",
            "Slices: 150",
            "Channels: 2"
        ]

        # Add each item to the QListWidget
        for item in metadata:
            self.meta_ls.addItem(item)




