---
name: electronic-structure
description: Electronic Structure Calculations (8 sub-skills: band-structure, convergence-testing, density-of-states, inverse-participation-ratio, projected-dos, scf-relax, spatially-resolved-dos, vasp-bands)
---

# Electronic Structure Calculations

## Overview

This skill group covers first-principles and machine-learning-potential-based electronic structure calculations. Two main approaches are available:

1. **MACE (via ASE)** -- Fast, ML-potential-based. Good for geometry optimization and quick screening. Cannot produce electronic properties (band structure, DOS) because it is a force field, not an electronic structure method.
2. **Quantum ESPRESSO (QE)** -- Full DFT. Required for any electronic property (band structure, DOS, charge density, etc.) and for publication-quality total energies.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| SCF and Relaxation | `scf-relax/` | Self-consistent field calculations and structure relaxation (MACE quick relax or QE SCF/vc-relax) |
| Band Structure | `band-structure/` | Electronic band structure along high-symmetry k-paths |
| Density of States | `density-of-states/` | Total and projected density of states (DOS / PDOS) |

## Method Decision Guide

```
Need electronic properties (bands, DOS, charge density)?
  YES --> Use Quantum ESPRESSO DFT
  NO  --> Is high accuracy required (publication, reaction energies)?
            YES --> Use Quantum ESPRESSO DFT (SCF or vc-relax)
            NO  --> Use ASE + MACE for fast relaxation / screening
```

## Common Prerequisites

- **Pseudopotentials**: QE calculations require pseudopotential files. All sub-skills show how to download SSSP pseudopotentials automatically.
- **Structure files**: Start from a CIF, POSCAR, or build with pymatgen/ASE. All sub-skills show how to convert formats.
- **Python environment**: pymatgen, ASE, MACE-torch, numpy, scipy, matplotlib are pre-installed. Install extras with `pip install seekpath sumo phonopy` as needed.
