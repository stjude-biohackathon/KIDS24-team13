from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QProgressBar, QWidget, QVBoxLayout, QListWidget, QMessageBox
import os
from qtpy import uic
from qtpy.QtCore import Qt
import sys
from .checkable_combobox import CheckableComboBox, CheckBoxPopup
from .advanced_settings import Adv_Settings_FormWidget
from qtpy.QtWidgets import QApplication
import numpy as np

# IDMS Main class
class IDMS_main_widget(QWidget):
    def __init__(self, viewer,idms_api=None):
        # Initializing
        super().__init__()
        self.viewer = viewer
        self.roi_from_settings = "ROI from Advanced Settings"
        self.ic_id_list=None
        self.ic_list = None

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "IDMS_main.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Get Buttons and connect them to functions
        self.load_metadata_btn = self.findChild(QPushButton, "load_metadata_btn")
        self.load_main_btn = self.findChild(QPushButton, "load_main_btn")
        self.advanced_settings_btn = self.findChild(QPushButton, "advanced_settings_btn")
        self.clear_btn = self.findChild(QPushButton, "clear_btn")

        self.load_metadata_btn.clicked.connect(self.load_metadata)
        self.load_main_btn.clicked.connect(self.load_data_from_IDMS)
        self.advanced_settings_btn.clicked.connect(self.load_adv_settings)
        self.clear_btn.clicked.connect(self.clear_all_items)

        # Get meta data list space
        self.meta_ls = self.findChild(QListWidget, "meta_ls")

        # Get progress bar
        self.status_progress = self.findChild(QProgressBar, "status_progress")

        # Set advanced settings
        self.adv_settings = Adv_Settings_FormWidget()


        # Get the dropdown boxes from ui file
        self.owner_cbbox = self.findChild(QComboBox, "owner_cbbox")
        self.project_cbbox = self.findChild(QComboBox, "project_cbbox")
        self.group_cbbox = self.findChild(QComboBox, "group_cbbox")
        self.ic_cbbox = self.findChild(QComboBox, "ic_cbbox")

        # Get ROI and Segmentation buttons
        self.roi_select_btn = self.findChild(QPushButton, "roi_select_btn")
        self.seg_select_btn = self.findChild(QPushButton, "seg_select_btn")

        self.roi_select_btn.clicked.connect(self.roi_selection)
        self.seg_select_btn.clicked.connect(self.seg_selection)

        self.roi_select_btn.setEnabled(False)
        self.seg_select_btn.setEnabled(False)

        self.roi_cbbox = CheckBoxPopup()
        self.seg_cbbox = CheckBoxPopup()

        # Trigger IDMS
        self.idms = idms_api

        # Populate Initially
        self.populate_combobox(self.owner_cbbox, [""] + self.idms.get_owners()) # Owner populated


        # Populate one by one based on selection of previous - event triggers
        self.owner_cbbox.currentIndexChanged.connect(self.owner_changed)
        self.project_cbbox.currentIndexChanged.connect(self.project_changed)
        self.group_cbbox.currentIndexChanged.connect(self.group_changed)
        self.ic_cbbox.currentIndexChanged.connect(self.ic_changed)
        #self.roi_cbbox.model().itemChanged.connect(self.roi_changed) # ROI changed will be trigger inside roi selection function


    # Function to load meta data
    def load_metadata(self):
        # Clear the QListWidget first (optional)
        self.meta_ls.clear()

        if self.ic_cbbox.currentText() == "":
            self.show_message("Selection required for fetching metadata")
            return

        # Get data from IDMS
        current_ic_id = self.get_current_ic_id()
        if current_ic_id is not None:
            data_all = self.idms.get_image_collection_details(self.get_current_ic_id())
            data = data_all[0]
            # Access the 'metadata' list of dictionaries
            metadata_list = data.get('metadata', [])

            # Loop through each dictionary in the 'metadata' list
            for metadata in metadata_list:
                # Extract the 'key' and 'value' and format them
                key_value_pair = f"{metadata.get('key')} : {metadata.get('value')}"
                self.meta_ls.addItem(key_value_pair)

    # Get particular meta data
    def get_specific_meta(self,target_key):
        current_ic_id = self.get_current_ic_id()
        if current_ic_id is not None:
            data_all = self.idms.get_image_collection_details(current_ic_id)
            data = data_all[0]

            # Access the 'metadata' list of dictionaries
            metadata_list = data.get('metadata', [])

            # Loop through each dictionary in the 'metadata' list
            for metadata in metadata_list:
                # Check if the current metadata dictionary has the target key
                if metadata.get('key') == target_key:
                    # Return the corresponding value
                    target_value = metadata.get('value')
                    #print(f"The value for '{target_key}' is: {target_value}")
                    return target_value


    def load_data_from_IDMS(self):
        print("Materializing from IDMS")
        if self.ic_cbbox.currentText() == "":
            self.show_message("Selection required for Materialization")
            return

        if not self.roi_cbbox.checked_items:
            self.show_message("ROI Selection required for Materialization")
            return

        self.status_progress.setValue(10)
        QApplication.processEvents()

        # Check if Advanced ROI is selected - to be implemented
        if self.roi_from_settings in self.roi_cbbox.checked_items:
            self.adv_settings.x_val = int(
                self.adv_settings.x_input.text()) if self.adv_settings.x_input.text() != "" else 0
            self.adv_settings.y_val = int(
                self.adv_settings.y_input.text()) if self.adv_settings.y_input.text() != "" else 0
            self.adv_settings.z_val = int(
                self.adv_settings.z_input.text()) if self.adv_settings.z_input.text() != "" else 0
            self.adv_settings.width_val = int(
                self.adv_settings.width_input.text()) if self.adv_settings.width_input.text() != "" else (self.get_specific_meta("SIZEX"))
            self.adv_settings.height_val = int(
                self.adv_settings.height_input.text()) if self.adv_settings.height_input.text() != "" else (self.get_specific_meta("SIZEY"))
            self.adv_settings.depth_val = int(
                self.adv_settings.depth_input.text()) if self.adv_settings.depth_input.text() != "" else (self.get_specific_meta("SIZEZ"))

            data = self.idms.get_array_from_box_coordinate(self.adv_settings.x_val, self.adv_settings.y_val, self.adv_settings.z_val, self.adv_settings.width_val, self.adv_settings.height_val, self.adv_settings.depth_val, self.get_current_ic_id())
            offset = (self.adv_settings.z_val,self.adv_settings.y_val,self.adv_settings.x_val)
            if data.ndim == 2:
                data = np.expand_dims(data,axis=0)

            # Add the data to viewer
            self.viewer.add_image(data,name=self.roi_from_settings,translate=offset)

        self.status_progress.setValue(30)


        # Check if ROI is choosen - loop through
        for i,roi_to_pull in enumerate(self.roi_cbbox.checked_items):
            if roi_to_pull==self.roi_from_settings:
                continue

            current_roi_id = self.get_roi_id_for_roi_name(roi_to_pull)
            x_offset,y_offset,z_offset = self.get_roi_offset_for_roi_name(roi_to_pull)
            data = self.idms.get_array_from_box_id(current_roi_id)
            if data.ndim == 2:
                data = np.expand_dims(data,axis=0)
            self.viewer.add_image(data,name=roi_to_pull,translate=(z_offset,y_offset,x_offset))

            # Update progress bar based on the nth roi
            progress_value = int(30 + (((len(self.roi_cbbox.checked_items)-2 + i) / (len(self.roi_cbbox.checked_items))) * 30))
            self.status_progress.setValue(progress_value)


        # Load Segmentations
        for i,seg_to_pull in enumerate(self.seg_cbbox.checked_items):
            current_seg_id = self.get_seg_id_for_seg_name(seg_to_pull)
            x_offset, y_offset, z_offset = self.get_seg_offset_for_seg_name(seg_to_pull)
            data = self.idms.get_array_from_seg_id(current_seg_id)
            if data.ndim == 2:
                data = np.expand_dims(data,axis=0)
            self.viewer.add_labels(data ,name=seg_to_pull,translate=(z_offset,y_offset,x_offset))

            # Update progress bar based on the nth roi
            progress_value = int(60 + (((len(self.seg_cbbox.checked_items)+ i) / (len(self.seg_cbbox.checked_items))) * 38))
            self.status_progress.setValue(progress_value)

        self.status_progress.setValue(100)


    def load_adv_settings(self):
        if self.ic_cbbox.currentText() != "":
            self.adv_settings.show()
        else:
            self.show_message("Valid Image Collection needed")


    def clear_all_items(self):
        self.owner_cbbox.clear()
        self.project_cbbox.clear()
        self.group_cbbox.clear()
        self.ic_cbbox.clear()
        self.roi_cbbox.clear()
        self.seg_cbbox.clear()
        self.meta_ls.clear()

        self.populate_combobox(self.owner_cbbox, [""] + self.idms.get_owners())  # Owner populated
        self.status_progress.setValue(0)

        self.roi_select_btn.setEnabled(False)
        self.seg_select_btn.setEnabled(False)


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
            ic_list_of_dicts = self.idms.get_image_collections(self.owner_cbbox.currentText(), self.project_cbbox.currentText(), self.group_cbbox.currentText())
            self.ic_list = [name_dict["name"] for name_dict in ic_list_of_dicts if "name" in name_dict]
            self.ic_id_list = [id_dict["id"] for id_dict in ic_list_of_dicts if "id" in id_dict]
            self.populate_combobox(self.ic_cbbox, [""] + self.ic_list)

    def ic_changed(self):
        # Clear all other combo boxes in hierarchy - could be a deign pattern code later ?
        self.roi_cbbox.clear()
        self.seg_cbbox.clear()
        self.roi_select_btn.setEnabled(False)
        self.seg_select_btn.setEnabled(False)


        # Get all rois for this owner and update projects list
        if self.ic_cbbox.currentText() != "":
            list_of_roi_dicts = self.idms.get_roi_boxes(self.owner_cbbox.currentText(), self.project_cbbox.currentText(),
                                                      self.group_cbbox.currentText(), self.ic_cbbox.currentText())


            # Do it if only roi list is not empty
            self.roi_list = []
            self.roi_ids = []
            self.roi_info = []
            if list_of_roi_dicts:
                for item in list_of_roi_dicts:
                    if "boxName" in item:
                        self.roi_list.append(item["boxName"])
                        self.roi_ids.append(item["boxId"])
                        self.roi_info.append(item)

                self.roi_cbbox.populate_items(self.roi_list + [self.roi_from_settings])

            else:
                self.roi_cbbox.populate_items([self.roi_from_settings])

            self.roi_select_btn.setEnabled(True)


    def roi_refresh(self):
        # Get all rois for this owner and update projects list
        if self.ic_cbbox.currentText() != "":
            list_of_roi_dicts = self.idms.get_roi_boxes(self.owner_cbbox.currentText(), self.project_cbbox.currentText(),
                                                      self.group_cbbox.currentText(), self.ic_cbbox.currentText())


            # Do it if only roi list is not empty
            self.roi_list = []
            self.roi_ids = []
            self.roi_info = []
            if list_of_roi_dicts:
                for item in list_of_roi_dicts:
                    if "boxName" in item:
                        self.roi_list.append(item["boxName"])
                        self.roi_ids.append(item["boxId"])
                        self.roi_info.append(item)

                self.roi_cbbox.update_items(self.roi_list + [self.roi_from_settings])

            else:
                self.roi_cbbox.update_items([self.roi_from_settings])

            self.roi_select_btn.setEnabled(True)


    def roi_selection(self):
        if not self.roi_cbbox.checkboxes:
            self.show_message("No ROIs available for the current selection")
            self.seg_select_btn.setEnabled(False)
            return

        # Refresh ROI
        self.roi_refresh()

        if self.roi_cbbox.exec_():
            # Trigger ROI changed
            self.seg_select_btn.setEnabled(True)
            self.roi_changed()

    def seg_selection(self):
        if not self.seg_cbbox.checkboxes:
            self.show_message("No Segmentations available for the current selection")
            return

        # Refresh Segmentation change
        self.seg_refresh()

        if self.seg_cbbox.exec_():
            print("")

    def seg_refresh(self):
        if self.roi_cbbox.checked_items:
            # Get all segmentations for this owner and update projects list
            seg_list_dict = self.idms.get_roi_box_seg(self.owner_cbbox.currentText(),self.project_cbbox.currentText(), self.group_cbbox.currentText(), self.ic_cbbox.currentText(),self.roi_cbbox.checked_items)

            # Do it if only roi list is not empty
            self.seg_list = []
            self.seg_ids = []
            self.seg_all_info = []
            if seg_list_dict:
                for item in seg_list_dict:
                    self.seg_list.append(item["name"])
                    self.seg_ids.append(item["segId"])
                    self.seg_all_info.append(item)

                self.seg_cbbox.update_items(self.seg_list)

    def roi_changed(self):
        # Clear all other combo boxes in hierarchy
        self.seg_cbbox.clear()

        if self.roi_cbbox.checked_items:
            # Get all segmentations for this owner and update projects list
            seg_list_dict = self.idms.get_roi_box_seg(self.owner_cbbox.currentText(),self.project_cbbox.currentText(), self.group_cbbox.currentText(), self.ic_cbbox.currentText(),self.roi_cbbox.checked_items)


            # Do it if only roi list is not empty
            self.seg_list = []
            self.seg_ids = []
            self.seg_all_info = []
            if seg_list_dict:
                for item in seg_list_dict:
                    self.seg_list.append(item["name"])
                    self.seg_ids.append(item["segId"])
                    self.seg_all_info.append(item)

                self.seg_cbbox.populate_items(self.seg_list)


    def get_current_ic_id(self):
        query = self.ic_cbbox.currentText()
        if query in self.ic_list:
            index = self.ic_list.index(query)
            return self.ic_id_list[index]
        else:
            return None  # Or handle this case as needed


    def get_roi_id_for_roi_name(self,roi_name):
        query = roi_name
        if query in self.roi_list:
            index = self.roi_list.index(query)
            return self.roi_ids[index]
        else:
            return None  # Or handle this case as needed


    def get_roi_offset_for_roi_name(self,roi_name):
        query = roi_name
        if query in self.roi_list:
            index = self.roi_list.index(query)
            info = self.roi_info[index]
            x_offset = info["x"]
            y_offset = info["y"]
            z_offset = info["z"]
            return x_offset,y_offset,z_offset


    def get_seg_offset_for_seg_name(self,seg_name):
        query = seg_name
        if query in self.seg_list:
            index = self.seg_list.index(query)
            info = self.seg_all_info[index]
            x_offset = info["x"]
            y_offset = info["y"]
            z_offset = info["z"]
            return x_offset,y_offset,z_offset


    def get_seg_id_for_seg_name(self,seg_name):
        query = seg_name
        if query in self.seg_list:
            index = self.seg_list.index(query)
            return self.seg_ids[index]
        else:
            return None  # Or handle this case as needed

    def show_message(self, message):
        """Show a pop-up message with an OK button."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Message")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()  # Show the message box