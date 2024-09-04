from typing import TYPE_CHECKING

from qtpy.QtWidgets import QWidget, QTabWidget
import os
from qtpy import uic
from .IDMS_main_widget import IDMS_main_widget
from .roi_generator_widget import ROI_Generator_widget
from .segmentation_generator_widget import Segmentation_widget
from .idms_backend import IDMS_Backend

if TYPE_CHECKING:
    import napari

class Main_Widget(QWidget):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        # Initializing
        super().__init__()
        self.viewer = viewer

        # Load the UI file - Main window - just the panel
        script_dir = os.path.dirname(__file__)
        ui_file_name = "Main_UI.ui"
        abs_file_path = os.path.join(script_dir, '..', 'UI_files', ui_file_name)
        uic.loadUi(abs_file_path, self)

        # Get the tab widget and add all our individual widgets there
        self.tab_widget = self.findChild(QTabWidget, "tab_widget")
        self.tab_widget.addTab(IDMS_main_widget(self.viewer,IDMS_Backend()), "IDMS main")
        # self.tab_widget.addTab(IDMS_main_widget(self.viewer), "IDMS main")
        self.tab_widget.addTab(ROI_Generator_widget(self.viewer), "ROI Generator")
        self.tab_widget.addTab(Segmentation_widget(self.viewer), "Segmentation/Annotation")

