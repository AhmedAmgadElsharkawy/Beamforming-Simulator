import numpy as np

class BeamCalculator:
    """Handles beam pattern calculations"""
    
    @staticmethod
    def calculate_steering_vector(params, use_phase=False):
        elements = params['elements']
        spacing = params['spacing']
        steering = params['steering']
        array_type = params['array_type']
        radius = params['curvature']
        frequency = params['frequency']
        x_pos = params['x_position']
        y_pos = params['y_position']
        phase = np.deg2rad(params['phase']) if use_phase else 0

        wavelength = 3e8 / (frequency * 1e6)
        k = 2 * np.pi / wavelength

        if array_type == 'linear':
            d = spacing
            array_phase = k * d * np.arange(elements) * np.sin(steering)
            position_phase = k * (x_pos * np.cos(steering) + y_pos * np.sin(steering))
            return np.exp(-1j * (array_phase + position_phase + phase))
        else:
            d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/elements)))
            sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/elements)))
            x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements)) + x_pos
            y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements)) + y_pos
            s = np.exp(1j * k * (x * np.cos(steering) + y * np.sin(steering)))
            return s.reshape(-1, 1) * np.exp(1j * phase)
