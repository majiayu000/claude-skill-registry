---
name: topological
description: Topological Properties (2 sub-skills: berry-curvature, z2-invariant)
---

# Topological Properties

## Skills Index

| Skill | Description |
|-------|-------------|
| [z2-invariant](z2-invariant/SKILL.md) | Z2 topological invariant via Wilson loops (z2pack) or parity analysis (Fu-Kane) |
| [berry-curvature](berry-curvature/SKILL.md) | Berry curvature, Chern number, and anomalous Hall conductivity |

## Overview

These skills compute topological invariants and related quantities from DFT band structures.
All workflows use Quantum ESPRESSO with spin-orbit coupling (SOC) as the DFT engine.
Wannier90 provides smooth gauge for interpolation; z2pack and custom Python scripts compute invariants.

## Common Requirements

- Fully relativistic pseudopotentials (FR-ONCV or PSlibrary `_rel` PPs) for SOC
- `noncolin = .true.` and `lspinorb = .true.` in QE `pw.x`
- Dense k-grids for converged topological invariants
- Python packages: `numpy`, `matplotlib`, `z2pack` (pip installable)
