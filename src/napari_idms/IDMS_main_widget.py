from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget
import os
from qtpy import uic
from qtpy.QtCore import Qt
import sys
from .checkable_combobox import CheckableComboBox

# IDMS Main class
class IDMS_main_widget(QWidget):
    def __init__(self, viewer,idms_api=None):
        # Initializing
        super().__init__()
        self.viewer = viewer
        self.full_image = "Full Image"

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "IDMS_main.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Get the dropdown boxes from ui file
        self.owner_cbbox = self.findChild(QComboBox, "owner_cbbox")
        self.project_cbbox = self.findChild(QComboBox, "project_cbbox")
        self.group_cbbox = self.findChild(QComboBox, "group_cbbox")
        self.ic_cbbox = self.findChild(QComboBox, "ic_cbbox")


        # Get the layout boxes to add
        self.roi_hbox = self.findChild(QHBoxLayout, "roi_hbox")
        self.seg_hbox = self.findChild(QHBoxLayout, "seg_hbox")


        # Add initial items to combobox inside the hboxes
        self.roi_cbbox =  CheckableComboBox()
        self.roi_hbox.addWidget(self.roi_cbbox)

        self.seg_cbbox =  CheckableComboBox()
        self.seg_hbox.addWidget(self.seg_cbbox)

        # Trigger IDMS
        self.idms = idms_api

        # Populate Initially
        self.populate_combobox(self.owner_cbbox, [""] + self.idms.get_owners()) # Owner populated


        # Populate one by one based on selection of previous - event triggers
        self.owner_cbbox.currentIndexChanged.connect(self.owner_changed)
        self.project_cbbox.currentIndexChanged.connect(self.project_changed)
        self.group_cbbox.currentIndexChanged.connect(self.group_changed)
        self.ic_cbbox.currentIndexChanged.connect(self.ic_changed)
        self.roi_cbbox.currentIndexChanged.connect(self.roi_changed)
        #self.seg_cbbox.currentIndexChanged.connect(self.segmentation_changed)


    # Function to add list of items to the combo box
    def populate_combobox(self,combo_box,items):
        combo_box.clear()  # Clear existing items
        combo_box.addItems(items)  # Add new items from the list


    # Group of Functions to populate combo boxes based on hirarchy and events
    def owner_changed(self):
        # Clear all other combo boxes in hierarchy - could be a deign pattern code later ?
        self.project_cbbox.clear()
        self.group_cbbox.clear()
        self.ic_cbbox.clear()
        self.roi_cbbox.clear()
        self.seg_cbbox.clear()

        # Get all projects for this owner and update projects list
        if self.owner_cbbox.currentText() != "":
            projects_list = self.idms.get_projects(self.owner_cbbox.currentText())
            self.populate_combobox(self.project_cbbox, [""] + projects_list)


    def project_changed(self):
        # Clear all other combo boxes in hierarchy - could be a deign pattern code later ?
        self.group_cbbox.clear()
        self.ic_cbbox.clear()
        self.roi_cbbox.clear()
        self.seg_cbbox.clear()

        # Get all groups for this owner and update projects list
        if self.project_cbbox.currentText() != "":
            groups_list = self.idms.get_groups(self.owner_cbbox.currentText(), self.project_cbbox.currentText())
            self.populate_combobox(self.group_cbbox, [""] + groups_list)

    def group_changed(self):
        # Clear all other combo boxes in hierarchy - could be a deign pattern code later ?
        self.ic_cbbox.clear()
        self.roi_cbbox.clear()
        self.seg_cbbox.clear()

        # Get all image collections for this owner and update projects list
        if self.group_cbbox.currentText() != "":
            ic_list = self.idms.get_image_collections(self.owner_cbbox.currentText(), self.project_cbbox.currentText(), self.group_cbbox.currentText())
            self.populate_combobox(self.ic_cbbox, [""] + ic_list)

    def ic_changed(self):
        # Clear all other combo boxes in hierarchy - could be a deign pattern code later ?
        self.roi_cbbox.clear()
        self.seg_cbbox.clear()

        # Get all rois for this owner and update projects list
        if self.ic_cbbox.currentText() != "":
            roi_list = self.idms.get_roi_boxes(self.owner_cbbox.currentText(), self.project_cbbox.currentText(),
                                                      self.group_cbbox.currentText(), self.ic_cbbox.currentText())

            print("hi",roi_list)

            roi_list = ["","1","2"]

            self.roi_cbbox.set_items([""]+roi_list)


    def roi_changed(self):
        # Clear all other combo boxes in hierarchy - could be a deign pattern code later ?
        self.seg_cbbox.clear()

        # Get all rois for this owner and update projects list
        if self.roi_cbbox.currentText() != "":
            seg_list = ["", "Seg_2", "Seg 3"]
            self.seg_cbbox.set_items([""]+seg_list)


















