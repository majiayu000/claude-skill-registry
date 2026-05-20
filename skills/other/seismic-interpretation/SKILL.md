---
name: seismic-interpretation
skill_type: workflow
description: |
  End-to-end seismic interpretation workflow from SEG-Y loading through
  signal processing, rock physics, and visualization. Use when working
  with seismic data analysis pipelines.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Seismic, Interpretation, SEG-Y, Rock Physics, Workflow, AVO, Processing]
dependencies: [segyio, obspy, bruges, pyvista]
complements: [segyio, obspy, bruges, disba, pyvista]
workflow_role: processing
---

# Seismic Interpretation Workflow

End-to-end pipeline for seismic data analysis, from loading SEG-Y files through
signal processing, rock physics modelling, and 3D visualization.

## Skill Chain

```text
segyio          obspy           bruges          disba           pyvista
[SEG-Y I/O] --> [Signal Proc] --> [Rock Physics] --> [Dispersion] --> [3D Viz]
  |               |                |                 |                |
  Load traces     Filter/FFT       AVO modelling     Surface waves    Volume render
  Read headers    Instrument resp   Fluid sub         Phase velocity   Slice display
  3D geometry     Spectral anal    Synthetics        Inversion        Horizon pick
```

## Decision Points

| Question | If Yes | If No |
|----------|--------|-------|
| Working with SEG-Y files? | Start with `segyio` | Use `obspy` for miniSEED/SAC |
| Need frequency filtering or spectral analysis? | Use `obspy` signal tools | Skip to rock physics |
| Performing AVO or fluid substitution? | Use `bruges` | Skip to visualization |
| Analysing surface waves (MASW/SASW)? | Use `disba` for dispersion | Skip `disba` |
| Need 3D volume rendering? | Use `pyvista` | Use matplotlib for 2D |

## Step-by-Step Orchestration

### Stage 1: Data Loading (segyio)

```python
import segyio
import numpy as np

# Load and inspect SEG-Y
with segyio.open('survey.sgy', 'r', iline=189, xline=193) as f:
    n_traces = f.tracecount
    n_samples = len(f.samples)
    dt = f.samples[1] - f.samples[0]  # ms
    cube = segyio.tools.cube(f)        # (ilines, xlines, samples)

    # Extract header info for coordinates
    cdp_x = f.attributes(segyio.TraceField.CDP_X)[:]
    cdp_y = f.attributes(segyio.TraceField.CDP_Y)[:]
```

### Stage 2: Signal Processing (obspy)

```python
from obspy import Trace, Stream
from obspy.signal.filter import bandpass

# Convert numpy trace to obspy for processing
tr = Trace(data=cube[50, 100, :].astype(np.float64))
tr.stats.sampling_rate = 1000.0 / dt  # Hz
tr.stats.delta = dt / 1000.0          # seconds

# Bandpass filter
tr.filter('bandpass', freqmin=5, freqmax=80, corners=4, zerophase=True)

# Spectral analysis
from obspy.signal.tf_misfit import cwt
scalogram = cwt(tr.data, dt=tr.stats.delta, w0=6, fmin=1, fmax=100, nf=50)
```

### Stage 3: Rock Physics (bruges)

```python
from bruges.reflection import zoeppritz, shuey
from bruges.filters import ricker
from bruges.rockphysics import gassmann
from scipy.signal import convolve

# AVO modelling
theta = np.arange(0, 45, 1)
Rpp = zoeppritz(vp1, vs1, rho1, vp2, vs2, rho2, theta)

# Fluid substitution
vp_new, vs_new, rho_new = gassmann(
    vp_sat, vs_sat, rho_sat,
    k_mineral, rho_mineral,
    k_brine, rho_brine,
    k_oil, rho_oil,
    porosity
)

# Synthetic seismogram
impedance = vp * rho
rc = np.diff(impedance) / (impedance[:-1] + impedance[1:])
_, wavelet = ricker(duration=0.128, dt=0.001, f=25)
synthetic = convolve(rc, wavelet, mode='same')
```

### Stage 4: Surface Wave Analysis (disba, optional)

```python
from disba import PhaseDispersion

# Define velocity model (thickness, Vp, Vs, density)
velocity_model = disba.PhaseDispersion(
    thickness=[5, 10, 20, 0],       # m (0 = half-space)
    velocity_p=[300, 600, 1200, 2500],
    velocity_s=[150, 300, 600, 1200],
    density=[1.8, 1.9, 2.1, 2.4]
)
# Compute Rayleigh wave dispersion
pd = velocity_model(wave="rayleigh", mode=0, period=np.linspace(0.01, 1.0, 50))
```

### Stage 5: Visualization (pyvista)

```python
import pyvista as pv

# Create structured grid from seismic cube
grid = pv.ImageData(dimensions=cube.shape)
grid.point_data['amplitude'] = cube.flatten(order='F')

# Volume rendering
plotter = pv.Plotter()
plotter.add_volume(grid, scalars='amplitude', cmap='seismic', opacity='sigmoid')
plotter.show()

# Inline slice
inline_slice = grid.slice(normal='x', origin=grid.center)
plotter = pv.Plotter()
plotter.add_mesh(inline_slice, scalars='amplitude', cmap='seismic')
plotter.show()
```

## Common Pipelines

### Basic Seismic QC
```
- [ ] Load SEG-Y with `segyio.open()`, check trace count and geometry
- [ ] Inspect text and binary headers for acquisition parameters
- [ ] Read trace headers to verify coordinates and fold
- [ ] Compute amplitude statistics (min, max, RMS) per trace
- [ ] Display representative inlines/crosslines with matplotlib
- [ ] Check for dead traces (zero or constant amplitude)
- [ ] Verify sample rate and recording length
```

### AVO Analysis Pipeline
```
- [ ] Load near and far angle stacks from SEG-Y (segyio)
- [ ] Extract well log Vp, Vs, density at target zone (lasio/welly)
- [ ] Compute AVO response with `bruges.reflection.zoeppritz()`
- [ ] Classify AVO anomaly (Class I-IV) from intercept and gradient
- [ ] Perform Gassmann fluid substitution for scenario modelling
- [ ] Generate synthetic seismogram and compare to seismic
- [ ] Create AVO crossplot (intercept vs gradient)
```

### Surface Wave Analysis (MASW)
```
- [ ] Load shot gathers from SEG-Y (segyio)
- [ ] Apply f-k or phase-shift transform to extract dispersion image
- [ ] Pick fundamental mode dispersion curve
- [ ] Invert dispersion curve for 1D Vs profile using disba
- [ ] Repeat for multiple shot points
- [ ] Interpolate Vs profiles into 2D section (verde)
- [ ] Visualize with pyvista or matplotlib
```

### Seismic-to-Well Tie
```
- [ ] Load seismic section (segyio) and well logs (lasio)
- [ ] Compute acoustic impedance from Vp and density logs
- [ ] Generate reflectivity series from impedance
- [ ] Create Ricker wavelet at dominant frequency (bruges)
- [ ] Convolve reflectivity with wavelet for synthetic
- [ ] Extract seismic trace at well location
- [ ] Cross-correlate synthetic with seismic to find time shift
- [ ] Apply bulk shift and stretch/squeeze for best tie
```

## When to Use

Use the seismic interpretation workflow when:

- Processing seismic data from SEG-Y files through to interpretation
- Building AVO analysis pipelines that combine well logs and seismic
- Performing seismic QC, attribute extraction, or volume visualization
- Running surface wave analysis (MASW/SASW) workflows
- Creating synthetic seismograms for well ties

Use individual domain skills when:
- Only reading/writing SEG-Y files (use `segyio` alone)
- Only processing waveforms without seismic context (use `obspy` alone)
- Only computing rock physics equations (use `bruges` alone)

## Common Issues

| Issue | Solution |
|-------|----------|
| SEG-Y geometry not detected | Specify `iline=` and `xline=` byte positions in `segyio.open()` |
| obspy Trace stats wrong | Set `sampling_rate` and `delta` correctly from SEG-Y sample interval |
| AVO angles unrealistic | Verify angle range matches acquisition (typically 0-40 degrees) |
| Synthetic does not tie | Check time-depth relationship and wavelet phase |
| Memory error on large cube | Load inline-by-inline instead of full cube |
