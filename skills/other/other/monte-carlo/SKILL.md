---
name: monte-carlo
description: Monte Carlo Simulations (5 sub-skills: adsorption-isotherm, gas-adsorption, gas-separation, gcmc-simulation, pore-analysis)
---

# Monte Carlo Simulations

Grand Canonical Monte Carlo (GCMC) and related ensemble simulations for gas adsorption, mixture separation, and thermodynamic property estimation in porous materials (MOFs, zeolites, covalent organic frameworks).

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Gas Adsorption | `gas-adsorption/` | GCMC adsorption isotherms, Henry coefficients, mixture selectivity, and heat of adsorption using RASPA3 |

## Method Decision Guide

```
What Monte Carlo property do you need?

Single-component adsorption isotherm (loading vs pressure)?
  --> gas-adsorption/  (GCMC at multiple pressures)

Henry coefficient / heat of adsorption at infinite dilution?
  --> gas-adsorption/  (Widom insertion method)

Mixture selectivity (e.g., CO2/N2)?
  --> gas-adsorption/  (multi-component GCMC)

Diffusion in pores?
  --> Consider MD instead (molecular-dynamics/ in thermal-properties/)
  --> Or use RASPA3 with MSD tracking in NVT/NVE ensemble

Framework: need charges for polar molecules (CO2, H2O)?
  --> gas-adsorption/ covers charge assignment strategies
```

## Tool

All Monte Carlo simulations use **RASPA3** (`raspa3` binary). RASPA3 uses JSON-based input files (`simulation.json`) rather than the legacy RASPA2 text format. Official examples are at `/usr/share/raspa3/examples/`.
