---
name: ferroelectric
description: Ferroelectric Properties (5 sub-skills: born-effective-charge, dielectric-tensor, ferroelectric-switching, piezoelectric, polarization)
---

# Ferroelectric Properties

## Overview

This skill group covers first-principles calculations of ferroelectric properties using Quantum ESPRESSO. The workflow follows the modern theory of polarization: relax both the centrosymmetric (nonpolar) reference and the ferroelectric (polar) phase, interpolate between them, and compute the Berry phase polarization along the switching path to obtain the spontaneous polarization. Born effective charges provide a complementary local probe of polar instability.

The workflow logic mirrors atomate2's `FerroelectricMaker`: relax polar and nonpolar endpoints, interpolate structures, compute polarization at each image, and perform branch-resolved polarization analysis.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Spontaneous Polarization (Berry Phase) | `polarization/` | Berry phase calculation of the spontaneous polarization difference between polar and nonpolar phases via QE `pw.x` with `lberry=.true.` |
| Born Effective Charges | `born-effective-charge/` | Born effective charge tensors Z* and high-frequency dielectric tensor via QE `ph.x` with `epsil=.true.` at Gamma |

## Workflow Decision Guide

```
Want the macroscopic spontaneous polarization (C/m^2)?
  YES --> Use polarization/ sub-skill (Berry phase along interpolation path)
  NO  --> Want Born effective charge tensors Z* or dielectric tensor?
            YES --> Use born-effective-charge/ sub-skill (ph.x at Gamma)
            NO  --> Want both? Run born-effective-charge first (lighter),
                    then polarization (heavier but gives the full P_s)
```

## Common Prerequisites

- **Pseudopotentials**: QE calculations require pseudopotential files. Sub-skills show how to download SSSP pseudopotentials.
- **Structure files**: Need both a polar and a centrosymmetric reference structure (CIF, POSCAR, or built with pymatgen/ASE).
- **Python environment**: pymatgen, ASE, numpy, scipy, matplotlib are pre-installed.
- **Quantum ESPRESSO 7.5**: pw.x and ph.x must be available on PATH.
