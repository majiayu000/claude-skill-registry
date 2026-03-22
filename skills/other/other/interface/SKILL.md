---
name: interface
description: Interface and Defect Structure Workflows (2 sub-skills: grain-boundary, heterostructure)
---

# Interface and Defect Structure Workflows

## Sub-skills

| Skill | Path | Description |
|-------|------|-------------|
| Grain Boundary | [grain-boundary/SKILL.md](grain-boundary/SKILL.md) | Construct CSL grain boundaries with pymatgen, relax with MACE, compute GB energies |
| Heterostructure | [heterostructure/SKILL.md](heterostructure/SKILL.md) | Build lattice-matched heterostructures, relax with MACE, compute adhesion energy and interface properties |

## General Pattern

1. **Build interface** -- use pymatgen generators (GrainBoundaryGenerator, ZSLGenerator, SubstrateAnalyzer) to create atomistic models.
2. **Relax with MACE** -- fast geometry optimization with selective dynamics (fix bulk-like atoms).
3. **Compute interface energy** -- compare slab/interface energy to bulk references.
4. **Validate with QE** -- single-point or full relaxation for key structures.
5. **Analyze** -- energy vs. geometric descriptor plots, structure visualization.

## Prerequisites

- Python packages: `pymatgen`, `ase`, `mace-torch`, `numpy`, `matplotlib`.
- For QE validation: Quantum ESPRESSO 7.5 (`pw.x`) with appropriate pseudopotentials.
