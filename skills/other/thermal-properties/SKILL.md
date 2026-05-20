---
name: thermal-properties
description: Thermal Properties (13 sub-skills: anharmonicity, bond-distribution, free-energy-calculation, gruneisen-qha, md-trajectory-tools, molecular-dynamics, msd-diffusion, phonon, phonon-from-outcar, quasi-harmonic-debye, rdf-analysis, thermal-conductivity, vacf-vdos)
---

# Thermal Properties

Phonon calculations, molecular dynamics, free energy calculations, and quasi-harmonic thermodynamics for crystalline and amorphous materials.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Phonon Calculations | `phonon/` | Harmonic phonon band structure, DOS, and thermodynamic properties via finite displacements (ASE+MACE+phonopy) or DFPT (QE ph.x) |
| Molecular Dynamics | `molecular-dynamics/` | NVE/NVT/NPT MD simulations with ASE+MACE or LAMMPS; trajectory analysis (RDF, MSD, diffusion) |
| Free Energy Calculation | `free-energy-calculation/` | Helmholtz/Gibbs free energy via thermodynamic integration (Frenkel-Ladd for solids, UF model for liquids, reversible scaling for F(T)), phase stability and melting points |
| Gruneisen and QHA | `gruneisen-qha/` | Mode Gruneisen parameters, quasi-harmonic approximation for thermal expansion and T-dependent bulk modulus |
| Quasi-Harmonic Debye Model | `quasi-harmonic-debye/` | Debye model thermodynamics from E(V) data: Debye temperature, heat capacity, thermal expansion, Gruneisen parameter without phonon calculations |
| Anharmonicity Score | `anharmonicity/` | Quantify anharmonicity (sigma^A) via one-shot thermal displacement; decide if QHA is valid or MD is needed |

## Method Decision Guide

```
What thermal property do you need?

Phonon band structure / DOS / Cv / entropy / free energy (harmonic)?
  --> phonon/  (finite displacement or DFPT)

Helmholtz/Gibbs free energy (full anharmonic) / melting point / phase stability?
  --> free-energy-calculation/  (thermodynamic integration via LAMMPS)

Diffusion coefficient / melting / phase transition / liquid properties?
  --> molecular-dynamics/  (MD simulation)

Thermal expansion / T-dependent bulk modulus / Gruneisen parameters?
  --> gruneisen-qha/  (QHA with phonons at multiple volumes)

Quick Debye temperature / heat capacity estimate without phonon calculations?
  --> quasi-harmonic-debye/  (Debye model from E(V) curve only)

Is my material too anharmonic for QHA? Need sigma^A score?
  --> anharmonicity/  (one-shot thermal displacement test)
      sigma^A < 0.2  --> QHA is safe
      sigma^A 0.2-0.5 --> QHA is marginal, validate with MD
      sigma^A > 0.5  --> Use MD instead of QHA

Quick screening vs. publication accuracy?
  Quick --> ASE + MACE (all sub-skills support this)
  Publication --> QE DFT (phonon/, gruneisen-qha/) or LAMMPS with validated potential (molecular-dynamics/, free-energy-calculation/)
```
