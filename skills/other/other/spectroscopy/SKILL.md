---
name: spectroscopy
description: Spectroscopy Simulation (2 sub-skills: raman-ir, xas-xanes)
---

# Spectroscopy Simulation

## Overview

Skills for computing spectroscopic observables from first principles: vibrational spectra (IR, Raman) and core-level X-ray absorption spectra (XAS/XANES). These connect atomistic simulations to experimental measurements.

## Sub-skills

| Skill | Path | Description |
|-------|------|-------------|
| [Raman & IR Spectroscopy](raman-ir/SKILL.md) | `raman-ir/` | Compute infrared and Raman spectra from Gamma-point phonons. Uses QE `ph.x` or MACE + finite differences. Includes Born effective charges, dielectric tensors, and Lorentzian broadening. |
| [XAS/XANES Spectroscopy](xas-xanes/SKILL.md) | `xas-xanes/` | Simulate X-ray absorption near-edge structure using QE `xspectra.x`. Core-hole pseudopotential approach for K-edge and L-edge spectra. |

## Typical Workflow

1. **Relax structure** with QE `pw.x` or MACE.
2. **IR/Raman**: Compute Gamma-point phonons, extract intensities, plot spectra.
3. **XAS/XANES**: Run core-hole SCF, then `xspectra.x` for absorption cross-section.

## Prerequisites

```bash
# QE binaries: pw.x, ph.x, pp.x, dynmat.x, xspectra.x
# Python: ase, pymatgen, phonopy (pip install phonopy), numpy, scipy, matplotlib
# MACE: mace-torch (for finite-difference approach)
```
