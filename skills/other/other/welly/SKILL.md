---
name: welly
description: |
  Subsurface well data analysis toolkit for loading, processing, and analyzing
  well logs, projects, and formation tops. Built on lasio with enhanced curve
  processing. Use when Claude needs to: (1) Load wells from LAS files with
  metadata, (2) Work with multi-well Projects, (3) Process curves (despike,
  smooth, resample, normalize), (4) Manage formation tops, (5) Export well
  data to DataFrame/LAS/CSV, (6) Perform cross-well analysis and QC.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Well Logs, Petrophysics, Data Analysis, Multi-Well, Welly, LAS, Formation Tops, Curve Processing]
dependencies: [welly>=0.5.0, lasio]
complements: [lasio, dlisio, petropy, striplog, pyvista]
workflow_role: processing
---

# welly - Well Data Analysis

## Quick Reference

```python
from welly import Well, Project

# Load single well
w = Well.from_las('well.las')

# Access data
df = w.df()                      # DataFrame
gr = w.data['GR']                # Curve object
values = gr.values               # numpy array
depth = gr.basis                 # depth array

# Well info
print(w.name, w.uwi)
print(w.data.keys())             # Available curves

# Load multiple wells
p = Project.from_las('wells/*.las')
for well in p:
    print(well.name)
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `Well` | Single well with curves, location, tops |
| `Project` | Collection of wells for multi-well workflows |
| `Curve` | Log curve with depth basis, units, and processing methods |

## Essential Operations

### Access Curve Data
```python
gr = w.data['GR']
print(gr.mnemonic, gr.units)     # Metadata
print(gr.start, gr.stop, gr.step)  # Depth range
```

### Process Curves
```python
gr = w.data['GR']

# Clean and filter
gr_clean = gr.despike(window=5, z=2)
gr_smooth = gr.smooth(window=11)

# Transform
gr_norm = gr.normalize()         # 0-1 range
gr_resampled = gr.resample(step=0.5)
gr_clipped = gr.clip(top=1500, bottom=2000)
```

### Work with Formation Tops
```python
w.tops = {
    'TopFormationA': 1500.0,
    'TopFormationB': 1750.0,
}

for name, depth in w.tops.items():
    print(f"{name}: {depth} m")
```

### Multi-Well Project
```python
from welly import Project

p = Project.from_las('wells/*.las')
print(f"Loaded {len(p)} wells")

# Filter and analyze
for w in p:
    if 'GR' in w.data:
        print(f"{w.name}: GR mean={w.data['GR'].values.mean():.1f}")
```

### Export Data
```python
# To DataFrame
df = w.df()

# To LAS file
w.to_las('output.las')

# To CSV
df.to_csv('well_data.csv')
```

## Common Curve Mnemonics

| Mnemonic | Description | Units |
|----------|-------------|-------|
| GR | Gamma Ray | GAPI |
| NPHI | Neutron Porosity | v/v |
| RHOB | Bulk Density | g/cc |
| DT | Sonic | us/ft |
| RT/ILD | Deep Resistivity | ohm.m |
| CALI | Caliper | in |

## Tips

1. **Use Project** for multi-well workflows - easier than managing individual files
2. **Check units** - welly tracks units, ensure consistency
3. **Despike before analysis** - remove outliers with `curve.despike()`
4. **Resample to common basis** - use `curve.resample()` for cross-well comparison
5. **welly extends lasio** - all lasio functionality available

## When to Use vs Alternatives

| Tool | Best For |
|------|----------|
| **welly** | Multi-well projects, curve processing, formation tops management |
| **lasio** | Low-level LAS file I/O, header manipulation, malformed files |
| **petropy** | Petrophysical calculations (Vsh, porosity, Sw, permeability) |

**Use welly when** you need to manage wells as objects with curves, tops, and
metadata -- especially for multi-well QC and cross-well analysis via Project.

**Use lasio instead** when you only need to read/write LAS files, handle
malformed headers, or need fine control over LAS formatting.

**Use petropy instead** when your focus is formation evaluation calculations
(shale volume, porosity, water saturation) rather than data management.

## Common Workflows

### Load and QC a multi-well project
```
- [ ] Load wells with `Project.from_las('wells/*.las')`
- [ ] Check well count and names: `len(p)`, iterate wells
- [ ] Verify required curves exist in each well (`'GR' in w.data`)
- [ ] Despike and clean noisy curves: `curve.despike()`
- [ ] Resample to common depth basis for cross-well comparison
- [ ] Compute summary statistics per well (mean, min, max)
- [ ] Export cleaned data to LAS or DataFrame
```

## References

- **[Curve Processing](references/curve_processing.md)** - Despike, smooth, normalize, resample methods
- **[Project Workflows](references/project_workflows.md)** - Multi-well analysis patterns

## Scripts

- **[scripts/well_qc.py](scripts/well_qc.py)** - QC well data for gaps and issues
- **[scripts/project_stats.py](scripts/project_stats.py)** - Compute project-level statistics
