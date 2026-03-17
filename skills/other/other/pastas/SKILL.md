---
name: pastas
description: |
  Groundwater time series analysis and modelling using transfer function noise
  models. Use when Claude needs to: (1) Analyze groundwater level time series,
  (2) Model well responses to precipitation/pumping, (3) Calibrate aquifer
  parameters from head data, (4) Forecast or hindcast groundwater levels,
  (5) Decompose hydrological signals into components, (6) Compare response
  functions, (7) Perform model diagnostics and uncertainty analysis.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Groundwater, Hydrology, Time Series, Transfer Function, Well Response]
dependencies: [pastas>=1.0.0, pandas, scipy]
complements: [xarray]
workflow_role: analysis
---

# Pastas - Groundwater Time Series Analysis

## Quick Reference

```python
import pastas as ps
import pandas as pd

# Load data
head = pd.read_csv('well.csv', index_col=0, parse_dates=True).squeeze()
precip = pd.read_csv('precip.csv', index_col=0, parse_dates=True).squeeze()
evap = pd.read_csv('evap.csv', index_col=0, parse_dates=True).squeeze()

# Create model
ml = ps.Model(head, name='Well_001')

# Add recharge stress
sm = ps.RechargeModel(precip, evap, rfunc=ps.Gamma(), name='recharge')
ml.add_stressmodel(sm)

# Solve and plot
ml.solve()
ml.plot()
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `ps.Model` | Main model container |
| `ps.StressModel` | Response to external stress (pumping, river) |
| `ps.RechargeModel` | Recharge from precipitation minus evaporation |
| `ps.Gamma` | Gamma distribution response function |
| `ps.Exponential` | Simple exponential response function |

## Essential Operations

### Create and Solve Model
```python
ml = ps.Model(head, name='well')
ml.add_stressmodel(ps.RechargeModel(precip, evap, rfunc=ps.Gamma(), name='recharge'))
ml.solve()
```

### Add Pumping Well
```python
pumping = pd.read_csv('pumping.csv', index_col=0, parse_dates=True).squeeze()
ml.add_stressmodel(ps.StressModel(pumping, rfunc=ps.Hantush(),
                                   name='pumping', up=False))  # up=False for drawdown
```

### Model Diagnostics
```python
print(f"EVP: {ml.stats.evp():.1f}%")      # Explained variance
print(f"RMSE: {ml.stats.rmse():.3f} m")   # Root mean square error
print(f"AIC: {ml.stats.aic():.1f}")       # Model selection criterion

ml.plots.diagnostics()                     # Diagnostic plots
ml.plots.acf()                            # Autocorrelation
```

### Get Contributions
```python
contributions = ml.get_contributions()
for name, contrib in contributions.items():
    print(f"{name}: mean={contrib.mean():.2f}")
```

### Step and Impulse Response
```python
step = ml.get_step_response('recharge')    # Step response
block = ml.get_block_response('recharge')  # Impulse response
```

### Export and Load
```python
ml.to_json('model.pas')                    # Save model
ml_loaded = ps.io.load('model.pas')        # Load model

sim = ml.simulate()
sim.to_csv('simulation.csv')               # Export results
```

## Model Statistics

| Statistic | Description | Good Value |
|-----------|-------------|------------|
| EVP | Explained variance percentage | >70% |
| RMSE | Root mean square error | Low (context-dependent) |
| AIC | Akaike Information Criterion | Lower = better |
| BIC | Bayesian Information Criterion | Lower = better |

## Common Patterns

### Compare Response Functions
```python
for rfunc in [ps.Gamma(), ps.Exponential(), ps.Hantush()]:
    ml = ps.Model(head)
    ml.add_stressmodel(ps.RechargeModel(precip, evap, rfunc=rfunc, name='r'))
    ml.solve(report=False)
    print(f"{rfunc.name}: EVP={ml.stats.evp():.1f}%, AIC={ml.stats.aic():.1f}")
```

### Forecast Future Levels
```python
ml.solve()
forecast = ml.simulate(tmin='2024-01-01', tmax='2025-12-31')
ml.plot(tmax='2025-12-31')
```

### River or Custom Stress
```python
river = pd.read_csv('river_stage.csv', index_col=0, parse_dates=True).squeeze()
sm = ps.StressModel(river, rfunc=ps.Exponential(), name='river',
                    settings='waterlevel')
ml.add_stressmodel(sm)
```

## When to Use vs Alternatives

| Use Case | Tool | Why |
|----------|------|-----|
| Groundwater time series analysis | **Pastas** | Purpose-built transfer function models |
| Well response to recharge/pumping | **Pastas** | Built-in stress models and response functions |
| Numerical groundwater flow (MODFLOW) | **FloPy** | Full 3D finite-difference groundwater model |
| Simple exponential decay fitting | **Custom scipy** | `scipy.optimize.curve_fit` is sufficient |
| Regional groundwater flow modelling | **FloPy** | Spatially distributed parameters and boundaries |
| Aquifer test analysis (pumping tests) | **Aqtesolv / custom** | Dedicated well test interpretation |
| Multi-well network analysis | **Pastas** | Model each well independently, compare responses |
| Signal decomposition | **Pastas** | Separate recharge, pumping, and trend contributions |

**Choose Pastas when**: You have groundwater level time series and want to model
responses to precipitation, evaporation, or pumping using transfer function noise
models. Excellent for rapid model building with diagnostics.

**Choose FloPy when**: You need spatially distributed groundwater flow modelling
with MODFLOW, including multiple layers, boundary conditions, and transport.

**Choose custom scipy when**: You only need to fit a simple analytical model
(e.g., Theis equation) to pumping test data without time series decomposition.

## Common Workflows

### Groundwater Response Model with Diagnostics
- [ ] Load head time series and stress data (precipitation, evaporation, pumping)
- [ ] Inspect data: check for gaps, outliers, and time coverage
- [ ] Create `ps.Model(head)` with observation data
- [ ] Add recharge stress with `ps.RechargeModel(precip, evap, rfunc=ps.Gamma())`
- [ ] Add pumping or river stresses if applicable
- [ ] Solve model with `ml.solve()`
- [ ] Check EVP (>70%), RMSE, and AIC
- [ ] Run `ml.plots.diagnostics()` to inspect residuals
- [ ] Check residual autocorrelation; enable noise model if needed: `ml.solve(noise=True)`
- [ ] Compare response functions (Gamma vs Exponential vs Hantush) using AIC
- [ ] Extract step/block responses to interpret aquifer behavior
- [ ] Decompose signal into individual stress contributions
- [ ] Export model to JSON and simulation results to CSV

## Tips

1. **Start simple** - Add stresses incrementally
2. **Check residuals** - Should be white noise (use `ml.plots.diagnostics()`)
3. **Compare response functions** - Use AIC/BIC to select best model
4. **Use daily data** - Pastas works best with daily time series
5. **Normalize units** - Precipitation in mm/day, head in meters

## Common Issues

| Issue | Solution |
|-------|----------|
| Poor fit (low EVP) | Try different response functions |
| Residual autocorrelation | Add noise model: `ml.solve(noise=True)` |
| Unstable parameters | Set parameter bounds or fix values |
| Missing stress data | Interpolate or use `fillna()` before modeling |

## References

- **[Stress Models](references/stress_models.md)** - Available stress model types
- **[Response Functions](references/response_functions.md)** - Response function selection

## Scripts

- **[scripts/groundwater_model.py](scripts/groundwater_model.py)** - Complete groundwater modeling workflow
