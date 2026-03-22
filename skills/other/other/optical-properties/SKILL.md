---
name: optical-properties
description: Optical Properties Calculations (6 sub-skills: absorption-spectrum, dielectric-function, joint-dos, optical-conductivity, slme, transition-dipole)
---

# Optical Properties Calculations

## Overview

This skill group covers the calculation of optical properties from first principles using Quantum ESPRESSO. The central quantity is the frequency-dependent dielectric function, from which all other optical properties (absorption coefficient, reflectivity, refractive index, optical conductivity) are derived.

The workflow always begins with a well-converged SCF calculation followed by QE's `epsilon.x` post-processing tool, which computes the dielectric function within the Random Phase Approximation (RPA) / independent-particle approximation.

**MACE cannot compute optical properties.** Optical response requires electronic wavefunctions and transition matrix elements, which are only available from DFT. MACE can be used to pre-relax the structure before a QE calculation.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Dielectric Function | `dielectric-function/` | Frequency-dependent dielectric function (real and imaginary parts), static dielectric constant, Born effective charges |
| Absorption Spectrum | `absorption-spectrum/` | Optical absorption coefficient, joint density of states, reflectivity, refractive index vs photon energy |
| Optical Conductivity | `optical-conductivity/` | Frequency-dependent optical conductivity from dielectric function, Drude model for metals, sum rules |

## Method Decision Guide

```
Need optical properties of a material?
  |
  +--> Step 1: Relax structure (MACE quick relax or QE vc-relax)
  |
  +--> Step 2: QE SCF with dense k-grid and many empty bands
  |
  +--> Step 3: epsilon.x to compute dielectric function
  |
  +--> Step 4: Post-process to desired property
         |
         +--> Dielectric function? --> dielectric-function/ skill
         |
         +--> Absorption, reflectivity, refractive index? --> absorption-spectrum/ skill
         |
         +--> Optical conductivity? --> optical-conductivity/ skill
```

## Common Prerequisites

- **Pseudopotentials**: QE calculations require pseudopotential files. All sub-skills show how to download SSSP pseudopotentials automatically.
- **Structure files**: Start from a CIF, POSCAR, or build with pymatgen/ASE.
- **Dense k-grid**: Optical properties converge slowly with k-point density. Use at least 12x12x12 for bulk, denser for small-gap systems.
- **Many empty bands**: `nbnd` must be large enough to capture transitions up to the desired photon energy. Typically 2--4x the number of occupied bands.
- **Python environment**: pymatgen, ASE, numpy, scipy, matplotlib are pre-installed.
- **QE executables**: `pw.x`, `epsilon.x`, `ph.x` (for Born charges).

## Important Notes

- QE `epsilon.x` computes the **independent-particle** (RPA) dielectric function. It does not include excitonic effects (use BSE/GW for that, not available in standard QE).
- PBE underestimates band gaps, which shifts optical absorption onset to lower energies. Use scissors correction (`intersmear` broadening can partially compensate but does not fix the gap).
- For metals, the intraband (Drude) contribution must be added separately -- see the optical-conductivity skill.
- All optical property sub-skills share the same SCF + epsilon.x foundation. Run SCF once, then derive multiple properties from the same epsilon.x output.
