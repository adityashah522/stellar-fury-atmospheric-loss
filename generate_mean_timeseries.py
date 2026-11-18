import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def generate_mean_time_plots(stats_csv, template_log, output_dir):
    """
    Generate mean over time plots by scaling a template time-series 
    with ensemble final-state statistics.
    """
    df = pd.read_csv(stats_csv)
    
    # Load the template log (from the "Mean Condition" run or the last trial)
    # We will use the last trial (Trial 199) as the "Shape Template"
    print(f"Reading template log: {template_log}")
    
    iters, rhos, ps, ts = [], [], [], []
    with open(template_log, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 12 and parts[0][0].isdigit():
                iters.append(int(parts[0]))
                rhos.append(float(parts[3])) # Rho
                ts.append(float(parts[7]))   # Temp proxy
                ps.append(float(parts[11]))  # Pmax proxy
                
    # Convert to arrays and normalize
    iters = np.array(iters)
    rhos = np.array(rhos) / rhos[-1]
    ps = np.array(ps) / ps[-1]
    ts = np.array(ts) / ts[-1]
    
    # Ensemble Means
    ens_rho_mean = df['mean_rho'].mean()
    ens_p_mean = df['mean_p'].mean()
    ens_t_mean = df['mean_t'].mean()
    ens_loss_mean = df['escape_rate_kg_s'].mean()
    
    # Shaded regions (Std Dev)
    ens_rho_std = df['mean_rho'].std()
    ens_p_std = df['mean_p'].std()
    ens_t_std = df['mean_t'].std()

    # 1. Mean Density, Pressure, Temp over Time
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # Density
    ax1.plot(iters, rhos * ens_rho_mean, 'b-', label='Mean Density')
    ax1.fill_between(iters, rhos * (ens_rho_mean - ens_rho_std), 
                     rhos * (ens_rho_mean + ens_rho_std), color='blue', alpha=0.2)
    ax1.set_ylabel('Density [amu/cm³]')
    ax1.set_title('Ensemble Mean Atmospheric Parameters over Time')
    ax1.grid(True, alpha=0.3)
    
    # Pressure
    ax2.plot(iters, ps * ens_p_mean, 'g-', label='Mean Pressure')
    ax2.fill_between(iters, ps * (ens_p_mean - ens_p_std), 
                     ps * (ens_p_mean + ens_p_std), color='green', alpha=0.2)
    ax2.set_ylabel('Pressure [nPa]')
    ax2.grid(True, alpha=0.3)
    
    # Temperature
    ax3.plot(iters, ts * ens_t_mean, 'r-', label='Mean Temperature')
    ax3.fill_between(iters, ts * (ens_t_mean - ens_t_std), 
                     ts * (ens_t_mean + ens_t_std), color='red', alpha=0.2)
    ax3.set_ylabel('Temp Proxy')
    ax3.set_xlabel('Iteration Step')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "mean_params_over_time.png"))
    
    # 2. Mean Atmospheric Mass vs Time (Cumulative Loss)
    plt.figure(figsize=(10, 6))
    time_years = np.linspace(0, 1000000, 100) # Linearly up to 1 Myr
    cumulative_loss = ens_loss_mean * (time_years * 365 * 24 * 3600)
    loss_std = df['escape_rate_kg_s'].std() * (time_years * 365 * 24 * 3600)
    
    plt.plot(time_years/1e6, cumulative_loss/1e12, 'k-', linewidth=2, label='Mean Cumulative Loss')
    plt.fill_between(time_years/1e6, (cumulative_loss - loss_std)/1e12, 
                     (cumulative_loss + loss_std)/1e12, color='gray', alpha=0.3, label='Ensemble Spread')
    
    plt.title('Mean Cumulative Atmospheric Mass Loss (1 Million Year Extrapolation)')
    plt.xlabel('Time [Million Years]')
    plt.ylabel('Cumulative Loss [Teratonnes]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "mean_mass_loss_v_time_1Myr.png"))
    
    # 3. Mean % Atmospheric Loss vs Time
    plt.figure(figsize=(10, 6))
    earth_mass = 5.15e18 # kg
    percent_loss = (cumulative_loss / earth_mass) * 100
    percent_std = (loss_std / earth_mass) * 100
    
    plt.plot(time_years/1e6, percent_loss, 'm-', linewidth=2, label='Mean % Loss')
    plt.fill_between(time_years/1e6, percent_loss - percent_std, 
                     percent_loss + percent_std, color='magenta', alpha=0.2, label='Ensemble Spread')
    
    plt.title('Percentage of Total Atmosphere Lost (1 Million Year Extrapolation)')
    plt.xlabel('Time [Million Years]')
    plt.ylabel('Atmospheric Loss [%]')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "percent_loss_v_time_1Myr.png"))
    
    print(f"Time-series plots generated in {output_dir}")

if __name__ == "__main__":
    stats_csv = "/home/aditya/IPSProject/sim_results/all_trials_data.csv"
    template_log = "/home/aditya/IPSProject/PartC_AtmosphericEscape_Simulation/input_SWMF_escape/GM/IO2/log_n000001.log"
    output_dir = "/home/aditya/IPSProject/sim_results"
    
    generate_mean_time_plots(stats_csv, template_log, output_dir)
