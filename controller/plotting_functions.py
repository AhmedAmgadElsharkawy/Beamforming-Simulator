import numpy as np
import matplotlib.pyplot as plt

def calculate_steering_vector(params, use_phase=False):
    elements = params['elements']
    spacing = params['spacing']
    steering = params['steering']
    array_type = params['array_type']
    radius = params['curvature']
    frequency = params['frequency']
    x_pos = params['x_position']
    y_pos = params['y_position']
    # Only use phase when multiple arrays
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

def plot_beam_pattern(ax, params_list):
    ax.clear()
    use_phase = len(params_list) > 1
    
    steering_angles = np.linspace(-np.pi/2, np.pi/2, 1000)
    combined_results = np.zeros_like(steering_angles)
    
    for params in params_list:
        elements = params['elements']
        spacing = params['spacing']
        array_type = params['array_type']
        radius = params['curvature']
        frequency = params['frequency']
        wavelength = 3e8 / (frequency * 1e6)
        k = 2 * np.pi / wavelength
        
        results = []
        for theta_i in steering_angles:
            if array_type == 'linear':
                d = spacing
                phase = k * d * np.arange(elements) * np.sin(theta_i)
                w = np.exp(-1j * phase)
            else:
                d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/elements)))
                sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/elements)))
                x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements))
                y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements))
                w = np.exp(1j * k * (x * np.cos(theta_i) + y * np.sin(theta_i)))
            
            s = calculate_steering_vector(params, use_phase)
            results.append(np.abs(np.dot(w.conj(), s.flatten()))**2)
        
        combined_results += np.array(results)
    
    combined_results = 10 * np.log10(combined_results)
    combined_results -= np.max(combined_results)
    
    ax.plot(steering_angles, combined_results)
    ax.set_title('Combined Beam Pattern')
    ax.grid(True)

    
def plot_array_geometry(ax, params_list):
    ax.clear()
    
    for params in params_list:
        # Extract parameters
        x_pos = params['x_position']
        y_pos = params['y_position']
        elements = params['elements']
        array_type = params['array_type']
        radius = params['curvature']
        
        # Plot array geometry
        if array_type == 'linear':
            x = np.arange(elements) * 0.5 + x_pos
            y = np.zeros_like(x) + y_pos
        else:
            d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/elements)))
            sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/elements)))
            x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements)) + x_pos
            y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements)) + y_pos
    
        ax.scatter(x, y, label=f'Array {params.get("id", "")}')
        
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title('Array Configuration')
    ax.set_xlabel('X Position (λ)')
    ax.set_ylabel('Y Position (λ)')
    ax.legend()

def plot_interference(ax, params_list):
    ax.clear()
    fig = ax.figure
    use_phase = len(params_list) > 1
    
    # Clear existing elements
    for cbar in fig.get_axes():
        if cbar is not ax and isinstance(cbar, plt.Axes):
            if cbar.get_label() == 'colorbar':
                cbar.remove()
    
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    
    # Create spatial grid
    x = np.linspace(-10, 10, 200)
    y = np.linspace(-10, 10, 200)
    X, Y = np.meshgrid(x, y)
    Z_total = np.zeros_like(X)
    
    # Calculate interference pattern for each array
    for params in params_list:
        elements = params['elements']
        spacing = params['spacing']
        steering = params['steering']
        array_type = params['array_type']
        radius = params['curvature']
        frequency = params['frequency']
        wavelength = 3e8 / (frequency * 1e6)
        k = 2 * np.pi / wavelength
        
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                theta_ij = np.arctan2(Y[i,j], X[i,j])
                R = np.sqrt(X[i,j]**2 + Y[i,j]**2)
                
                if array_type == 'linear':
                    d = spacing
                    phase = k * d * np.arange(elements) * np.sin(theta_ij)
                    w = np.exp(-1j * phase)
                else:
                    d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/elements)))
                    sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/elements)))
                    x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements))
                    y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements))
                    w = np.exp(1j * k * (x * np.cos(theta_ij) + y * np.sin(theta_ij)))
                
                s = calculate_steering_vector(params, use_phase)
                Z[i,j] = np.abs(np.dot(w.conj(), s))**2
        
        Z_total += Z
    
    Z_total = 10 * np.log10(Z_total)
    Z_total -= np.max(Z_total)
    Z_total = np.clip(Z_total, -40, 0)
    
    # Create and apply circular mask
    center = [100, 100]
    radius = 100
    y, x = np.ogrid[-center[0]:200-center[0], -center[1]:200-center[1]]
    mask = x*x + y*y <= radius*radius
    Z_masked = np.ma.array(Z_total, mask=~mask)
    
    # Plot interference pattern
    im = ax.imshow(Z_masked, extent=[-10, 10, -10, 10],
                   origin='lower', cmap='coolwarm',
                   vmin=-40, vmax=0)
    
    ax.set_aspect('equal')
    cax = fig.add_axes([0.87, 0.1, 0.03, 0.8])
    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label('Power (dB)')
    cbar.ax.set_label('colorbar')
    ax.set_title('Interference Pattern')

    
def plot_rectangular_beam(ax_rect, params_list):
    ax_rect.clear()
    use_phase = len(params_list) > 1
    
    steering_angles = np.linspace(-np.pi/2, np.pi/2, 1000)
    combined_results = np.zeros_like(steering_angles)
    
    for params in params_list:
        elements = params['elements']
        spacing = params['spacing']
        steering = params['steering']
        array_type = params['array_type']
        radius = params['curvature']
        frequency = params['frequency']
        wavelength = 3e8 / (frequency * 1e6)
        k = 2 * np.pi / wavelength
        
        results = np.zeros_like(steering_angles)
        for i, theta_i in enumerate(steering_angles):
            if array_type == 'linear':
                d = spacing
                phase = k * d * np.arange(elements) * np.sin(theta_i)
                w = np.exp(-1j * phase)
            else:
                d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/elements)))
                sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/elements)))
                x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements))
                y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements))
                w = np.exp(1j * k * (x * np.cos(theta_i) + y * np.sin(theta_i)))
            
            s = calculate_steering_vector(params, use_phase)
            results[i] = np.abs(np.dot(w.conj(), s.flatten()))**2
        
        combined_results += results
    
    combined_results = 10 * np.log10(combined_results)
    combined_results -= np.max(combined_results)
    
    ax_rect.plot(steering_angles*180/np.pi, combined_results)
    ax_rect.set_xlabel('Theta [Degrees]')
    ax_rect.set_ylabel('Combined Beam Pattern [dB]')
    ax_rect.grid(True)


    
 # def plot_bottom_xy(ax_rect, params):
    # ax.clear()
    
    # x_pos = params.x_position
    # y_pos = params.y_position
    # elements = params.elements
    # spacing = params.spacing
    # array_type = params.array_type
    # steering = params.steering
    
    # theta = np.deg2rad(steering)
    # dx = np.cos(theta)
    # dy = np.sin(theta)
    
    # ax.scatter(x_pos, y_pos, c='red', marker='o')
    
    # length = 5
    # ax.arrow(x_pos, y_pos, length*dx, length*dy, 
    #          head_width=0.3, head_length=0.5, fc='red', ec='red')
    
    # ax.set_title('Array Position and Beam Direction')
    # ax.grid(True)
    # ax.set_aspect('equal')
    # ax.set_xlim(-10, 10)
    # ax.set_ylim(-10, 10)


# # 2. Calculate and overlay beam pattern
    # theta = np.linspace(-np.pi/2, np.pi/2, 1000)
    # r = np.zeros_like(theta)
    
    # for i, theta_i in enumerate(theta):
    #     # Similarly update the beam pattern calculation
    #     if params['array_type'] == 'linear':
    #         d = spacing  # Use direct spacing value
    #         phase = k * d * np.arange(elements) * np.sin(theta_i)
    #         w = np.exp(-1j * phase)
    #     else:
    #         radius = params['curvature']
    #         d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/elements)))
    #         sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/elements)))
    #         x = d * sf * np.cos(2 * np.pi / elements * np.arange(elements))
    #         y = -1 * d * sf * np.sin(2 * np.pi / elements * np.arange(elements))
    #         w = np.exp(1j * k * (x * np.cos(theta_i) + y * np.sin(theta_i)))
        
    #     s = calculate_steering_vector(params)
    #     r[i] = np.abs(np.dot(w.conj(), s))
    
    # # Normalize and scale beam pattern
    # r = r / np.max(r) * 10  # Scale factor of 10 for visibility
    
    # # Convert to Cartesian coordinates for overlay
    # x_beam = r * np.cos(theta)
    # y_beam = r * np.sin(theta)
    
    # # Add this line to actually plot the beam pattern
    # ax.plot(x_beam, y_beam, 'w-', linewidth=2, alpha=0.8, label='Beam Pattern')