---
name: catalysis-electrochem
description: Catalysis and Electrochemistry Toolkit (6 sub-skills: band-center, imaginary-freq-correction, implicit-solvation, neb-analysis, reaction-kinetics, thermal-corrections)
---

# Catalysis and Electrochemistry Toolkit

## Overview

This skill group covers computational catalysis and electrochemistry workflows corresponding to VASPKIT menu 05 (tasks 501-509). It provides tools for computing thermodynamic corrections to DFT energies, analyzing reaction pathways (NEB), extracting d-band descriptors for catalytic activity, and applying transition state theory for reaction kinetics.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Thermal Corrections | `thermal-corrections/` | Zero-point energy, thermal corrections for adsorbates and gas-phase molecules (VASPKIT 501-502). Uses ASE thermochemistry, ideal gas, and harmonic approximations. |
| NEB Analysis | `neb-analysis/` | NEB path analysis, converting NEB paths to PDB trajectories, interpolating NEB images (VASPKIT 504-505). Uses ASE NEB, pymatgen, QE NEB. |
| d-Band Center | `band-center/` | d-band center calculation from projected DOS (VASPKIT 503). Parse QE/VASP PDOS data for catalytic activity descriptors. |
| Reaction Kinetics | `reaction-kinetics/` | Imaginary frequency correction (VASPKIT 507), half-life calculation (VASPKIT 509). Transition state theory rate constants and kinetic analysis. |
| Implicit Solvation | `implicit-solvation/` | Implicit solvation models for electrode-electrolyte interfaces. VASPsol, QE+Environ, and ASE-based Born/GBSA corrections. Solvation free energies, pKa, electrochemical reaction energetics with solvent effects. |

## Method Decision Guide

```
Need free energy corrections for reaction energetics?
  YES --> thermal-corrections/ (ZPE + thermal + entropy from vibrational frequencies)

Need to analyze an NEB calculation result?
  YES --> neb-analysis/ (extract energies, interpolate images, convert to trajectory)

Need a catalytic activity descriptor?
  YES --> band-center/ (d-band center from PDOS data)

Need reaction rate constants or half-lives?
  YES --> reaction-kinetics/ (transition state theory, Eyring equation)

Need to correct for imaginary frequencies at a transition state?
  YES --> reaction-kinetics/ (project out imaginary mode from ZPE sum)

Need solvation effects for electrode-electrolyte interfaces?
  YES --> implicit-solvation/ (VASPsol, QE+Environ, or Born/GBSA corrections)

Need solvation free energies or pKa values?
  YES --> implicit-solvation/ (implicit solvent models, Born model for ions)
```

## Common Prerequisites

- **ASE**: Thermochemistry modules (`ase.thermochemistry`), NEB tools
- **pymatgen**: Structure manipulation, DOS parsing
- **MACE**: Fast frequency calculations via finite displacements
- **Quantum ESPRESSO**: DFT-quality frequencies via DFPT or finite differences
- **numpy, scipy, matplotlib**: Numerical analysis and plotting
