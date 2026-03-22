---
name: electron-phonon
description: Electron-Phonon Properties (4 sub-skills: deformation-potential, electronic-transport, elph-coupling, superconductivity)
---

# Electron-Phonon Properties

Skills for computing electron-phonon interactions and related transport properties using Quantum ESPRESSO and Python post-processing tools.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Electron-Phonon Coupling | `elph-coupling/` | Full QE workflow for electron-phonon coupling constant lambda, Eliashberg spectral function alpha2F(omega), and superconducting Tc via McMillan/Allen-Dynes formula |
| Electronic Transport | `electronic-transport/` | BoltzTraP2-based workflow for Seebeck coefficient, electrical conductivity, electronic thermal conductivity, power factor, and ZT from QE band structures on dense k-grids |

## General Notes

- All workflows start from a converged QE SCF calculation. Ensure pseudopotentials, ecutwfc, and k-grid are well converged before proceeding.
- Electron-phonon calculations require **metallic systems** (or heavily doped semiconductors treated as metals). Use appropriate smearing.
- Transport calculations via BoltzTraP2 work for both metals and semiconductors but require extremely dense k-grids.
- These are computationally demanding calculations. Start with coarse grids to verify the workflow, then increase to production quality.
