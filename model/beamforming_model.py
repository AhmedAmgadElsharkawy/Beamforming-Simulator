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


class ArrayStrategy:
    @staticmethod
    def calculate_linear_weights(wave_number, params, steering_angle):
        phase = (np.arange(params.elements) * params.spacing).reshape(-1, 1) 
        steering = np.asarray(steering_angle).reshape(1, -1)  
        return np.exp(-1j * wave_number * phase * np.sin(steering))

    @staticmethod
    def calculate_curved_weights(wave_number, params, steering_angle):
        elements = params.elements 
        distance, scale_factor = ArrayModel()._calculate_curved_params(elements, params.curvature) 
        theta = 2 * np.pi / elements * np.arange(elements) 
        x = (distance * scale_factor * np.cos(theta)).reshape(-1, 1)
        y = (-distance * scale_factor * np.sin(theta)).reshape(-1, 1)
        steering = np.asarray(steering_angle).reshape(1, -1)
        return np.exp(1j * wave_number * (x * np.cos(steering) + y * np.sin(steering)))

class BeamformingModel:
    def __init__(self):
        self._array = ArrayModel()
        self._array_strategy = ArrayStrategy()
        self.base_controller = BaseController()
        self.magnitude_min = -60
        self.magnitude_max = 0

    def calculate_steering_vector(self, params, use_phase=False):
        wave_number = self.base_controller._calculate_wavenumber(params.frequency)
        phase = self._calculate_phase(params.phase, use_phase)
        
        if params.array_type == 'linear':
            return self.calculate_linear_steering_vector(wave_number, params, phase)
        return self.calculate_curved_steering_vector(wave_number, params, phase)

    def calculate_linear_steering_vector(self, wave_number, params, phase):
        x = np.arange(params.elements) * params.spacing
        array_phase = wave_number * x * np.sin(params.steering)
        position_phase = wave_number * (params.x_position * np.cos(params.steering) + 
                                    params.y_position * np.sin(params.steering))
        return np.exp(-1j * (array_phase + position_phase + phase))
    
    def calculate_curved_steering_vector(self, wave_number, params, phase):
        distance, scale_factor = self._array._calculate_curved_params(params.elements, params.curvature)
        x = distance * scale_factor * np.cos(2 * np.pi / params.elements * np.arange(params.elements)) + params.x_position
        y = -distance * scale_factor * np.sin(2 * np.pi / params.elements * np.arange(params.elements)) + params.y_position
        steering_vector = np.exp(1j * wave_number * (x * np.cos(params.steering) + y * np.sin(params.steering)))
        return steering_vector.reshape(-1, 1) * np.exp(1j * phase)
    
    def calculate_weights(self, params, steering_angle):
        wave_number = self.base_controller._calculate_wavenumber(params.frequency)
        if params.array_type == 'linear':
            return self._array_strategy.calculate_linear_weights(wave_number, params, steering_angle)
        return self._array_strategy.calculate_curved_weights(wave_number, params, steering_angle)

    def calculate_pattern(self, params, angles, use_phase):
        array_factor = self._calculate_array_factor(params, angles, use_phase)
        return self._normalize_pattern(array_factor)

    def calculate_interference_pattern(self, params):
        grid = self._setup_interference_grid()
        params = BeamformingParameters(**params[0])
        steering_angles = np.arctan2(grid['Y'], grid['X'])
        array_factor = self._calculate_array_factor(params, steering_angles.reshape(-1), False)
        return self._normalize_pattern(array_factor.reshape(grid['X'].shape))

    def _calculate_array_factor(self, params, steering_angle, use_phase):
        steering_vector = self.calculate_steering_vector(params, use_phase).reshape(-1, 1)
        weights = self.calculate_weights(params, steering_angle)
        return np.sum(weights.conj() * steering_vector, axis=0)

    def _calculate_phase(self, phase, use_phase=True):
        return np.deg2rad(phase) if use_phase else 0
    
    def _setup_interference_grid(self):
        x = np.linspace(-10, 10, 200)
        y = np.linspace(-10, 10, 200)
        X, Y = np.meshgrid(x, y)
        return {'X': X, 'Y': Y}

    def _normalize_pattern(self, pattern):
        normalized = 20 * np.log10(np.abs(pattern))
        normalized = normalized - np.max(normalized)
        return np.clip(normalized, self.magnitude_min, self.magnitude_max)