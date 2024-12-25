from dataclasses import dataclass
import numpy as np

@dataclass
class ArrayParameters:
    elements: int
    steering: float
    phase: float
    frequency: float
    spacing: float
    array_type: str
    x_position: float
    y_position: float
    curvature: float

@dataclass
class ArrayPositions:
    x: np.ndarray
    y: np.ndarray
    
    def __post_init__(self):
        self.x = np.nan_to_num(self.x, nan=0.0, posinf=0.0, neginf=0.0)
        self.y = np.nan_to_num(self.y, nan=0.0, posinf=0.0, neginf=0.0)

class ArrayModel:
    def __init__(self):
        self._params = None
    
    @classmethod
    def _process_parameters(cls, params):
        return ArrayParameters(**params) if isinstance(params, dict) else params
    
    def calculate_positions(self, params):
        self._params = self._process_parameters(params)
        return self._calculate_array_positions()
    
    def _create_zero_array(self):
        return ArrayPositions(
            x=np.zeros(self._params.elements),
            y=np.zeros(self._params.elements)
        )
    
    def _apply_position_offset(self, x, y):
        return ArrayPositions(
            x=x + self._params.x_position,
            y=y + self._params.y_position
        )
    
    def _calculate_array_positions(self):
        if self._params.elements <= 0:
            return ArrayPositions(x=np.array([]), y=np.array([]))
            
        return (self._calculate_linear_positions() 
                if self._params.array_type == 'linear' 
                else self._calculate_curved_positions())
    
    def _calculate_linear_positions(self):
        x = np.arange(self._params.elements) * self._params.spacing
        y = np.zeros_like(x)
        return self._apply_position_offset(x, y)
    
    def _calculate_curved_positions(self):
        distance, scale_factor = self._calculate_curved_params(self._params.elements, self._params.curvature)
        if distance == 0 and scale_factor == 0:
            return self._create_zero_array()
        
        angles = 2 * np.pi / self._params.elements * np.arange(self._params.elements)
        x = distance * scale_factor * np.cos(angles)
        y = -distance * scale_factor * np.sin(angles)
        return self._apply_position_offset(x, y)
    
    def _calculate_curved_params(self, elements, curvature):
        cos_term = np.cos(2*np.pi/elements)
        
        if abs(1 - cos_term) < 1e-10:
            return 0, 0
            
        distance = np.sqrt(2 * curvature**2 * (1 - cos_term))
        scale_factor = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - cos_term))
        return distance, scale_factor
