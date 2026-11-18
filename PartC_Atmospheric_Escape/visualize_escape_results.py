import os
import matplotlib.pyplot as plt

def main():
    # Path to the log file (relative to this script)
    log_path = "../PartC_AtmosphericEscape_Simulation/input_SWMF_escape/GM/IO2/log_n000001.log"
    
    if not os.path.exists(log_path):
        print(f"Error: Log file not found at {log_path}")
        return

    iterations = []
    hp_flux = []
    op_flux = []
    o2p_flux = []
    co2p_flux = []

    print(f"Reading {log_path}...")
    
    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and headers
            if not line or not line[0].isdigit():
                continue
            
            check_valid = False
            try:
                parts = line.split()
                # Ensure we have enough columns (expecting 16)
                if len(parts) >= 16:
                   it = int(parts[0])
                   # Columns 12, 13, 14, 15 are fluxes (Hp, Op, O2p, CO2p)
                   hp = float(parts[12])
                   op = float(parts[13])
                   o2p = float(parts[14])
                   co2p = float(parts[15])
                   
                   iterations.append(it)
                   hp_flux.append(hp)
                   op_flux.append(op)
                   o2p_flux.append(o2p)
                   co2p_flux.append(co2p)
            except ValueError:
                continue

    if not iterations:
        print("No valid data found.")
        return

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, hp_flux, label='Hp Flux', linewidth=2)
    plt.plot(iterations, op_flux, label='Op Flux', linewidth=2)
    plt.plot(iterations, o2p_flux, label='O2p Flux', linewidth=2)
    plt.plot(iterations, co2p_flux, label='CO2p Flux', linewidth=2)
    
    plt.xlabel('Iteration')
    plt.ylabel('Ion Flux integrated over Sphere (Particles/s)')
    plt.title('Mars Atmospheric Escape Rates vs Iteration')
    plt.legend()
    plt.grid(True)
    plt.yscale('symlog') # Use symlog to handle negative flux values if any
    
    output_file = "escape_rates.png"
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")
    print(f"Final Rates (Step {iterations[-1]}):")
    print(f"  Hp: {hp_flux[-1]:.2e}")
    print(f"  Op: {op_flux[-1]:.2e}")
    print(f"  O2p: {o2p_flux[-1]:.2e}")
    print(f"  CO2p: {co2p_flux[-1]:.2e}")

if __name__ == "__main__":
    main()
