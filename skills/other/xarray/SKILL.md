---
name: xarray
description: |
  N-dimensional labeled arrays for geoscience data. Read/write NetCDF, work with
  climate and oceanographic datasets, perform multi-dimensional analysis with
  labeled coordinates. Use when Claude needs to: (1) Read/write NetCDF or Zarr
  files, (2) Work with multidimensional arrays with labeled dimensions, (3)
  Analyze climate, ocean, or atmosphere data, (4) Compute temporal aggregations
  (daily/monthly/annual means), (5) Perform area-weighted statistics, (6)
  Process large datasets with Dask, (7) Apply CF conventions to scientific data.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [NetCDF, Climate Data, Multi-Dimensional Arrays, Dask, Zarr, Geoscience]
dependencies: [xarray>=2023.0, numpy, pandas, netcdf4]
complements: [verde, pyvista, pooch]
workflow_role: data-loading
---

# xarray - Multi-Dimensional Geoscience Data

## Quick Reference

```python
import xarray as xr

# Read
ds = xr.open_dataset('data.nc')

# Access data
temp = ds['temperature']         # DataArray
values = temp.values             # numpy array
df = ds.to_dataframe()           # pandas DataFrame

# Structure info
print(ds)                        # Overview
print(ds.dims)                   # Dimensions
print(ds.data_vars)              # Variables

# Write
ds.to_netcdf('output.nc')
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `Dataset` | Collection of aligned DataArrays (like NetCDF file) |
| `DataArray` | Single variable with labeled dimensions |
| `Coordinates` | Dimension labels (time, lat, lon) |

## Essential Operations

### Select Data
```python
# By coordinate value
temp_jan = ds['temperature'].sel(time='2020-01-15')
temp_region = ds['temperature'].sel(lat=slice(-30, 30), lon=slice(-60, 60))

# Nearest value
temp_point = ds['temperature'].sel(lat=35.5, lon=-120.3, method='nearest')

# By index
temp_first = ds['temperature'].isel(time=0)
```

### Compute Statistics
```python
temp = ds['temperature']
temp_mean_time = temp.mean(dim='time')           # Spatial map
temp_mean_space = temp.mean(dim=['lat', 'lon'])  # Time series

# Area-weighted mean
import numpy as np
weights = np.cos(np.deg2rad(ds.lat))
temp_weighted = temp.weighted(weights).mean(dim=['lat', 'lon'])
```

### GroupBy and Resample
```python
temp = ds['temperature']

# Temporal aggregations
monthly_mean = temp.groupby('time.month').mean()
annual_mean = temp.groupby('time.year').mean()

# Climatology and anomalies
climatology = temp.groupby('time.month').mean('time')
anomalies = temp.groupby('time.month') - climatology

# Resample time series
monthly = temp.resample(time='1M').mean()
rolling_30d = temp.rolling(time=30, center=True).mean()
```

### Create New Dataset
```python
import numpy as np
import pandas as pd

times = pd.date_range('2020-01-01', periods=365, freq='D')
lats = np.linspace(-90, 90, 180)
lons = np.linspace(-180, 180, 360)

da = xr.DataArray(
    data=np.random.randn(365, 180, 360),
    dims=['time', 'lat', 'lon'],
    coords={'time': times, 'lat': lats, 'lon': lons},
    attrs={'units': 'degC', 'long_name': 'Temperature'}
)

ds = xr.Dataset({'temperature': da})
ds.to_netcdf('output.nc')
```

### Masking
```python
temp_warm = temp.where(temp > 20)                 # Mask by condition
temp_clipped = temp.where(temp > 0, 0)            # Replace negative with 0

tropics = (ds.lat > -23.5) & (ds.lat < 23.5)
temp_tropics = temp.where(tropics, drop=True)    # Mask by coordinate
```

### Large Datasets (Dask)
```python
# Open with chunking (lazy loading)
ds = xr.open_dataset('large_file.nc', chunks={'time': 100})
ds = xr.open_mfdataset('data_*.nc', chunks='auto')

# Operations are lazy until .compute()
result = ds['temperature'].mean(dim='time').compute()
```

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **xarray** | Labeled multi-dim arrays, NetCDF/Zarr, Dask integration | Learning curve for newcomers from numpy |
| **iris** | Met Office climate workflows, UGRID mesh support | Smaller community, UK-centric conventions |
| **CDO** | Fast command-line climate data operations | Not Python-native, limited custom analysis |
| **NCO** | Quick NetCDF file manipulation and arithmetic | Command-line only, no visualization |

**Use xarray when** you need labeled dimension handling, seamless NetCDF/Zarr I/O,
groupby/resample operations, or Dask-based parallel processing of large datasets.

**Consider alternatives when** you need fast one-off command-line operations on NetCDF
files (use CDO/NCO), or you work within the Met Office ecosystem with UGRID meshes
(use iris).

## Common Workflows

### Climate data analysis with temporal aggregation
- [ ] Open NetCDF dataset with `xr.open_dataset()` (use `chunks=` if large)
- [ ] Inspect dimensions, coordinates, and variables with `print(ds)`
- [ ] Select region of interest with `.sel(lat=slice(), lon=slice())`
- [ ] Compute climatology with `.groupby('time.month').mean('time')`
- [ ] Calculate anomalies by subtracting climatology from data
- [ ] Compute area-weighted spatial mean using cosine latitude weights
- [ ] Resample to desired temporal resolution (monthly, annual)
- [ ] Save results to NetCDF with `.to_netcdf()`

## Common Issues

| Issue | Solution |
|-------|----------|
| Memory error | Use `chunks=` for lazy loading |
| Time decoding fails | `decode_times=False` then manual decode |
| Missing coordinates | Check `ds.coords` and `ds.dims` |
| Alignment errors | Check coordinate values match |

## References

- **[I/O Formats](references/io_formats.md)** - NetCDF, Zarr, and other formats
- **[Computation](references/computation.md)** - Aggregation and analysis methods

## Scripts

- **[scripts/climate_analysis.py](scripts/climate_analysis.py)** - Climate data analysis
