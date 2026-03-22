---
name: kpath-utilities
description: K-Path Utilities (5 sub-skills: 1d-kpath, 2d-kpath, bulk-kpath, cp2k-kpath, phonopy-kpath)
---

# K-Path Utilities

## Overview

This skill group covers generation of high-symmetry k-point paths for band structure, phonon dispersion, and Wannier90 calculations. It corresponds to VASPKIT menu 03 (tasks 301--309) and provides equivalent functionality using Python tools (seekpath, pymatgen, spglib), with output formatted for Quantum ESPRESSO, VASP, Wannier90, and phonopy.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Bulk K-Path | `bulk-kpath/` | Generate k-paths for 3D bulk crystals using seekpath, pymatgen HighSymmKpath, or spglib. Output for QE, VASP, Wannier90, phonopy. Includes BZ visualization. (VASPKIT 301--303) |
| 2D K-Path | `2d-kpath/` | K-paths for 2D materials (hexagonal, square, rectangular lattices). Special handling for 2D Brillouin zones. (VASPKIT 304) |
| 1D K-Path | `1d-kpath/` | K-paths for 1D structures (nanowires, nanotubes). (VASPKIT 305) |
| Phonopy K-Path | `phonopy-kpath/` | Generate KPATH.in for phonopy, band_conf settings, seekpath integration. (VASPKIT 303, 309) |

## Method Decision Guide

```
Need a k-path for a 3D crystal?
  --> bulk-kpath/ (seekpath recommended for standardized paths)

Need a k-path for a 2D material (slab, monolayer)?
  --> 2d-kpath/ (uses 2D BZ conventions)

Need a k-path for a 1D system (nanotube, nanowire)?
  --> 1d-kpath/ (Gamma-X path along the periodic axis)

Need k-path formatted for phonopy?
  --> phonopy-kpath/ (generates band.conf or KPATH.in)

Which k-path convention?
  seekpath (Hinuma et al.)  --> recommended, standardized, handles all 14 Bravais lattices
  pymatgen HighSymmKpath    --> uses Setyawan-Curtarolo convention, well-tested
  spglib                    --> lower-level, useful for custom BZ queries
```

## Common Prerequisites

- **seekpath**: `pip install seekpath` (recommended for standardized k-paths)
- **pymatgen**: pre-installed (HighSymmKpath, BandStructureSymmLine)
- **spglib**: pre-installed (space group detection, standardization)
- **matplotlib**: pre-installed (BZ visualization)
- Structure files: CIF, POSCAR, or pymatgen/ASE Structure objects
