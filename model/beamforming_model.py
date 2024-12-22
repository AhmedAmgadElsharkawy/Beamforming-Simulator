from dataclasses import dataclass
import numpy as np
from typing import Dict, Tuple, Optional
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
        phase = wave_number * params.spacing * np.arange(params.elements) * np.sin(steering_angle)
        return np.exp(-1j * phase)

    @staticmethod
    def calculate_curved_weights(wave_number, params, steering_angle):
        distance, scale_factor = BeamformingModel._get_curved_params(params.elements, params.curvature)
        x = distance * scale_factor * np.cos(2 * np.pi / params.elements * np.arange(params.elements))
        y = -1 * distance * scale_factor * np.sin(2 * np.pi / params.elements * np.arange(params.elements))
        return np.exp(1j * wave_number * (x * np.cos(steering_angle) + y * np.sin(steering_angle)))

class BeamformingModel:
    def __init__(self, array_model):
        self._array = array_model
        self._array_strategy = ArrayStrategy()
        self.base_controller = BaseController()
        self._weights_cache = {}
        self._wavenumber_cache = {}
        self._curved_params_cache = {}
        self.magnitude_min = -60
        self.magnitude_max = 0

    def _get_wavenumber(self, frequency):
        if frequency not in self._wavenumber_cache:
            self._wavenumber_cache[frequency] = self.base_controller._calculate_wavenumber(frequency)
        return self._wavenumber_cache[frequency]

    def _get_curved_params(self, elements, curvature):
        key = (elements, curvature)
        if key not in self._curved_params_cache:
            self._curved_params_cache[key] = ArrayModel._calculate_curved_params(elements, curvature)
        return self._curved_params_cache[key]
    
    def calculate_steering_vector(self, params, use_phase = False):
        cache_key = (params.frequency, params.spacing, params.steering, params.elements, 
                    params.array_type, params.curvature, params.x_position, params.y_position, 
                    params.phase, use_phase)
        
        steering_cache = self._init_cache('_steering_cache')
        if cache_key in steering_cache:
            return steering_cache[cache_key]
            
        wave_number = self._get_wavenumber(params.frequency)
        phase = self._calculate_phase(params.phase, use_phase)
        
        result = (self._calculate_linear_steering_vector(wave_number, params, phase) 
                if params.array_type == 'linear' 
                else self._calculate_curved_steering_vector(wave_number, params, phase))
                
        steering_cache[cache_key] = result
        return result
    
    def _calculate_linear_steering_vector(self, wave_number, params, phase):
        array_phase = wave_number * params.spacing * np.arange(params.elements) * np.sin(params.steering)
        position_phase = wave_number * (params.x_position * np.cos(params.steering) + 
                            params.y_position * np.sin(params.steering))
        return np.exp(-1j * (array_phase + position_phase + phase))
    
    def _calculate_curved_steering_vector(self, wave_number, params, phase):
        distance, scale_factor = self._get_curved_params(params.elements, params.curvature)
        x = distance * scale_factor * np.cos(2 * np.pi / params.elements * np.arange(params.elements)) + params.x_position
        y = -1 * distance * scale_factor * np.sin(2 * np.pi / params.elements * np.arange(params.elements)) + params.y_position
        s = np.exp(1j * wave_number * (x * np.cos(params.steering) + y * np.sin(params.steering)))
        return s.reshape(-1, 1) * np.exp(1j * phase)

    def calculate_weights(self, params, steering_angle):
        # Create cache key from relevant parameters
        cache_key = (params.elements, params.spacing, params.array_type, 
                    params.curvature, params.frequency, steering_angle)
        
        # Return cached result if available
        if cache_key in self._weights_cache:
            return self._weights_cache[cache_key]
            
        # Calculate if not in cache
        wave_number = self.base_controller._calculate_wavenumber(params.frequency)
        if params.array_type == 'linear':
            weights = self._array_strategy.calculate_linear_weights(wave_number, params, steering_angle)
        else:
            weights = self._array_strategy.calculate_curved_weights(wave_number, params, steering_angle)
            
        # Store in cache
        self._weights_cache[cache_key] = weights
        return weights
    
    def _normalize_pattern(self, pattern):
        normalized = 20 * np.log10(np.abs(pattern))
        normalized = normalized - np.max(normalized)
        return np.clip(normalized, self.magnitude_min, self.magnitude_max)

    def calculate_pattern(self, params, angles, use_phase):
        cache_key = (params.frequency, params.spacing, params.steering,
                    params.elements, params.phase, use_phase, tuple(angles))
        
        pattern_cache = self._init_cache('_pattern_cache')
        if cache_key in pattern_cache:
            return pattern_cache[cache_key]
        
        wave_number = self._get_wavenumber(params.frequency)
        array_factor = self._calculate_vectorized_array_factor(params, angles, wave_number)
        pattern = self._normalize_pattern(array_factor)
        
        pattern_cache[cache_key] = pattern
        return pattern

    def calculate_interference_pattern(self, params):
        grid = self._setup_interference_grid()
        return self._calculate_interference_factors(grid, params)
    
    def _setup_interference_grid(self):
        x = np.linspace(-10, 10, 200)
        y = np.linspace(-10, 10, 200)
        X, Y = np.meshgrid(x, y)
        return {'X': X, 'Y': Y}
    
    
    def _calculate_interference_factors(self, grid, params):
        params = BeamformingParameters(**params[0])
        
        cache_key = (params.elements, params.spacing, params.steering,
                    params.frequency, params.phase,
                    grid['X'].tobytes(), grid['Y'].tobytes())
                    
        interference_cache = self._init_cache('_interference_cache')
        if cache_key in interference_cache:
            return interference_cache[cache_key]
        
        wave_number = self._get_wavenumber(params.frequency)
        steering_angle_ij = np.arctan2(grid['Y'], grid['X'])
        array_factor = self._calculate_vectorized_array_factor(params, steering_angle_ij, wave_number)
        result = self._normalize_pattern(array_factor)
        
        interference_cache[cache_key] = result
        return result
    
    def _calculate_vectorized_array_factor(self, params, steering_angle, wave_number):
        phase_diff = self._calculate_phase_difference(wave_number, params)
        element_phase = self._calculate_phase(params.phase)
        
        # Handle different input shapes for pattern vs interference
        if steering_angle.ndim == 1:
            n_array = np.arange(params.elements)[:, np.newaxis]
            steering_angle = steering_angle[np.newaxis, :]
        else:
            n_array = np.arange(params.elements)[:, np.newaxis, np.newaxis]
            steering_angle = steering_angle[np.newaxis, :, :]
        
        array_factor = self._calculate_array_factor(wave_number, params.spacing, n_array, steering_angle, phase_diff, element_phase)
        return array_factor / params.elements
    
    def _calculate_array_factor(self, wave_number, spacing, n_array,
        steering_angle, phase_diff,
        element_phase):
        return np.sum(np.exp(1j * (wave_number * spacing * n_array * np.sin(steering_angle) +
             n_array * phase_diff + element_phase)), axis=0)

    def _init_cache(self, cache_name):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, {})
        return getattr(self, cache_name)
    
    def _calculate_phase(self, phase, use_phase = True):
        return np.deg2rad(phase) if use_phase else 0
    
    def _calculate_phase_difference(self, wave_number, params):
        return -wave_number * params.spacing * np.sin(params.steering)






