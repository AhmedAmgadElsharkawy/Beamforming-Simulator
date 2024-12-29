from .base_controller import BaseController
import numpy as np
from model.beamforming_model import BeamformingModel, BeamformingParameters
from model.array_model import ArrayModel

class BeamPatternController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = BeamformingModel()
        self.array_model = ArrayModel()
        
        
    # def _setup_beam_plot_polar(self, params_list):
    #     # Calculate steering angles for curved array geometry
    #     distance, scale_factor = self.array_model.calculate_curved_params(params_list.elements, params_list.curvature)
    #     steering_angles = np.linspace(-np.pi/2, np.pi/2, 1000) * scale_factor
        
    #     converted_params = self.convert_steering_angles(params_list)
    #     params = BeamformingParameters(**converted_params[0])
    #     return steering_angles, self.model.calculate_pattern(params)

    # def plot_curved_beam(self, ax, params_list):
    #     ax.clear()
    #     steering_angles, beam_pattern = self._setup_beam_plot_polar(params_list)
    #     distance, scale_factor = self.array_model.calculate_curved_params(params_list.elements, params_list.curvature)
    #     # Adjust x-axis limits and tick values for curved array geometry
    #     ax.set_xlim(-10 * scale_factor, 10 * scale_factor)
    #     ax.plot(steering_angles*180/np.pi, beam_pattern)
    #     ax.set_xlabel('Theta [Degrees]', color='white')
    #     ax.set_ylabel('Beam Pattern [dB]', color='white')
    #     ax.set_xticks(np.arange(-90 * scale_factor, 91 * scale_factor, 20 * scale_factor))
    #     self._style_plot_axes(ax, 'Curved Beam Pattern')
        
    def _setup_beam_plot(self, params_list):
        steering_angles = np.linspace(-np.pi/2, np.pi/2, 1000) 
        converted_params = self.convert_steering_angles(params_list)
        params = BeamformingParameters(**converted_params[0])
        return steering_angles, self.model.calculate_pattern(params)
    
    def _style_plot_axes(self, ax, title, is_polar=False):
        ax.grid(True, color="gray")
        ax.tick_params(colors='white')
        ax.set_title(title, color='white', pad=23 if not is_polar else 10)
        
    def plot_rectangular_beam(self, ax, params_list):
        ax.clear()
        steering_angles, beam_pattern = self._setup_beam_plot(params_list) 
        
        ax.set_xlim(-10, 10)
        ax.plot(steering_angles*180/np.pi, beam_pattern)
        ax.set_xlabel('Theta [Degrees]', color='white')
        ax.set_ylabel('Beam Pattern [dB]', color='white')
        ax.set_xticks(np.arange(-90, 91, 20))
        self._style_plot_axes(ax, 'Rectangular Beam Pattern')
        
    def plot_polar_beam(self, ax, params_list):
        ax.clear()
        steering_angles, beam_pattern = self._setup_beam_plot(params_list)
        
        if hasattr(ax, 'set_theta_zero_location'):
            self._configure_polar_axes(ax)
            
        ax.plot(steering_angles, beam_pattern)
        self._style_plot_axes(ax, 'Polar Beam Pattern', is_polar=True)
        
    def _configure_polar_axes(self, ax):
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetamin(-90)
        ax.set_thetamax(90)
        ax.set_rmin(-60)
        ax.set_rmax(0)
        ax.set_rticks([-60, -50, -40, -30, -20, -10, 0])
        ax.set_rlabel_position(90)
        ax.text(-0.1, -30, 'dB', color='white')
