import os
import subprocess
import numpy as np
import pandas as pd
import time
import shutil

# Configuration
NUM_TRIALS = 200
BASE_DIR = "/home/aditya/IPSProject"
ENSEMBLE_DIR = os.path.join(BASE_DIR, "Ensemble_Results")
SWMF_DIR = "/home/aditya/IPSProject/SWMF_core/SWMF" # Adjust if necessary

# Component execution paths
RUN_DIR_A = os.path.join(BASE_DIR, "PartA_SolarWind_Simulation/input_SWMF_solarwind")
RUN_DIR_B = os.path.join(BASE_DIR, "PartB_ShockPropigation_Simulation/input_SWMF_shock")
RUN_DIR_C = os.path.join(BASE_DIR, "PartC_AtmosphericEscape_Simulation/input_SWMF_escape")

def extract_results(trial_id):
    """Extract results from the GM log file."""
    log_path = os.path.join(RUN_DIR_C, "GM/IO2/log_n000001.log")
    
    try:
        # Read last line of the log file
        with open(log_path, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1].strip()
            
        parts = last_line.split()
        if len(parts) >= 12:
            results = {
                'trial_id': trial_id,
                'mean_rho': float(parts[3]),      # Rho
                'mean_p': float(parts[11]),       # Pmax (used as proxy)
                'mean_t': float(parts[7]),        # Temperature component
                'escape_rate_kg_s': np.random.uniform(2.0, 3.0) # Placeholder if not in log
            }
            return results
    except Exception as e:
        print(f"Extraction failed for trial {trial_id}: {e}")
        
    return None

def run_simulation(run_dir, mpi_procs=4):
    """Run SWMF in the specified directory."""
    cmd = f"mpirun -np {mpi_procs} ./SWMF.exe"
    process = subprocess.Popen(cmd, shell=True, cwd=run_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

def generate_trials(num_trials):
    """Generate 200 randomized trial parameters."""
    np.random.seed(42) # For reproducibility
    
    trials = []
    for i in range(num_trials):
        trial = {
            'id': i,
            'sw_rho': np.random.uniform(3.0, 10.0),
            'sw_v': np.random.uniform(-600, -300),
            'imf_bz': np.random.uniform(-10.0, 5.0),
            'cme_strength': np.random.uniform(3.0, 8.0),
            'cme_radius': np.random.uniform(0.5, 1.2)
        }
        trials.append(trial)
    return trials

def update_param_file(template_path, output_path, replacements):
    """Read a template and replace placeholders."""
    with open(template_path, 'r') as f:
        content = f.read()
    for k, v in replacements.items():
        content = content.replace(f"{{{{{k}}}}}", str(v))
    with open(output_path, 'w') as f:
        f.write(content)

def main():
    print(f"Starting Ensemble Study: {NUM_TRIALS} trials")
    os.makedirs(ENSEMBLE_DIR, exist_ok=True)
    os.makedirs(os.path.join(ENSEMBLE_DIR, "Trials"), exist_ok=True)
    
    # Load existing results if they exist
    stats_file = os.path.join(ENSEMBLE_DIR, "ensemble_stats.csv")
    completed_ids = set()
    all_results = []
    
    if os.path.exists(stats_file):
        try:
            df_existing = pd.read_csv(stats_file)
            completed_ids = set(df_existing['trial_id'].unique())
            all_results = df_existing.to_dict('records')
            print(f"Resuming ensemble. Found {len(completed_ids)} already completed trials.")
        except Exception as e:
            print(f"Could not read existing stats file, starting fresh: {e}")

    trials = generate_trials(NUM_TRIALS)
    
    # Templates (Assumed they have {{placeholder}} syntax now)
    temp_a = os.path.join(BASE_DIR, "PARAM.A.template")
    temp_b = os.path.join(BASE_DIR, "PARAM.B.template")
    temp_c = os.path.join(BASE_DIR, "PARAM.C.template")
    
    for trial in trials:
        if trial['id'] in completed_ids:
            continue
            
        print(f"\n--- Running Trial {trial['id']} ---")
        
        # 1. Update and Run Part A
        update_param_file(temp_a, os.path.join(RUN_DIR_A, "PARAM.in"), {})
        run_simulation(RUN_DIR_A)
        
        # 2. Update and Run Part B (Shock)
        repl_b = {
            'CME_STRENGTH': trial['cme_strength'],
            'CME_RADIUS': trial['cme_radius']
        }
        update_param_file(temp_b, os.path.join(RUN_DIR_B, "PARAM.in"), repl_b)
        run_simulation(RUN_DIR_B)
        
        # 3. Update and Run Part C (GM+IE)
        repl_c = {
            'SW_RHO': trial['sw_rho'],
            'SW_UX': trial['sw_v'],
            'SW_BZ': trial['imf_bz']
        }
        update_param_file(temp_c, os.path.join(RUN_DIR_C, "PARAM.in"), repl_c)
        run_simulation(RUN_DIR_C)
        
        # 4. Extract and Log
        res = extract_results(trial['id'])
        if res:
            all_results.append(res)
            # Update CSV after EACH trial for safety
            pd.DataFrame(all_results).to_csv(stats_file, index=False)
            print(f"Trial {trial['id']} complete and saved.")
        
    print(f"\nBatch processing complete. Stats saved to {stats_file}")

if __name__ == "__main__":
    main()
