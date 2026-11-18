import pandas as pd
import numpy as np
from scipy import stats
import os

def run_advanced_stats(csv_path, output_dir):
    df = pd.read_csv(csv_path)
    
    # 1. One-way ANOVA: Categorize trials by Solar Wind Density (Proxy for "scenario")
    # Low (<5), Medium (5-8), High (>8)
    def categorize(rho):
        if rho < 5: return 'Low'
        elif rho < 8: return 'Medium'
        else: return 'High'
    
    df['Scenario'] = df['mean_rho'].apply(categorize)
    
    groups = [df[df['Scenario'] == s]['escape_rate_kg_s'] for s in ['Low', 'Medium', 'High']]
    f_stat, p_val = stats.f_oneway(*groups)
    
    # 2. Detailed Report Generation
    with open(os.path.join(output_dir, "detailed_statistical_report.md"), "w") as f:
        f.write("# Earth Ensemble Simulation: Detailed Statistical Report\n\n")
        
        f.write("## 1. Mean and Median Atmospheric Parameters\n")
        f.write("| Parameter | Mean | Median | Std Dev |\n")
        f.write("|-----------|------|--------|---------|\n")
        f.write(f"| Density (amu/cm³) | {df['mean_rho'].mean():.4f} | {df['mean_rho'].median():.4f} | {df['mean_rho'].std():.4f} |\n")
        f.write(f"| Pressure (nPa) | {df['mean_p'].mean():.4f} | {df['mean_p'].median():.4f} | {df['mean_p'].std():.4f} |\n")
        f.write(f"| Temperature (Proxy) | {df['mean_t'].mean():.4f} | {df['mean_t'].median():.4f} | {df['mean_t'].std():.4f} |\n\n")
        
        f.write("## 2. Atmospheric Mass Loss Summary\n")
        mean_loss = df['escape_rate_kg_s'].mean()
        f.write(f"- **Mean Atmospheric Loss (Trials)**: {mean_loss:.4f} kg/s\n")
        
        total_lost_1myr = mean_loss * 1e6 * 365 * 24 * 3600
        f.write(f"- **Total Loss (1 Myr)**: {total_lost_1myr:.4e} kg\n")
        
        earth_mass = 5.15e18
        percent_loss = (total_lost_1myr / earth_mass) * 100
        f.write(f"- **Percentage Atmospheric Loss**: {percent_loss:.6f}% of initial mass\n\n")
        
        f.write("## 3. Shock Interaction Variance\n")
        f.write("Changes in plasma parameters caused by the shock interaction (variability across 200 trials):\n")
        f.write(f"- **Density Variance**: {df['mean_rho'].var():.4f}\n")
        f.write(f"- **Pressure Variance**: {df['mean_p'].var():.8f}\n\n")
        
        f.write("## 4. Cumulative Loss Over Time\n")
        f.write("| Time (Years) | Cumulative Loss (kg) |\n")
        f.write("|--------------|----------------------|\n")
        for yrs in [1000, 10000, 100000, 1000000]:
            loss = mean_loss * yrs * 365 * 24 * 3600
            f.write(f"| {yrs:,} | {loss:.4e} |\n")
        f.write("\n")
        
        f.write("## 5. Statistical Test: One-way ANOVA\n")
        f.write("Comparing escape rates across different Solar Wind Scenarios (Low, Medium, High Density):\n")
        f.write(f"- **F-Statistic**: {f_stat:.4f}\n")
        f.write(f"- **P-Value**: {p_val:.4e}\n")
        if p_val < 0.05:
            f.write("- **Result**: Statistically Significant difference found between scenarios.\n")
        else:
            f.write("- **Result**: No statistically significant difference found.\n")
            
    print(f"Detailed report saved to {output_dir}")

if __name__ == "__main__":
    run_advanced_stats("/home/aditya/IPSProject/sim_results/all_trials_data.csv", "/home/aditya/IPSProject/sim_results")
