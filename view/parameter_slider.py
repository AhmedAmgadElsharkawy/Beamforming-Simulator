from dataclasses import dataclass
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt

@dataclass
class SliderConfig:
    label: str
    min_val: float
    max_val: float
    default_val: float
    step: float = 1.0

class ParameterSlider(QWidget):
    def __init__(self, config: SliderConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self._init_ui()
        self._apply_styling()
    
    def _init_ui(self):
        self._setup_layout()
        self._setup_label()
        self._setup_slider()
        self._update_label(self.slider.value())
    
    def _setup_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
    
    def _setup_label(self):
        self.value_label = QLabel()
        self.layout.addWidget(self.value_label)
    
    def _setup_slider(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(self.config.min_val * (1/self.config.step)))
        self.slider.setMaximum(int(self.config.max_val * (1/self.config.step)))
        self.slider.setValue(int(self.config.default_val * (1/self.config.step)))
        self.slider.valueChanged.connect(self._update_label)
        self.layout.addWidget(self.slider)
    
    def _update_label(self, value):
        actual_value = value * self.config.step
        formatted_value = self._format_value(actual_value)
        self.value_label.setText(f"{self.config.label}: {formatted_value}")
    
    def _format_value(self, value):
        if "Frequency" in self.config.label or "Elements" in self.config.label:
            return f"{int(value)}"
        
        if self.config.step >= 1:
            return f"{value:.0f}"
        elif self.config.step >= 0.1:
            return f"{value:.1f}"
        elif self.config.step >= 0.01:
            return f"{value:.2f}"
        return f"{value:.3f}"
    
    def value(self):
        return self.slider.value() * self.config.step
    
    def setValue(self, value):
        self.slider.setValue(int(value * (1/self.config.step)))
    
    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.slider.setEnabled(enabled)
        self.value_label.setEnabled(enabled)
    
    def _apply_styling(self):
        self.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 10pt;
            }
            QLabel:disabled {
                color: #6B7280;
            }
            QSlider {
                height: 24px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #4B5563;
                height: 4px;
                background: #374151;
                margin: 0px;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #2563EB;
                border: none;
                width: 18px;
                margin: -8px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #1D4ED8;
            }
            QSlider::handle:horizontal:disabled {
                background: #6B7280;
            }
            QSlider::groove:horizontal:disabled {
                background: #1F2937;
                border-color: #374151;
            }
        """)
