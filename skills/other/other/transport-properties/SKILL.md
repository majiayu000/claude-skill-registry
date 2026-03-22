---
name: transport-properties
description: Transport Properties (2 sub-skills: boltzmann-transport, kpoints-transport)
---

# Transport Properties

## Overview

This skill group covers first-principles calculation of electronic transport properties using the Boltzmann transport equation (BTE) within the constant relaxation time approximation (CRTA). The workflow uses Quantum ESPRESSO for the underlying DFT calculation and BoltzTraP2 for solving the BTE. VASP-based workflows are also documented for sites with VASP access.

Transport properties computed include: Seebeck coefficient (thermopower), electrical conductivity (sigma/tau), electronic thermal conductivity (kappa_e/tau), power factor (S^2*sigma/tau), and the thermoelectric figure of merit ZT (when lattice thermal conductivity and relaxation time are provided externally).

The workflow logic follows the standard DFT+BoltzTraP2 pipeline: converge SCF on a coarse k-grid, compute eigenvalues on a very dense uniform k-grid (NSCF), then feed the eigenvalues into BoltzTraP2 for Fourier interpolation and transport coefficient evaluation.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Boltzmann Transport | `boltzmann-transport/` | Full BoltzTraP2 workflow: SCF, dense-k NSCF, BoltzTraP2 interpolation, Seebeck/sigma/kappa/PF/ZT as functions of temperature and carrier concentration |
| K-Points for Transport | `kpoints-transport/` | Generate and converge dense KPOINTS grids for transport calculations. Convergence testing methodology for transport properties. |

## Workflow Decision Guide

```
Want Seebeck coefficient, conductivity, or thermoelectric properties?
  YES --> Do you have a converged dense k-grid?
            YES --> Go to boltzmann-transport/ sub-skill (BoltzTraP2 analysis)
            NO  --> Go to kpoints-transport/ sub-skill first (generate dense grid)
                    Then boltzmann-transport/
  NO  --> Want effective mass or band gap?
            YES --> See semiconductor-kit/ skill group
            NO  --> Want phonon-limited transport (beyond CRTA)?
                    YES --> See electron-phonon/elph-coupling/ skill (EPW)
```

## Common Prerequisites

- **Quantum ESPRESSO 7.5**: `pw.x` must be available on PATH.
- **BoltzTraP2**: Install via `pip install BoltzTraP2`. Provides Fourier interpolation of band energies and BTE solver.
- **Pseudopotentials**: QE calculations require pseudopotential files. Sub-skills show how to download SSSP pseudopotentials.
- **Structure files**: Start from CIF, POSCAR, or build with pymatgen/ASE.
- **Python environment**: pymatgen, ASE, numpy, scipy, matplotlib are pre-installed.
- **Dense k-grids**: Transport properties require much denser k-meshes (40x40x40+) than total energy or DOS calculations. The kpoints-transport sub-skill covers convergence testing.
