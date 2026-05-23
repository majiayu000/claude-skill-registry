---
name: alloy-disorder
description: Alloy Disorder Modeling (2 sub-skills: cluster-expansion, sqs-generation)
---

# Alloy Disorder Modeling

## Overview

Skills for modeling chemical disorder in alloys: generating representative structures, fitting energy models, and predicting thermodynamic properties (phase diagrams, order-disorder transitions).

## Sub-skills

| Skill | Path | Description |
|-------|------|-------------|
| [SQS Generation](sqs-generation/SKILL.md) | `sqs-generation/` | Generate Special Quasirandom Structures to model random alloys in small periodic cells. Uses icet or pymatgen with Monte Carlo optimization. |
| [Cluster Expansion](cluster-expansion/SKILL.md) | `cluster-expansion/` | Fit lattice energy models (cluster expansions) to MACE/QE data. Run Monte Carlo simulations for phase diagrams and order-disorder temperatures. |

## Typical Workflow

1. **SQS Generation** -- Build a representative disordered structure for a target composition.
2. **Relax with MACE or QE** -- Obtain ground-state geometry and energy.
3. **Cluster Expansion** -- Fit a Hamiltonian across many compositions, then run Monte Carlo for finite-temperature thermodynamics.

## Prerequisites

```bash
pip install icet sqsgenerator
# Already available: pymatgen, ase, mace-torch, numpy, scipy, matplotlib
```
