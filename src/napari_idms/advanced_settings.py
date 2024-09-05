from qtpy.QtWidgets import QLineEdit, QPushButton, QWidget, QComboBox, QLabel, QWidget, QFormLayout, QListWidget

class Adv_Settings_FormWidget(QWidget):
    def __init__(self,defaults=None):
        super().__init__()

        # Backend variables
        if defaults is None:
            self.x_val = ""
            self.y_val = ""
            self.z_val = ""
            self.width_val = ""
            self.height_val = ""
            self.depth_val = ""

        else:
            self.x_val = defaults[0]
            self.y_val =  defaults[1]
            self.z_val =  defaults[2]
            self.width_val =  defaults[3]
            self.height_val =  defaults[4]
            self.depth_val =  defaults[5]

        self.init_ui()

    def init_ui(self):
        # Create form layout and input fields
        layout = QFormLayout()

        # Initialize QLineEdit fields with default values
        self.x_input = QLineEdit()
        self.x_input.setText(str(self.x_val))  # Set default value for x

        self.y_input = QLineEdit()
        self.y_input.setText(str(self.y_val))  # Set default value for y

        self.z_input = QLineEdit()
        self.z_input.setText(str(self.z_val))  # Set default value for z

        self.width_input = QLineEdit()
        self.width_input.setText(str(self.width_val))  # Set default value for width

        self.height_input = QLineEdit()
        self.height_input.setText(str(self.height_val))  # Set default value for height

        self.depth_input = QLineEdit()
        self.depth_input.setText(str(self.depth_val))  # Set default value for depth

        layout.addRow('x:', self.x_input)
        layout.addRow('y:', self.y_input)
        layout.addRow('z:', self.z_input)
        layout.addRow('Width:', self.width_input)
        layout.addRow('Height:', self.height_input)
        layout.addRow('Depth:', self.depth_input)

        # Submit button
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit_form)
        layout.addWidget(submit_button)

        # Set layout for the form window
        self.setLayout(layout)

    def submit_form(self):
        # Store the values from textboxes into backend variables
        self.x_val = int(self.x_input.text())
        self.y_val = int(self.y_input.text())
        self.z_val = int(self.z_input.text())
        self.width_val = int(self.width_input.text())
        self.height_val = int(self.height_input.text())
        self.depth_val = int(self.depth_input.text())

        # Output updated values (you can remove or modify this part as needed)
        print(f"Updated Values - x: {self.x_val}, y: {self.y_val}, z: {self.z_val}, "
              f"width: {self.width_val}, height: {self.height_val}, depth: {self.depth_val}")

        self.close()