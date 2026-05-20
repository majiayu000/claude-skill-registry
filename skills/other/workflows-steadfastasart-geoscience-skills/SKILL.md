---
name: using-geoscience-skills
skill_type: meta
description: |
  Foundation skill for the geoscience skills library. Routes user intent
  to the correct domain skills, slash commands, and workflow skills.
  Loaded automatically at session start via SessionStart hook.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geoscience, Skills, Routing, Discovery, Workflows, Agents]
dependencies: []
---

# Using Geoscience Skills

Meta-skill for discovering, routing, and composing the geoscience skills library.
This skill maps user intent to domain skills, workflow skills, slash commands, and agents.

## Domain Routing Table

Match user intent keywords to the appropriate domain skill.

| Keywords / Triggers | Skill | Domain |
|---------------------|-------|--------|
| SEG-Y, seismic traces, trace headers, inline, crossline | `segyio` | Seismic I/O |
| waveform, earthquake, FDSN, seismogram, miniSEED | `obspy` | Seismology |
| surface wave, dispersion, Rayleigh, Love wave | `disba` | Seismology |
| LAS, well logs, wireline, borehole curves | `lasio` | Well Logs |
| DLIS, RP66, array logs, modern well data | `dlisio` | Well Logs |
| well analysis, curve QC, multi-well, despike | `welly` | Well Logs |
| petrophysics, Sw, porosity, formation evaluation | `petropy` | Petrophysics |
| lithology, stratigraphy, striplog, facies log | `striplog` | Stratigraphy |
| 3D model, geology, implicit surface, faults | `gempy` | 3D Modelling |
| fold modelling, structural frame, Loop3D | `loopstructural` | 3D Modelling |
| GIS, spatial data prep, borehole to GemPy | `gemgis` | GIS Preprocessing |
| inversion, DC resistivity, magnetics, gravity, EM | `simpeg` | Inversion |
| ERT, SRT, IP, near-surface inversion | `pygimli` | Inversion |
| PDE, wave equation, finite differences, stencil | `devito` | Simulation |
| linear operator, inverse problem, sparsity | `pylops` | Inverse Problems |
| gravity, magnetic, Bouguer, upward continuation | `harmonica` | Potential Fields |
| AVO, Zoeppritz, Gassmann, fluid substitution, wavelet | `bruges` | Rock Physics |
| gridding, interpolation, spatial, Verde | `verde` | Spatial Analysis |
| variogram, kriging, GSLIB, geostatistics | `geostatspy` | Geostatistics |
| variogram fitting, scikit-learn style geostat | `scikit-gstat` | Geostatistics |
| groundwater, time series, pumping test | `pastas` | Hydrology |
| landscape, erosion, surface processes, DEM | `landlab` | Surface Processes |
| stereonet, strike, dip, poles, structural | `mplstereonet` | Structural Geology |
| geochemistry, REE, spider diagram, ternary | `pyrolite` | Geochemistry |
| GPR, ground-penetrating radar, radargram | `gprpy` | Near-Surface |
| magnetotellurics, MT, impedance tensor | `mtpy` | Near-Surface |
| NetCDF, xarray, multi-dimensional, climate | `xarray` | Data Formats |
| 3D visualization, mesh, VTK, point cloud | `pyvista` | Visualization |
| data download, sample data, cache, fetch | `pooch` | Utilities |

## Workflow Skills

Workflow skills chain multiple domain skills into end-to-end pipelines.

| Workflow | Slash Command | Skill Chain |
|----------|---------------|-------------|
| Seismic Interpretation | `/seismic-workflow` | segyio -> obspy -> bruges -> disba -> pyvista |
| Well Log Evaluation | `/well-analysis` | lasio/dlisio -> welly -> petropy -> striplog -> pyvista |
| Geological Modelling | `/model-3d` | gemgis -> gempy/loopstructural -> pyvista |
| Geophysical Inversion | `/inversion-workflow` | simpeg/pygimli -> verde -> pyvista |
| Rock Physics & AVO | `/rock-physics` | lasio/welly -> bruges -> segyio |

## Available Agents

| Agent | Purpose | Typical Trigger |
|-------|---------|-----------------|
| `data-qc-reviewer` | Automated data quality checks across formats | "QC my data", "check data quality" |
| `geoscience-mentor` | Guided explanations of geoscience concepts and methods | "explain", "teach me", "what is" |

## All 29 Domain Skills by Category

### Seismic and Seismology
- `segyio` -- SEG-Y file I/O, trace and header access
- `obspy` -- seismological waveform processing, FDSN services
- `disba` -- surface wave dispersion (Rayleigh, Love)

### Well Log Analysis
- `lasio` -- LAS file reading and writing
- `dlisio` -- DLIS/RP66 binary well log parsing
- `welly` -- well data analysis, curve QC, multi-well projects
- `petropy` -- petrophysical analysis, formation evaluation
- `striplog` -- lithological and stratigraphic log display

### 3D Geological Modelling
- `gempy` -- implicit 3D geological modelling
- `loopstructural` -- 3D modelling with fold and fault support
- `gemgis` -- spatial data preprocessing for GemPy

### Geophysical Inversion
- `simpeg` -- multi-method geophysical inversion framework
- `pygimli` -- ERT, SRT, IP inversion with simple API
- `devito` -- symbolic PDE solver for wave propagation
- `pylops` -- linear operators for inverse problems

### Potential Fields and Rock Physics
- `harmonica` -- gravity and magnetic data processing
- `bruges` -- AVO, Gassmann, wavelets, elastic moduli

### Spatial Analysis and Geostatistics
- `verde` -- spatial gridding and interpolation
- `geostatspy` -- variograms, kriging (GSLIB-style)
- `scikit-gstat` -- geostatistics with scikit-learn API

### Hydrology and Surface Processes
- `pastas` -- groundwater time series modelling
- `landlab` -- landscape evolution modelling

### Structural Geology and Geochemistry
- `mplstereonet` -- stereonet plots for orientation data
- `pyrolite` -- geochemical analysis and diagrams

### Near-Surface Geophysics
- `gprpy` -- GPR data processing
- `mtpy` -- magnetotelluric data analysis

### Data Formats and Visualization
- `xarray` -- NetCDF, multi-dimensional labeled arrays
- `pyvista` -- 3D mesh visualization and analysis
- `pooch` -- data file fetching and caching

## Skill Composition Rules

Chain skills when a task spans multiple stages of a geoscience workflow.

### Composition Patterns

```text
Data Loading -> Processing -> Modelling -> Visualization

1. Always start with a data I/O skill (segyio, lasio, dlisio, xarray)
2. Use processing skills for QC and transformation (welly, obspy, verde)
3. Apply domain modelling (bruges, gempy, simpeg, pygimli)
4. Finish with visualization (pyvista, matplotlib via domain skill)
```

### When to Chain vs Use Standalone

| Scenario | Approach |
|----------|----------|
| Single file format question | Standalone domain skill |
| End-to-end analysis pipeline | Workflow skill to orchestrate |
| Data QC across formats | `data-qc-reviewer` agent |
| Concept explanation | `geoscience-mentor` agent |
| Multi-library code generation | Chain domain skills in order |

### Dependency Awareness

When composing skills, respect data flow:

```python
# Correct: segyio loads, obspy processes, bruges models
import segyio
import obspy
from bruges.reflection import zoeppritz

# Load with segyio
with segyio.open('seismic.sgy') as f:
    data = f.trace[:]

# Process with obspy (convert to Stream if needed)
# Model with bruges
Rpp = zoeppritz(vp1, vs1, rho1, vp2, vs2, rho2, theta)
```

## When to Use This Skill

This is the **discovery and routing** skill. Use it when:

- Starting a new geoscience coding session and unsure which library to use
- A user request spans multiple geoscience domains
- You need to find the right slash command or workflow for a task
- Composing multiple domain skills into a pipeline
- Looking up which skill handles a specific file format or analysis type

This skill does not perform any analysis itself. It directs to the appropriate
domain skill, workflow skill, or agent for execution.

## Quick Decision Tree

```text
User wants to...
  |
  +-- Load/write a file? --> Check format:
  |     SEG-Y -> segyio    LAS -> lasio    DLIS -> dlisio
  |     NetCDF -> xarray    VTK -> pyvista
  |
  +-- Process signals? --> obspy (seismology), welly (well logs)
  |
  +-- Build a model?
  |     3D geology -> gempy or loopstructural
  |     Rock physics -> bruges
  |     Inversion -> simpeg or pygimli
  |
  +-- Visualize results? --> pyvista (3D), matplotlib (2D via domain skill)
  |
  +-- Run a full pipeline? --> Use workflow skills above
```
