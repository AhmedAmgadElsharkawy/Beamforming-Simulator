import numpy as np

def plot_beam_pattern(ax, params):
    if not hasattr(ax, '_has_data'):
            ax.clear()
            ax._has_data = True
        
    elements = params['elements']
    spacing = params['spacing']
    steering = params['steering']
    phase = params['phase']
    
    theta = np.linspace(-np.pi, np.pi, 360)
    array_factor = np.zeros_like(theta, dtype=np.complex128)
    
    for n in range(elements):
        array_factor += np.exp(1j * (2 * np.pi * spacing * n * np.sin(theta) + 
                                    np.deg2rad(steering) + np.deg2rad(phase)))
    
    array_factor = 20 * np.log10(np.abs(array_factor) / np.max(np.abs(array_factor)))
    array_factor[array_factor < -50] = -50
    
    ax.plot(theta, array_factor, color='blue')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rticks([-50, -40, -30, -20, -10, 0])
    ax.set_thetagrids(range(0, 360, 45), labels=['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'])
    ax.set_title('Beam Pattern', color='white', pad=-20)
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)


def plot_top_xy(ax, params):
    ax.clear()
    
    x_pos = params['x_position']
    y_pos = params['y_position']
    elements = params['elements']
    spacing = params['spacing']
    array_type = params['array_type']
    curvature = params['curvature']
    
    x_elements = np.zeros(elements)
    y_elements = np.zeros(elements)
    
    if array_type.lower() == 'linear':
        x_elements = np.linspace(-spacing * (elements-1)/2, 
                               spacing * (elements-1)/2, 
                               elements) + x_pos
        y_elements = np.full(elements, y_pos)
    else:
        theta = np.linspace(-np.pi/4, np.pi/4, elements)
        radius = elements * spacing * curvature
        x_elements = radius * np.sin(theta) + x_pos
        y_elements = radius * (1 - np.cos(theta)) + y_pos
    
    ax.scatter(x_elements, y_elements, c='blue', marker='o')
    ax.set_title('Array Configuration',color='white')
    ax.grid(True)
    ax.set_aspect('equal')

def plot_interference(ax, params):
    ax.clear()
    
    elements = params['elements']
    spacing = params['spacing']
    frequency = params['frequency']
    
    x = np.linspace(-10, 10, 200)
    y = np.linspace(-10, 10, 200)
    X, Y = np.meshgrid(x, y)
    
    Z = np.zeros_like(X)
    wavelength = 3e8 / (frequency * 1e6)
    
    for n in range(elements):
        pos = spacing * wavelength * (n - (elements-1)/2)
        R = np.sqrt(X**2 + (Y-pos)**2)
        Z += np.cos(2 * np.pi * R / wavelength)
    
    ax.imshow(Z, extent=[-10, 10, -10, 10], origin='lower')
    ax.set_title('Interference Pattern',color='white')
    ax.grid(True)

def plot_bottom_xy(ax, params):
    ax.clear()
    
    x_pos = params.x_position
    y_pos = params.y_position
    elements = params.elements
    spacing = params.spacing
    array_type = params.array_type
    steering = params.steering
    
    theta = np.deg2rad(steering)
    dx = np.cos(theta)
    dy = np.sin(theta)
    
    ax.scatter(x_pos, y_pos, c='red', marker='o')
    
    length = 5
    ax.arrow(x_pos, y_pos, length*dx, length*dy, 
             head_width=0.3, head_length=0.5, fc='red', ec='red')
    
    ax.set_title('Array Position and Beam Direction',color='white')
    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)