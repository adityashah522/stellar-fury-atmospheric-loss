# Surviving Stellar Fury

**A Million-Year Analysis of Atmospheric Loss from Exoplanets Caused by Interplanetary Shocks**

This repository contains a comparative numerical simulation and analysis project studying atmospheric escape for Mars and Earth under solar and interplanetary driving conditions. The research workflow combines the SWMF and PLUTO simulation frameworks, Python post-processing, ensemble analysis, and long-term atmospheric-loss extrapolation.

## Scientific Scope

- Part A: solar wind and corona simulations
- Part B: interplanetary shock and CME propagation
- Part C: planetary magnetosphere and atmospheric escape
- Ensemble analysis: statistical comparison across randomized solar-wind and shock conditions
- Long-duration analysis: million-year extrapolation of cumulative atmospheric mass loss

> The analysis scripts contain research-model assumptions and extrapolations. Results should be interpreted as numerical estimates, not directly as observational measurements.

## Repository Layout

```text
.
├── PARAM.A.template       Solar-wind parameter template
├── PARAM.B.template       Shock/CME parameter template
├── PARAM.C.template       Planetary escape parameter template
├── run_full_ensemble.py   Multi-trial ensemble driver
├── sim_results_analysis.py Statistical report generator
├── generate_mean_timeseries.py  Ensemble time-series visualizer
├── sim_results/           Statistical results and published figures
├── Data_PostProcessing/   Output-merging and visualization utilities
├── Docs/                  Scientific summaries and parameter documentation
├── PartC_Atmospheric_Escape/ Earth and Mars escape scripts and data
├── PartC_AtmosphericEscape_Simulation/ SWMF escape simulation inputs
├── SWMF_core/             Bundled SWMF source workspace
└── PLUTO_core/            Bundled PLUTO source workspace
```

## Data and Analysis Workflow

1. Configure one of the parameter templates for a simulation trial.
2. Run the applicable SWMF or PLUTO input case.
3. Extract the simulation logs or output quantities.
4. Run `run_full_ensemble.py` to manage ensemble trials and generated statistics.
5. Run `sim_results_analysis.py` to create a detailed statistical report.
6. Run `generate_mean_timeseries.py` to generate mean and spread plots.

Example:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python sim_results_analysis.py
python generate_mean_timeseries.py
```

Paths in the scripts may be Linux-specific or workstation-specific. Update them under `__main__` blocks or replace them with command-line configuration before running on another system.

## Dependencies

Python analysis uses NumPy, pandas, Matplotlib, and SciPy. The numerical simulation components require MPI, Fortran/C/C++ toolchains, and framework-specific dependencies documented within SWMF and PLUTO.

## Reproducibility Notes

- Seeded random sampling is used where implemented.
- Ensemble scripts should be treated as workstation automation rather than turnkey HPC workflows.
- Generated restart files, cached environments, test outputs, and local editor settings are excluded through `.gitignore`.

## Credits

### Project author

- **Aditya Shah** — project design, simulations, post-processing, ensemble workflow, and scientific analysis.
- GitHub: https://github.com/adityashah522

### SWMF

The **Space Weather Modeling Framework (SWMF)** was developed by the University of Michigan and collaborators. This repository includes a source workspace for reproducibility and configuration context. SWMF is distributed under the Apache License 2.0; see `SWMF_core/SWMF/LICENSE.txt`.

### PLUTO

**PLUTO** is a modular astrophysical gas-dynamic and magnetohydrodynamic code developed by Andrea Mignone and collaborators. It is included here for the atmospheric-escape modeling configuration and retains its upstream GPL license notice in `PLUTO_core/PLUTO/COPYING`.

### Scientific tooling

Analysis and visualization rely on NumPy, pandas, Matplotlib, SciPy, and the Python ecosystem.

Please cite the relevant upstream SWMF, PLUTO, and scientific software papers when using this work in publications. The project author and original framework authors must be credited for their respective contributions.

## License

The project-specific scripts and documentation are the work of Aditya Shah unless otherwise noted. Third-party simulation frameworks retain their original licenses:

- SWMF: Apache License 2.0
- PLUTO: GNU General Public License v2

A repository-level license should not be interpreted as superseding nested third-party licenses. If you intend to redistribute this repository, review the framework source licenses and applicable data restrictions.
