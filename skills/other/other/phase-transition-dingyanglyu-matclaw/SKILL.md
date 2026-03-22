---
name: phase-transition
description: Phase Transitions (6 sub-skills: amorphous-structure, melting-point-coexistence, metadynamics, mpmorph-melting, order-parameter, phase-diagram)
---

# Phase Transitions

Melting point determination, amorphous structure generation, free energy surface exploration via metadynamics, and solid-solid phase transition analysis using molecular dynamics and energy-based methods.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| MPMorph Melting | `mpmorph-melting/` | Melting point determination via heating curves, Lindemann criterion, two-phase coexistence, and liquid structure analysis (ASE+MACE or LAMMPS) |
| Amorphous Structure | `amorphous-structure/` | Amorphous/glassy structure generation via melt-quench MD; structural analysis (RDF, coordination, bond angles, structure factor); glass transition temperature |
| Melting Point Coexistence | `melting-point-coexistence/` | Melting point via solid-liquid coexistence method (two-phase simulation); more accurate than heating curves; MACE or LAMMPS |
| Metadynamics | `metadynamics/` | Free energy surface exploration via well-tempered metadynamics; bias potential on collective variables (distance, coordination number, volume, Steinhardt Q6); ASE+MACE or LAMMPS+PLUMED; FES reconstruction and convergence analysis |

## Method Decision Guide

```
What phase transition property do you need?

Melting point / melting temperature?
  --> mpmorph-melting/  (heating curve or Lindemann criterion)
  --> melting-point-coexistence/  (solid-liquid coexistence, more accurate)

Liquid structure (RDF, diffusion, viscosity)?
  --> mpmorph-melting/  (high-temperature MD above Tm)

Amorphous / glassy structure generation?
  --> amorphous-structure/  (melt-quench protocol)

Glass transition temperature (Tg)?
  --> amorphous-structure/  (volume vs T during quench)

Structural analysis of disordered phase (RDF, coordination, bond angles)?
  --> amorphous-structure/  (post-processing tools)

Free energy surface / barrier for rare events (phase transition, diffusion, reaction)?
  --> metadynamics/  (well-tempered metadynamics with ASE+MACE or LAMMPS+PLUMED)

Free energy landscape along structural order parameters (Q4, Q6)?
  --> metadynamics/  (Steinhardt CV with PLUMED)

Quick screening vs. publication accuracy?
  Quick --> ASE + MACE (both sub-skills support this)
  Publication --> LAMMPS with validated potential (mpmorph-melting/) or larger MACE supercells
```
