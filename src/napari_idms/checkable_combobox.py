from qtpy.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QComboBox
from qtpy.QtCore import Qt

class CheckableComboBox2(QComboBox):
    def __init__(self, items, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.items = items
        self.initUI()

    def initUI(self):
        self.model().itemChanged.connect(self.on_item_changed)
        for item in self.items:
            self.addItem(item)
            item_model = self.model().item(self.count() - 1)
            item_model.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item_model.setCheckState(Qt.Unchecked)

    def on_item_changed(self):
        checked_items = []
        for i in range(self.count()):
            if self.model().item(i).checkState() == Qt.Checked:
                checked_items.append(self.model().item(i).text())
        print("Checked items:", checked_items)


class CheckableComboBox3(QComboBox):
    def __init__(self, items, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.items = items
        self.checked_items = []
        self.initUI()

    def initUI(self):
        self.setEditable(True)  # Make the combo box editable to display checked items at the top
        self.lineEdit().setReadOnly(True)  # Prevent manual editing of the checked items display
        self.model().itemChanged.connect(self.on_item_changed)

        for item in self.items:
            self.addItem(item)
            item_model = self.model().item(self.count() - 1)
            item_model.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item_model.setCheckState(Qt.Unchecked)

    def on_item_changed(self):
        # Clear current checked items
        self.checked_items.clear()

        # Gather all checked items
        for i in range(self.count()):
            if self.model().item(i).checkState() == Qt.Checked:
                self.checked_items.append(self.model().item(i).text())

        # Display checked items at the top, separated by semicolons
        self.update_checked_items_display()

    def update_checked_items_display(self):
        checked_items_str = "; ".join(self.checked_items)
        self.lineEdit().setText(checked_items_str)


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