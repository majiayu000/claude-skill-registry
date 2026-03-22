---
name: structure-tools
description: Structure Tools Skills (8 sub-skills: advanced-optimization, format-conversion, input-generation, pdf-analysis, structure-editing, structure-matching, symmetry-analysis, xrd-pattern)
---

# Structure Tools Skills

Tools for crystal structure preparation, manipulation, symmetry analysis, format conversion, and DFT input generation. This skill group covers the foundational operations needed before running any calculation: getting a structure into the right format, building supercells, analyzing symmetry, and generating complete input files for QE and VASP.

## Available Skills

| Skill | Description |
|-------|-------------|
| [advanced-optimization](advanced-optimization/SKILL.md) | Advanced structure optimization: quasi-Newton methods (BFGS, SR1, PSB), scipy minimizers (CG, L-BFGS-B, TNC), simultaneous cell+position optimization with Voigt strain, staged optimization for disordered/amorphous materials. |
| [input-generation](input-generation/SKILL.md) | Generate DFT input files for QE and VASP from CIF/POSCAR/Materials Project. Covers INCAR, KPOINTS, POTCAR, POSCAR generation (VASPKIT 101-109 equivalent), and QE pw.x input generation with automatic pseudopotential selection. |
| [structure-editing](structure-editing/SKILL.md) | Build supercells, fix/move/delete/substitute atoms, redefine lattice vectors, convert between fractional and Cartesian coordinates, sort atoms by element/coordinate. Covers VASPKIT 400-415 equivalent. |
| [symmetry-analysis](symmetry-analysis/SKILL.md) | Find space group, point group, primitive/conventional cell, Wyckoff positions, equivalent atoms, symmetry of relaxed structures, molecular point group. Uses spglib and pymatgen. Covers VASPKIT 601-609 equivalent. |
| [format-conversion](format-conversion/SKILL.md) | Convert between CIF, POSCAR, XYZ, PDB, QE input, LAMMPS data, and extxyz formats. Bidirectional conversion with symmetry preservation. Covers VASPKIT 419 equivalent. |
| [xrd-pattern](xrd-pattern/SKILL.md) | Simulate powder X-ray diffraction patterns. Supports multiple wavelengths, peak labeling with hkl indices, phase comparison, and Scherrer broadening. |
| [pdf-analysis](pdf-analysis/SKILL.md) | Pair distribution function g(r) computation. Total and partial (element-specific) PDFs, crystalline vs amorphous comparison, MD trajectory averaging. |
| [structure-matching](structure-matching/SKILL.md) | Structure comparison and matching using pymatgen StructureMatcher. RMSD calculation, site mapping, symmetry comparison with spglib. |

## Decision Guide

```
What do you need to do with a crystal structure?

Advanced structure relaxation (custom optimizers, difficult convergence)?
  --> advanced-optimization/SKILL.md

Generate DFT input files?
  --> input-generation/SKILL.md

Modify the structure (supercell, substitution, fix atoms)?
  --> structure-editing/SKILL.md

Analyze or determine symmetry?
  --> symmetry-analysis/SKILL.md

Convert between file formats?
  --> format-conversion/SKILL.md

Simulate XRD patterns or compare phases by diffraction?
  --> xrd-pattern/SKILL.md

Compute pair distribution function g(r)?
  --> pdf-analysis/SKILL.md

Compare or match two structures (RMSD, symmetry, deduplication)?
  --> structure-matching/SKILL.md
```

## Common Prerequisites

- **Python packages**: pymatgen, ASE, spglib, numpy are pre-installed. Install extras with `pip install seekpath` as needed.
- **Structure files**: Start from a CIF, POSCAR, or query Materials Project with `mp-api`. All sub-skills show how to load structures from any common format.
- **Pseudopotentials**: QE input generation requires UPF files (SSSP library recommended). VASP input generation requires POTCAR files from a licensed VASP distribution.
