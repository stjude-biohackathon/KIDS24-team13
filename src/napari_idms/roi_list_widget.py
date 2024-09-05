from qtpy.QtWidgets import QWidget, QLabel, QWidget, QLabel, QDoubleSpinBox
import os
from qtpy import uic

class RoiListWidget(QWidget):
    def __init__(self, header, roi_dict, idms_api, parent=None):
        super().__init__(parent)

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "roi_list_item.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        self.roi_lbl = self.findChild(QLabel, "roi_lbl")
        self.x_dsb = self.findChild(QDoubleSpinBox, "x_dsb")
        self.y_dsb = self.findChild(QDoubleSpinBox, "y_dsb")
        self.width_dsb = self.findChild(QDoubleSpinBox, "width_dsb")
        self.height_dsb = self.findChild(QDoubleSpinBox, "height_dsb")
        self.z_dsb = self.findChild(QDoubleSpinBox, "z_dsb")
        self.depth_dsb = self.findChild(QDoubleSpinBox, "depth_dsb")

        self.roi_lbl.setText(header)

        self.x_dsb.setValue(roi_dict['x'])
        self.y_dsb.setValue(roi_dict['y'])
        self.width_dsb.setValue(roi_dict['width'])
        self.height_dsb.setValue(roi_dict['height'])
        self.z_dsb.setValue(roi_dict['z'])
        self.depth_dsb.setValue(roi_dict['depth'])
        
        ic_details = idms_api.get_image_collection_details('ic_3422f10e2b0bf10e2b0b6e80ccd6ffffffff1725371996398')

        # print(ic_details[0]['bounds'])
        # print(ic_details[0]['bounds']['maxX'])
        # Setting the spinner limits
        y_max = int(ic_details[0]['bounds']['maxY'])
        x_max = int(ic_details[0]['bounds']['maxX'])
        z_max = int(ic_details[0]['bounds']['maxZ'])


        #Has to be dynamically changed?
        width_max = int(ic_details[0]['bounds']['maxX'])
        height_max = int(ic_details[0]['bounds']['maxY'])
        depth_max = int(ic_details[0]['bounds']['maxZ'])

        self.x_dsb.setMaximum(x_max)
        self.y_dsb.setMaximum(y_max)
        self.width_dsb.setMaximum(width_max)
        self.height_dsb.setMaximum(height_max)
        self.z_dsb.setMaximum(z_max)
        self.depth_dsb.setMaximum(depth_max)

    def get_x(self):
        return int(self.x_dsb.value())
    
    def get_y(self):
        return int(self.y_dsb.value())
    
    def get_width(self):
        return int(self.width_dsb.value())
    
    def get_height(self):
        return int(self.height_dsb.value())
    
    def get_z(self):
        return int(self.z_dsb.value())
    
    def get_depth(self):
        return int(self.depth_dsb.value())
    
    def set_x(self, x):
        self.x_dsb.setValue(x)

    def set_y(self, y):
        self.y_dsb.setValue(y)

    def set_width(self, width):
        self.width_dsb.setValue(width)

    def set_height(self, height):
        self.height_dsb.setValue(height)
    
    def set_z(self, z):
        self.z_dsb.setValue(z)

    def set_depth(self, depth):
        self.depth_dsb.setValue(depth)
    