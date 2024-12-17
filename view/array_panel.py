from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QGridLayout, QSpinBox, QDoubleSpinBox, 
                            QDialogButtonBox, QComboBox)

class ArrayPanel(QFrame):
    def __init__(self, array_data, on_delete=None, on_edit=None, on_visibility_change=None):
        super().__init__()
        self.array_data = array_data
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_visibility_change = on_visibility_change if on_visibility_change else lambda id, state: None
        self._init_ui(self.on_visibility_change)
        self._apply_styles()

    def _init_ui(self, on_visibility_change):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel(f"Array {self.array_data['id']}"))
        
        controls_layout = QHBoxLayout()
        
        # Visibility checkbox
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setChecked(True)
        if on_visibility_change:
            self.visibility_checkbox.stateChanged.connect(
                lambda state: on_visibility_change(self.array_data['id'], state == Qt.Checked)
            )
        controls_layout.addWidget(self.visibility_checkbox)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        edit_btn.clicked.connect(self._edit_array)
        controls_layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        delete_btn.clicked.connect(lambda: self.on_delete(self.array_data['id']))
        controls_layout.addWidget(delete_btn)
        
        main_layout.addLayout(controls_layout)

    def _create_spinbox(self, value_type, min_val, max_val, current_val):
        spinbox = QDoubleSpinBox() if isinstance(current_val, float) else QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(current_val)
        return spinbox

    def _edit_array(self):
        dialog = QDialog(self)
        layout = QGridLayout(dialog)
        
        # Array Type ComboBox
        array_type = QComboBox()
        array_type.addItems(["Linear", "Curved"])
        array_type.setCurrentText(self.array_data['array_type'].capitalize())
        layout.addWidget(QLabel("Array Type:"), 0, 0)
        layout.addWidget(array_type, 0, 1)
        
        # Create spinboxes
        elements = self._create_spinbox("Elements", 1, 100, self.array_data['elements'])
        spacing = self._create_spinbox("Spacing", 0.1, 10.0, self.array_data['spacing'])
        steering = self._create_spinbox("Steering", -90, 90, self.array_data['steering'])
        curvature = self._create_spinbox("Curvature", 0.1, 10.0, self.array_data['curvature'])
        frequency = self._create_spinbox("Frequency", 1, 28000, self.array_data['frequency'])
        x_position = self._create_spinbox("X Position", -50, 50, self.array_data['x_position'])
        y_position = self._create_spinbox("Y Position", -50, 50, self.array_data['y_position'])
        
        # Style for disabled parameters
        disabled_style = """
            QDoubleSpinBox:disabled {
                background-color: #2D3748;
                color: #718096;
            }
        """
        curvature.setStyleSheet(disabled_style)
        spacing.setStyleSheet(disabled_style)
        
        # Function to update parameter states
        def update_parameters(array_type):
            is_curved = array_type == "Curved"
            curvature.setEnabled(is_curved)
            spacing.setEnabled(not is_curved)
        
        # Connect array type changes to parameter updates
        array_type.currentTextChanged.connect(update_parameters)
        update_parameters(array_type.currentText())
        
        # Add widgets to layout
        layout.addWidget(QLabel("Elements:"), 1, 0)
        layout.addWidget(elements, 1, 1)
        layout.addWidget(QLabel("Spacing:"), 2, 0)
        layout.addWidget(spacing, 2, 1)
        layout.addWidget(QLabel("Steering:"), 3, 0)
        layout.addWidget(steering, 3, 1)
        layout.addWidget(QLabel("Curvature:"), 4, 0)
        layout.addWidget(curvature, 4, 1)
        layout.addWidget(QLabel("Frequency:"), 5, 0)
        layout.addWidget(frequency, 5, 1)
        layout.addWidget(QLabel("X Position:"), 6, 0)
        layout.addWidget(x_position, 6, 1)
        layout.addWidget(QLabel("Y Position:"), 7, 0)
        layout.addWidget(y_position, 7, 1)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons, 8, 0, 1, 2)
        
        if dialog.exec_():
            new_values = {
                'array_type': array_type.currentText().lower(),
                'elements': elements.value(),
                'spacing': spacing.value(),
                'steering': steering.value(),
                'curvature': curvature.value(),
                'frequency': frequency.value(),
                'x_position': x_position.value(),
                'y_position': y_position.value()
            }
            self.array_data.update(new_values)
            if self.on_edit:
                self.on_edit(self.array_data['id'], new_values)

    def _apply_styles(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 4px;
                padding: 8px;
                margin: 4px;
            }
            QLabel {
                color: white;
            }
            QCheckBox {
                color: white;
            }
            QPushButton {
                padding: 4px 8px;
                border-radius: 4px;
                border: none;
            }
        """)
