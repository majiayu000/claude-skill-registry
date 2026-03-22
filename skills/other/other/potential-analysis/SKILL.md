---
name: potential-analysis
description: Potential Analysis (3 sub-skills: macroscopic-average, planar-average, work-function)
---

# Potential Analysis

## Overview

This skill group covers electrostatic potential analysis from first-principles calculations.
It provides workflows for extracting, averaging, and interpreting the electrostatic potential
from Quantum ESPRESSO and VASP outputs. These analyses are essential for work function
calculations, band alignment at interfaces, and understanding interface dipoles.

All workflows correspond to VASPKIT menu 42 (tasks 420--430).

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Work Function | `work-function/` | Calculate work function from planar-averaged electrostatic potential. Vacuum level minus Fermi energy. QE: pp.x + average.x. VASP: LOCPOT parsing. |
| Planar Average | `planar-average/` | Planar-average and macroscopic-average of charge density and potential along a chosen axis. QE: pp.x + average.x. VASP: LOCPOT/CHGCAR parsing. Line profiles along specified paths. |
| Macroscopic Average | `macroscopic-average/` | Double (macroscopic) averaging technique for interface dipoles, band offsets, and heterojunction band alignment. |

## When to Use

- **work-function/** -- You need the work function of a surface slab (vacuum level minus Fermi energy).
- **planar-average/** -- You need 1D profiles of the electrostatic potential or charge density
  averaged over planes perpendicular to a slab normal or interface direction.
- **macroscopic-average/** -- You need smooth macroscopic averages for band alignment at
  heterojunctions, interface dipole determination, or Schottky barrier estimation.

## General Prerequisites

- Quantum ESPRESSO 7.5 (`pw.x`, `pp.x`, `average.x`)
- Python packages: `pymatgen`, `ase`, `numpy`, `scipy`, `matplotlib`
- A converged slab calculation with sufficient vacuum (typically 15--20 Angstrom)
- For VASP workflows: LOCPOT and/or CHGCAR files from a slab calculation
