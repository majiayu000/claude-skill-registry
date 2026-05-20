---
name: band-advanced
description: Advanced Band Structure Methods (3 sub-skills: 3d-band-structure, band-unfolding, hybrid-dft-bands)
---

# Advanced Band Structure Methods

## Overview

This skill group covers advanced electronic band structure techniques beyond the standard k-path band calculation. These methods address specific challenges in electronic structure theory: visualizing the full Brillouin zone dispersion for 2D materials, obtaining accurate band gaps with hybrid functionals, and recovering effective primitive-cell band structures from supercell calculations.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| 3D Band Structure | `3d-band-structure/` | Full E(kx,ky) surface over the 2D BZ for layered/2D materials (VASPKIT 231-233) |
| Hybrid-DFT Bands | `hybrid-dft-bands/` | HSE06/PBE0 band structures with accurate band gaps (VASPKIT 250-257) |
| Band Unfolding | `band-unfolding/` | Unfold supercell bands back to primitive BZ to reveal effective band structure (VASPKIT 281-285) |

## Method Decision Guide

```
Need advanced band structure analysis?
  |
  +--> Full BZ dispersion for 2D material?
  |      YES --> 3d-band-structure/
  |
  +--> Accurate band gap (hybrid functional)?
  |      YES --> hybrid-dft-bands/
  |
  +--> Supercell with defect/alloy/interface, want primitive-cell-like bands?
         YES --> band-unfolding/
```

## Common Prerequisites

- **Converged structure**: Always start from a well-relaxed structure (use `scf-relax` skill).
- **Pseudopotentials**: QE calculations require pseudopotential files. Use SSSP or PseudoDojo libraries.
- **Python environment**: `pymatgen`, `ase`, `numpy`, `scipy`, `matplotlib` are pre-installed. Install extras with `pip install seekpath` as needed.
- **QE executables**: `pw.x`, `bands.x`, `pp.x`, `projwfc.x` (Quantum ESPRESSO 7.5).
- **MACE limitation**: MACE is a machine-learning force field and cannot compute electronic band structures. Use it only for structure pre-relaxation before DFT.

## Important Notes

- Standard PBE band gaps are underestimated by 30--50%. Use hybrid-DFT bands for quantitative gap values.
- 3D band structure calculations require dense k-meshes and are significantly more expensive than standard k-path calculations.
- Band unfolding is essential when studying defects, alloys, or interfaces in supercells -- without it, the zone-folded bands are uninterpretable.
- All three sub-skills share the same SCF foundation. A well-converged SCF charge density is the starting point for each method.
