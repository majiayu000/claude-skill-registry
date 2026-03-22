---
name: spin-texture
description: Spin Texture (2 sub-skills: 2d-spin-texture, 3d-spin-texture)
---

# Spin Texture

## Overview

This skill group covers the calculation and visualization of spin textures from
spin-orbit coupled (SOC) DFT calculations. Spin texture maps the expectation values
of the spin operator (Sx, Sy, Sz) for each electronic state across the Brillouin zone,
revealing phenomena such as Rashba/Dresselhaus splitting, topological surface states,
and spin-momentum locking.

All workflows correspond to VASPKIT menu 65 (tasks 651--653).

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| 2D Spin Texture | `2d-spin-texture/` | Spin texture for 2D materials and surfaces with SOC. Dense k-mesh around band extrema, spin expectation values per k-point per band, arrow plots on constant-energy contours. |
| 3D Spin Texture | `3d-spin-texture/` | Spin texture for bulk 3D materials with SOC. Similar workflow but for arbitrary 2D slices through the 3D Brillouin zone. |

## When to Use

- **2d-spin-texture/** -- You have a 2D material or surface and need to visualize
  spin-momentum locking, Rashba splitting, or topological surface state spin texture.
- **3d-spin-texture/** -- You have a bulk 3D material with SOC and need spin texture
  on specific BZ planes (e.g., kz=0, kz=pi/c) for Fermi surface spin analysis.

## General Prerequisites

- Quantum ESPRESSO 7.5 (`pw.x`, `projwfc.x`) with noncollinear + SOC support
- Fully relativistic pseudopotentials (FR-ONCV or PSlibrary `_rel` PPs)
- `noncolin = .true.` and `lspinorb = .true.` in QE input
- Python packages: `pymatgen`, `ase`, `numpy`, `matplotlib`
- For VASP workflows: PROCAR file from a SOC calculation with `LSORBIT = .TRUE.`
