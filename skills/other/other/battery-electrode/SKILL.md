---
name: battery-electrode
description: Battery Electrode Analysis (2 sub-skills: intercalation-voltage, ion-diffusion)
---

# Battery Electrode Analysis

Computational workflows for battery electrode characterization: voltage profiles, ion transport, and electrochemical stability.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Intercalation Voltage | `intercalation-voltage/` | Average and step voltage profiles for intercalation cathodes/anodes. Convex hull of Li_xMO compositions. Methods: ASE+MACE (screening) or QE DFT+U (publication). |
| Ion Diffusion | `ion-diffusion/` | Li-ion (or Na, K, Mg) diffusion coefficients and migration barriers. AIMD with Arrhenius analysis or NEB for single-barrier. Methods: ASE+MACE MD or ASE+MACE NEB. |

## Method Decision Guide

```
What electrode property do you need?

Voltage profile (average V, step V, capacity)?
  --> intercalation-voltage/
  Quick screening --> ASE + MACE
  Publication quality --> QE DFT+U

Ion transport (diffusion coefficient, migration barrier, activation energy)?
  --> ion-diffusion/
  Single migration barrier --> NEB (Method B in ion-diffusion/)
  Full diffusion coefficient D(T) and Ea --> AIMD + Arrhenius (Method A in ion-diffusion/)

Both voltage and transport for a new cathode material?
  --> Run intercalation-voltage/ first to confirm electrochemical viability,
      then ion-diffusion/ for rate capability assessment.
```

## Common Prerequisites

- **Structures**: Start from experimental CIF or Materials Project. Use pymatgen to build supercells and enumerate Li orderings.
- **DFT+U**: Transition metal oxide cathodes (LiCoO2, LiFePO4, LiMn2O4, etc.) require Hubbard U corrections. See `dft-corrections/hubbard-u/` for U value tables and self-consistent U calculation with hp.x.
- **Python packages**: pymatgen, ASE, mace-torch, numpy, scipy, matplotlib are pre-installed. Install extras with `pip install pymatgen-analysis-diffusion` for advanced diffusion analysis.

## Typical Voltage Ranges for Common Cathodes

| Material | Working Ion | Voltage vs Li/Li+ (V) | Capacity (mAh/g) |
|----------|-------------|------------------------|-------------------|
| LiCoO2 (LCO) | Li | 3.7 -- 4.2 | ~140 |
| LiFePO4 (LFP) | Li | ~3.4 (flat) | ~170 |
| LiMn2O4 (LMO) | Li | 3.9 -- 4.1 | ~120 |
| LiNi0.33Mn0.33Co0.33O2 (NMC111) | Li | 3.6 -- 4.3 | ~160 |
| LiNi0.8Mn0.1Co0.1O2 (NMC811) | Li | 3.6 -- 4.3 | ~200 |
| Li4Ti5O12 (LTO, anode) | Li | ~1.55 (flat) | ~175 |
| Graphite (anode) | Li | 0.01 -- 0.2 | ~372 |
