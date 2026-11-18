import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    """Create schematic spatial visualization of Earth's magnetosphere."""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Set up coordinate system
    ax.set_xlim(-50, 20)
    ax.set_ylim(-35, 35)
    ax.set_aspect('equal')
    
    # Earth at origin
    earth = plt.Circle((0, 0), 1.0, color='blue', alpha=0.8, zorder=10)
    ax.add_patch(earth)
    ax.text(0, 0, 'Earth', ha='center', va='center', color='white', 
            fontsize=10, fontweight='bold')
    
    # Inner boundary (ionosphere coupling)
    inner_boundary = plt.Circle((0, 0), 2.5, fill=False, edgecolor='cyan', 
                                linewidth=2, linestyle='--', zorder=5, 
                                label='Inner boundary (2.5 Re)')
    ax.add_patch(inner_boundary)
    
    # Bow shock (approximate position for southward IMF)
    theta = np.linspace(-np.pi/2, np.pi/2, 100)
    # Bow shock equation (simplified)
    r_bs = 15 / (1 + 0.5 * np.cos(theta))
    x_bs = r_bs * np.cos(theta)
    y_bs = r_bs * np.sin(theta)
    ax.plot(x_bs, y_bs, 'r-', linewidth=3, label='Bow Shock', zorder=3)
    
    # Magnetopause (compressed by southward IMF)
    r_mp = 10 / (1 + 0.5 * np.cos(theta))
    x_mp = r_mp * np.cos(theta)
    y_mp = r_mp * np.sin(theta)
    ax.plot(x_mp, y_mp, 'g-', linewidth=3, label='Magnetopause', zorder=4)
    
    # Magnetotail
    tail_width = 20
    tail_x = np.array([-10, -45])
    tail_y_upper = np.array([tail_width/2, tail_width/2 * 0.9])
    tail_y_lower = -tail_y_upper
    ax.plot(tail_x, tail_y_upper, 'g-', linewidth=2.5)
    ax.plot(tail_x, tail_y_lower, 'g-', linewidth=2.5)
    
    # Magnetotail current sheet
    ax.plot([-10, -45], [0, 0], 'orange', linewidth=2, linestyle='--', 
            label='Current Sheet')
    
    # Magnetic field lines (schematic)
    # Dayside field lines
    for y0 in [0, 5, 10, -5, -10]:
        theta_field = np.linspace(-np.pi*0.4, np.pi*0.4, 50)
        r_field = 8 * np.abs(np.cos(theta_field))**0.3
        x_field = r_field * np.cos(theta_field)
        y_field = r_field * np.sin(theta_field) + y0
        mask = x_field > -5
        ax.plot(x_field[mask], y_field[mask], 'b-', linewidth=1, alpha=0.5)
    
    # Nightside field lines (stretched)
    for y0 in [3, 8, -3, -8]:
        x_night = np.linspace(-5, -30, 30)
        y_night = y0 * np.exp(-x_night/40)
        ax.plot(x_night, y_night, 'b-', linewidth=1, alpha=0.5)
        ax.plot(x_night, -y_night, 'b-', linewidth=1, alpha=0.5)
    
    # Solar wind flow
    for y in np.linspace(-30, 30, 13):
        ax.arrow(15, y, -5, 0, head_width=1.5, head_length=1, 
                fc='yellow', ec='orange', alpha=0.6, linewidth=1.5)
    
    # IMF direction (southward)
    ax.arrow(15, -25, 0, -3, head_width=2, head_length=1,
            fc='red', ec='darkred', linewidth=2.5, alpha=0.8)
    ax.text(17, -27, 'IMF Bz=-5nT\n(Southward)', fontsize=11, 
            fontweight='bold', color='darkred')
    
    # Reconnection regions
    # Subsolar reconnection
    ax.plot([10], [0], 'r*', markersize=20, label='Reconnection site')
    ax.text(10, -3, 'Dayside\nReconnection', ha='center', fontsize=9, 
            color='red', fontweight='bold')
    
    # Tail reconnection  
    ax.plot([-20], [0], 'r*', markersize=20)
    ax.text(-20, 3, 'Tail\nReconnection', ha='center', fontsize=9,
            color='red', fontweight='bold')
    
    # Polar cap regions (open field lines)
    polar_cap_n = patches.Wedge((0, 0), 2.5, 30, 150, 
                                facecolor='yellow', alpha=0.3, 
                                edgecolor='gold', linewidth=2)
    polar_cap_s = patches.Wedge((0, 0), 2.5, 210, 330,
                                facecolor='yellow', alpha=0.3,
                                edgecolor='gold', linewidth=2)
    ax.add_patch(polar_cap_n)
    ax.add_patch(polar_cap_s)
    
    # Polar wind outflow
    ax.arrow(0, 2.5, 0, 5, head_width=1, head_length=1,
            fc='white', ec='yellow', linewidth=2, alpha=0.8)
    ax.arrow(0, -2.5, 0, -5, head_width=1, head_length=1,
            fc='white', ec='yellow', linewidth=2, alpha=0.8)
    ax.text(2, 5, 'Polar Wind\nH⁺ Outflow\n~2 kg/s', fontsize=10,
            color='yellow', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    # Labels and annotations
    ax.text(-35, 32, 'EARTH MAGNETOSPHERE STRUCTURE', fontsize=16,
            fontweight='bold', bbox=dict(boxstyle='round', 
            facecolor='white', alpha=0.9))
    
    # Simulation parameters box
    params_text = ('Simulation: GM+IE Coupled\n'
                  'Solar Wind: 5 amu/cm³, 400 km/s\n'
                  'IMF: Southward (Bz=-5 nT)\n'
                  'Grid: Adaptive, 3 levels\n'
                  'Ionosphere: Realistic oval')
    ax.text(-47, -32, params_text, fontsize=9, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Axes and grid
    ax.set_xlabel('X [Earth Radii, Re]', fontsize=12, fontweight='bold')
    ax.set_ylabel('Z [Earth Radii, Re]', fontsize=12, fontweight='bold')
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(0, color='gray', linestyle=':', alpha=0.5)
    ax.grid(True, alpha=0.2)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    
    plt.title('Earth Magnetosphere - Y=0 Meridional Plane\nGM+IE Coupled Simulation', 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    output_file = "earth_magnetosphere_spatial.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Spatial visualization saved to {output_file}")

if __name__ == "__main__":
    main()
