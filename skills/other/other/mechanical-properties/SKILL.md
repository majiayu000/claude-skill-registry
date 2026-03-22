---
name: mechanical-properties
description: Mechanical Properties (5 sub-skills: angular-mechanics, elastic-constants, energy-strain-method, equation-of-state, stress-strain-method)
---

# Mechanical Properties

## Overview

This skill group covers calculations of mechanical properties of crystalline materials. Two main approaches are available:

1. **MACE (via ASE)** -- Fast ML-potential-based calculations. Good for screening, rapid estimation of elastic constants and equations of state. Seconds to minutes per structure.
2. **Quantum ESPRESSO (QE)** -- Full DFT. Required for publication-quality results and when MACE accuracy is insufficient for the system of interest.

Both approaches follow the same physical workflow (inspired by atomate2's elastic and EOS flows): relax the structure, apply systematic deformations, compute response properties, and fit constitutive models.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Elastic Constants | `elastic-constants/` | Full elastic tensor via stress-strain method, Voigt-Reuss-Hill moduli, stability criteria |
| Equation of State | `equation-of-state/` | E-V curves, Birch-Murnaghan / Vinet / Murnaghan EOS fits, bulk modulus and its pressure derivative |

## Method Decision Guide

```
Need publication-quality elastic constants?
  YES --> Use Quantum ESPRESSO DFT (stress-strain with pw.x)
  NO  --> Is the material well-represented by MACE training data?
            YES --> Use ASE + MACE (fast, ~seconds)
            NO  --> Use Quantum ESPRESSO DFT
```

## Common Prerequisites

- **Structure**: Start from a CIF, POSCAR, or Materials Project query. Symmetrize before deformation workflows to reduce the number of independent deformations.
- **Pseudopotentials**: QE calculations need pseudopotential files (SSSP library recommended).
- **Python packages**: pymatgen, ASE, mace-torch, numpy, scipy, matplotlib are pre-installed.
