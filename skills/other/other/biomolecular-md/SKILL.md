---
name: biomolecular-md
description: Biomolecular MD (1 sub-skills: openmm-simulation)
---

# Biomolecular MD

Biomolecular molecular dynamics simulations using OpenMM for proteins, solvated molecular systems, drug-protein interactions, and soft matter. Covers force field assignment (AMBER, CHARMM, OpenFF), explicit solvent models, free energy calculations, and trajectory analysis with mdtraj.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| OpenMM Simulation | `openmm-simulation/` | Full biomolecular MD workflows: protein-in-water from PDB, small molecule solvation with Open Force Field, temperature annealing, equilibration protocols (NVT/NPT), and trajectory analysis with mdtraj |

## Method Decision Guide

```
What biomolecular simulation do you need?

Protein folding / dynamics / conformational sampling?
  --> openmm-simulation/  (Workflow 1: Protein in Water from PDB)

Small molecule solvation free energy / drug-like molecule in water?
  --> openmm-simulation/  (Workflow 2: Small Molecule Solvation with OpenFF)

Temperature-driven conformational changes / simulated annealing?
  --> openmm-simulation/  (Workflow 3: Temperature Annealing)

Drug-protein binding / ligand-receptor interactions?
  --> openmm-simulation/  (Workflow 1 with ligand, or use openmmtools for alchemical FE)

Polymer / soft matter in solution?
  --> openmm-simulation/  (Workflow 2 with polymer topology via OpenFF)

Force field selection:
  Protein/nucleic acid     --> AMBER ff14SB or CHARMM36m
  Small organic molecule   --> OpenFF (Sage / Parsley) via openff-toolkit
  Lipid bilayer            --> CHARMM36 lipid parameters
  General organic          --> GAFF2 (via AmberTools) or OpenFF
```
