from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton, QWidget, 
                            QDoubleSpinBox, QSpinBox, QComboBox, QVBoxLayout, QDialog,
                            QCheckBox)


class EditArrayDialog(QDialog):
    def __init__(self, unit_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Array Parameters")
        layout = QVBoxLayout(self)
        
        # Array Type
        self.array_type = QComboBox()
        self.array_type.addItems(["Linear", "Curved"])
        self.array_type.setCurrentText(unit_data['type'].capitalize())
        layout.addWidget(QLabel("Array Type:"))
        layout.addWidget(self.array_type)
        
        # Elements
        self.elements = QSpinBox()
        self.elements.setRange(1, 100)
        self.elements.setValue(unit_data['elements'])
        layout.addWidget(QLabel("Elements:"))
        layout.addWidget(self.elements)
        
        # Spacing
        self.spacing = QDoubleSpinBox()
        self.spacing.setRange(0.1, 10.0)
        self.spacing.setValue(unit_data['spacing'])
        layout.addWidget(QLabel("Spacing (λ):"))
        layout.addWidget(self.spacing)
        
        # Steering
        self.steering = QDoubleSpinBox()
        self.steering.setRange(-90, 90)
        self.steering.setValue(unit_data['steering'])
        layout.addWidget(QLabel("Steering (°):"))
        layout.addWidget(self.steering)
        
        # Phase
        self.phase = QDoubleSpinBox()
        self.phase.setRange(-360, 360)
        self.phase.setValue(unit_data['phase'])
        layout.addWidget(QLabel("Phase (°):"))
        layout.addWidget(self.phase)
        
        # Curvature
        self.curvature = QDoubleSpinBox()
        self.curvature.setRange(0.1, 10.0)
        self.curvature.setValue(unit_data['curvature'])
        layout.addWidget(QLabel("Curvature:"))
        layout.addWidget(self.curvature)
        
        # Frequency
        self.frequency = QDoubleSpinBox()
        self.frequency.setRange(1, 1000)
        self.frequency.setValue(unit_data['frequency'])
        layout.addWidget(QLabel("Frequency (MHz):"))
        layout.addWidget(self.frequency)
        
        # Position controls
        self.x_position = QDoubleSpinBox()
        self.x_position.setRange(-50, 50)
        self.x_position.setValue(unit_data['x_position'])
        layout.addWidget(QLabel("X Position:"))
        layout.addWidget(self.x_position)
        
        self.y_position = QDoubleSpinBox()
        self.y_position.setRange(-50, 50)
        self.y_position.setValue(unit_data['y_position'])
        layout.addWidget(QLabel("Y Position:"))
        layout.addWidget(self.y_position)
        
        # Buttons
        buttons = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

    def get_values(self):
        return {
            'type': self.array_type.currentText().lower(),
            'elements': self.elements.value(),
            'spacing': self.spacing.value(),
            'steering': self.steering.value(),
            'phase': self.phase.value(),
            'curvature': self.curvature.value(),
            'frequency': self.frequency.value(),
            'x_position': self.x_position.value(),
            'y_position': self.y_position.value()
        }


class SavedUnit(QFrame):
    def __init__(self, parent=None, unit_data=None, on_delete=None, on_edit=None, on_visibility_change=None):
        super().__init__(parent)
        self.unit_data = unit_data
        self.on_delete = on_delete
        self.on_edit = on_edit
        
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        
        # Add label at the top
        main_layout.addWidget(QLabel(f"Array {unit_data['id']}"))
        
        # Horizontal layout for controls
        controls_layout = QHBoxLayout()
        
        # Add checkbox without text
        self.visibility_checkbox = QCheckBox()
        self.visibility_checkbox.setChecked(True)
        self.visibility_checkbox.stateChanged.connect(
            lambda state: on_visibility_change(unit_data['id'], state == 2)
        )
        controls_layout.addWidget(self.visibility_checkbox)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        edit_btn.clicked.connect(self.edit_unit)
        controls_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        delete_btn.clicked.connect(lambda: on_delete(unit_data['id']))
        controls_layout.addWidget(delete_btn)
        
        main_layout.addLayout(controls_layout)

        
    def edit_unit(self):
        dialog = EditArrayDialog(self.unit_data, self)
        if dialog.exec_():
            new_values = dialog.get_values()
            self.unit_data.update(new_values)
            if self.on_edit:
                self.on_edit(self.unit_data)
