import numpy as np

class BaseController:
    def __init__(self):
        self.speed_of_light = 3e8
        
    def _calculate_wavelength(self, frequency):
        if frequency <= 0:
            frequency = 1
        return self.speed_of_light / (frequency * 1e6)

    def _calculate_wavenumber(self, frequency):
        return 2 * np.pi / self._calculate_wavelength(frequency)

    def _convert_steering_angles(self, params_list):
        return [{**params, 'steering': np.deg2rad(params['steering'])} for params in params_list]