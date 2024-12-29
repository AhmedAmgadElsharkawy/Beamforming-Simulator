from dataclasses import dataclass
import numpy as np
from model.array_model import ArrayModel
from controller.base_controller import BaseController

@dataclass
class BeamformingParameters:
    elements: int
    spacing: float
    steering: float
    array_type: str
    curvature: float
    frequency: float
    phase: float
    x_position: float = 0
    y_position: float = 0

class BeamformingModel:
    def __init__(self):
        self.array_model = ArrayModel()
        self.base_controller = BaseController()
        self.magnitude_min = -60
        self.magnitude_max = 0
        
    def calculate_pattern(self, params):
        steering_angle = np.linspace(-np.pi/2, np.pi/2, 1000) 
        array_factor = self._calculate_steering_vector(params, steering_angle)
        pattern = np.sum(array_factor, axis=0)
        return self._normalize_pattern(pattern)

    def calculate_interference_map(self, params):
        grid = self._setup_interference_grid()
        params = BeamformingParameters(**params[0])
        steering_angles = np.arctan2(grid['Y'], grid['X']) 
        array_factor = self._calculate_steering_vector(params, steering_angles.flatten()) 
        array_factor = np.sum(array_factor, axis=0)
        return self._normalize_pattern(array_factor.reshape(grid['X'].shape))

    def _calculate_steering_vector(self, params, steering_angle):
        if params.array_type == 'linear':
            steering_vector = self._calculate_linear_steering_vector(params, steering_angle)
        else:
            steering_vector = self._calculate_curved_steering_vector(params, steering_angle)
        if steering_vector.ndim == 1:
            steering_vector = steering_vector.reshape(-1, 1)
        return steering_vector

    def _calculate_linear_steering_vector(self, params, steering_angle):
        elements = params.elements
        spacing = params.spacing / self.base_controller._calculate_wavelength(params.frequency)
        element_positions = (np.arange(elements) * spacing)[:, np.newaxis]
        steering_angle = np.asarray(steering_angle) - params.steering
        steering_vector = np.exp(-2j * np.pi * element_positions * np.sin(steering_angle))
        return steering_vector
    
    def _calculate_curved_steering_vector(self, params, steering_angle):
        elements = params.elements 
        radius = params.curvature / self.base_controller._calculate_wavelength(params.frequency)
        distance, scale_factor = self.array_model.calculate_curved_params(elements, radius) 
        theta = 2 * np.pi / elements * np.arange(elements) 
        x = ((distance * scale_factor * np.cos(theta))) [:, np.newaxis]  
        y = ((-distance * scale_factor * np.sin(theta))) [:, np.newaxis]
        steering_angle = np.asarray(steering_angle) - params.steering
        steering_vector = np.exp(1j * 2 * np.pi * (x * np.cos(steering_angle) + y * np.sin(steering_angle)))
        return steering_vector
                
    def _normalize_pattern(self, pattern):
        normalized = 28 * np.log10(np.abs(pattern))
        normalized = normalized - np.max(normalized)
        return np.clip(normalized, self.magnitude_min, self.magnitude_max)
    
    def _setup_interference_grid(self):
        x = np.linspace(-10, 10, 200)
        y = np.linspace(-10, 10, 200)
        X, Y = np.meshgrid(x, y)
        return {'X': X, 'Y': Y}
    