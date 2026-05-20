---
name: bonding-analysis
description: Bonding Analysis (10 sub-skills: bader2pqr, bader-charge, charge-density, charge-density-difference, charge-format-conversion, elf-analysis, lobster-cohp, orbital-projection, planar-charge, stm-simula
---

# Bonding Analysis

Chemical bonding analysis using Quantum ESPRESSO and Python post-processing tools.

## Sub-Skills

| Sub-Skill | Directory | Description |
|-----------|-----------|-------------|
| Charge Density Analysis | `charge-density/` | Total charge, charge difference, deformation density plots (2D slices, 1D profiles) via pp.x |
| ELF Analysis | `elf-analysis/` | Electron Localization Function for bond character identification (covalent/ionic/metallic) |
| Bader Charge Analysis | `bader-charge/` | Bader charge partitioning for charge transfer and oxidation states; includes Lowdin charge fallback via projwfc.x |
| Orbital Projection | `orbital-projection/` | Projected DOS, fat bands, orbital hybridization, and crystal field splitting via projwfc.x |

## General Workflow

All bonding analyses follow the same initial step:

1. **SCF calculation** with `pw.x` (self-consistent field)
2. **Post-processing** with `pp.x`, `projwfc.x`, or external tools
3. **Visualization / quantification** with Python (matplotlib, numpy)

## Prerequisites

- Quantum ESPRESSO 7.5 (`pw.x`, `pp.x`, `projwfc.x`)
- Python packages: `numpy`, `scipy`, `matplotlib`, `pymatgen`, `ase`
- For Bader analysis: Henkelman group `bader` binary (pip install or download)
- Pseudopotential files appropriate for your system

## When to Use

- **Charge density**: Visualize where electrons accumulate; compare bonded vs isolated atoms.
- **ELF**: Identify bond types -- covalent bonds show ELF near 1, metallic bonds near 0.5.
- **Bader charges**: Quantify charge transfer between atoms; estimate oxidation states.
- **Orbital projection**: Understand which orbitals participate in bonding; identify hybridization and crystal field effects.
