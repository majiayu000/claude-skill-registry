---
name: wannier-functions
description: Wannier Functions (1 sub-skills: wannier90-workflow)
---

# Wannier Functions

## Overview

This skill group covers the construction of maximally localized Wannier functions (MLWFs) from DFT Bloch states. Wannier functions provide a real-space, localized representation of electronic structure that enables tight-binding model construction, Wannier-interpolated band structures, topological invariant calculations, and electron-phonon coupling.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Wannier90 Workflow | `wannier90-workflow/` | Full QE + Wannier90 pipeline: SCF, NSCF, wannierization, band interpolation, spread minimization |

## Method Decision Guide

```
Need Wannier functions or tight-binding Hamiltonian?
  YES --> wannier90-workflow/
  Need topological invariants (Z2, Chern number)?
    YES --> wannier90-workflow/ (then use WannierTools or custom Z2 script)
  Need Wannier-interpolated band structure?
    YES --> wannier90-workflow/ (produces smooth interpolated bands on arbitrary k-paths)
  Need electron-phonon coupling via Wannier interpolation?
    YES --> wannier90-workflow/ (provides the Wannier basis for EPW)
```

## Common Prerequisites

- **Quantum ESPRESSO**: pw.x for SCF/NSCF, pw2wannier90.x for interface.
- **Wannier90**: wannier90.x binary or Python interface. If the binary is not available, the workflow explains alternatives.
- **Pseudopotentials**: SSSP or PSlibrary UPF files (see `electronic-structure/scf-relax` skill).
- **Python packages**: pymatgen, numpy, matplotlib for post-processing.
