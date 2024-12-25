from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox
from .parameter_slider import ParameterSlider, SliderConfig

class ParameterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        self._setup_layout()
        self._setup_array_type()
        self._setup_sliders()
        self._apply_styling()
    
    def _setup_layout(self):
        self.layout = QVBoxLayout(self)
        self.group = QGroupBox("Current Unit")
        self.grid_layout = QGridLayout()
        
    def _setup_array_type(self):
        self.grid_layout.addWidget(QLabel("Array Type:"), 0, 0)
        self.array_type = QComboBox()
        self.array_type.addItems(["Linear", "Curved"])
        self.grid_layout.addWidget(self.array_type, 0, 1)
    
    def _setup_sliders(self):
        slider_configs = {
            'elements': SliderConfig("Elements", 1, 512, 16, 1),
            'spacing': SliderConfig("Spacing (λ)", 0.1, 1.0, 0.5, 0.1),
            'steering': SliderConfig("Steering (°)", -90, 90, 0, 1),
            'curvature': SliderConfig("Curvature", 0.1, 1.0, 0.5, 0.1),
            'frequency': SliderConfig("Frequency (MHz)", 1, 28000, 100, 10),
            'x_position': SliderConfig("X-Position", -10, 10, 0.0, 1),
            'y_position': SliderConfig("Y-Position", -10, 10, 0.0, 1)
        }
        
        self.sliders = {}
        for i, (name, config) in enumerate(slider_configs.items(), start=1):
            self.sliders[name] = ParameterSlider(config)
            self.grid_layout.addWidget(self.sliders[name], i, 0, 1, 2)
        
        self.sliders['curvature'].setEnabled(False)
        
        self.group.setLayout(self.grid_layout)
        self.layout.addWidget(self.group)
    
    def _apply_styling(self):
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
    
    @property
    def elements(self): return self.sliders['elements']
    @property
    def spacing(self): return self.sliders['spacing']
    @property
    def steering(self): return self.sliders['steering']
    @property
    def curvature(self): return self.sliders['curvature']
    @property
    def frequency(self): return self.sliders['frequency']
    @property
    def x_position(self): return self.sliders['x_position']
    @property
    def y_position(self): return self.sliders['y_position']
