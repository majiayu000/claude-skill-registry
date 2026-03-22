---
name: structure-models
description: Advanced Structure Models (8 sub-skills: alloy-builder, defect-builder, heterostructure, moire-superlattice, nanowire-nanotube, quantum-dot, supercell-builder, surface-builder)
---

# Advanced Structure Models

## Overview

This skill group covers construction of advanced structural models for computational materials science. It corresponds to VASPKIT menu 08 (tasks 800--827) and provides equivalent functionality using Python tools (pymatgen, ASE, spglib), with output in CIF, POSCAR, and QE input formats.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Supercell Builder | `supercell-builder/` | Build supercells (diagonal and non-diagonal), orthogonal supercells from non-orthogonal cells. (VASPKIT 800, 401) |
| Surface Builder | `surface-builder/` | Build surface slabs by Miller indices using pymatgen SlabGenerator. (VASPKIT 803) |
| Alloy Builder | `alloy-builder/` | Random substitutional alloys, SQS (Special Quasi-random Structure) generation. (VASPKIT 802) |
| Heterostructure | `heterostructure/` | Build heterostructures from two slabs, lattice matching. (VASPKIT 804) |
| Nanowire/Nanotube | `nanowire-nanotube/` | Build nanowires, nanotubes, quantum dots, nanoribbons. (VASPKIT 806--808) |
| Defect Builder | `defect-builder/` | Build point defects (vacancies, substitutions, interstitials) in supercells. (VASPKIT 821--822) |

## Method Decision Guide

```
Need a supercell?
  Simple NxNxN --> supercell-builder/ (make_supercell)
  Orthogonal from non-orthogonal --> supercell-builder/ (CubicSupercellTransformation)

Need a surface slab?
  --> surface-builder/ (SlabGenerator by Miller index)

Need an alloy model?
  Random alloy --> alloy-builder/ (random substitution)
  Ordered representative --> alloy-builder/ (SQS via icet or pymatgen)

Need a heterostructure (interface)?
  --> heterostructure/ (ZSLGenerator for lattice matching)

Need a nanostructure?
  Nanowire --> nanowire-nanotube/ (carve from bulk)
  Nanotube --> nanowire-nanotube/ (roll a sheet)
  Nanoribbon --> nanowire-nanotube/ (cut from 2D sheet)

Need a defect model?
  Vacancy, substitution, interstitial --> defect-builder/
```

## Common Prerequisites

- **pymatgen**: pre-installed (Structure, SlabGenerator, SubstitutionTransformation, etc.)
- **ASE**: pre-installed (structure manipulation, visualization)
- **spglib**: pre-installed (symmetry analysis)
- **numpy**: pre-installed
- Optional: `pip install icet` for SQS generation, `pip install pymatgen-analysis-defects` for advanced defect workflows
