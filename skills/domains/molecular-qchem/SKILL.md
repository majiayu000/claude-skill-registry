---
name: molecular-qchem
description: Molecular Quantum Chemistry (1 sub-skills: gaussian-qchem-workflow)
---

# Molecular Quantum Chemistry

Quantum chemistry calculations for molecules and molecular clusters (non-periodic systems). This skill group covers geometry optimization, vibrational analysis, thermochemistry, solvation, excited states, and reaction energetics using open-source quantum chemistry engines (PySCF, Psi4) that can be installed via pip/conda. Inspired by the atomate2 Q-Chem module but adapted for the open-source tools available in MatClaw's container environment.

Unlike the periodic electronic-structure skills (which target crystals with Quantum ESPRESSO), this group targets isolated molecules, molecular complexes, and cluster models where Gaussian-type orbital (GTO) basis sets are natural and efficient.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Molecular QChem Workflows | `gaussian-qchem-workflow/` | Complete workflows for geometry optimization + frequency, solvation energy, reaction profiles, and excited-state (TD-DFT) calculations using PySCF |

## Method Decision Guide

```
What kind of system are you studying?

Periodic crystal or slab?
  --> Use electronic-structure/ skills (Quantum ESPRESSO / MACE)

Isolated molecule, molecular cluster, or reaction?
  --> This skill group (molecular-qchem/)

What property do you need?

Optimized geometry + thermochemistry (ZPE, H, G)?
  --> gaussian-qchem-workflow/ : Workflow 1

Solvation free energy (gas vs solution)?
  --> gaussian-qchem-workflow/ : Workflow 2

Reaction energy or barrier (A + B -> C)?
  --> gaussian-qchem-workflow/ : Workflow 3

UV-Vis absorption spectrum / excited states?
  --> gaussian-qchem-workflow/ : Workflow 4

What level of theory?

Quick screening or large molecule (> 50 atoms)?
  --> DFT: B3LYP/def2-SVP or PBE0/def2-SVP

Accurate thermochemistry (small molecule, < 20 atoms)?
  --> MP2/cc-pVTZ or CCSD(T)/cc-pVTZ (single-point on DFT geometry)

Organic reaction energetics?
  --> B3LYP-D3/def2-TZVP (DFT with dispersion)

Transition metal complex?
  --> PBE0/def2-SVP or B3LYP/def2-SVP with ECPs (automatic in def2 basis)
```

## Common Prerequisites

- **PySCF**: `pip install pyscf` -- the primary quantum chemistry engine used in all workflows.
- **geomeTRIC**: `pip install geometric` -- geometry optimizer that interfaces with PySCF.
- **RDKit** (optional): `pip install rdkit` -- for building molecules from SMILES strings.
- **ASE** (optional): pre-installed in container -- for reading/writing molecular structures in various formats.
- **NumPy / SciPy / matplotlib**: pre-installed -- for post-processing and plotting.
