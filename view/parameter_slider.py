from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt

class ParameterSlider(QWidget):
    def __init__(self, label, min_val, max_val, default_val, step=1, parent=None):
        super().__init__(parent)
        self.step = step
        self.label_text = label
        self._init_ui(label, min_val, max_val, default_val)

    def _init_ui(self, label, min_val, max_val, default_val):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label with current value
        self.value_label = QLabel()
        layout.addWidget(self.value_label)
        
        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(min_val * (1/self.step)))
        self.slider.setMaximum(int(max_val * (1/self.step)))
        self.slider.setValue(int(default_val * (1/self.step)))
        self.slider.valueChanged.connect(self._update_label)
        layout.addWidget(self.slider)
        
        # Set initial label value
        self._update_label(self.slider.value())
        
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

    def _update_label(self, value):
        actual_value = value * self.step
        
        # Determine number of decimal places based on step size
        if self.step >= 1:
            formatted_value = f"{actual_value:.0f}"
        elif self.step >= 0.1:
            formatted_value = f"{actual_value:.1f}"
        elif self.step >= 0.01:
            formatted_value = f"{actual_value:.2f}"
        else:
            formatted_value = f"{actual_value:.3f}"
        
        # Special formatting for specific parameters
        if "Frequency" in self.label_text:
            formatted_value = f"{int(actual_value)}"  
        elif "Elements" in self.label_text:
            formatted_value = f"{int(actual_value)}"  
        
        self.value_label.setText(f"{self.label_text}: {formatted_value}")

    def value(self):
        return self.slider.value() * self.step

    def setValue(self, value):
        self.slider.setValue(int(value * (1/self.step)))

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.slider.setEnabled(enabled)
        self.value_label.setEnabled(enabled)