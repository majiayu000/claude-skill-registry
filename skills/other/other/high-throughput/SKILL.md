---
name: high-throughput
description: High-Throughput Computational Workflows (8 sub-skills: batch-calculations, batch-screening, convergence-automation, materials-filtering, matpes-dual-static, phase-stability, property-prediction, screening-workflow)
---

# High-Throughput Computational Workflows

## Sub-skills

| Skill | Path | Description |
|-------|------|-------------|
| Screening Workflow | [screening-workflow/SKILL.md](screening-workflow/SKILL.md) | End-to-end materials screening: query Materials Project for candidates, batch MACE relaxation, filter by stability/band gap/elastic modulus, rank candidates, validate top hits with DFT |
| Batch Calculations | [batch-calculations/SKILL.md](batch-calculations/SKILL.md) | Run batch DFT calculations on multiple structures: input generation with pymatgen sets, parallel execution, result collection, error handling and restart logic for QE and VASP |
| Phase Stability | [phase-stability/SKILL.md](phase-stability/SKILL.md) | Phase stability and convex hull analysis: compute formation energies, build convex hulls, determine energy above hull, phase diagram sections, integration with Materials Project reference data |
| Property Prediction | [property-prediction/SKILL.md](property-prediction/SKILL.md) | Rapid MACE-based property prediction pipeline: lattice constants, bulk modulus, DOS-based band gap proxy, surface energy, vacancy formation energy, comparison with databases, correlation plots |
| Batch Screening | [batch-screening/SKILL.md](batch-screening/SKILL.md) | High-throughput screening workflow: fetch candidates from Materials Project, rapid MACE screening, filter/rank, detailed QE for top hits |
| Materials Filtering | [materials-filtering/SKILL.md](materials-filtering/SKILL.md) | Query and filter the Materials Project database: chemical system search, property ranges, stability criteria, export structures and data |
| Convergence Automation | [convergence-automation/SKILL.md](convergence-automation/SKILL.md) | Automated DFT convergence testing: sweep ecutwfc and k-grids, find optimal parameters via energy-per-atom threshold (1 meV/atom), combined cutoff-then-kgrid workflow, batch mode for multiple materials, convergence plots and JSON reports. Inspired by pyiron_atomistics ConvEncutParallel/ConvKpointParallel. |
| MatPES Dual Static | [matpes-dual-static/SKILL.md](matpes-dual-static/SKILL.md) | Dual-functional PBE + r2SCAN static calculations: run PBE first, reuse wavefunction for efficient r2SCAN, optional PBE+U, collect energies at two levels of theory for ML training data or cross-validation |

## General Pattern

1. **Source candidates** -- query Materials Project or build structures programmatically.
2. **Fast screen** -- use MACE-MP-0 to relax and evaluate properties in seconds per structure.
3. **Filter and rank** -- apply thermodynamic / electronic / mechanical criteria.
4. **Validate** -- run Quantum ESPRESSO (or VASP) DFT on the short-listed candidates.
5. **Report** -- export CSV/JSON, generate plots, build property tables.

## Method Decision Guide

```
What kind of high-throughput task?

Screen many candidates for a target property?
  --> screening-workflow/ (full pipeline with MP query + MACE + DFT validation)

Run DFT on a known set of structures?
  --> batch-calculations/ (input generation, parallel execution, error handling)

Assess thermodynamic stability of candidate phases?
  --> phase-stability/ (convex hull, formation energies, decomposition analysis)

Rapidly predict multiple properties for a set of structures?
  --> property-prediction/ (MACE-based lattice constants, bulk modulus, surface energy, etc.)

Just query/filter the Materials Project database?
  --> materials-filtering/ (database queries, property ranges, export)

Need both PBE and r2SCAN energies efficiently (ML training data, cross-validation)?
  --> matpes-dual-static/ (PBE wavefunction warm-starts r2SCAN, optional PBE+U)

Determine optimal ecutwfc / k-grid for a new material or pseudopotential?
  --> convergence-automation/ (automated sweeps, threshold-based selection, batch mode)
```

## Prerequisites

- `MP_API_KEY` environment variable set (obtain from https://next-gen.materialsproject.org/api).
- Python packages: `mp-api`, `pymatgen`, `ase`, `mace-torch`, `numpy`, `pandas`, `matplotlib`.
- For DFT validation: Quantum ESPRESSO 7.5 (`pw.x`). VASP support via external access in future.
- Optional: `pip install fireworks jobflow atomate2 custodian` for advanced workflow management.
