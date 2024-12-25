from .base_controller import BaseController
import numpy as np
import matplotlib.pyplot as plt
from model.beamforming_model import BeamformingModel

class InterferenceController(BaseController):
    def __init__(self):
        super().__init__()
        self.magnitude_min = -60
        self.magnitude_max = 0
        self.model = BeamformingModel()

    def _create_colorbar(self, fig, ax, im):
        cax = fig.add_axes([0.92, 0.1, 0.03, 0.8])
        cax.set_label('colorbar')
        cbar = fig.colorbar(im, cax=cax)
        self._style_colorbar(cbar)
        return cbar

    def _style_colorbar(self, cbar):
        tick_values = np.linspace(self.magnitude_min, self.magnitude_max, 7)
        cbar.set_ticks(tick_values)
        cbar.set_ticklabels([f'{val:.0f}' for val in tick_values], fontsize=8)
        cbar.ax.tick_params(colors='white', pad=0)
        cbar.ax.yaxis.set_label_position('right')
        cbar.set_label('dB', color='white', rotation=0, labelpad=-5, y=1.08)

    def _setup_interference_plot(self, ax, masked_pattern):
        circle = plt.Circle((0, 0), 10, transform=ax.transData)
        im = ax.imshow(masked_pattern, 
                    extent=[-10, 10, -10, 10],
                    origin='lower', 
                    cmap='coolwarm',
                    vmin=self.magnitude_min,
                    vmax=self.magnitude_max,  # Set to 0 to match pattern scaling
                    clip_path=circle)
        return im

    def _add_interference_labels(self, ax):
        ax.text(8, 10.5, 'Constructive\nInterference', color='white', fontsize=8)
        ax.text(8, -9.7, 'Destructive\nInterference', color='white', fontsize=8)

    def _clear_existing_colorbars(self, fig, ax):
        for cbar in fig.get_axes():
            if cbar is not ax and isinstance(cbar, plt.Axes):
                if cbar.get_label() == 'colorbar':
                    cbar.remove()

    def plot_interference(self, ax, params_list):
        ax.clear()
        fig = ax.figure
        
        self._clear_existing_colorbars(fig, ax)
        
        converted_params = self._convert_steering_angles(params_list)
        interference_pattern = self.model.calculate_interference_pattern(converted_params)
        masked_pattern = self._apply_circular_mask(interference_pattern)
        masked_pattern = np.rot90(masked_pattern)
        
        im = self._setup_interference_plot(ax, masked_pattern)
        self._create_colorbar(fig, ax, im)
        
        ax.set_frame_on(False)
        ax.set_aspect('equal')
        
        self._add_interference_labels(ax)
        ax.set_title('Interference Map', color='white', pad=21)
        ax.set_xticks([])
        ax.set_yticks([])
        
    def _apply_circular_mask(self, pattern):
        ny, nx = pattern.shape
        y, x = np.ogrid[-ny//2:ny//2, -nx//2:nx//2]
        
        circle = x*x + y*y <= (min(nx, ny)//2)**2
        top_half = x <= 0
        mask = circle & top_half
        
        return np.ma.array(pattern, mask=~mask)
