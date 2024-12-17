from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QSpinBox, QDoubleSpinBox, QPushButton)

class ArrayEditorDialog(QDialog):
    """Dialog for editing array parameters"""
    
    def __init__(self, array_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Array Parameters")
        self._init_ui(array_data)

    def _init_ui(self, array_data):
        layout = QVBoxLayout(self)
        
        # Array Type
        self.array_type = self._create_array_type_combo(array_data['array_type'])
        layout.addWidget(QLabel("Array Type:"))
        layout.addWidget(self.array_type)
        
        # Elements
        self.elements = self._create_elements_spinbox(array_data['elements'])
        layout.addWidget(QLabel("Elements:"))
        layout.addWidget(self.elements)
        
        # Parameters
        self.parameters = {
            'spacing': self._create_parameter_spinbox(0.1, 10.0, array_data['spacing'], "Spacing (λ):"),
            'steering': self._create_parameter_spinbox(-90, 90, array_data['steering'], "Steering (°):"),
            'phase': self._create_parameter_spinbox(-360, 360, array_data['phase'], "Phase (°):"),
            'curvature': self._create_parameter_spinbox(0.1, 10.0, array_data['curvature'], "Curvature:"),
            'frequency': self._create_parameter_spinbox(1, 1000, array_data['frequency'], "Frequency (MHz):"),
            'x_position': self._create_parameter_spinbox(-50, 50, array_data['x_position'], "X Position:"),
            'y_position': self._create_parameter_spinbox(-50, 50, array_data['y_position'], "Y Position:")
        }
        
        for label, spinbox in self.parameters.items():
            layout.addWidget(QLabel(f"{label.replace('_', ' ').title()}:"))
            layout.addWidget(spinbox)
        
        # Buttons
        self._add_dialog_buttons(layout)

    def _create_array_type_combo(self, current_type):
        combo = QComboBox()
        combo.addItems(["Linear", "Curved"])
        # Set current type (capitalize first letter to match combo items)
        index = combo.findText(current_type.capitalize())
        if index >= 0:
            combo.setCurrentIndex(index)
        return combo

    def _create_elements_spinbox(self, value):
        spinbox = QSpinBox()
        spinbox.setRange(1, 100)
        spinbox.setValue(value)
        return spinbox

    def _create_parameter_spinbox(self, min_val, max_val, value, label):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(value)
        return spinbox

    def _add_dialog_buttons(self, layout):
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def get_values(self):
        return {
            'array_type': self.array_type.currentText().lower(),  # Changed from 'type' to 'array_type'
            'elements': self.elements.value(),
            **{key: spinbox.value() for key, spinbox in self.parameters.items()}
        }
