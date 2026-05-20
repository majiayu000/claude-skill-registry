---
name: catalyst-screening
description: Catalyst Screening (3 sub-skills: d-band-center, overpotential, scaling-relations)
---

# Catalyst Screening

## Skills Index

| Skill | Description |
|-------|-------------|
| [d-band-center](d-band-center/SKILL.md) | d-band center analysis from projected DOS for catalyst ranking |
| [scaling-relations](scaling-relations/SKILL.md) | Linear scaling relations and volcano plots for electrocatalysis |
| [overpotential](overpotential/SKILL.md) | Electrocatalytic overpotential and free energy diagrams (OER/ORR/HER) |

## Overview

These skills implement computational catalyst screening workflows based on descriptor-based
approaches. The d-band center model (Norskov) connects electronic structure to adsorption
energetics. Scaling relations reduce the multi-dimensional adsorption energy space to a
single descriptor. Volcano plots identify optimal catalysts.

## Common Requirements

- Quantum ESPRESSO for DFT (SCF, NSCF, projwfc.x for PDOS)
- ASE for slab construction and structure manipulation
- MACE-torch for rapid adsorption energy screening (structure optimization)
- Python: `numpy`, `scipy`, `matplotlib` for analysis and plotting
