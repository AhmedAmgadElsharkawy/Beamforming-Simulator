from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
import numpy as np
from controller.visualization_controller import VisualizationController
from view.visualization_panel import VisualizationPanel
from view.control_panel import ControlPanel

class BeamformingSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Beamforming Simulator")
        
        # Initialize visualization components
        self.visualization_panel = VisualizationPanel()
        self.visualization_controller = VisualizationController()
        
        # Setup UI
        self._init_ui()
        self._apply_stylesheet()
        self.update_plots()

    def _init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Setup visualization panel
        layout.addWidget(self.visualization_panel, stretch=2)
        
        # Setup control panel
        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel, stretch=1)
        
        # Connect signals
        self.control_panel.array_type.currentTextChanged.connect(self._toggle_parameters)
        for slider in [
            self.control_panel.elements,
            self.control_panel.spacing,
            self.control_panel.steering,
            self.control_panel.curvature,
            self.control_panel.frequency,
            self.control_panel.x_position,
            self.control_panel.y_position
        ]:
            slider.slider.valueChanged.connect(self.update_plots)

    def _toggle_parameters(self, array_type):
        is_curved = array_type == "Curved"
        self.control_panel.curvature.setEnabled(is_curved)
        self.control_panel.spacing.setEnabled(not is_curved)
        self.update_plots()

    def update_plots(self):
        params = {
            'elements': self.control_panel.elements.value(),
            'spacing': self.control_panel.spacing.value(),
            'steering': self.control_panel.steering.value(),
            'array_type': self.control_panel.array_type.currentText().lower(),
            'curvature': self.control_panel.curvature.value(),
            'frequency': self.control_panel.frequency.value(),
            'x_position': self.control_panel.x_position.value(),
            'y_position': self.control_panel.y_position.value(),
            'phase': 0
        }
        
        self.visualization_panel.clear_all_plots()
        self.visualization_panel.update_plots([params], self.visualization_controller)
        self.visualization_panel.refresh_all_canvases()

    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
                font-family: 'Arial', sans-serif;
            }
        """)

