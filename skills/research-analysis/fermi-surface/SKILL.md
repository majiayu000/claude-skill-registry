---
name: fermi-surface
description: Fermi Surface Calculations (3 sub-skills: 2d-fermi-surface, 3d-fermi-surface, projected-fermi-surface)
---

# Fermi Surface Calculations

## Overview

This skill group covers the calculation and visualization of Fermi surfaces -- the constant-energy surface in reciprocal space that separates occupied from unoccupied electronic states at zero temperature. The Fermi surface determines the electronic transport, thermodynamic, and superconducting properties of metals. These skills correspond to VASPKIT menu 26 (tasks 261-267).

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| 3D Fermi Surface | `3d-fermi-surface/` | Full 3D Fermi surface for bulk metals: isosurface extraction, XcrySDen/FermiSurfer output (VASPKIT 261-263) |
| 2D Fermi Surface | `2d-fermi-surface/` | 2D Fermi contour for layered/2D materials: constant-energy slices in the kx-ky plane (VASPKIT 264-265) |
| Projected Fermi Surface | `projected-fermi-surface/` | Orbital-resolved Fermi surface: color-map orbital character onto the Fermi surface (VASPKIT 266-267) |

## Method Decision Guide

```
Need Fermi surface analysis?
  |
  +--> 3D bulk metal?
  |      YES --> 3d-fermi-surface/
  |
  +--> 2D or layered material (single kz slice)?
  |      YES --> 2d-fermi-surface/
  |
  +--> Need orbital character on the Fermi surface?
         YES --> projected-fermi-surface/
```

## Common Prerequisites

- **Metallic system**: Fermi surfaces only exist for metals (bands crossing the Fermi level). For semiconductors/insulators, use constant-energy contour analysis instead.
- **Well-converged SCF**: A standard SCF on a coarse k-grid to obtain the charge density and Fermi energy.
- **Dense k-mesh NSCF**: A non-self-consistent calculation on a very dense uniform k-grid (typically 30x30x30 or denser for 3D, 60x60x1 or denser for 2D).
- **QE executables**: `pw.x`, `pp.x`, `projwfc.x` (Quantum ESPRESSO 7.5).
- **Python packages**: `numpy`, `scipy` (for interpolation and marching cubes), `matplotlib` (for 2D/3D plotting), `pymatgen`, `ase`.
- **MACE limitation**: MACE cannot compute Fermi surfaces. It is a force field with no electronic degrees of freedom. Use it only for structure pre-relaxation.

## Important Notes

- Fermi surface quality depends critically on k-mesh density. Undersampled meshes produce jagged or incomplete surfaces.
- For QE, use `occupations = 'smearing'` with small `degauss` (0.005-0.01 Ry) for the SCF step. The NSCF step should also use smearing (not tetrahedra) to obtain eigenvalues on every k-point.
- Spin-polarized metals have separate Fermi surfaces for majority and minority spin channels. Set `nspin = 2` and analyze each spin independently.
- The Fermi energy from SCF may differ slightly from the NSCF Fermi energy due to k-mesh differences. Use the NSCF Fermi energy for surface extraction.
