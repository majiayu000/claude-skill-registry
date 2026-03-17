---
name: mtpy
description: |
  Magnetotelluric data processing and modelling. Read EDI files, analyze MT
  responses, perform inversions, and visualize resistivity models. Use when
  Claude needs to: (1) Read/write EDI files, (2) Process MT impedance tensors,
  (3) Analyze phase tensors and dimensionality, (4) Plot apparent resistivity
  and phase curves, (5) Create pseudosections, (6) Perform strike analysis,
  (7) Run 1D inversions, (8) Prepare data for 2D/3D modelling.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Magnetotellurics, MT, EDI, Impedance Tensor, EM, Geophysics]
dependencies: [mtpy>=2.0.0, numpy, matplotlib]
complements: [simpeg, pyvista]
workflow_role: analysis
---

# mtpy - Magnetotelluric Analysis

## Quick Reference

```python
from mtpy import MT, MTCollection

# Read single station
mt = MT('station001.edi')

# Access data
Z = mt.Z                         # Complex impedance tensor
freq = mt.frequency              # Frequency array
rho_xy = mt.apparent_resistivity[:, 0, 1]  # Apparent resistivity

# Station info
print(mt.station, mt.latitude, mt.longitude)

# Write EDI
mt.write_edi('output.edi')
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `MT` | Single station MT data container |
| `MTCollection` | Multiple stations management |
| `PlotMTResponse` | Plot impedance, resistivity, phase |
| `PlotPhaseTensor` | Phase tensor ellipse visualization |
| `PlotPseudoSection` | Profile pseudosection display |
| `PlotStrike` | Strike direction analysis |

## Essential Operations

### Load and Inspect EDI
```python
from mtpy import MT

mt = MT('station001.edi')
print(f"Station: {mt.station}")
print(f"Location: ({mt.latitude}, {mt.longitude})")
print(f"Frequencies: {len(mt.frequency)} points")
print(f"Period range: {1/mt.frequency.max():.2f} - {1/mt.frequency.min():.0f} s")
```

### Load Multiple Stations
```python
from mtpy import MTCollection

mc = MTCollection()
mc.from_edis('survey_data/*.edi')
print(f"Loaded {len(mc)} stations")

for station in mc:
    print(f"  {station.station}: ({station.latitude:.4f}, {station.longitude:.4f})")
```

### Plot MT Response
```python
from mtpy import MT
from mtpy.imaging import PlotMTResponse

mt = MT('station001.edi')
plot = PlotMTResponse(mt)
plot.plot()  # Apparent resistivity and phase
```

### Phase Tensor Analysis
```python
from mtpy import MT
from mtpy.imaging import PlotPhaseTensor

mt = MT('station001.edi')

# Get phase tensor parameters
phi_min = mt.phase_tensor.phimin
phi_max = mt.phase_tensor.phimax
skew = mt.phase_tensor.skew       # 3D indicator

# Plot
pt = PlotPhaseTensor(mt)
pt.plot()
```

### Rotate Impedance Tensor
```python
from mtpy import MT

mt = MT('station001.edi')
mt_rotated = mt.rotate(30)        # 30 degrees clockwise
mt.rotate_to_strike()             # Auto-rotate to geoelectric strike
```

### Create Pseudosection
```python
from mtpy import MTCollection
from mtpy.imaging import PlotPseudoSection

mc = MTCollection()
mc.from_edis('profile/*.edi')

ps = PlotPseudoSection(mc)
ps.plot(plot_type='apparent_resistivity', mode='te')  # or 'tm', 'det'
```

### Export Data
```python
from mtpy import MT
import pandas as pd

mt = MT('station001.edi')

# Export to CSV
df = pd.DataFrame({
    'frequency': mt.frequency,
    'rho_xy': mt.apparent_resistivity[:, 0, 1],
    'rho_yx': mt.apparent_resistivity[:, 1, 0],
    'phase_xy': mt.phase[:, 0, 1],
    'phase_yx': mt.phase[:, 1, 0]
})
df.to_csv('mt_data.csv', index=False)

# Export for ModEM
mt.write_modem('station001.dat')
```

## Impedance Tensor Components

| Component | Description | Mode |
|-----------|-------------|------|
| Zxx | Ex/Bx response | Diagonal (usually small) |
| Zxy | Ex/By response | TE mode |
| Zyx | Ey/Bx response | TM mode |
| Zyy | Ey/By response | Diagonal (usually small) |

## Phase Tensor Parameters

| Parameter | Description | Interpretation |
|-----------|-------------|----------------|
| phi_min | Minimum phase | Relates to resistivity gradient |
| phi_max | Maximum phase | Relates to resistivity gradient |
| skew | Skew angle | >5 suggests 3D structure |
| ellipticity | (phi_max-phi_min)/(phi_max+phi_min) | 2D/3D indicator |

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **mtpy** | Full MT workflow in Python, EDI I/O, visualization, modelling prep | Complex API, evolving between v1 and v2 |
| **EMTF** | USGS time-series to impedance processing | Fortran-based, processing only |
| **WinGLink** | Commercial integrated MT processing and inversion | Expensive commercial license |

**Use mtpy when** you need end-to-end MT analysis in Python: reading EDI files,
QC, phase tensor analysis, pseudosections, and preparing data for ModEM or other
inversion codes.

**Consider alternatives when** you need time-series to impedance processing from raw
field data (use EMTF), or a fully integrated commercial inversion package with GUI
(use WinGLink).

## Common Workflows

### Load, QC, and analyze MT station data
- [ ] Load EDI file(s) with `MT()` or `MTCollection()`
- [ ] Inspect station metadata (location, frequency range)
- [ ] Plot apparent resistivity and phase with `PlotMTResponse`
- [ ] Check phase tensor parameters for dimensionality (skew > 5 = 3D)
- [ ] Identify and mask noisy data points using error thresholds
- [ ] Rotate impedance tensor to geoelectric strike if needed
- [ ] Create pseudosection for profile data
- [ ] Export cleaned data for inversion (ModEM format)

## Common Issues

| Issue | Solution |
|-------|----------|
| No tipper data | Check `mt.has_tipper` before accessing |
| Bad data points | Use `mt.Z_err / np.abs(mt.Z) > threshold` to mask |
| Static shift | Apply correction before interpretation |
| Wrong rotation | Verify coordinate system (N vs E convention) |

## References

- **[EDI Format](references/edi_format.md)** - EDI file structure and sections
- **[Plotting Options](references/plotting.md)** - Visualization parameters and styles

## Scripts

- **[scripts/mt_analysis.py](scripts/mt_analysis.py)** - MT data analysis and QC
