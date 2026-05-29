---
name: gprpy
description: |
  Process and visualize ground-penetrating radar (GPR) data with signal processing,
  velocity analysis, and depth conversion. Use when Claude needs to: (1) Load GPR
  files (.DZT, .DT1, .GPR, .rd3), (2) Apply dewow, gain, and filters to radargrams,
  (3) Convert two-way travel time to depth, (4) Perform CMP/WARR velocity analysis,
  (5) Apply topographic corrections, (6) Export processed profiles as images or SEG-Y,
  (7) Batch process multiple GPR survey lines.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [GPR, Ground-Penetrating Radar, Near-Surface, Signal Processing, GPRPy, Geophysics, Depth Conversion, Radargram]
dependencies: [gprpy>=1.0.0, numpy, matplotlib, scipy]
complements: [pyvista]
workflow_role: data-loading
---

# GPRPy - Ground Penetrating Radar Processing

## Quick Reference

```python
import gprpy.gprpy as gp
import matplotlib.pyplot as plt

# Load and display
data = gp.gprpyProfile()
data.importdata('profile.DZT')
data.showProfile()
plt.show()

# Access data
print(f"Traces: {data.data.shape[1]}")
print(f"Samples: {data.data.shape[0]}")
print(f"Time range: {data.twtt.max():.1f} ns")
```

## Supported Formats

| Format | Manufacturer |
|--------|-------------|
| .DZT | GSSI |
| .DT1 | Sensors & Software |
| .GPR | MALA |
| .rd3/.rad | MALA |
| .sgy | SEG-Y |

## Essential Operations

### Basic Processing
```python
data = gp.gprpyProfile()
data.importdata('profile.DZT')

data.dewow(window=10)           # Remove low-frequency drift
data.remMeanTrace(ntraces=50)   # Remove background ringing
data.tpowGain(power=1.5)        # Time-power gain
data.agcGain(window=25)         # Automatic gain control

data.showProfile()
```

### Apply Filters
```python
data.bandpassFilter(minfreq=100, maxfreq=800)  # MHz
data.lowpassFilter(maxfreq=500)
data.highpassFilter(minfreq=50)
```

### Time-to-Depth Conversion
```python
velocity = 0.1  # m/ns (typical for dry sand)
data.setVelocity(velocity)
data.showProfile(yrng=[0, 5])  # Top 5 meters
```

### Topographic Correction
```python
data.topoCorrect(topofile='topography.txt', velocity=0.1)
# File format: x_position, elevation
```

### Export Results
```python
data.exportFig('processed.png', dpi=300)
data.exportSEGY('processed.sgy')
data.exportASCII('processed.txt')
```

## Velocity Analysis (CMP)

```python
cmp = gp.gprpyCMP()
cmp.importdata('cmp_survey.DZT')
cmp.showCMP()

cmp.semblance(vmin=0.05, vmax=0.15, vstep=0.01)
cmp.showSemblance()
```

## Processing Parameters

| Parameter | Typical Value | Description |
|-----------|---------------|-------------|
| Dewow window | 5-20 ns | Low-frequency removal window |
| Gain power | 1.0-2.0 | Time-power gain exponent |
| AGC window | 10-50 ns | Automatic gain window |
| Bandpass | 100-800 MHz | Frequency filter range |

## Material Velocities

| Material | Velocity (m/ns) |
|----------|-----------------|
| Air | 0.30 |
| Dry sand | 0.10-0.15 |
| Wet sand | 0.06-0.08 |
| Dry soil | 0.08-0.12 |
| Wet soil | 0.05-0.08 |
| Limestone | 0.10-0.12 |
| Granite | 0.10-0.13 |
| Water | 0.033 |
| Ice | 0.16-0.17 |

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **gprpy** | Python-based GPR processing, scripted workflows, open-source | Limited advanced migration algorithms |
| **GPRMax** | Forward modelling and simulation of GPR responses | Simulation only, not for data processing |
| **REFLEXW** | Full commercial processing suite, advanced migration | Commercial license required |
| **Custom scipy** | Custom signal processing, research algorithms | Must build everything from scratch |

**Use gprpy when** you need open-source GPR processing in Python, batch processing
of survey lines, or integration with other Python geoscience tools.

**Consider alternatives when** you need forward modelling of GPR responses (use GPRMax),
advanced migration or commercial-grade processing (use REFLEXW), or highly custom
signal processing algorithms (use scipy directly).

## Common Workflows

### Process raw GPR profile for interpretation
- [ ] Import raw data with `gp.gprpyProfile()` and `importdata()`
- [ ] Apply dewow filter to remove low-frequency drift
- [ ] Remove mean trace to eliminate background ringing
- [ ] Apply time-power gain or AGC for depth equalization
- [ ] Apply bandpass filter to remove noise
- [ ] Determine velocity from CMP analysis or material tables
- [ ] Convert time axis to depth with `setVelocity()`
- [ ] Apply topographic correction if survey has elevation changes
- [ ] Export processed profile as image and/or SEG-Y

## References

- **[Processing Steps](references/processing_steps.md)** - Complete processing workflow guide
- **[Material Velocities](references/processing_steps.md#velocity-selection)** - Velocity selection by material type

## Scripts

- **[scripts/process_gpr.py](scripts/process_gpr.py)** - Batch process GPR files with standard workflow
