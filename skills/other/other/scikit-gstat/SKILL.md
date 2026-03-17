---
name: scikit-gstat
description: |
  Geostatistical analysis with scikit-learn style API. Compute variograms, kriging
  interpolation, and spatial correlation analysis. Use when Claude needs to: (1) Compute
  experimental variograms from spatial data, (2) Fit variogram models (spherical,
  exponential, gaussian, matern), (3) Perform Ordinary or Universal Kriging interpolation,
  (4) Assess spatial anisotropy with directional variograms, (5) Cross-validate spatial
  models, (6) Analyze spatio-temporal data, (7) Export variogram parameters for other
  geostatistical software.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geostatistics, Variogram, Kriging, Scikit-Learn, Spatial Statistics, Scikit-Gstat, Interpolation, Directional Analysis]
dependencies: [scikit-gstat>=1.0.0, numpy, scipy, scikit-learn]
complements: [verde, geostatspy]
workflow_role: analysis
---

# SciKit-GStat - Geostatistics

## Quick Reference

```python
import skgstat as skg
import numpy as np

# Create variogram
V = skg.Variogram(coordinates=coords, values=values, n_lags=15)

# Fit model
V.model = 'spherical'
print(f"Range: {V.parameters[0]:.2f}, Sill: {V.parameters[1]:.2f}")

# Kriging interpolation
ok = skg.OrdinaryKriging(V)
predictions = ok.transform(grid_coords)
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `Variogram` | Empirical and theoretical variograms |
| `OrdinaryKriging` | Interpolation with spatial correlation |
| `DirectionalVariogram` | Anisotropic variograms |
| `SpaceTimeVariogram` | Spatio-temporal analysis |

## Essential Operations

### Create and Fit Variogram
```python
import skgstat as skg

V = skg.Variogram(
    coordinates=coords,      # (n, 2) array of x, y
    values=values,           # (n,) array of measurements
    n_lags=15,
    maxlag='median'          # or specific distance
)

# Fit model: 'spherical', 'exponential', 'gaussian', 'matern', 'stable'
V.model = 'spherical'

# Get parameters
print(f"Range: {V.parameters[0]:.2f}")
print(f"Sill: {V.parameters[1]:.2f}")
print(f"Nugget: {V.parameters[2]:.2f}")
print(f"RMSE: {V.rmse:.4f}")
```

### Ordinary Kriging
```python
import skgstat as skg
import numpy as np

V = skg.Variogram(coords, values, model='spherical')
ok = skg.OrdinaryKriging(V)

# Create prediction grid
x = np.linspace(0, 100, 50)
y = np.linspace(0, 100, 50)
xx, yy = np.meshgrid(x, y)
grid_coords = np.column_stack([xx.ravel(), yy.ravel()])

# Predict
predictions = ok.transform(grid_coords)
Z = predictions.reshape(xx.shape)

# Get variance
ok.return_variance = True
predictions, variance = ok.transform(grid_coords)
```

### Directional Variogram
```python
import skgstat as skg

DV = skg.DirectionalVariogram(
    coordinates=coords,
    values=values,
    azimuth=45,          # Direction in degrees
    tolerance=22.5,      # Angular tolerance
    bandwidth='q33'      # Perpendicular bandwidth
)

# Check anisotropy
for az in [0, 45, 90, 135]:
    DV.azimuth = az
    print(f"Azimuth {az}: Range = {DV.parameters[0]:.2f}")
```

### Cross-Validation
```python
import skgstat as skg
from sklearn.model_selection import cross_val_score

V = skg.Variogram(coords, values, model='spherical')
ok = skg.OrdinaryKriging(V)

scores = cross_val_score(ok, coords, values, cv=5, scoring='neg_mean_squared_error')
print(f"CV RMSE: {np.sqrt(-scores.mean()):.4f}")
```

### Robust Estimators
```python
import skgstat as skg

# Use robust estimator for noisy data
V = skg.Variogram(
    coords, values,
    estimator='cressie'  # 'matheron', 'cressie', 'dowd', 'genton'
)
```

## Quick Model Reference

| Model | Behavior |
|-------|----------|
| `spherical` | Most common, linear near origin |
| `exponential` | Never reaches sill, gradual approach |
| `gaussian` | Parabolic near origin, smooth |
| `matern` | Flexible smoothness control |

## When to Use vs Alternatives

| Use Case | Tool | Why |
|----------|------|-----|
| Variogram analysis + kriging | **scikit-gstat** | Modern API, sklearn-compatible |
| GSLIB-style simulation (SGSIM) | **GeostatsPy** | Full GSLIB simulation engine |
| Kriging with trend/drift | **pykrige** | Universal kriging, regression kriging |
| Random field generation | **gstools** | Flexible covariance, SRF generation |
| Spatio-temporal variograms | **scikit-gstat** | Built-in SpaceTimeVariogram |
| Production geomodelling | **SGeMS / Petrel** | GUI, large-scale 3D models |
| Robust variogram estimation | **scikit-gstat** | Cressie, Dowd, Genton estimators |
| ML pipeline integration | **scikit-gstat** | sklearn `fit`/`transform` interface |

**Choose scikit-gstat when**: You want a Pythonic, scikit-learn-compatible API for
variogram fitting and kriging. Best for exploratory geostatistical analysis with
cross-validation and integration into ML pipelines.

**Choose GeostatsPy when**: You need GSLIB-compatible simulation workflows (SGSIM,
SISIM) or are working with traditional geostatistical conventions.

**Choose pykrige when**: You need universal kriging with external drift variables
or regression kriging combining geostatistics with machine learning predictions.

## Common Workflows

### Variogram Fitting and Ordinary Kriging
- [ ] Load spatial data as numpy arrays (coordinates and values)
- [ ] Create `Variogram` object with appropriate `n_lags` and `maxlag`
- [ ] Test estimators: matheron (default) vs cressie (robust) for noisy data
- [ ] Fit multiple models (spherical, exponential, gaussian) and compare RMSE
- [ ] Check anisotropy with `DirectionalVariogram` at 0, 45, 90, 135 degrees
- [ ] Select best model based on RMSE and visual fit
- [ ] Create `OrdinaryKriging` object from fitted variogram
- [ ] Define prediction grid and run `ok.transform(grid_coords)`
- [ ] Set `ok.return_variance = True` to get kriging variance
- [ ] Cross-validate with `cross_val_score()` to assess prediction quality
- [ ] Map predictions and kriging variance

## Common Issues

| Issue | Solution |
|-------|----------|
| Variogram flat or erratic | Adjust `n_lags` and `maxlag` (try `maxlag='median'`) |
| Poor model fit (high RMSE) | Try different model types or nested structures |
| Kriging too slow | Reduce number of conditioning points or grid resolution |
| Nugget too large | May indicate measurement error; try robust estimators |
| Anisotropy unclear | Use smaller angular tolerance in `DirectionalVariogram` |

## Tips

1. **Maxlag** should be ~50% of study area diagonal
2. **Use robust estimators** (cressie, dowd) with noisy data
3. **Test multiple models** and compare RMSE
4. **Check anisotropy** with directional variograms before kriging

## References

- **[Variogram Models](references/variogram_models.md)** - Model equations and parameters
- **[Kriging Methods](references/kriging_methods.md)** - Kriging types and configuration

## Scripts

- **[scripts/variogram_analysis.py](scripts/variogram_analysis.py)** - Complete variogram analysis workflow
