from .beam_pattern_controller import BeamPatternController
from .array_geometry_controller import ArrayGeometryController
from .interference_controller import InterferenceController

class VisualizationController:
    def __init__(self):
        self.beam_visualizer = BeamPatternController()
        self.array_visualizer = ArrayGeometryController()
        self.interference_visualizer = InterferenceController()
        self.beam_ax = None
        self.top_xy_ax = None 
        self.interference_ax = None
        self.bottom_xy_ax = None
        
    def update_plots(self, params_list):
        self.beam_visualizer.plot_rectangular_beam(self.beam_ax, params_list)
        self.array_visualizer.plot_array_geometry(self.top_xy_ax, params_list)
        self.interference_visualizer.plot_interference(self.interference_ax, params_list)
        self.beam_visualizer.plot_polar_beam(self.bottom_xy_ax, params_list)