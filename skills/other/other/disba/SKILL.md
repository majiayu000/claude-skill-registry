---
name: disba
description: |
  Compute surface wave dispersion curves for layered Earth models using the
  Thomson-Haskell matrix method with Numba acceleration. Use when Claude needs to:
  (1) Calculate Rayleigh or Love wave phase velocities, (2) Compute group velocity
  dispersion, (3) Generate sensitivity kernels for inversion, (4) Forward model
  dispersion curves from velocity profiles, (5) Compare dispersion between different
  Earth models, (6) Set up surface wave tomography workflows.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Surface Waves, Dispersion, Rayleigh, Love, Seismology, Disba, Phase Velocity, Group Velocity]
dependencies: [disba>=0.5.0, numpy, numba]
complements: [obspy, segyio]
workflow_role: analysis
---

# disba - Surface Wave Dispersion

## Quick Reference

```python
import numpy as np
from disba import PhaseDispersion, GroupDispersion

# Define velocity model (thickness, Vp, Vs, density)
# thickness in km, velocities in km/s, density in g/cm3
thickness = np.array([0.5, 1.0, 2.0, 0.0])  # 0.0 = half-space
vp = np.array([1.5, 2.5, 4.0, 6.0])
vs = np.array([0.8, 1.4, 2.3, 3.5])
rho = np.array([1.8, 2.0, 2.3, 2.6])

# Periods to compute (seconds)
periods = np.linspace(0.1, 5.0, 50)

# Calculate Rayleigh wave phase velocity
pd = PhaseDispersion(*zip(thickness, vp, vs, rho))
cpr = pd(periods, mode=0, wave='rayleigh')  # Fundamental mode

# Calculate group velocity
gd = GroupDispersion(*zip(thickness, vp, vs, rho))
ugr = gd(periods, mode=0, wave='rayleigh')
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `PhaseDispersion` | Phase velocity dispersion curves |
| `GroupDispersion` | Group velocity dispersion curves |
| `PhaseSensitivity` | Sensitivity kernels (dc/dVs, dc/dVp, dc/drho) |

## Essential Operations

### Rayleigh and Love Waves
```python
pd = PhaseDispersion(*zip(thickness, vp, vs, rho))
cpr = pd(periods, mode=0, wave='rayleigh')  # Vertical + radial motion
cpl = pd(periods, mode=0, wave='love')       # Horizontal SH motion
```

### Multiple Modes
```python
for mode in range(3):  # Fundamental + higher modes
    try:
        cpr = pd(periods, mode=mode, wave='rayleigh')
    except Exception:
        pass  # Higher modes may not exist at all periods
```

### Sensitivity Kernels
```python
from disba import PhaseSensitivity

ps = PhaseSensitivity(*zip(thickness, vp, vs, rho))
kernel_vs = ps(period=1.0, mode=0, wave='rayleigh', parameter='velocity_s')
# Other parameters: 'velocity_p', 'density'
```

### Forward Modelling
```python
def forward_model(vs_profile, thickness, vp_vs_ratio=1.73):
    """Compute dispersion curve from Vs profile."""
    vp = vs_profile * vp_vs_ratio
    rho = 0.32 * vp + 0.77  # Gardner relation
    pd = PhaseDispersion(*zip(thickness, vp, vs_profile, rho))
    return pd(periods, mode=0, wave='rayleigh')
```

## Model Parameters

| Parameter | Unit | Description |
|-----------|------|-------------|
| thickness | km | Layer thickness (0 = half-space) |
| vp | km/s | P-wave velocity |
| vs | km/s | S-wave velocity |
| rho | g/cm3 | Density |

## Wave Types

| Type | Motion | Sensitivity |
|------|--------|-------------|
| Rayleigh | Vertical + radial | Vs (primary), Vp (secondary) |
| Love | Horizontal (SH) | Vs only |

## Key Points

1. **Last layer thickness = 0** indicates half-space (infinite depth)
2. **Numba JIT** - First call is slower due to compilation
3. **Higher modes** may not exist at all periods
4. **Sensitivity kernels** show which depths affect each period

## When to Use vs Alternatives

| Tool | Best For |
|------|----------|
| **disba** | Fast dispersion computation, Numba-accelerated, Python-native |
| **CPS (Herrmann)** | Full surface wave analysis suite, Fortran-based, broader features |
| **pysurf** | Surface wave processing from field data, MASW/SASW workflows |

**Use disba when** you need fast forward modelling of dispersion curves for
inversion or parameter studies. Numba acceleration makes it ideal for iterative
workflows requiring thousands of forward computations.

**Use CPS instead** when you need the full Herrmann suite: receiver functions,
synthetic seismograms, or established research-grade tools.

**Use pysurf instead** when processing raw field data (shot gathers) through
MASW/SASW workflows to extract dispersion curves from measured data.

## Common Workflows

### Compute and analyze dispersion curves
```
- [ ] Define layered velocity model (thickness, Vp, Vs, density)
- [ ] Set last layer thickness to 0.0 (half-space)
- [ ] Choose period range appropriate for model depth
- [ ] Compute phase/group velocity for fundamental mode
- [ ] Compute higher modes if needed (wrap in try/except)
- [ ] Generate sensitivity kernels to assess depth resolution
- [ ] Compare computed curves against observed data
```

## Common Issues

| Issue | Solution |
|-------|----------|
| No dispersion at short periods | Increase model resolution (thinner layers) |
| Higher mode not computed | Mode may not exist at those periods |
| Slow first run | Normal - Numba compiles on first call |
| NaN in results | Check model validity (Vs < Vp, positive values) |

## References

- **[Dispersion Curves](references/dispersion_curves.md)** - Phase vs group velocity, mode numbering
- **[Velocity Models](references/velocity_models.md)** - Model setup, units, common profiles

## Scripts

- **[scripts/dispersion_analysis.py](scripts/dispersion_analysis.py)** - Compute and plot dispersion curves
