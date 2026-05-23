---
name: geostatspy
description: |
  GSLIB-inspired geostatistics library for variogram analysis, kriging, and
  simulation. Use when Claude needs to: (1) Calculate experimental variograms,
  (2) Fit variogram models, (3) Perform simple/ordinary kriging, (4) Run
  sequential Gaussian simulation (SGSIM), (5) Apply normal score transforms,
  (6) Decluster spatial data, (7) Generate multiple realizations for uncertainty.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geostatistics, Variogram, Kriging, SGSIM, GSLIB, Spatial Estimation]
dependencies: [geostatspy>=0.0.40, numpy, pandas, matplotlib]
complements: [verde, scikit-gstat]
workflow_role: analysis
---

# GeostatsPy - Geostatistical Analysis

## Quick Reference

```python
import geostatspy.GSLIB as GSLIB
import geostatspy.geostats as geostats
import pandas as pd

df = pd.read_csv('data.csv')
df['npor'], tvpor, tnspor = geostats.nscore(df, 'porosity')  # Transform

lag, gamma, npairs = geostats.gamv(df, 'X', 'Y', 'npor',      # Variogram
    tmin=-9999, tmax=9999, xlag=50, xltol=25, nlag=15,
    azm=0, atol=22.5, bandwh=9999, bandwd=9999)

vario = GSLIB.make_variogram(nug=0.0, nst=1, it1=1, cc1=1.0,  # Model
                              azi1=0, hmaj1=300, hmin1=300)

est, var = geostats.kb2d(df, 'X', 'Y', 'npor', ..., vario=vario)  # Krige
```

## Key Functions

| Category | Functions |
|----------|-----------|
| Visualization | `locmap`, `pixelplt`, `hist` |
| Variogram | `gamv`, `vmodel` |
| Kriging | `kb2d`, `kb3d` |
| Simulation | `sgsim`, `sisim` |
| Transforms | `nscore`, `backtr` |
| Declustering | `declus` |

## Common Operations

### 1. Normal Score Transform
```python
df['npor'], tvpor, tnspor = geostats.nscore(df, 'porosity')
original = geostats.backtr(nscore_data, tvpor, tnspor, zmin=0, zmax=0.3)
```

### 2. Experimental Variogram
```python
lag, gamma, npairs = geostats.gamv(
    df, 'X', 'Y', 'npor',
    tmin=-9999, tmax=9999,    # Trimming limits
    xlag=50, xltol=25,        # Lag distance, tolerance
    nlag=15, azm=0, atol=22.5, bandwh=9999, bandwd=9999)
```

### 3. Variogram Model
```python
# Types: 1=spherical, 2=exponential, 3=gaussian
vario = GSLIB.make_variogram(
    nug=0.0, nst=1,            # Nugget, number of structures
    it1=1, cc1=1.0,            # Type, sill contribution
    azi1=0, hmaj1=300, hmin1=300)  # Azimuth, major/minor range
```

### 4. Kriging (kb2d)
```python
est, var = geostats.kb2d(
    df, 'X', 'Y', 'npor', tmin=-9999, tmax=9999,
    nx=50, xmn=25, xsiz=50,    # Grid X: ncells, origin, size
    ny=50, ymn=25, ysiz=50,    # Grid Y
    nxdis=1, nydis=1, ndmin=1, ndmax=10,
    radius=500, ktype=0, skmean=0.0, vario=vario)  # ktype: 0=simple, 1=ordinary
```

### 5. Sequential Gaussian Simulation
```python
sim = geostats.sgsim(
    df, 'X', 'Y', 'npor', wcol=-1, scol=-1,
    tmin=-9999, tmax=9999, itrans=0,
    ismooth=0, dession=0, dmession=0,
    zmin=-4, zmax=4, ltail=1, ltpar=0, utail=1, utpar=0,
    nsim=1, nx=50, xmn=25, xsiz=50, ny=50, ymn=25, ysiz=50,
    nz=1, zmn=0, zsiz=1, seed=73073,
    ndmin=1, ndmax=10, nodmax=10, radius=500, radius1=500,
    sang1=0, sang2=0, sang3=0, mxctx=10, mxcty=10, mxctz=1,
    ktype=0, vario=vario)
```

### 6. Declustering
```python
wts, cell_size, ncut = geostats.declus(
    df, 'X', 'Y', 'porosity', iminmax=1, noff=10, ncell=20, cmin=10, cmax=500)
declustered_mean = np.average(df['porosity'], weights=wts)
```

## Variogram Models

| Code | Model | Use Case |
|------|-------|----------|
| 1 | Spherical | Most common, finite range |
| 2 | Exponential | Reaches sill asymptotically |
| 3 | Gaussian | Very smooth, parabolic near origin |
| 4 | Power | Unbounded, fractal-like |

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `nug` | Nugget effect (measurement error + micro-scale variation) |
| `sill` | Total variance (nugget + structure contributions) |
| `range` | Distance where correlation becomes negligible |
| `azimuth` | Direction of maximum continuity (degrees from N) |
| `ktype` | 0=simple kriging (known mean), 1=ordinary kriging |

## When to Use vs Alternatives

| Use Case | Tool | Why |
|----------|------|-----|
| GSLIB-style workflows | **GeostatsPy** | Direct port of GSLIB programs to Python |
| SGSIM / SISIM simulation | **GeostatsPy** | Full GSLIB simulation engine |
| Declustering spatial data | **GeostatsPy** | Built-in `declus` function |
| Modern variogram API | **scikit-gstat** | Cleaner API, sklearn integration |
| Kriging only (no simulation) | **pykrige** | Focused API, universal kriging support |
| Random field generation | **gstools** | Flexible covariance models, field generation |
| Large-scale 3D geomodelling | **SGeMS / Petrel** | GUI-based, industrial workflows |
| Indicator simulation | **GeostatsPy** (`sisim`) | Categorical property simulation |

**Choose GeostatsPy when**: You need GSLIB-compatible workflows in Python, especially
for sequential simulation (SGSIM/SISIM), declustering, or if you are familiar with
GSLIB parameter conventions. Best for reservoir characterization workflows.

**Choose scikit-gstat when**: You prefer a modern scikit-learn-style API for variogram
analysis and kriging, with better integration into Python data science workflows.

**Choose pykrige when**: You only need kriging interpolation (no simulation) and want
universal kriging with external drift or regression kriging capabilities.

## Common Workflows

### Variogram Analysis and Kriging Interpolation
- [ ] Load spatial data into a pandas DataFrame
- [ ] Explore data with `GSLIB.locmap()` and `GSLIB.hist()`
- [ ] Check for clustering and decluster with `geostats.declus()` if needed
- [ ] Apply normal score transform with `geostats.nscore()`
- [ ] Compute experimental variogram with `geostats.gamv()` (isotropic first)
- [ ] Check directional variograms for anisotropy (azimuths 0, 45, 90, 135)
- [ ] Fit variogram model with `GSLIB.make_variogram()`
- [ ] Overlay model on experimental variogram to verify fit
- [ ] Run kriging with `geostats.kb2d()` (ktype=1 for ordinary)
- [ ] Run SGSIM for uncertainty quantification (50-100 realizations)
- [ ] Back-transform results with `geostats.backtr()`
- [ ] Validate with cross-validation or holdout data

## Common Issues

| Issue | Solution |
|-------|----------|
| Variogram doesn't reach sill | Increase `nlag` or `xlag` to capture full range |
| Kriging produces negative values | Back-transform after kriging, not before |
| SGSIM artifacts | Check grid definition (xmn, xsiz) matches data extent |
| Too few variogram pairs | Increase `atol` (angular tolerance) or `xltol` (lag tolerance) |
| Hole effect in variogram | May indicate periodicity; try nested structures |

## Tips

1. **Always transform to normal scores** - Most methods assume Gaussian
2. **Start isotropic** - Add anisotropy only if justified by directional variograms
3. **Check variogram pairs** - Ensure enough pairs at each lag
4. **Multiple realizations** - Use 50-100+ for uncertainty quantification
5. **Back-transform last** - Apply to final results only

## References

- **[GSLIB Programs](references/gslib_programs.md)** - GSLIB program reference
- **[Simulation Methods](references/simulation_methods.md)** - SGSIM, SISIM, and other methods

## Scripts

- **[scripts/kriging_example.py](scripts/kriging_example.py)** - Complete kriging workflow
