---
name: materials-databases
description: Materials Databases Toolkit (2 sub-skills: 2d-semiconductors, materials-project)
---

# Materials Databases Toolkit

## Overview

This skill group covers querying and using computational materials databases for structure retrieval, property screening, and phase diagram construction. It corresponds to VASPKIT menu 07 (tasks 702, 705) and leverages the Materials Project API (mp-api) and computational 2D materials databases.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Materials Project | `materials-project/` | Query the Materials Project API (mp-api) for structures, properties, phase diagrams, and band gaps. Search by formula, composition, or property range. (VASPKIT 702) |
| 2D Semiconductors | `2d-semiconductors/` | Access computational 2D semiconductor databases, screen 2D materials by band gap, stability, and electronic properties. (VASPKIT 705) |

## Method Decision Guide

```
Need a crystal structure for a known composition?
  --> materials-project/ (search by formula or mp-id)

Need to screen materials by band gap, formation energy, or other properties?
  --> materials-project/ (property-based queries)

Need a phase diagram or convex hull?
  --> materials-project/ (PhaseDiagram from mp-api entries)

Need 2D material structures or properties?
  --> 2d-semiconductors/ (specialized 2D databases)

Need to find stable 2D semiconductors for a specific application?
  --> 2d-semiconductors/ (screen by band gap, band edge alignment)
```

## Common Prerequisites

- `mp-api` package (`pip install mp-api`)
- A valid Materials Project API key (set as `MP_API_KEY` environment variable)
- `pymatgen` (structure handling, phase diagram analysis)
- `matplotlib` (plotting)
