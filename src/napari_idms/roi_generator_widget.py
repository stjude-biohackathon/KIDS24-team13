from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QComboBox, QLabel, QWidget, QVBoxLayout, QListWidget, QListView, QListWidgetItem, QLabel
from qtpy.QtWidgets import QMessageBox, QDoubleSpinBox
import os
from qtpy import uic
import sys
import numpy as np

def show_warning_messagebox(message): 
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Warning) 
  
    # setting message for Message Box 
    msg.setText(message) 
      
    # setting Message box window title 
    msg.setWindowTitle("Warning MessageBox") 
      
    # declaring buttons on Message Box 
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
      
    # start the app 
    retval = msg.exec_() 
  

def show_info_messagebox(message): 
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Information) 

    # setting message for Message Box 
    msg.setText(message) 
    
    # setting Message box window title 
    msg.setWindowTitle("Info") 
    
    # declaring buttons on Message Box 
    msg.setStandardButtons(QMessageBox.Ok) 
    
    # start the app 
    retval = msg.exec_() 

def show_critical_messagebox(message): 
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Critical) 

    # setting message for Message Box 
    msg.setText(message) 
    
    # setting Message box window title 
    msg.setWindowTitle("Error") 
    
    # declaring buttons on Message Box 
    msg.setStandardButtons(QMessageBox.Ok) 
    
    # start the app 
    retval = msg.exec_() 


class RoiListWidget(QWidget):
    def __init__(self, header, roi_dict, idms_api, idms_main, parent=None, remove_callback=None):
        super().__init__(parent)

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "roi_list_item.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        self.roi_lbl = self.findChild(QLabel, "roi_lbl")
        self.remove_btn = self.findChild(QPushButton, "remove_btn")
        self.x_dsb = self.findChild(QDoubleSpinBox, "x_dsb")
        self.y_dsb = self.findChild(QDoubleSpinBox, "y_dsb")
        self.width_dsb = self.findChild(QDoubleSpinBox, "width_dsb")
        self.height_dsb = self.findChild(QDoubleSpinBox, "height_dsb")
        self.z_dsb = self.findChild(QDoubleSpinBox, "z_dsb")
        self.depth_dsb = self.findChild(QDoubleSpinBox, "depth_dsb")

        self.roi_lbl.setText(header)

        self.remove_callback = remove_callback  # Store the remove callback function

        ic_id = idms_main.get_current_ic_id()
        ic_details = idms_api.get_image_collection_details(ic_id)
        
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

        self.x_dsb.setValue(roi_dict['x'])
        self.y_dsb.setValue(roi_dict['y'])
        self.width_dsb.setValue(roi_dict['width'])
        self.height_dsb.setValue(roi_dict['height'])
        self.z_dsb.setValue(roi_dict['z'])
        self.depth_dsb.setValue(roi_dict['depth'])

        # Connect the remove button to the remove function
        self.remove_btn.clicked.connect(self.remove_item)

    def remove_item(self):
        if self.remove_callback:
            self.remove_callback(self)  # Call the parent widget's remove function with this widget

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
    
    def update_info(self, roi_dict):
        self.set_x(roi_dict['x'])
        self.set_y(roi_dict['y'])
        self.set_width(roi_dict['width'])
        self.set_height(roi_dict['height'])
        self.set_z(roi_dict['z'])
        self.set_depth(roi_dict['depth'])


class ROI_Generator_widget(QWidget):
    def __init__(self, viewer, idms_api=None, idms_main= None):
        # Initializing
        super().__init__()
        self.viewer = viewer
        self.idms_api = idms_api
        self.widget_list1 = None
        self.idms_main = idms_main
        # Initialize shapes_dict as an instance attribute
        self.shapes_dict = {}
        self.shape_widget_map = {}
        self.widget_list_map = {}
        self.shape_id_map = {}

        # Load the UI file - Main window
        script_dir = os.path.dirname(__file__)
        ui_file_name = "roi_generate_tab.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Create a QListWidget
        self.list_widget = self.findChild(QListWidget, "roi_lw")

        # Example usage
        self.idms_register_btn = self.findChild(QPushButton, "register_btn")
        self.idms_register_btn.clicked.connect(self.register_with_IDMS)

        self.viewer.layers.events.inserted.connect(self.on_layer_added)

        # Registering with IDMS

    def highlight_shape(self, shape_id):
        # Highlight the shape in the napari viewer
        self.shapes_layer.selected_data = [shape_id]

    def unhighlight_shape(self, shape_id):
        # Unhighlight the shape in the napari viewer
        self.shapes_layer.selected_data = []

    def on_layer_added(self, event):
        """Check if a new shapes layer has been added."""
        layer = event.value
        if layer.__class__.__name__ == 'Shapes':  # Check if the layer is a Shapes layer without importing napari
            # A new shapes layer has been added by the user
            self.shapes_layer = layer
            self.shapes_layer.events.data.connect(self.on_shape_drawn)
            print("New shapes layer added by the user.")
    
    def on_shape_drawn(self, event):
        shape_id = list(self.shapes_layer.selected_data)
        if shape_id: # Get the selected id only if it exists
            shape_id = int(shape_id[0])+1
        # Only focus on the most recently drawn shape

        if event.action == "added":
            # Get the last shape drawn
            shape = self.shapes_layer.data[-1]
            shape_int = shape.astype(int)

            #TODO: Make it always 3d even in 2D
            # If there are only two coordinates (x, y), set z to 0 by default
            if shape_int.shape[1] == 2:
                shape_int = np.hstack([shape_int, np.zeros((shape_int.shape[0], 1), dtype=int)])

            # Calculate the starting point (x, y, z)
            start_point = shape_int[0]  # The first corner of the rectangle (x, y, z)
            # Calculate width (w), height (h), and depth (d) based on the difference between first and opposite corner
            opposite_point = shape_int[2]  # The opposite corner of the rectangle
            w = opposite_point[2] - start_point[2]
            h = opposite_point[1] - start_point[1]
            d = 1 if self.viewer.dims.ndim == 2 else opposite_point[0] - start_point[0]

            shape_info = {
                "x": int(start_point[2]),
                "y": int(start_point[1]),
                "z": int(start_point[0]),
                "width": int(w),
                "height": int(h),
                "depth": int(d)
            }

            # Create the ROI for the last drawn shape
            shape_id = len(self.shapes_layer.data)
            self.shapes_dict[f'Shape {shape_id}'] = shape_info

            # Pass the last shape info to create_roi
            widget_id= self.create_roi(shape_id, shape_info)

            # Map the shape_id to the widget_id
            self.shape_widget_map[shape_id] = widget_id

            self.shape_id_map[shape_id] = self.shapes_layer.unique_id

            return shape_info, self.shapes_dict
        
        if event.action == "removed":
            widget_id = self.shape_widget_map[shape_id]
            self.remove_roi_item(widget_id)

        if event.action == "changed":
            self.on_shape_modified(shape_id-1)

        return self.shapes_dict

    def on_shape_modified(self, shape_id):
        """Handle modifications to existing shapes (like resize or move)."""
        # Get the modified shape's index
        shape = self.shapes_layer.data[shape_id]
        shape_int = shape.astype(int)

        # Handle both 2D and 3D cases (similar to on_shape_drawn)
        if shape_int.shape[1] == 2:
            shape_int = np.hstack([shape_int, np.zeros((shape_int.shape[0], 1), dtype=int)])

        start_point = shape_int[0]
        opposite_point = shape_int[2]

        # Recalculate width, height, and depth based on the new coordinates
        w = opposite_point[2] - start_point[2]
        h = opposite_point[1] - start_point[1]
        d = 1 if self.viewer.dims.ndim == 2 else opposite_point[0] - start_point[0]

        # Update shape info
        shape_info = {
            "x": int(start_point[2]),
            "y": int(start_point[1]),
            "z": int(start_point[0]),
            "width": int(w),
            "height": int(h),
            "depth": int(d)
        }

        # Update the dictionary with the new info
        shape_id = shape_id + 1  # Shape IDs start at 1, not 0
        self.shapes_dict[f'Shape {shape_id}'] = shape_info

        # Also update the widget associated with this shape (if necessary)
        widget = self.shape_widget_map.get(shape_id)
        if widget:
            widget.update_info(shape_info)


    def create_roi(self, id, shape_info) -> RoiListWidget:

        # Create the custom widget
        custom_widget = RoiListWidget(str(id), shape_info, self.idms_api, self.idms_main, remove_callback=self.remove_roi_item)

        # Wrap the custom widget in a QListWidgetItem
        list_item = QListWidgetItem()
        list_item.setSizeHint(custom_widget.sizeHint())
        

        # Add the widget to the QListWidget
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, custom_widget)

        self.widget_list_map[custom_widget] = list_item

        return custom_widget
    
    def remove_roi_item(self, widget):
        """Remove the widget from the QListWidget and delete it."""
        list_item = self.widget_list_map[widget]  # Get the QListWidgetItem associated with the widget
        row = self.list_widget.row(list_item)  # Get the row of the list item
        self.list_widget.takeItem(row)  # Remove the item from the QListWidget
       

        # Optionally remove the corresponding shape from the dictionary
        shape_id = int(widget.roi_lbl.text())
        if shape_id in self.shape_widget_map:
            del self.shape_widget_map[shape_id]
            del self.shapes_dict[f'Shape {shape_id}']
            
            # self.shapes_layer.remove(shape_id-1) #TODO Have to make layer selection dynamic
            # self.shapes_layer.data.pop(shape_id)
            # print(self.shapes_layer.data)
            del self.shape_id_map[shape_id]

        widget.deleteLater()  # Delete the widget from memory

        print(f"Removed shape {shape_id}. Current shapes:", self.shapes_dict)

    def register_with_IDMS(self, ic_id, idms_api=None):

        idms_api = self.idms_api
        self.widget_list = self.shape_widget_map[1]
        
        if not idms_api:
            show_critical_messagebox("IDMS API not found!")

            return

        ic_id = self.idms_main.get_current_ic_id()

        # Add check for z dimension
        try:

            box_id = idms_api.create_roi_box(self.widget_list.get_x(),
                                    self.widget_list.get_y(),
                                    self.widget_list.get_z(),
                                        self.widget_list.get_width(),
                                        self.widget_list.get_height(),
                                            self.widget_list.get_depth(),
                                            ic_id)
            
            if box_id:
                show_info_messagebox("Roi registered with IDMS!")
            else:
                raise Exception

        except Exception as e:
            show_critical_messagebox(f"Roi was not registered with IDMS!: \n{e}")
        


        

        



        

