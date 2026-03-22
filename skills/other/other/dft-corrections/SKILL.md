---
name: dft-corrections
description: DFT Corrections (3 sub-skills: hubbard-u, spin-orbit-coupling, vdw-correction)
---

# DFT Corrections

Beyond-standard-DFT corrections for improved accuracy in specific material classes. These corrections address known deficiencies of semi-local DFT functionals (GGA/LDA) and should be applied when the physics demands it.

## Sub-Skills

| Sub-Skill | Directory | Use Case | QE Keywords |
|---|---|---|---|
| Hubbard U (DFT+U) | `hubbard-u/` | Strongly correlated systems: transition metal oxides, f-electron systems, Mott insulators | `lda_plus_u`, `Hubbard_U(i)`, `hp.x` |
| Van der Waals Corrections | `vdw-correction/` | Layered materials, molecular crystals, adsorption, MOFs, weakly bound systems | `vdw_corr`, `input_dft='vdw-df'` |
| Spin-Orbit Coupling | `spin-orbit-coupling/` | Heavy elements, topological insulators, Rashba splitting, magnetic anisotropy | `noncolin`, `lspinorb`, rel pseudopotentials |

## Decision Guide

```
Is your system strongly correlated (open d/f shells)?
  YES --> Use DFT+U (hubbard-u/)
  NO  --> Standard DFT may be fine

Are van der Waals interactions important (layered, molecular, adsorption)?
  YES --> Use vdW correction (vdw-correction/)
  NO  --> Standard DFT may be fine

Does your system contain heavy elements (Z > 50) or need spin-orbit physics?
  YES --> Use SOC (spin-orbit-coupling/)
  NO  --> Scalar-relativistic PP is sufficient
```

Note: These corrections are NOT mutually exclusive. For example, a transition metal dichalcogenide may require both vdW corrections (layered structure) and SOC (heavy chalcogen). A correlated oxide surface with adsorbed molecules may need DFT+U and vdW together.

## General Prerequisites

- Quantum ESPRESSO 7.5 installed (`pw.x`, `pp.x`, `ph.x`, `hp.x`)
- Appropriate pseudopotentials from PseudoDojo or SSSP
- Python with `pymatgen`, `ASE`, `numpy`, `matplotlib` for post-processing
