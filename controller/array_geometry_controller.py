from .base_controller import BaseController
import numpy as np
import matplotlib.pyplot as plt
from model.array_model import ArrayModel

class ArrayGeometryController(BaseController):
    def __init__(self):
        super().__init__()
        self.array_model = ArrayModel()
        
    def _style_plot_axes(self, ax, limit_x, limit_y):
        ax.set_aspect('equal')
        ax.grid(True, color='gray')
        ax.set_title('Array Configuration', color='white', pad=13)
        ax.set_xlabel('X Position (λ)', color='white')
        ax.set_ylabel('Y Position (λ)', color='white')
        ax.tick_params(colors='white')
        
        x_ticks = np.arange(-limit_x, limit_x + 1, max(1, int(limit_x // 2)))
        y_ticks = np.arange(-limit_y, limit_y + 1, max(1, int(limit_y // 2)))
        
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.set_xlim(-limit_x, limit_x)
        ax.set_ylim(-limit_y, limit_y)
        
    def _calculate_plot_limits(self, x_positions, y_positions):
        max_abs_x = max(abs(min(x_positions)), abs(max(x_positions)))
        max_abs_y = max(abs(min(y_positions)), abs(max(y_positions)))
        padding = 2
        return (int(np.ceil(max_abs_x + padding)), 
                int(np.ceil(max_abs_y + padding)))
    
    def _plot_array_scatter(self, ax, positions, array_id, colors):
        color_index = (array_id - 1) % 10
        ax.scatter(positions.x, positions.y,
                  color=colors[color_index],
                  label=f'Array {array_id}')
    
    def plot_array_geometry(self, ax, params_list):
        ax.clear()
        if not params_list:
            return
            
        colors = plt.cm.tab10(np.linspace(0, 1, 10))
        x_positions = []
        y_positions = []
        
        for params in params_list:
            positions = self.array_model.calculate_positions(params)
            x_positions.extend(positions.x)
            y_positions.extend(positions.y)
            
            array_id = params.get("id", 1)
            self._plot_array_scatter(ax, positions, array_id, colors)
        
        limit_x, limit_y = self._calculate_plot_limits(x_positions, y_positions)
        self._style_plot_axes(ax, limit_x, limit_y)
        ax.legend(labelcolor='#1E293B', bbox_to_anchor=(1, 1.07), loc='upper right', fontsize=8)