import numpy as np
import matplotlib.pyplot as plt

class VisualizationController:
    def __init__(self, beam_ax=None, top_xy_ax=None, interference_ax=None, bottom_xy_ax=None):
        self.c = 3e8  # Speed of light
        self.array_controller = None
        self.beam_ax = beam_ax
        self.top_xy_ax = top_xy_ax
        self.interference_ax = interference_ax
        self.bottom_xy_ax = bottom_xy_ax

    def _calculate_wavelength(self, frequency):
        return self.c / (frequency * 1e6)

    def _calculate_wavenumber(self, frequency):
        return 2 * np.pi / self._calculate_wavelength(frequency)

    def _calculate_curved_array_params(self, elements, radius):
        if elements <= 0:
            return 0, 0
            
        cos_term = np.cos(2*np.pi/elements)
        if abs(1 - cos_term) < 1e-10:
            return 0, 0
            
        d = np.sqrt(2 * radius**2 * (1 - cos_term))
        sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - cos_term))
        
        return d, sf
    
    def _calculate_array_positions(self, params):
        elements = params['elements']
        if elements <= 0:
            return {'x': np.array([]), 'y': np.array([])}
            
        spacing = params['spacing']
        array_type = params['array_type']
        
        if array_type == 'linear':
            x = np.arange(elements) * spacing + params['x_position']
            y = np.zeros_like(x) + params['y_position']
        else:
            d, sf = self._calculate_curved_array_params(elements, params['curvature'])
            if d == 0 and sf == 0:
                return {'x': np.zeros(elements), 'y': np.zeros(elements)}
                
            angle_array = 2 * np.pi / elements * np.arange(elements)
            x_base = d * sf * np.cos(angle_array)
            y_base = -1 * d * sf * np.sin(angle_array)
            x = x_base + params['x_position']
            y = y_base + params['y_position']
        
        return {'x': x, 'y': y}
    
    def _calculate_interference_pattern(self, params_list):
        x = np.linspace(-10, 10, 200)
        y = np.linspace(-10, 10, 200)
        X, Y = np.meshgrid(x, y)
        Z_total = np.zeros_like(X)

        for params in params_list:
            Z = np.zeros_like(X)
            N = params['elements']
            d = params['spacing']
            k = 2 * np.pi / (3e8 / params['frequency'] / 1e6)
            steering = params['steering']
            element_phase = np.deg2rad(params['phase'])  # Added phase consideration
            
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    theta_ij = np.arctan2(Y[i,j], X[i,j])
                    array_factor = np.zeros(1, dtype=complex)
                    phase_diff = -k * d * np.sin(steering)
                    
                    for n in range(N):
                        total_phase = n * phase_diff + element_phase  # Combined phase
                        array_factor += np.exp(1j * (k * d * n * np.sin(theta_ij) + total_phase))
                    
                    Z[i,j] = 20 * np.log10(np.abs(array_factor) / N)
            
            Z_total += Z

        Z_total = np.clip(Z_total, self.magnitude_min, self.magnitude_max)
        return Z_total
    
    def _apply_circular_mask(self, pattern):
        ny, nx = pattern.shape
        y, x = np.ogrid[-ny//2:ny//2, -nx//2:nx//2]
        
        # Create circular mask
        circle = x*x + y*y <= (min(nx, ny)//2)**2
        
        # Create top half mask
        top_half = x <= 0
        
        # Combine masks to get top half circle
        mask = circle & top_half
        
        masked_pattern = np.ma.array(pattern, mask=~mask)
        return masked_pattern

    def calculate_steering_vector(self, params, use_phase=False):
        elements = params['elements']
        spacing = params['spacing']
        steering = params['steering']
        array_type = params['array_type']
        radius = params['curvature']
        k = self._calculate_wavenumber(params['frequency'])
        phase = np.deg2rad(params['phase']) if use_phase else 0
        
        if array_type == 'linear':
            array_phase = k * spacing * np.arange(elements) * np.sin(steering)
            position_phase = k * (params['x_position'] * np.cos(steering) + 
                                params['y_position'] * np.sin(steering))
            return np.exp(-1j * (array_phase + position_phase + phase))
        else:
            d, sf = self._calculate_curved_array_params(elements, radius)
            x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements)) + params['x_position']
            y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements)) + params['y_position']
            s = np.exp(1j * k * (x * np.cos(steering) + y * np.sin(steering)))
            return s.reshape(-1, 1) * np.exp(1j * phase)

    def _calculate_array_weights(self, params, theta, k):
        elements = params['elements']
        if params['array_type'] == 'linear':
            phase = k * params['spacing'] * np.arange(elements) * np.sin(theta)
            return np.exp(-1j * phase)
        else:
            d, sf = self._calculate_curved_array_params(elements, params['curvature'])
            x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements))
            y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements))
            return np.exp(1j * k * (x * np.cos(theta) + y * np.sin(theta)))

    def _calculate_beam_pattern(self, params, angles, use_phase):
        k = self._calculate_wavenumber(params['frequency'])
        results = np.zeros_like(angles)
        
        for i, theta in enumerate(angles):
            w = self._calculate_array_weights(params, theta, k)
            s = self.calculate_steering_vector(params, True)  # Always consider phase
            results[i] = np.abs(np.dot(w.conj(), s.flatten()))**2
            
        return results

    def _process_combined_results(self, results):
        processed = 10 * np.log10(results)
        return processed - np.max(processed)
    
    def _convert_steering_angles(self, params_list):
        return [{**params, 'steering': np.deg2rad(params['steering'])} for params in params_list]

    def plot_beam_pattern(self, ax, params_list):
        ax.clear()
        steering_angles = np.linspace(-np.pi/2, np.pi/2, 1000)
        converted_params = self._convert_steering_angles(params_list)
        combined_results = self._get_combined_pattern(converted_params, steering_angles)
        
        if hasattr(ax, 'set_theta_zero_location'):
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_thetamin(-90)
            ax.set_thetamax(90)
            ax.set_rmin(-60)
            ax.set_rmax(0)
            ax.set_rticks([-60, -50, -40, -30, -20, -10, 0])
            ax.set_rlabel_position(90)
            
            # Add single dB label
            ax.text(-0.1, -30, 'dB', color='white')
        
        ax.plot(steering_angles, combined_results)
        ax.set_title('Polar Beam Pattern', color='white', pad=10)
        ax.grid(True, color="gray")
        ax.tick_params(colors='white')

    def plot_rectangular_beam(self, ax_rect, params_list):
        ax_rect.clear()
        steering_angles = np.linspace(-np.pi/2, np.pi/2, 1000)
        converted_params = self._convert_steering_angles(params_list)
        combined_results = self._get_combined_pattern(converted_params, steering_angles)
        
        # Set fixed axis limits
        ax_rect.set_xlim(-10, 10)
        ax_rect.plot(steering_angles*180/np.pi, combined_results)
        ax_rect.set_xlabel('Theta [Degrees]', color='white')
        ax_rect.set_ylabel('Beam Pattern [dB]', color='white')
        ax_rect.set_title('Rectangular Beam Pattern', color='white', pad=23)
        ax_rect.grid(True, color="gray")
        ax_rect.tick_params(colors='white')
        
        # Explicitly include zero in tick marks
        ax_rect.set_xticks(np.arange(-90, 91, 20))
        
    def _calculate_magnitude_range(self, params_list, angles):
        patterns = []
        for params in params_list:
            N = params['elements']
            d = params['spacing']
            k = 2 * np.pi / (3e8 / params['frequency'] / 1e6)
            steering = params['steering']
            
            array_factor = np.zeros_like(angles, dtype=complex)
            phase_diff = -k * d * np.sin(steering)
            
            for n in range(N):
                phase = n * phase_diff
                array_factor += np.exp(1j * (k * d * n * np.sin(angles) + phase))
                
            pattern = 20 * np.log10(np.abs(array_factor) / N)
            patterns.append(pattern)
        
        combined = np.sum(patterns, axis=0)
        magnitude_range = {'min': np.min(combined), 'max': np.max(combined)}
        return magnitude_range
        
    def _get_combined_pattern(self, params_list, angles):
        if not params_list:
            return np.zeros_like(angles)
        
        patterns = []
        for params in params_list:
            N = params['elements']
            d = params['spacing']
            k = 2 * np.pi / (3e8 / params['frequency'] / 1e6)
            steering = params['steering']
            element_phase = np.deg2rad(params['phase'])  # Added phase consideration
            
            phase_diff = -k * d * np.sin(steering)
            array_factor = np.zeros_like(angles, dtype=complex)
            
            for n in range(N):
                total_phase = n * phase_diff + element_phase  # Combined phase
                array_factor += np.exp(1j * (k * d * n * np.sin(angles) + total_phase))
            
            pattern = 20 * np.log10(np.abs(array_factor) / N)
            patterns.append(pattern)
        
        combined = np.sum(patterns, axis=0)
        self.magnitude_min = max(-60, np.min(combined))
        self.magnitude_max = 0
        combined = np.clip(combined, self.magnitude_min, self.magnitude_max)
        
        return combined
    
    def plot_array_geometry(self, ax, params_list):
        ax.clear()
        if not params_list:
            return
            
        colors = plt.cm.tab10(np.linspace(0, 1, 10))
        
        x_positions = []
        y_positions = []
        
        for params in params_list:
            positions = self._calculate_array_positions(params)
            x_positions.extend(positions['x'])
            y_positions.extend(positions['y'])
            
            array_id = params.get("id", 1)
            color_index = (array_id - 1) % 10
            label = f'Array {array_id}'
            ax.scatter(positions['x'], positions['y'],
                    color=colors[color_index],
                    label=label)
        
        max_abs_x = max(abs(min(x_positions)), abs(max(x_positions)))
        max_abs_y = max(abs(min(y_positions)), abs(max(y_positions)))
        padding = 2
        
        limit_x = int(np.ceil(max_abs_x + padding))
        limit_y = int(np.ceil(max_abs_y + padding))
        ax.set_xlim(-limit_x, limit_x)
        ax.set_ylim(-limit_y, limit_y)
        
        # Set integer ticks for both axes
        x_ticks = np.arange(-limit_x, limit_x + 1, max(1, int(limit_x // 2)))
        y_ticks = np.arange(-limit_y, limit_y + 1, max(1, int(limit_y // 2)))
        
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        
        ax.set_aspect('equal')
        ax.grid(True, color='gray')
        ax.set_title('Array Configuration', color='white', pad=13)
        ax.set_xlabel('X Position (λ)', color='white')
        ax.set_ylabel('Y Position (λ)', color='white')
        ax.tick_params(colors='white')
        ax.legend(labelcolor='#1E293B', bbox_to_anchor=(1, 1.07), loc='upper right', fontsize=8)
    
    def plot_interference(self, ax, params_list):
        ax.clear()
        fig = ax.figure

        # Clear existing colorbars before creating new one
        fig = ax.figure
        for cbar in fig.get_axes():
            if cbar is not ax and isinstance(cbar, plt.Axes):
                if cbar.get_label() == 'colorbar':
                    cbar.remove()

        converted_params = self._convert_steering_angles(params_list)
        interference_pattern = self._calculate_interference_pattern(converted_params)
        masked_pattern = self._apply_circular_mask(interference_pattern)

        masked_pattern = np.rot90(masked_pattern)
        circle = plt.Circle((0, 0), 10, transform=ax.transData)

        # Use magnitude range from beam pattern
        im = ax.imshow(masked_pattern, extent=[-10, 10, -10, 10],
                origin='lower', cmap='coolwarm',
                vmin=self.magnitude_min,
                vmax=self.magnitude_max,
                clip_path=circle)

        # Create new colorbar axes with fixed position
        cax = fig.add_axes([0.92, 0.1, 0.03, 0.8])
        cax.set_label('colorbar')  # Set label to identify colorbar axes
        
        # Create and configure colorbar
        cbar = fig.colorbar(im, cax=cax)
        tick_values = np.linspace(self.magnitude_min, self.magnitude_max, 7)
        cbar.set_ticks(tick_values)
        cbar.set_ticklabels([f'{val:.0f}' for val in tick_values], fontsize=8)
        cbar.ax.tick_params(colors='white', pad=0)
        cbar.ax.yaxis.set_label_position('right')
        cbar.set_label('dB', color='white', rotation=0, labelpad=-5, y=1.08)

        ax.set_frame_on(False)
        ax.set_aspect('equal')

        ax.text(8, 10.5, 'Constructive\nInterference', color='white', fontsize=8)
        ax.text(8, -9.7, 'Destructive\nInterference', color='white', fontsize=8)

        ax.set_title('Interference Map', color='white', pad=21)

        ax.set_xticks([])
        ax.set_yticks([])

    def _clear_colorbars(self, fig):
        for ax in fig.get_axes():
            if isinstance(ax, plt.Axes) and ax.get_label() == 'colorbar':
                ax.remove()

    def update_plots(self, params_list):
        # Get axes from main window's visualization panel
        beam_ax = self.main_window.visualization_panel.beam_ax
        top_xy_ax = self.main_window.visualization_panel.top_xy_ax
        interference_ax = self.main_window.visualization_panel.interference_ax
        bottom_xy_ax = self.main_window.visualization_panel.bottom_xy_ax
        
        # Update plots with current axes
        self.plot_rectangular_beam(beam_ax, params_list)
        self.plot_array_geometry(top_xy_ax, params_list)
        self.plot_interference(interference_ax, params_list)
        self.plot_beam_pattern(bottom_xy_ax, params_list)
    
    def refresh_canvases(self):
        if self.beam_ax:
            self.beam_ax.figure.canvas.draw()
        if self.top_xy_ax:
            self.top_xy_ax.figure.canvas.draw()
        if self.interference_ax:
            self.interference_ax.figure.canvas.draw()
        if self.bottom_xy_ax:
            self.bottom_xy_ax.figure.canvas.draw()

