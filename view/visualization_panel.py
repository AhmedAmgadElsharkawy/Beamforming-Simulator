from dataclasses import dataclass
from PyQt5.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from controller.beam_pattern_controller import BeamPatternController
from controller.array_geometry_controller import ArrayGeometryController
from controller.interference_controller import InterferenceController
@dataclass
class PlotConfig:
    title: str
    position: tuple
    figsize: tuple
    adjustments: dict
    is_polar: bool = False

class VisualizationPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.beam_controller = BeamPatternController()
        self.array_geometry_controller = ArrayGeometryController()
        self.interference_controller = InterferenceController()
        self._init_layout()
        self._setup_plots()

    def _init_layout(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 10, 10, 10)
        self.layout.setColumnStretch(0, 4)
        self.layout.setColumnStretch(1, 5)

    def _setup_plots(self):
        plot_configs = {
            'beam': PlotConfig(
                "Rectangular Beam Pattern", 
                (0, 0), 
                (6, 3),
                {'left': 0.17, 'right': 0.95, 'top': 0.85, 'bottom': 0.15}
            ),
            'polar': PlotConfig(
                "Polar Beam Pattern", 
                (0, 1), 
                (7, 3.5),
                {'left': 0.05, 'right': 0.97, 'top': 0.90, 'bottom': 0.05},
                True
            ),
            'array': PlotConfig(
                "Array Geometry", 
                (1, 0), 
                (6, 3),
                {'left': 0.19, 'right': 0.95, 'top': 0.9, 'bottom': 0.15}
            ),
            'interference': PlotConfig(
                "Interference Pattern", 
                (1, 1), 
                (6, 3),
                {'left': 0.05, 'right': 0.97, 'top': 0.86, 'bottom': 0.05}
            )
        }
        
        self.figures = {}
        self.canvases = {}
        self.axes = {}
        
        for name, config in plot_configs.items():
            self._create_plot(name, config)

    def _create_plot(self, name: str, config: PlotConfig):
        self.figures[name] = plt.figure(figsize=config.figsize, facecolor='#111827')
        self.canvases[name] = FigureCanvas(self.figures[name])
        
        projection = 'polar' if config.is_polar else None
        self.axes[name] = self.figures[name].add_subplot(111, projection=projection)
        
        self.figures[name].subplots_adjust(**config.adjustments)
        self._configure_plot(self.axes[name])
        self.layout.addWidget(self.canvases[name], *config.position)

    def _configure_plot(self, ax):
        ax.set_facecolor('#111827')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

    def update_plots(self, params_list, controller):
        self.beam_controller.plot_rectangular_beam(self.axes['beam'], params_list)
        self.interference_controller.plot_interference(self.axes['interference'], params_list)
        self.beam_controller.plot_polar_beam(self.axes['polar'], params_list)
        self.array_geometry_controller.plot_array_geometry(self.axes['array'], params_list)
        self.refresh_all_canvases()

    def refresh_all_canvases(self):
        for canvas in self.canvases.values():
            canvas.draw()

    def clear_all_plots(self):
        for name, ax in self.axes.items():
            ax.clear()
            
            if name == 'interference':
                ax.set_xticks([])
                ax.set_yticks([])
            else:
                ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        
        self.refresh_all_canvases()
