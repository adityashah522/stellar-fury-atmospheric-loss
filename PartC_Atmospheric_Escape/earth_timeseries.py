import numpy as np
import matplotlib.pyplot as plt

def main():
    """Create time-series plots from Earth GM log file."""
    
    log_file = "../PartC_AtmosphericEscape_Simulation/input_SWMF_escape/GM/IO2/log_n000001.log"
    
    # Read the log file
    iterations = []
    density = []
    bz = []
    energy = []
    pmin = []
    pmax = []
    
    print(f"Reading {log_file}...")
    
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            
            try:
                parts = line.split()
                if len(parts) >= 12:
                    iterations.append(int(parts[0]))
                    density.append(float(parts[3]))      # Rho
                    bz.append(float(parts[8]))           # Bz
                    energy.append(float(parts[9]))       # E
                    pmin.append(float(parts[10]))        # Pmin
                    pmax.append(float(parts[11]))        # Pmax
            except (ValueError, IndexError):
                continue
    
    if not iterations:
        print("No data found in log file")
        return
    
    iterations = np.array(iterations)
    density = np.array(density)
    bz = np.array(bz)
    energy = np.array(energy)
    pmin = np.array(pmin)
    pmax = np.array(pmax)
    
    print(f"Read {len(iterations)} data points")
    
    # Create multi-panel figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Earth Magnetosphere Evolution (GM Component)', fontsize=16, fontweight='bold')
    
    # Panel 1: Density
    ax = axes[0, 0]
    ax.plot(iterations, density, 'b-', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Volume-Averaged Density [amu/cm³]')
    ax.set_title('Magnetosphere Compression')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=5.0, color='r', linestyle='--', alpha=0.5, label='Solar Wind')
    ax.legend()
    
    # Panel 2: Magnetic Field Bz
    ax = axes[0, 1]
    ax.plot(iterations, bz, 'g-', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Volume-Averaged Bz [nT]')
    ax.set_title('Magnetotail Field Evolution')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=-5.0, color='r', linestyle='--', alpha=0.5, label='IMF Bz')
    ax.legend()
    
    # Panel 3: Energy
    ax = axes[1, 0]
    ax.plot(iterations, energy * 1e10, 'm-', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Total Energy [×10⁻¹⁰]')
    ax.set_title('System Energy Evolution')
    ax.grid(True, alpha=0.3)
    
    # Panel 4: Pressure Range
    ax = axes[1, 1]
    ax.semilogy(iterations, pmax, 'r-', linewidth=2, label='P_max')
    ax.semilogy(iterations, pmin, 'b-', linewidth=2, label='P_min')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Pressure [nPa]')
    ax.set_title('Pressure Range')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    output_file = "earth_magnetosphere_timeseries.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Time-series plot saved to {output_file}")
    
    # Print final statistics
    print(f"\nFinal State (Iteration {iterations[-1]}):")
    print(f"  Density: {density[-1]:.3f} amu/cm³")
    print(f"  Bz: {bz[-1]:.3f} nT")
    print(f"  Energy: {energy[-1]:.4e}")
    print(f"  Pressure range: {pmin[-1]:.4e} to {pmax[-1]:.4e} nPa")

if __name__ == "__main__":
    main()
