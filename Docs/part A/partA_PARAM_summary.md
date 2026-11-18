# PARAM.in Summary and Star/Planet Customization Guide

## Overview
This document provides a concise description of every section in the **`PARAM.in`** file used for the Part A Solar Wind simulation (Solar Corona + Inner Heliosphere). It also highlights the parameters that typically need to be adjusted when changing the stellar or planetary characteristics (e.g., a different G‑type star, a different planetary magnetosphere, or a different orbital distance).

---

## 1. General Description
- **File purpose**: Defines the simulation configuration for the SWMF framework, including component mapping, time settings, plasma properties, heating models, grid geometry, boundary conditions, output options, and coupling between components.
- **Components used**: `SC` (Solar Corona) and `IH` (Inner Heliosphere). Both are run on the same MPI rank range (processor 0) in this minimal example.

---

## 2. Component Map
```text
#COMPONENTMAP
SC 0 -1 1   ! SC runs on all available ranks (stride 1)
IH 0 -1 1   ! IH runs on the same ranks as SC
```
**What to change**: If you want to run the components on separate processor groups, modify the `First` and `Last` values and optionally the `Stride`. For a larger run you would typically allocate a contiguous block of ranks for each component.

---

## 3. Time Settings
```text
#TIMEACCURATE
F   ! IsTimeAccurate – use steady‑state mode (set to T for time‑accurate runs)

#STARTTIME
2014    iYear
09      iMonth
10      iDay
14      iHour
00      iMinute
00      iSecond
0.0     FracSecond
```
**Star/Planet dependent**:
- **Start date/time** – adjust to the desired epoch of the simulation (e.g., observation date or a specific stellar rotation phase).
- **`IsTimeAccurate`** – set to `T` if you need a time‑dependent simulation (e.g., to study transient events).

---

## 4. Restart Options
```text
#SAVERESTART
T   DoSaveRestart
100 DnSaveRestart   ! Save every 100 output intervals
-1.0 DtSaveRestart  ! Save every timestep (negative disables time‑based saving)
```
**What to change**: Frequency of restart files (`DnSaveRestart`) can be increased for longer runs or decreased for quick debugging.

---

## 5. Solar Corona (SC) Section
### 5.1 Grid and Geometry
```text
#GRIDBLOCKALL
2000   MaxBlock

#COORDSYSTEM
HGR    TypeCoordSystem
```
- **`MaxBlock`**: Maximum number of AMR blocks. Increase for higher resolution.
- **`TypeCoordSystem`**: `HGR` = spherical logarithmic radial grid (good for solar corona).

### 5.2 Plasma Properties
```text
#PLASMA
1.0    FluidMass [amu]          ! Average ion mass (change for different composition)
1.0    IonCharge [e]            ! Average ion charge (e.g., 2 for He++)
1.0    ElectronTemperatureRatio ! Ratio Te/Ti (often set to 1)
```
**Star/Planet dependent**:
- **`FluidMass`** – adjust if the wind is dominated by heavier ions (e.g., for a metal‑rich star).
- **`IonCharge`** – change for different ionization states.

### 5.3 Harmonic Grid (Magnetogram)
```text
#HARMONICSGRID
1.0    rMagnetogram
25     rSourceSurface
T      IsLogRadius
180    MaxOrder
400    nR
180    nLon
90     nLat
```
- **`rSourceSurface`**: Height of the source surface (in stellar radii). Typical solar value ≈ 2.5 R★; adjust for more/less extended coronae.
- **`MaxOrder`**, **`nR`**, **`nLon`**, **`nLat`**: Resolution of the spherical harmonic expansion – increase for higher fidelity.

### 5.4 Energy Input (Poynting Flux)
```text
#POYNTINGFLUX
1.0e6  PoyntingFluxPerBSi [J/m^2/s/T]
```
**Star dependent**: Scale with stellar magnetic field strength. For a more active G‑type star, increase this value (e.g., 2‑5 × 10⁶).

### 5.5 Coronal Heating
```text
#CORONALHEATING
turbulentcascade   TypeCoronalHeating
1.5e5   LperpTimesSqrtBSi   ! Correlation length scaling (∝ stellar radius)
0.0     rMinWaveReflection
F       UseReynoldsDecomposition
```
**What to change**:
- **`TypeCoronalHeating`** – options: `exponential`, `unsignedflux`, `alfvenwavedissipation`, `turbulentcascade`, `usmanov`. Choose based on the heating model you wish to employ.
- **`LperpTimesSqrtBSi`** – typically scales with stellar radius; increase for larger stars.

### 5.6 Heat Partitioning
```text
#HEATPARTITIONING
stochasticheating   TypeHeatPartitioning
0.21   StochasticExponent   ! Controls how heating scales with magnetic field
0.18   StochasticAmplitude  ! Overall heating amplitude
```
**Star dependent**: Adjust `StochasticExponent` and `StochasticAmplitude` to match observed wind acceleration for different activity levels.

### 5.7 Radiative Cooling (disabled in this minimal setup)
```text
#RADIATIVECOOLING
F   UseRadCooling   ! Set to T to enable radiative cooling
```
**Planet/Star dependent**: Enable (`T`) for cooler stars where line cooling is important; keep disabled (`F`) for hot coronae where conductive cooling dominates.

### 5.8 Grid Geometry (removed – optional)
The original file referenced `SC/Param/grid_awsom.dat`. This file is not required for the current configuration; the spherical grid is defined by the harmonic parameters above.

### 5.9 Domain Extent and Limits
```text
#GRID
2   nRootBlock1
2   nRootBlock2
1   nRootBlock3
-100.0   xMin   ! Domain size in stellar radii (negative = left side)
 100.0   xMax
-100.0   yMin
 100.0   yMax
-100.0   zMin
 100.0   zMax

#LIMITRADIUS
1.0   rMin   ! Inner boundary (stellar surface)
24.0  rMax   ! Outer radius of SC component (in stellar radii)
```
**Star dependent**:
- **`rMax`** – extend if you need a larger corona (e.g., very active stars may require > 30 R★).
- **Domain size (`xMin`/`xMax` …)** – increase for larger simulation boxes.

### 5.10 AMR Region
```text
#AMRREGION
InnerShell   NameRegion
shell0       StringShape
1.0          RadiusInner   ! Refinement starts at the stellar surface
1.7          Radius        ! Outer radius of refined shell (in stellar radii)
```
**What to change**: Adjust `RadiusInner` and `Radius` to control where higher resolution is needed (e.g., around active regions).

### 5.11 Grid Resolution & AMR Controls
```text
#GRIDRESOLUTION
6.0   Resolution   ! Base cell size (in stellar radii)
initial   StringShape

#DOAMR
T   DoAmr
5   DnAmr          ! AMR refinement every 5 output intervals
-1.0 DtAmr        ! Time‑based AMR disabled (negative)
T   IsStrictAmr
```
**Star dependent**: Reduce `Resolution` for finer grids; increase `DnAmr` for less frequent AMR.

### 5.12 Time Stepping & Numerical Scheme
```text
#TIMESTEPPING
2   nStage
0.8 CflExpl

#SCHEME
2   nOrder
Linde   TypeFlux
minmod  TypeLimiter
```
**What to change**: For more stringent stability you may lower `CflExpl` or increase `nStage`.

### 5.13 Limiters & Minimum Values
```text
#LIMITER
T   UseLogRhoLimiter
T   UseLogPLimiter
F   UseRhoRatioLimiter

#MINIMUMTEMPERATURE
5e4   TminDim  [K]
5e4   TeMinDim [K]

#MINIMUMPRESSURE
1E-9   pMinDim
1E-9   PeMinDim
```
**Star dependent**: Adjust `TminDim` for hotter or cooler coronae; modify pressure floors for different plasma beta regimes.

### 5.14 Outer Boundary Conditions
```text
#OUTERBOUNDARY
user   TypeBc1   ! Velocity / magnetic field (user‑defined)
float  TypeBc2   ! Density
periodic TypeBc3
periodic TypeBc4
periodic TypeBc5
periodic TypeBc6
```
**Planet dependent**: If coupling to a planetary magnetosphere, you may replace `user` with `fixed` or `open` conditions that match the planetary wind.

### 5.15 Plot Output
```text
#SAVEPLOT
4   nPlotFile
x=0 VAR idl_ascii   StringPlot
10  DnSavePlot
-1.0 DtSavePlot
-1.0 DxSavePlot
{MHD} b1x b1y b1z te ti dphi   NameVars
{default}   NamePars
... (similar blocks for y=0, z=0, LOS)
```
**What to change**: Add or remove variables in `NameVars` depending on diagnostics you need (e.g., include `rho` for density, `b2x` for magnetic field components, etc.).

---

## 6. Inner Heliosphere (IH) Section
The IH component mirrors many of the SC settings but with its own grid and boundary configuration.

### 6.1 Grid Block and Coordinate System
```text
#GRIDBLOCKALL
4000   MaxBlock

#COORDSYSTEM
HGC    TypeCoordSystem   ! HGC = spherical logarithmic radial grid for IH
```
- **`MaxBlock`**: Larger than SC because IH often covers a larger volume.

### 6.2 Plasma
```text
#PLASMA
1.0    FluidMass [amu]
1.0    IonCharge [e]
1.0    ElectronTemperatureRatio
```
Same notes as SC.

### 6.3 Domain Extent (IH covers a larger region)
```text
#GRID
1   nRootBlock1
1   nRootBlock2
1   nRootBlock3
-250.0   xMin   ! Extends to ±250 R★ (adjust for planetary distance)
 250.0   xMax
-250.0   yMin
 250.0   yMax
-250.0   zMin
 250.0   zMax
```
**Planet dependent**: Increase these limits if you need to place a planet farther out (e.g., Earth‑like orbit ≈ 215 R★ for the Sun).

### 6.4 AMR Region (OuterShell)
```text
#AMRREGION
OuterShell   NameRegion
shell0       StringShape
18.0   RadiusInner   ! Start refinement at 18 R★
21.0   Radius       ! Outer limit of refined shell
```
Adjust `RadiusInner`/`Radius` to focus resolution around the planetary orbit.

### 6.5 Buffer Grid (inner boundary handling)
```text
#INNERBOUNDARY
buffergrid   TypeBcBody

#BUFFERGRID
5   nRBuff
240 nLonBuff
120 nLatBuff
18.0 RBuffMin
20.0 RBuffMax
0.0  LonBuffMin
360.0 LonBuffMax
-90.0 LatBuffMin
90.0 LatBuffMax
```
**Planet dependent**: Modify `RBuffMin`/`RBuffMax` to set the inner buffer region size (e.g., to avoid the planetary magnetosphere intersecting the inner boundary).

### 6.6 Outer Boundary (IH)
```text
#OUTERBOUNDARY
float TypeBc1
float TypeBc2
float TypeBc3
float TypeBc4
float TypeBc5
float TypeBc6
```
Typically set to `float` (open) for solar wind outflow.

### 6.7 Coronal Heating & Heat Partitioning (same as SC)
```text
#CORONALHEATING
turbulentcascade   TypeCoronalHeating
1.5e5   LperpTimesSqrtBSi
0.0     rMinWaveReflection
F       UseReynoldsDecomposition

#HEATPARTITIONING
stochasticheating   TypeHeatPartitioning
0.21   StochasticExponent
0.18   StochasticAmplitude
```
Same notes as SC.

### 6.8 Numerical Scheme, Limits, etc.
Identical to SC (order, limiter, minimum temperature/pressure, etc.).

---

## 7. Component Coupling
```text
#COUPLE1
SC   NameSource
IH   NameTarget
1    DnCouple   ! Coupling frequency (output intervals)
-1.0 DtCouple  ! Time‑based coupling (negative disables)
```
**What to change**: Adjust `DnCouple` to control how often the SC and IH exchange boundary data. For more frequent coupling (e.g., during transients) set a smaller value.

---

## 8. Simulation Termination
```text
#STOP
100   MaxIter   ! Maximum number of global iterations
-1.0  TimeMax   ! No explicit time limit (negative disables)
```
**What to change**: Set `MaxIter` or `TimeMax` to stop the run after a desired physical time or number of iterations.

---

## 9. Quick Checklist for Changing Star/Planet Parameters
| Section | Parameter | Typical Star/Planet Dependency | Recommended Action |
|---------|-----------|--------------------------------|-------------------|
| `#STARTTIME` | Date/Time | Observation epoch or stellar rotation phase | Update to desired start date/time |
| `#PLASMA` | `FluidMass`, `IonCharge` | Stellar wind composition (e.g., H‑rich vs. metal‑rich) | Adjust values accordingly |
| `#HARMONICSGRID` | `rSourceSurface`, `MaxOrder`, `nR`, `nLon`, `nLat` | Size of the corona, magnetic field complexity | Increase for more active stars |
| `#POYNTINGFLUX` | `PoyntingFluxPerBSi` | Magnetic activity level | Scale up for more active stars |
| `#CORONALHEATING` | `LperpTimesSqrtBSi`, `TypeCoronalHeating` | Heating model & stellar radius | Adjust correlation length and model type |
| `#HEATPARTITIONING` | `StochasticExponent`, `StochasticAmplitude` | Turbulent heating efficiency | Tune to match observed wind speeds |
| `#LIMITRADIUS` | `rMax` | Extent of the corona | Increase for larger/extended coronae |
| `#GRID` (domain extents) | `xMin/xMax`, `yMin/yMax`, `zMin/zMax` | Desired simulation box size (e.g., to include a planet) | Expand for farther planetary orbits |
| `#AMRREGION` | `RadiusInner`, `Radius` | Where you need higher resolution (active regions, planetary magnetosphere) | Adjust to focus on region of interest |
| `#OUTERBOUNDARY` (IH) | Boundary type (`float`, `user`, `fixed`) | Interaction with planetary wind or interstellar medium | Choose appropriate BC for planetary coupling |
| `#COUPLE1` | `DnCouple` | Frequency of SC↔IH data exchange | Reduce for more tightly coupled runs |
| `#STOP` | `MaxIter` / `TimeMax` | Desired simulation length | Set to reach steady state or specific event time |

---

## 10. Final Remarks
- After editing any of the starred parameters, **re‑run** `Scripts/TestParam.pl -n=<num_procs> <run_dir>/PARAM.in` to verify the file again.
- When you move to a full production run, remember to enable the appropriate **grid files** (`#GRIDGEOMETRY` or lookup tables) if you need a custom magnetogram or radiative cooling.
- For planetary simulations, you will typically add a **planetary component** (e.g., `GM` or `IE`) and modify the `#COMPONENTMAP` and boundary conditions accordingly.

Feel free to copy this document to your project documentation folder (e.g., `Docs/partA_PARAM_summary.md`). It should serve as a quick reference whenever you need to adapt the simulation to a different star or planetary system.

---

*Document generated by Antigravity.*
