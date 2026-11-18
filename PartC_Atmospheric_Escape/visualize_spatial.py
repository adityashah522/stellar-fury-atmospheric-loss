import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

def parse_tecplot_header(filepath):
    """
    Parses the header of a Tecplot file to find the number of variables and zones.
    Returns the variable names and the line number where data starts.
    """
    variables = []
    data_start_line = 0
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line.startswith('VARIABLES'):
                # formatting can vary, crude parsing
                clean_line = line.replace('VARIABLES', '').replace('=', '').replace('"', '')
                variables = [v.strip() for v in clean_line.split(',')]
            
            # Data usually starts after the header lines (ZONE, AUXDATA, etc.)
            # We look for the first line that starts with a number
            if len(variables) > 0 and (not line.startswith('TITLE') and not line.startswith('VARIABLES') and not line.startswith('ZONE') and not line.startswith('AUXDATA')):
                 # Check if it looks like data
                 try:
                     parts = line.split()
                     float(parts[0])
                     data_start_line = i
                     break
                 except:
                     pass
    return variables, data_start_line

def read_tecplot_data(filepath, x_idx, z_idx, rho_idx):
    """
    Reads X, Z, and Rho from a single Tecplot file.
    """
    x_data = []
    z_data = []
    rho_data = []
    
    variables, start_line = parse_tecplot_header(filepath)
    
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            if i < start_line:
                continue
            try:
                parts = line.split()
                if len(parts) >= max(x_idx, z_idx, rho_idx) + 1:
                    x_data.append(float(parts[x_idx]))
                    z_data.append(float(parts[z_idx]))
                    rho_data.append(float(parts[rho_idx]))
            except ValueError:
                continue
                
    return np.array(x_data), np.array(z_data), np.array(rho_data)

def main():
    data_dir = "../PartC_AtmosphericEscape_Simulation/input_SWMF_escape/GM/IO2"
    # Find all pe*.tec files for y=0 at step 50
    pattern = os.path.join(data_dir, "y=0_mhd_*_n00000050_*_pe*.tec")
    files = glob.glob(pattern)
    
    if not files:
        print(f"No files found matching {pattern}")
        return

    print(f"Found {len(files)} files to combine.")

    # Indices based on header inspection:
    # VARIABLES ="X [R]", "Y [R]", "Z [R]", "Rho [amu/cm^3]", ...
    #             0        1        2        3
    x_idx = 0
    z_idx = 2
    rho_idx = 3

    all_x = []
    all_z = []
    all_rho = []

    for fpath in files:
        # print(f"Reading {fpath}...")
        x, z, rho = read_tecplot_data(fpath, x_idx, z_idx, rho_idx)
        all_x.extend(x)
        all_z.extend(z)
        all_rho.extend(rho)

    all_x = np.array(all_x)
    all_z = np.array(all_z)
    all_rho = np.array(all_rho)
    
    # Filter out potential zeros or negatives for log plot
    mask = all_rho > 0
    x_plot = all_x[mask]
    z_plot = all_z[mask]
    rho_plot = all_rho[mask]

    print(f"Total points: {len(x_plot)}")

    # Plotting
    plt.figure(figsize=(10, 8))
    
    # Use triangulation for unstructured data
    triang = tri.Triangulation(x_plot, z_plot)
    
    # Contour plot of Log10(Rho)
    cntr = plt.tricontourf(triang, np.log10(rho_plot), levels=20, cmap="viridis")
    cbar = plt.colorbar(cntr)
    cbar.set_label('Log10 Density [amu/cm^3]')
    
    # Add Mars body (circle)
    circle = plt.Circle((0, 0), 1.0, color='black', fill=True)
    plt.gca().add_patch(circle)
    
    plt.xlabel('X [Rm]')
    plt.ylabel('Z [Rm]')
    plt.title('Mars Ion Density (Y=0 Plane) - Step 50')
    plt.axis('equal')
    plt.xlim(-5, 5) # Adjust viewing window
    plt.ylim(-5, 5)
    
    output_file = "spatial_density_map.png"
    plt.savefig(output_file, dpi=150)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    main()
