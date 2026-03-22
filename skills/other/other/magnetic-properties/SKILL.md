---
name: magnetic-properties
description: Magnetic Properties (3 sub-skills: magnetic-anisotropy, magnetic-ordering, spin-polarized)
---

# Magnetic Properties

## Overview

This skill group covers first-principles calculations of magnetic properties using
Quantum ESPRESSO (QE) with Python-based pre/post-processing (pymatgen, ASE, matplotlib).
All workflows are designed for a Docker container environment with QE 7.5 installed.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Spin-Polarized DFT | `spin-polarized/` | Collinear spin-polarized SCF calculations (`nspin=2`), magnetic moments, spin-resolved DOS, and spin density visualization via `pp.x`. |
| Magnetic Ordering | `magnetic-ordering/` | Comparison of FM, AFM, and non-magnetic configurations to determine ground-state magnetic order. Estimation of exchange coupling constants. |
| Magnetic Anisotropy | `magnetic-anisotropy/` | Magnetic anisotropy energy (MAE) via noncollinear DFT with spin-orbit coupling (`noncolin=.true.`, `lspinorb=.true.`). Requires fully relativistic pseudopotentials. (VASPKIT 621) |
| Magnetic Moments | `magnetic-moments/` | Extract and visualize local magnetic moments. QE: Lowdin/Mulliken from projwfc.x. VASP: OUTCAR parsing. Generate MAGNETIC_MOMENTS.cif. Spin density visualization. (VASPKIT 629) |

## When to Use

- **spin-polarized/** -- You need to check whether a material is magnetic, compute atomic
  magnetic moments, or obtain spin-resolved electronic structure (DOS, charge density).
- **magnetic-ordering/** -- You need to determine whether a material prefers FM, AFM, or
  non-magnetic order, or estimate exchange coupling constants from total-energy differences.
- **magnetic-anisotropy/** -- You need the magnetic anisotropy energy (easy/hard axis),
  which requires spin-orbit coupling and noncollinear magnetism.
- **magnetic-moments/** -- You need per-atom magnetic moments, spin density maps, or a
  CIF file annotated with magnetic moment vectors for visualization.

## General Prerequisites

- Quantum ESPRESSO 7.5 (`pw.x`, `pp.x`, `projwfc.x`, `bands.x`, `dos.x`)
- Python packages: `pymatgen`, `ase`, `numpy`, `scipy`, `matplotlib`
- Appropriate pseudopotentials (SSSP Efficiency or PseudoDojo; fully relativistic for SOC)
- Sufficient computational resources (magnetic calculations are more expensive than non-magnetic)
