from PyQt5.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class VisualizationPanel(QWidget):
    """Manages all visualization plots in the application"""
    
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._setup_plots()

    def _init_layout(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 10, 10, 10)  # Increased left margin to 50
    
        # Set column stretches to control width distribution
        self.layout.setColumnStretch(0, 4)  # Left column
        self.layout.setColumnStretch(1, 5)  # Right column

    def _setup_plots(self):
        # Rectangular beam pattern (top left)
        self.beam_figure = plt.figure(figsize=(6, 3), facecolor='#111827')
        self.beam_canvas = FigureCanvas(self.beam_figure)
        self.beam_ax = self.beam_figure.add_subplot(111)
        self.beam_figure.subplots_adjust(left=0.17, right=0.95, top=0.85, bottom=0.15)
        self._configure_plot(self.beam_ax)
        self.layout.addWidget(self.beam_canvas, 0, 0)

        # Polar beam pattern (top right)
        self.bottom_xy_figure = plt.figure(figsize=(7, 3.5), facecolor='#111827')
        self.bottom_xy_canvas = FigureCanvas(self.bottom_xy_figure)
        self.bottom_xy_ax = self.bottom_xy_figure.add_subplot(111, projection='polar')
        self.bottom_xy_figure.subplots_adjust(left=0.05, right=0.97, top=0.90, bottom=0.05)
        self._configure_plot(self.bottom_xy_ax)
        self.layout.addWidget(self.bottom_xy_canvas, 0, 1)

        # Array geometry (bottom left)
        self.top_xy_figure = plt.figure(figsize=(6, 3), facecolor='#111827')
        self.top_xy_canvas = FigureCanvas(self.top_xy_figure)
        self.top_xy_ax = self.top_xy_figure.add_subplot(111)
        self.top_xy_figure.subplots_adjust(left=0.19, right=0.95, top=0.9, bottom=0.15)
        self._configure_plot(self.top_xy_ax)
        self.layout.addWidget(self.top_xy_canvas, 1, 0)

        # Interference map (bottom right)
        self.interference_figure = plt.figure(figsize=(6, 3), facecolor='#111827')
        self.interference_canvas = FigureCanvas(self.interference_figure)
        self.interference_ax = self.interference_figure.add_subplot(111)
        self.interference_figure.subplots_adjust(left=0.05, right=0.97, top=0.86, bottom=0.05)
        self._configure_plot(self.interference_ax)
        self.layout.addWidget(self.interference_canvas, 1, 1)

    def _configure_plot(self, ax):
        ax.set_facecolor('#111827')
        ax.tick_params(colors='white')
        # Add these lines to set label colors
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        # Set title color to white
        ax.title.set_color('white')

    def update_plots(self, params_list, controller):
        controller.plot_rectangular_beam(self.beam_ax, params_list)
        controller.plot_interference(self.interference_ax, params_list)
        controller.plot_beam_pattern(self.bottom_xy_ax, params_list)
        controller.plot_array_geometry(self.top_xy_ax, params_list)
        self.refresh_all_canvases()


    def refresh_all_canvases(self):
        self.beam_canvas.draw()
        self.bottom_xy_canvas.draw()
        self.interference_canvas.draw()
        self.top_xy_canvas.draw()

    def clear_all_plots(self):
        # Clear all axes
        self.beam_ax.clear()
        self.top_xy_ax.clear()
        self.interference_ax.clear()
        self.bottom_xy_ax.clear()
        
        # Remove all ticks and labels
        self.interference_ax.set_xticks([])
        self.interference_ax.set_yticks([])
        
        # Restore grids for plots that need them
        self.top_xy_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.bottom_xy_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.beam_ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        
        # Refresh to show changes
        self.refresh_all_canvases()