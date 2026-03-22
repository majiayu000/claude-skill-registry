---
name: code-interfaces
description: Code Interfaces and Conversion Utilities (5 sub-skills: boltztrap-interface, ifc-analysis, phonopy-interface, vasp-qe-converter, wannier90-interface)
---

# Code Interfaces and Conversion Utilities

Bridge between different computational materials science codes. Convert input/output formats, interface with post-processing tools, and chain workflows across QE, VASP, phonopy, BoltzTraP2, and Wannier90.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| VASP-QE Converter | `vasp-qe-converter/` | Convert between VASP and Quantum ESPRESSO input/output formats: POSCAR/INCAR/KPOINTS/OUTCAR to/from QE pw.x input/output |
| BoltzTraP2 Interface | `boltztrap-interface/` | BoltzTraP2 for Boltzmann transport: convert QE/VASP band structures, compute Seebeck, conductivity, thermal conductivity vs temperature and doping |
| Phonopy Interface | `phonopy-interface/` | Phonopy for lattice dynamics: generate displaced structures for QE/VASP, import forces, compute phonon bands, DOS, thermal properties, IFC analysis |
| Wannier90 Interface | `wannier90-interface/` | Wannier90 for maximally localized Wannier functions: QE pw2wannier90.x and VASP LWANNIER90, Wannier-interpolated bands, Berry phase, Z2 invariant |

## Method Decision Guide

```
What do you need to do?

Convert VASP inputs to QE (or vice versa)?
  --> vasp-qe-converter/

Compute thermoelectric transport properties (Seebeck, conductivity)?
  --> boltztrap-interface/

Compute phonon band structure, DOS, or thermal properties?
  --> phonopy-interface/  (for phonopy-based workflows)
  --> Also see thermal-properties/phonon/ for the full phonon skill

Compute Wannier functions, Wannier-interpolated bands, or topological invariants?
  --> wannier90-interface/
  --> Also see wannier-functions/wannier90-workflow/ for the complete QE+Wannier90 pipeline

Already have DFT results and need to post-process with an external tool?
  --> Check the specific interface sub-skill
```

## Cross-References

| Task | Primary Skill | Interface Skill |
|---|---|---|
| Phonon calculation from scratch | `thermal-properties/phonon/` | `phonopy-interface/` (for advanced phonopy features) |
| Electronic transport | `electron-phonon/electronic-transport/` | `boltztrap-interface/` (for standalone BoltzTraP2 usage) |
| Wannier functions | `wannier-functions/wannier90-workflow/` | `wannier90-interface/` (for format conversion and advanced features) |
| DFT input generation | `structure-tools/input-generation/` | `vasp-qe-converter/` (for cross-code conversion) |
