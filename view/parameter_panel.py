from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from .parameter_slider import ParameterSlider, SliderConfig

class ParameterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        self._setup_layout()
        self._setup_preset_buttons()
        self._setup_array_type()
        self._setup_sliders()
        self._apply_styling()
    
    def _setup_layout(self):
        self.layout = QVBoxLayout(self)
        
        # Add preset buttons group
        self.preset_group = QGroupBox("Preset Configurations")
        self.preset_layout = QVBoxLayout()
        self.preset_group.setLayout(self.preset_layout)
        self.layout.addWidget(self.preset_group)
        
        # Parameters group
        self.group = QGroupBox("Current Unit")
        self.grid_layout = QGridLayout()
        
    def _setup_preset_buttons(self):
        self.preset_buttons = {}
        
        # Create buttons for each preset
        presets = {
            '5G Communications': {
                'elements': 64,
                'spacing': 0.2,
                'steering': 0.0,
                'curvature': 0.0,
                'frequency': 1000.0,
                'x_position': 0.0,
                'y_position': 0.0,
                'array_type': 'Linear'
            },
            'Medical Ultrasound': {
                'elements': 7,
                'spacing': 10.0,
                'steering': 0.0,
                'curvature': 0.0,
                'frequency': 10.0,
                'x_position': 0.0,
                'y_position': 0.0,
                'array_type': 'Linear'
            },
            'Tumor Ablation': {
                'elements': 98,
                'spacing': 0.0,
                'steering': 0.0,
                'curvature': 2.1,
                'frequency': 900.0,
                'x_position': 0.0,
                'y_position': 0.0,
                'array_type': 'Linear'
            }
        }
        
        for name, config in presets.items():
            btn = QPushButton(name)
            btn.setProperty('config', config)
            btn.clicked.connect(lambda checked, c=config: self._apply_preset(c))
            self.preset_buttons[name] = btn
            self.preset_layout.addWidget(btn)
    
    def _apply_preset(self, config):
        # Update array type first
        index = self.array_type.findText(config['array_type'])
        if index >= 0:
            self.array_type.setCurrentIndex(index)
        
        # Update all sliders
        self.sliders['elements'].setValue(config['elements'])
        self.sliders['spacing'].setValue(config['spacing'])
        self.sliders['steering'].setValue(config['steering'])
        self.sliders['curvature'].setValue(config['curvature'])
        self.sliders['frequency'].setValue(config['frequency'])
        self.sliders['x_position'].setValue(config['x_position'])
        self.sliders['y_position'].setValue(config['y_position'])
    
    def _setup_array_type(self):
        self.grid_layout.addWidget(QLabel("Array Type:"), 0, 0)
        self.array_type = QComboBox()
        self.array_type.addItems(["Linear", "Curved"])
        self.grid_layout.addWidget(self.array_type, 0, 1)
    
    def _setup_sliders(self):
        slider_configs = {
            'elements': SliderConfig("Elements", 2, 100, 16, 1),
            'spacing': SliderConfig("Spacing (λ)", 0.1, 10.0, 0.5, 0.1),
            'steering': SliderConfig("Steering (°)", -90, 90, 0, 1),
            'curvature': SliderConfig("Curvature", 0.1, 5.0, 1.0, 0.1),
            'frequency': SliderConfig("Frequency (MHz)", 1, 1000, 300, 10),
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
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
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
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
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