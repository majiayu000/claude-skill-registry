---
name: mplstereonet
description: |
  Stereonet plots for structural geology using matplotlib. Create lower-hemisphere
  stereographic projections for orientation data. Use when Claude needs to: (1) Create
  stereonet plots for structural data, (2) Plot planes as great circles or poles,
  (3) Plot lineations with trend/plunge, (4) Generate density contours for orientations,
  (5) Calculate mean orientations and statistics, (6) Analyze fold axes with pi-diagrams,
  (7) Convert between strike/dip and trend/plunge formats.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Structural Geology, Stereonet, Orientation Data, Matplotlib, Visualization]
dependencies: [mplstereonet>=0.6, matplotlib, numpy]
complements: []
workflow_role: visualization
---

# mplstereonet - Stereonets for Matplotlib

## Quick Reference

```python
import mplstereonet
import matplotlib.pyplot as plt

# Create stereonet
fig, ax = mplstereonet.subplots()

# Plot plane and pole (strike/dip, right-hand rule)
ax.plane(315, 45, 'b-')          # Great circle
ax.pole(315, 45, 'ko')           # Pole to plane

# Plot lineation (trend/plunge)
ax.line(120, 30, 'r^')

ax.grid()
plt.savefig('stereonet.png', dpi=150)
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `mplstereonet.subplots()` | Create stereonet figure and axes |
| `ax.plane(strike, dip)` | Plot great circle |
| `ax.pole(strike, dip)` | Plot pole to plane |
| `ax.line(trend, plunge)` | Plot lineation point |
| `ax.density_contourf()` | Filled density contours |
| `mplstereonet.fit_girdle()` | Best-fit great circle |
| `mplstereonet.find_mean_vector()` | Mean orientation |

## Essential Operations

### Multiple Measurements with Contours
```python
import numpy as np

strikes = [45, 52, 38, 48, 55, 41, 50, 43]
dips = [25, 30, 22, 28, 35, 24, 32, 27]

fig, ax = mplstereonet.subplots()

# Density contour of poles
ax.density_contourf(strikes, dips, measurement='poles', cmap='Reds')
ax.pole(strikes, dips, 'k.', markersize=5)

ax.grid()
ax.set_title('Bedding Orientations')
plt.savefig('density.png', dpi=150)
```

### Calculate Mean Orientation
```python
# Fit best-fit plane (girdle)
mean_strike, mean_dip = mplstereonet.fit_girdle(strikes, dips)

# Or calculate mean pole for clustered data
lon, lat = mplstereonet.pole(strikes, dips)
mean_lon, mean_lat = mplstereonet.find_mean_vector(lon, lat)
mean_s, mean_d = mplstereonet.pole2strike(mean_lon, mean_lat)
```

### Pi-Diagram (Fold Axis)
```python
# Bedding measurements around a fold
strikes = np.array([20, 35, 50, 70, 90, 110, 130, 150, 165, 180])
dips = np.array([45, 40, 35, 30, 25, 30, 35, 40, 45, 50])

fig, ax = mplstereonet.subplots()
ax.pole(strikes, dips, 'ko', markersize=6)

# Fit girdle to poles - fold axis is pole to girdle
girdle_strike, girdle_dip = mplstereonet.fit_girdle(strikes, dips)
ax.plane(girdle_strike, girdle_dip, 'r-', linewidth=2)

fold_trend, fold_plunge = mplstereonet.pole(girdle_strike, girdle_dip)
ax.line(fold_trend, fold_plunge, 'r^', markersize=12, label='Fold axis')

ax.grid()
ax.legend()
```

### Fault Plane with Slip Vector
```python
fault_strike, fault_dip = 45, 60
rake = 30  # Degrees from strike

# Convert rake to trend/plunge
slip_trend, slip_plunge = mplstereonet.rake(fault_strike, fault_dip, rake)

fig, ax = mplstereonet.subplots()
ax.plane(fault_strike, fault_dip, 'r-', linewidth=2)
ax.line(slip_trend, slip_plunge, 'r>', markersize=10)
ax.grid()
```

### Multiple Joint Sets
```python
set1 = {'strikes': [45, 50, 42, 48], 'dips': [70, 75, 68, 72]}
set2 = {'strikes': [135, 140, 130, 138], 'dips': [60, 65, 58, 62]}

fig, ax = mplstereonet.subplots()
ax.pole(set1['strikes'], set1['dips'], 'ro', label='Set 1')
ax.pole(set2['strikes'], set2['dips'], 'bs', label='Set 2')
ax.grid()
ax.legend()
```

## Measurement Conventions

| Format | Description | Example |
|--------|-------------|---------|
| Strike/Dip | Right-hand rule (dip to right of strike) | 045/60 |
| Dip Direction/Dip | Azimuth of dip direction | 135/60 |
| Trend/Plunge | Linear orientation | 180/30 |

## Format Conversions

```python
# Strike/dip to dip direction
strike, dip = 45, 60
dip_direction = (strike + 90) % 360

# Pole to strike/dip
lon, lat = mplstereonet.pole(strike, dip)
back_strike, back_dip = mplstereonet.pole2strike(lon, lat)
```

## Contouring Methods

| Method | Description |
|--------|-------------|
| `kamb` | Statistical significance (default) |
| `schmidt` | Point counting |
| `exponential_kamb` | Smoothed Kamb |

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **mplstereonet** | Quick stereonets in Python, matplotlib integration, scripted workflows | No interactive rotation, limited 3D |
| **apsg** | Advanced structural analysis, tensors, orientation statistics | Steeper learning curve |
| **JTOPO** | Interactive GUI exploration, teaching | Java-based, not scriptable |

**Use mplstereonet when** you need programmatic stereonet generation integrated with
matplotlib, batch processing of orientation datasets, or reproducible structural plots
for publications.

**Consider alternatives when** you need interactive 3D visualization of orientations
(use apsg), a GUI for teaching or quick inspection (use JTOPO), or advanced tensor
statistics beyond what mplstereonet provides.

## Common Workflows

### Analyze bedding orientations and determine fold axis
- [ ] Load strike/dip measurements from CSV or array
- [ ] Create stereonet with `mplstereonet.subplots()`
- [ ] Plot poles to bedding with `ax.pole(strikes, dips)`
- [ ] Generate density contours with `ax.density_contourf()`
- [ ] Fit girdle to poles with `mplstereonet.fit_girdle()`
- [ ] Calculate fold axis as pole to girdle with `mplstereonet.pole()`
- [ ] Plot fold axis with `ax.line(trend, plunge)`
- [ ] Add grid, legend, and save figure

## References

- **[Projection Types](references/projections.md)** - Equal-area vs equal-angle projections
- **[Plotting Options](references/plotting_options.md)** - Customization and styling

## Scripts

- **[scripts/structural_analysis.py](scripts/structural_analysis.py)** - Analyze structural data and generate plots
