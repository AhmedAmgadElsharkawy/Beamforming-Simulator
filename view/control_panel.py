from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox
from view.parameter_slider import ParameterSlider

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Current Unit Controls
        current_unit_group = QGroupBox("Current Unit")
        current_unit_layout = QGridLayout()
        
        # Array Type
        current_unit_layout.addWidget(QLabel("Array Type:"), 0, 0)
        self.array_type = QComboBox()
        self.array_type.addItems(["Linear", "Curved"])
        current_unit_layout.addWidget(self.array_type, 0, 1)
        
        # Parameter Sliders
        self.elements = ParameterSlider("Elements", 1, 512, 16, 1)
        self.spacing = ParameterSlider("Spacing (λ)", 0.1, 1.0, 0.5, 0.1)
        self.steering = ParameterSlider("Steering (°)", -90, 90, 0, 1)
        self.curvature = ParameterSlider("Curvature", 0.1, 1.0, 0.5, 0.1)
        self.frequency = ParameterSlider("Frequency (MHz)", 1, 1000, 100, 10)
        self.x_position = ParameterSlider("X-Position", -10, 10, 0.0, 1)
        self.y_position = ParameterSlider("Y-Position", -10, 10, 0.0, 1)
        
        # Initialize disabled state for curvature (since Linear is default)
        self.curvature.setEnabled(False)
        
        # Add sliders to layout
        current_unit_layout.addWidget(self.elements, 1, 0, 1, 2)
        current_unit_layout.addWidget(self.spacing, 2, 0, 1, 2)
        current_unit_layout.addWidget(self.steering, 3, 0, 1, 2)
        current_unit_layout.addWidget(self.curvature, 4, 0, 1, 2)
        current_unit_layout.addWidget(self.frequency, 5, 0, 1, 2)
        current_unit_layout.addWidget(self.x_position, 6, 0, 1, 2)
        current_unit_layout.addWidget(self.y_position, 7, 0, 1, 2)
        
        current_unit_group.setLayout(current_unit_layout)
        layout.addWidget(current_unit_group)
        
        self.setStyleSheet("""
            QGroupBox {
                background-color: #1F2937;
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-weight: bold;
            }
            QLabel {
                color: white;
                font-size: 10pt;
            }
            QComboBox {
                background-color: #374151;
                color: white;
                border: 1px solid #4B5563;
                border-radius: 4px;
                padding: 4px;
                min-width: 100px;
            }
            QComboBox:focus {
                border: 1px solid #2563EB;
                background-color: #1F2937;
            }
        """)