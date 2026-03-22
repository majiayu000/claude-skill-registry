---
name: surface-energy
description: Surface Energy Calculations (2 sub-skills: surface-energy-calc, wulff-construction)
---

# Surface Energy Calculations

## Overview

This skill group covers the calculation of surface energies and the prediction of equilibrium crystal shapes via the Wulff construction. Surface energies quantify the thermodynamic cost of cleaving a crystal along a given Miller plane and are fundamental to understanding crystal growth, catalysis, nanoparticle morphology, and interface stability.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Surface Energy Calculation | `surface-energy-calc/` | Compute surface energy for a given facet using MACE (fast) or QE DFT (accurate). Convergence testing vs slab thickness and vacuum. |
| Wulff Construction | `wulff-construction/` | Predict equilibrium crystal shape from surface energies of multiple facets using pymatgen WulffShape. |

## Method Decision Guide

```
Need surface energy for one specific facet?
  YES --> surface-energy-calc/ (Method A: MACE for screening, Method B: QE for accuracy)
Need equilibrium crystal shape?
  YES --> First compute surface energies for all relevant facets (surface-energy-calc/)
          Then build Wulff shape (wulff-construction/)
Need nanoparticle morphology prediction?
  YES --> wulff-construction/ (gives dominant facets, area fractions, shape factor)
Quick screening of many facets?
  YES --> surface-energy-calc/ Method A (MACE, seconds per facet)
Publication-quality surface energy?
  YES --> surface-energy-calc/ Method B (QE DFT, minutes to hours per facet)
```

## Common Prerequisites

- **pymatgen**: SlabGenerator for slab construction from bulk structure.
- **ASE + MACE**: For fast ML-potential-based surface energy screening.
- **Quantum ESPRESSO**: For DFT-quality surface energies.
- **Pseudopotentials**: SSSP or PSlibrary UPF files (see `electronic-structure/scf-relax` skill).
