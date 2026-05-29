---
name: 2d-materials
description: 2D Materials Toolkit (4 sub-skills: band-edges, layer-manipulation, stacking-energy, vacuum-resize)
---

# 2D Materials Toolkit

## Overview

This skill group covers computational tools for building, manipulating, and analyzing 2D (layered) materials. It corresponds to VASPKIT menu 92 (tasks 920-929) and provides workflows for layer manipulation, vacuum control, band edge alignment, and stacking energy calculations.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Layer Manipulation | `layer-manipulation/` | Move/center atomic layers, standardize 2D cell orientation, extract monolayers from bulk (VASPKIT 920-923) |
| Vacuum Resize | `vacuum-resize/` | Resize vacuum thickness for slab/2D models, optimize vacuum for convergence testing (VASPKIT 922) |
| Band Edges | `band-edges/` | Band edge alignment relative to vacuum level: work function, ionization potential, electron affinity (VASPKIT 927) |
| Stacking Energy | `stacking-energy/` | Stacking-dependent potential energy surface for layered materials, interlayer binding energy vs lateral displacement (VASPKIT 926) |

## Method Decision Guide

```
Need to prepare a 2D material structure?
  --> layer-manipulation/ (center layers, extract monolayer, set orientation)

Need to adjust vacuum for slab calculations?
  --> vacuum-resize/ (set vacuum thickness, convergence testing)

Need band edge positions for photocatalysis or heterojunction design?
  --> band-edges/ (vacuum level alignment from electrostatic potential)

Need interlayer interaction energy or stacking order preference?
  --> stacking-energy/ (PES scan of lateral displacement)

Need to build a 2D heterostructure?
  --> layer-manipulation/ + vacuum-resize/ (stack layers, set spacing, add vacuum)
```

## Common Prerequisites

- **pymatgen**: Structure manipulation, slab generation
- **ASE**: Structure I/O, calculator interface
- **MACE**: Fast energy calculations for screening
- **Quantum ESPRESSO**: DFT-quality electronic structure (band edges, accurate energies)
- **numpy, matplotlib**: Numerical analysis and plotting
