from qtpy.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QComboBox, QScrollArea, QHBoxLayout, QPushButton, QDialog
from qtpy.QtCore import Qt

class CheckBoxPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Items")
        self.checked_items = []
        self.checkboxes = []
        self.items = []  # This will be populated dynamically

        # Main layout
        self.main_layout = QVBoxLayout(self)

        # Scrollable area for checkboxes
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)

        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)

        # Add buttons for select all, deselect all, and submit
        button_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.deselect_all_btn = QPushButton("Deselect All")
        self.submit_btn = QPushButton("Submit")

        self.select_all_btn.clicked.connect(self.select_all)
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        self.submit_btn.clicked.connect(self.submit)

        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.deselect_all_btn)
        button_layout.addWidget(self.submit_btn)

        # Add scroll area and button layout to main layout
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addLayout(button_layout)

    def populate_items(self, items):
        # Clear existing checkboxes
        for checkbox in self.checkboxes:
            checkbox.setParent(None)
        self.checkboxes.clear()

        # Dynamically add new checkboxes
        for item in items:
            checkbox = QCheckBox(item)
            self.checkboxes.append(checkbox)
            self.scroll_area_layout.addWidget(checkbox)

        self.scroll_area_widget.adjustSize()

    def select_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def deselect_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def submit(self):
        self.checked_items = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        self.accept()  # Close the pop-up

    def clear(self):
        self.deselect_all()
        self.checked_items=[]

        # Depopulate checkboxes (remove them from the layout)
        for checkbox in self.checkboxes:
            checkbox.setParent(None)
        self.checkboxes.clear()

        self.scroll_area_widget.adjustSize()

class CheckableComboBox(QComboBox):
    def __init__(self, items=None, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.items = items if items is not None else []
        self.checked_items = []
        self.initUI()

    def initUI(self):
        self.setEditable(True)  # Make the combo box editable to display checked items at the top
        self.lineEdit().setReadOnly(True)  # Prevent manual editing of the checked items display
        self.model().itemChanged.connect(self.on_item_changed)

        # Initialize the combo box with provided items
        self.populate_items(self.items)

    def populate_items(self, items):
        """Populate the combo box with items and make them checkable."""
        self.clear()  # Clear any existing items
        for item in items:
            self.addItem(item)
            item_model = self.model().item(self.count() - 1)
            item_model.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item_model.setCheckState(Qt.Unchecked)

    def set_items(self, items):
        """Dynamically change the list of items in the combobox."""
        self.items = items
        self.populate_items(items)

    def on_item_changed(self):
        """Handle the change in check state of items."""
        self.checked_items.clear()  # Clear current checked items

        # Gather all checked items
        for i in range(self.count()):
            if self.model().item(i).checkState() == Qt.Checked:
                self.checked_items.append(self.model().item(i).text())

        # Display checked items at the top, separated by semicolons
        self.update_checked_items_display()

    def update_checked_items_display(self):
        """Update the combobox display with checked items."""
        checked_items_str = "; ".join(self.checked_items)
        self.lineEdit().setText(checked_items_str)
