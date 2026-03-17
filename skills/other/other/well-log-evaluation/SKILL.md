---
name: well-log-evaluation
skill_type: workflow
description: |
  Complete well log evaluation workflow from LAS/DLIS loading through QC,
  petrophysical analysis, lithology classification, and visualization.
  Use when performing formation evaluation from well log data.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Well Logs, Petrophysics, LAS, DLIS, Formation Evaluation, Workflow]
dependencies: [lasio, welly, petropy, striplog, pyvista]
complements: [lasio, dlisio, welly, petropy, striplog, pyvista]
workflow_role: analysis
---

# Well Log Evaluation Workflow

End-to-end pipeline for formation evaluation, from loading well log files
through quality control, petrophysical analysis, lithology classification,
and multi-dimensional visualization.

## Skill Chain

```text
lasio/dlisio     welly           petropy         striplog        pyvista
[File I/O]   --> [QC & Prep]  --> [Petrophysics] --> [Lithology] --> [3D Viz]
  |               |                |                 |               |
  LAS parsing     Despike          Vshale calc       Facies log      3D well
  DLIS frames     Normalize        Porosity          Intervals       Fence diagram
  Curve extract   Merge curves     Sw, Perm          Correlation     Property vol
```

## Decision Points

| Question | If Yes | If No |
|----------|--------|-------|
| LAS format (.las)? | Use `lasio` for loading | Check DLIS format |
| DLIS format (.dlis)? | Use `dlisio` for loading | Check file type |
| Multiple wells or curve QC needed? | Use `welly` for management | Use lasio directly |
| Full formation evaluation (Sw, phi, Vsh)? | Use `petropy` | Compute manually with numpy |
| Need lithology column or stratigraphic log? | Use `striplog` | Skip to visualization |
| 3D well trajectory visualization? | Use `pyvista` | Use matplotlib for log plots |

## Step-by-Step Orchestration

### Stage 1: Data Loading (lasio / dlisio)

```python
import lasio
import numpy as np
import pandas as pd

# Load LAS file
las = lasio.read('well_A.las')
df = las.df().reset_index()  # DataFrame with depth as column
null_val = float(las.well['NULL'].value)
df = df.replace(null_val, np.nan)

# Inspect available curves
print(las.curves.keys())  # ['DEPT', 'GR', 'RHOB', 'NPHI', 'RT', 'DT']
well_name = las.well['WELL'].value
```

```python
import dlisio

# Load DLIS file (for modern well data)
with dlisio.dlis.load('well_B.dlis') as files:
    f = files[0]
    for frame in f.frames:
        print(frame.name, [ch.name for ch in frame.channels])
    # Extract channels to numpy arrays
    frame = f.frames[0]
    depth = frame.channels[0].curves()
    gr = frame.channels[1].curves()
```

### Stage 2: QC and Preparation (welly)

```python
from welly import Well, Curve

# Load well with welly (uses lasio internally)
w = Well.from_las('well_A.las')

# Access curves
gr = w.data['GR']
print(gr.start, gr.stop, gr.step)

# Despike gamma ray log
gr_clean = gr.despike(z=2.0)  # Remove spikes > 2 std dev

# Normalize to 0-1 range
gr_norm = (gr_clean - gr_clean.min()) / (gr_clean.max() - gr_clean.min())

# Resample curves to common depth basis
df_resampled = w.df(keys=['GR', 'RHOB', 'NPHI', 'RT'], step=0.5)
df_resampled = df_resampled.dropna()
```

### Stage 3: Petrophysical Analysis (petropy)

```python
import petropy as ptr

# Load into petropy Log object
log = ptr.Log(las)

# Formation evaluation workflow
# 1. Calculate Vshale from GR
log.formation_multimineral_model()

# Manual Vshale calculation (linear method)
gr = df['GR'].values
gr_clean = np.nanmin(gr)   # Sand line
gr_shale = np.nanmax(gr)   # Shale line
vshale = (gr - gr_clean) / (gr_shale - gr_clean)
vshale = np.clip(vshale, 0, 1)

# 2. Porosity from density log
rho_matrix = 2.65   # g/cc (quartz)
rho_fluid = 1.0     # g/cc (freshwater)
phi_density = (rho_matrix - df['RHOB']) / (rho_matrix - rho_fluid)
phi_density = np.clip(phi_density, 0, 0.5)

# 3. Water saturation (Archie equation)
a, m, n = 1.0, 2.0, 2.0  # Archie parameters
Rw = 0.05                  # Formation water resistivity (ohm-m)
Rt = df['RT'].values       # True resistivity
phi = phi_density.values
Sw = ((a * Rw) / (phi**m * Rt))**(1/n)
Sw = np.clip(Sw, 0, 1)

# 4. Permeability (Timur-Coates)
k_timur = 0.136 * (phi**4.4) / (Sw**2) * 1e4  # mD
```

### Stage 4: Lithology Classification (striplog)

```python
from striplog import Striplog, Component, Interval

# Build lithology log from Vshale cutoffs
intervals = []
depth = df['DEPT'].values
for i in range(len(depth) - 1):
    if vshale[i] < 0.3:
        lith = Component({'lithology': 'sandstone'})
    elif vshale[i] < 0.6:
        lith = Component({'lithology': 'siltstone'})
    else:
        lith = Component({'lithology': 'shale'})
    intervals.append(Interval(top=depth[i], base=depth[i+1], components=[lith]))

strip = Striplog(intervals)
strip = strip.anneal()  # Merge adjacent identical intervals

# Display
strip.plot(aspect=10)
```

### Stage 5: Visualization (pyvista)

```python
import pyvista as pv

# 3D well path with property
trajectory = np.column_stack([
    df['X'].values, df['Y'].values, df['DEPT'].values * -1
])
well_path = pv.Spline(trajectory, n_points=len(trajectory))
well_path['GR'] = df['GR'].values
well_path['Porosity'] = phi_density.values

plotter = pv.Plotter()
plotter.add_mesh(well_path, scalars='Porosity', cmap='viridis',
                 line_width=5, render_lines_as_tubes=True)
plotter.show()
```

## Common Pipelines

### Standard Formation Evaluation
```
- [ ] Load LAS file with `lasio.read()`, replace null values with NaN
- [ ] Inspect available curves (GR, RHOB, NPHI, RT, DT minimum)
- [ ] QC curves with welly: despike, check ranges, identify washouts (caliper)
- [ ] Calculate Vshale from GR (linear, Larionov, or Clavier method)
- [ ] Calculate porosity from density or neutron-density crossplot
- [ ] Calculate water saturation using Archie or dual-water model
- [ ] Estimate permeability from Timur-Coates or Wyllie-Rose
- [ ] Flag pay zones: phi > cutoff, Sw < cutoff, Vsh < cutoff
- [ ] Generate composite log plot (GR, resistivity, porosity, Sw, pay flag)
- [ ] Export results to LAS or CSV
```

### Multi-Well Correlation
```
- [ ] Load multiple LAS files with lasio or welly batch loading
- [ ] Standardize curve mnemonics across wells (GR, GRGC, SGR -> GR)
- [ ] Normalize GR logs to common scale across wells
- [ ] Pick formation tops manually or from Vshale transitions
- [ ] Create striplog for each well with formation intervals
- [ ] Build correlation panel with matplotlib or pyvista
- [ ] Export formation tops to CSV
```

### Quick Log QC
```
- [ ] Load LAS file with `lasio.read()`
- [ ] Check depth range, step, and null values
- [ ] Print curve statistics: min, max, mean, NaN count
- [ ] Flag out-of-range values (GR: 0-300, RHOB: 1.5-3.0, NPHI: -0.05-0.6)
- [ ] Check for constant or stuck readings
- [ ] Identify depth intervals with poor data (washout from caliper)
- [ ] Plot all curves for visual inspection
```

## When to Use

Use the well log evaluation workflow when:

- Performing formation evaluation from LAS or DLIS well log data
- Running petrophysical calculations (Vshale, porosity, Sw, permeability)
- Building lithology classifications from log responses
- Correlating formations across multiple wells
- Generating composite log displays or 3D well visualizations

Use individual domain skills when:
- Only reading/writing LAS files (use `lasio` alone)
- Only parsing DLIS data (use `dlisio` alone)
- Only making stereonet plots from oriented data (use `mplstereonet`)

## Common Issues

| Issue | Solution |
|-------|----------|
| LAS encoding errors | Use `lasio.read(f, encoding='latin-1')` |
| Curves have different depth sampling | Resample with `welly` or `np.interp` |
| Negative porosity values | Clip to 0; check matrix density assumption |
| Sw > 1.0 from Archie | Check Rw, Archie parameters; use clay-corrected model |
| Vshale > 1 in hot shales | Apply non-linear Vshale correction (Larionov) |
| DLIS multi-frame confusion | Iterate `f.frames` to find correct frame with target channels |
