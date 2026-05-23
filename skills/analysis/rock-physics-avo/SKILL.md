---
name: rock-physics-avo
skill_type: workflow
description: |
  Rock physics and AVO analysis workflow from well log preparation
  through elastic property calculation, fluid substitution, AVO
  modelling, and synthetic seismogram generation. Use when performing
  rock physics studies or AVO feasibility analysis.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Rock Physics, AVO, Gassmann, Fluid Substitution, Synthetics, Workflow]
dependencies: [lasio, welly, bruges, segyio]
complements: [lasio, welly, bruges, segyio, obspy]
workflow_role: analysis
---

# Rock Physics & AVO Workflow

End-to-end pipeline for rock physics analysis and AVO feasibility studies,
from well log preparation through elastic property calculation, Gassmann
fluid substitution, AVO modelling, and synthetic seismogram generation.

## Skill Chain

```text
lasio / welly          bruges                    segyio / obspy
[Well Log Prep]     --> [Rock Physics]         --> [Synthetics / Tie]
  |                      |                          |
  Load LAS/DLIS          Elastic moduli             Wavelet extraction
  QC & despike           Gassmann fluid sub         Reflectivity series
  Resample curves        AVO intercept/gradient     Convolve synthetic
  Extract Vp, Vs, rho    Backus averaging           Well-seismic tie
```

## Decision Points

| Task | Library | When to Use |
|------|---------|-------------|
| Load well logs | lasio / dlisio | Always the first step |
| Curve QC and management | welly | Multi-curve processing, despiking |
| Elastic moduli, AVO equations | bruges | Core rock physics calculations |
| Gassmann fluid substitution | bruges | Predict fluid replacement effects |
| Wavelet extraction from seismic | segyio + bruges | When tying to seismic |
| Synthetic seismogram | bruges | Generate reflectivity and convolve |
| Dispersion curves | disba | Surface wave rock physics |

## Step-by-Step Orchestration

### Stage 1: Well Log Preparation (lasio + welly)

```python
import lasio
import numpy as np
from welly import Well

# Load well with sonic, density, and shear sonic
las = lasio.read('well.las')
df = las.df().dropna()

# Extract elastic logs
depth = df.index.values
vp = 1e6 / df['DT'].values       # P-wave velocity (m/s) from sonic (us/ft)
vs = 1e6 / df['DTS'].values      # S-wave velocity (m/s) from shear sonic
rho = df['RHOB'].values * 1000   # Density (kg/m3) from g/cc

# QC: check ranges
assert np.all(vp > 1500) and np.all(vp < 7000), "Vp out of range"
assert np.all(vs > 500) and np.all(vs < 4000), "Vs out of range"
assert np.all(rho > 1500) and np.all(rho < 3200), "Density out of range"

# If no shear sonic, estimate from Vp
# Castagna mudrock line: Vs = 0.8621 * Vp - 1172.4 (m/s)
if 'DTS' not in df.columns:
    vs = 0.8621 * vp - 1172.4
    vs = np.maximum(vs, 300)  # Floor for shallow sediments
```

### Stage 2: Rock Physics Analysis (bruges)

```python
import bruges

# Elastic moduli from velocities
K = bruges.rockphysics.moduli.bulk(vp=vp, vs=vs, rho=rho)   # Bulk modulus
G = bruges.rockphysics.moduli.shear(vs=vs, rho=rho)          # Shear modulus
E = bruges.rockphysics.moduli.youngs(K=K, G=G)               # Young's modulus
nu = bruges.rockphysics.moduli.poissons(vp=vp, vs=vs)        # Poisson's ratio
AI = bruges.rockphysics.moduli.impedance(vp=vp, rho=rho)     # Acoustic impedance
SI = bruges.rockphysics.moduli.impedance(vp=vs, rho=rho)     # Shear impedance

# Vp/Vs ratio (key AVO indicator)
vp_vs = vp / vs
```

### Stage 3: Gassmann Fluid Substitution (bruges)

```python
# Gassmann fluid substitution
# Replace brine with gas in reservoir interval
phi = df['NPHI'].values  # Porosity

# Mineral and fluid properties
K_mineral = 36.6e9   # Quartz bulk modulus (Pa)
K_brine = 2.6e9      # Brine bulk modulus (Pa)
rho_brine = 1050     # Brine density (kg/m3)
K_gas = 0.02e9       # Gas bulk modulus (Pa)
rho_gas = 100        # Gas density (kg/m3)

# Dry rock modulus from saturated (reverse Gassmann)
K_sat = K.copy()
K_dry = bruges.rockphysics.fluidsub.vrh(
    volumes=[1-phi, phi],
    moduli=[K_mineral, K_brine]
)[0]

# Forward Gassmann: substitute gas for brine
K_sat_gas = bruges.rockphysics.fluidsub.gassmann(
    k_sat=K_sat, k_fl=K_brine, k_min=K_mineral,
    phi=phi, k_fl2=K_gas
)

# Updated density with gas
rho_gas_sat = rho - phi * rho_brine + phi * rho_gas

# Updated velocities
vp_gas = np.sqrt((K_sat_gas + 4/3 * G) / rho_gas_sat)
vs_gas = np.sqrt(G / rho_gas_sat)
```

### Stage 4: AVO Analysis (bruges)

```python
# AVO intercept and gradient (Shuey approximation)
# For a single interface between layers i and i+1
for i in range(len(vp) - 1):
    rc = bruges.reflection.shuey(
        vp1=vp[i], vs1=vs[i], rho1=rho[i],
        vp2=vp[i+1], vs2=vs[i+1], rho2=rho[i+1],
        theta=np.arange(0, 40, 1)
    )

# AVO classification from intercept (R0) and gradient (G)
# Class I:   R0 > 0, G < 0  (hard sand, dim with offset)
# Class II:  R0 ~ 0, G < 0  (near-zero, polarity reversal)
# Class III: R0 < 0, G < 0  (soft sand, bright with offset)
# Class IV:  R0 < 0, G > 0  (very soft, dim with offset)

# Zoeppritz exact for full offset range
rc_exact = bruges.reflection.zoeppritz(
    vp1=vp[i], vs1=vs[i], rho1=rho[i],
    vp2=vp[i+1], vs2=vs[i+1], rho2=rho[i+1],
    theta=np.arange(0, 50, 1)
)
```

### Stage 5: Synthetic Seismogram (bruges + segyio)

```python
# Create reflectivity series
rc_series = bruges.reflection.reflectivity(vp, rho)

# Create wavelet
duration = 0.128  # seconds
dt = 0.002        # sample rate (2ms)
wavelet = bruges.filters.ricker(duration=duration, dt=dt, f=25)

# Convolve to create synthetic
synthetic = np.convolve(rc_series, wavelet, mode='same')

# If tying to seismic, extract wavelet from seismic trace
import segyio
with segyio.open('seismic.sgy') as f:
    near_trace = f.trace[0]  # Nearest trace to well
    # Extract statistical wavelet from trace
    # Or use bruges.filters for analytic wavelets
```

## Common Pipelines

### AVO Feasibility Study
```
- [ ] Load well logs (Vp, Vs, Rho, porosity) with lasio
- [ ] QC logs: check ranges, despike, fill gaps
- [ ] If no Vs log: estimate from Castagna or Greenberg-Castagna
- [ ] Calculate elastic moduli and impedances with bruges
- [ ] Run Gassmann fluid substitution (brine to gas/oil)
- [ ] Compare Vp, Vs, density, impedance before/after fluid sub
- [ ] Compute AVO response at target interface (Shuey or Zoeppritz)
- [ ] Classify AVO response (Class I-IV)
- [ ] Generate synthetic seismograms for both fluid scenarios
- [ ] Plot AVO crossplot (intercept vs gradient)
```

### Well-Seismic Tie
```
- [ ] Load well logs and seismic trace at well location
- [ ] Create time-depth relationship from check shots or sonic
- [ ] Convert logs to time domain
- [ ] Extract wavelet from seismic (statistical or deterministic)
- [ ] Generate synthetic seismogram from reflectivity * wavelet
- [ ] Cross-correlate synthetic with seismic trace
- [ ] Adjust stretch/squeeze to optimize tie
- [ ] Report correlation coefficient
```

### Backus Averaging (Upscaling)
```
- [ ] Load thin-bed well logs at fine sampling (0.5 ft)
- [ ] Define averaging window (e.g., quarter wavelength at target frequency)
- [ ] Apply Backus averaging to get effective anisotropic elastic properties
- [ ] Compare fine-scale vs upscaled reflectivity
- [ ] Assess thin-bed tuning effects
```

## When to Use

Use the rock physics & AVO workflow when:

- Performing AVO feasibility studies for exploration prospects
- Running Gassmann fluid substitution to predict fluid effects
- Generating synthetic seismograms for well-seismic ties
- Calculating elastic properties from well logs
- Classifying AVO response at target horizons

Use individual domain skills when:
- Only loading well logs (use `lasio` alone)
- Only computing dispersion curves (use `disba` alone)
- Only creating wavelets or filters (use `bruges` alone)

## Common Issues

| Issue | Solution |
|-------|----------|
| No shear sonic log | Estimate Vs from Castagna mudrock line or Greenberg-Castagna |
| Gassmann gives unrealistic velocities | Check porosity and mineral modulus inputs; phi must be > 0 |
| Negative Poisson's ratio | Usually indicates bad Vs data; QC shear sonic |
| Poor well-seismic tie | Check time-depth relationship; try different wavelets |
| AVO effect too small | May be real; check impedance contrast and Vp/Vs ratio |
| Fluid sub in shales | Gassmann assumes connected pore space; not valid for shales |
