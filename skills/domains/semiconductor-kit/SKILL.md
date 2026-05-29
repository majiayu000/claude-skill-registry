---
name: semiconductor-kit
description: Semiconductor Kit (4 sub-skills: angular-effective-mass, band-gap, effective-mass, fermi-velocity)
---

# Semiconductor Kit

## Overview

This skill group covers essential semiconductor property calculations from first principles. It provides tools to extract band gaps (direct and indirect), carrier effective masses, and Fermi velocities from DFT band structures computed with Quantum ESPRESSO or VASP.

These properties are fundamental inputs for device modeling, materials screening, and understanding electronic behavior of semiconductors, semimetals, and Dirac materials. The workflows combine DFT eigenvalue calculations with numerical post-processing in Python.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Band Gap | `band-gap/` | Extract direct/indirect band gap from band structure or DOS. Scissor correction for DFT underestimation. QE and VASP parsers. |
| Effective Mass | `effective-mass/` | Carrier effective mass from band curvature via parabolic fitting near VBM/CBM. Full effective mass tensor. QE and VASP approaches. |
| Fermi Velocity | `fermi-velocity/` | Fermi velocity from band slope at Fermi level. Relevant for metals and Dirac materials (graphene, topological insulators). |

## Workflow Decision Guide

```
What semiconductor property do you need?

Band gap (direct/indirect, value in eV)?
  YES --> Use band-gap/ sub-skill
          Need accurate gap? Apply scissor correction or use hybrid functional.

Carrier effective mass (m*/m_e)?
  YES --> Use effective-mass/ sub-skill
          Need full tensor? Compute along multiple k-directions.

Fermi velocity (for metals/Dirac materials)?
  YES --> Use fermi-velocity/ sub-skill
          Best for graphene, topological surface states, metals.

Transport properties (Seebeck, conductivity)?
  YES --> See transport-properties/ skill group (BoltzTraP2)
```

## Common Prerequisites

- **Quantum ESPRESSO 7.5**: `pw.x`, `bands.x` available on PATH.
- **Pseudopotentials**: SSSP or PSlibrary pseudopotentials in `./pseudo/`.
- **Python environment**: pymatgen, ASE, numpy, scipy, matplotlib pre-installed. Install extras with `pip install seekpath sumo` as needed.
- **Band structure calculation**: Most sub-skills require a completed band structure calculation (SCF + bands NSCF along k-path). See `electronic-structure/band-structure/` skill for the full band structure workflow.
- **Structure files**: CIF, POSCAR, or built programmatically with pymatgen/ASE.
