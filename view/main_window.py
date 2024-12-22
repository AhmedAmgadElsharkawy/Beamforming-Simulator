from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from dataclasses import dataclass
from controller.visualization_controller import VisualizationController
from .visualization_panel import VisualizationPanel
from .parameter_panel import ParameterPanel

@dataclass
class SimulationParameters:
    elements: float
    spacing: float
    steering: float
    array_type: str
    curvature: float
    frequency: float
    x_position: float
    y_position: float
    phase: float = 0

class BeamformingSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Beamforming Simulator")
        self._init_components()
        self._setup_ui()
        self._connect_signals()
        self._apply_styling()
        self.update_plots()

    def _init_components(self):
        self.visualization_panel = VisualizationPanel()
        self.visualization_controller = VisualizationController()
        self.parameter_panel = ParameterPanel()

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.addWidget(self.visualization_panel, stretch=2)
        layout.addWidget(self.parameter_panel, stretch=1)

    def _connect_signals(self):
        self.parameter_panel.array_type.currentTextChanged.connect(self._toggle_parameters)
        self._connect_slider_signals()

    def _connect_slider_signals(self):
        sliders = [
            self.parameter_panel.elements,
            self.parameter_panel.spacing,
            self.parameter_panel.steering,
            self.parameter_panel.curvature,
            self.parameter_panel.frequency,
            self.parameter_panel.x_position,
            self.parameter_panel.y_position
        ]
        for slider in sliders:
            slider.slider.valueChanged.connect(self.update_plots)

    def _toggle_parameters(self, array_type: str):
        is_curved = array_type == "Curved"
        self.parameter_panel.curvature.setEnabled(is_curved)
        self.parameter_panel.spacing.setEnabled(not is_curved)
        self.update_plots()

    def update_plots(self):
        params = SimulationParameters(
            elements=self.parameter_panel.elements.value(),
            spacing=self.parameter_panel.spacing.value(),
            steering=self.parameter_panel.steering.value(),
            array_type=self.parameter_panel.array_type.currentText().lower(),
            curvature=self.parameter_panel.curvature.value(),
            frequency=self.parameter_panel.frequency.value(),
            x_position=self.parameter_panel.x_position.value(),
            y_position=self.parameter_panel.y_position.value(),
            phase=0
        )
        
        self._update_visualization(params)

    def _update_visualization(self, params: SimulationParameters):
        self.visualization_panel.clear_all_plots()
        self.visualization_panel.update_plots([vars(params)], self.visualization_controller)
        self.visualization_panel.refresh_all_canvases()

    def _apply_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
                font-family: 'Arial', sans-serif;
            }
        """)
