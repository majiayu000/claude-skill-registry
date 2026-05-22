---
name: xarray-for-multidimensional-data
description: Work with labeled multidimensional arrays for scientific data analysis using Xarray. Use when handling climate data, satellite imagery, oceanographic data, or any multidimensional datasets with coordinates and metadata. Ideal for NetCDF/HDF5 files, time series analysis, and large datasets requiring lazy loading with Dask.
---

# Xarray for Multidimensional Data

Master **Xarray**, the powerful library for working with labeled multidimensional arrays in scientific Python. Learn how to efficiently handle complex datasets with multiple dimensions, coordinates, and metadata - from climate data and satellite imagery to experimental measurements and simulations.

**Official Documentation**: https://docs.xarray.dev/

**GitHub**: https://github.com/pydata/xarray

## Quick Reference Card

### Installation & Setup
```bash
# Using pixi (recommended for scientific projects)
pixi add xarray netcdf4 dask

# Using pip
pip install xarray[complete]

# Optional dependencies for specific formats
pixi add zarr h5netcdf scipy bottleneck

# Geospatial extensions (for raster data, CRS handling, reprojection)
pixi add rioxarray xesmf

# DataTree is built into Xarray (no separate installation needed)
```

### Essential Xarray Concepts
```python
import xarray as xr
import numpy as np

# DataArray: Single labeled array
temperature = xr.DataArray(
    data=np.random.randn(3, 4),
    dims=["time", "location"],
    coords={
        "time": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "location": ["A", "B", "C", "D"]
    },
    name="temperature"
)

# Dataset: Collection of DataArrays
ds = xr.Dataset({
    "temperature": temperature,
    "pressure": (["time", "location"], np.random.randn(3, 4))
})
```

### Essential Operations
```python
# Selection by label
ds.sel(time="2024-01-01")
ds.sel(location="A")

# Selection by index
ds.isel(time=0)

# Slicing
ds.sel(time=slice("2024-01-01", "2024-01-02"))

# Aggregation
ds.mean(dim="time")
ds.sum(dim="location")

# Computation
ds["temperature"] + 273.15  # Celsius to Kelvin
ds.groupby("time.month").mean()

# I/O operations
ds.to_netcdf("data.nc")
ds = xr.open_dataset("data.nc")
```

### Quick Decision Tree

```
Working with multidimensional scientific data?
├─ YES → Use Xarray for labeled dimensions
└─ NO → NumPy/Pandas sufficient

Need to track coordinates and metadata?
├─ YES → Xarray keeps everything aligned
└─ NO → Plain NumPy arrays work

Working with geospatial raster data?
├─ YES → Use rioxarray for CRS-aware operations
└─ NO → Standard Xarray sufficient

Data has natural hierarchical structure?
├─ YES → Use DataTree for organization
└─ NO → Dataset/DataArray sufficient

Data too large for memory?
├─ YES → Use Xarray with Dask backend
└─ NO → Standard Xarray is fine

Need to save/load scientific data formats?
├─ NetCDF/HDF5 → Xarray native support
├─ Zarr → Use Xarray with zarr backend
└─ CSV/Excel → Pandas then convert to Xarray

Working with time series data?
├─ Multi-dimensional → Xarray
└─ Tabular → Pandas

Need to align data from different sources?
├─ YES → Xarray handles alignment automatically
└─ NO → Manual alignment with NumPy
```

## When to Use This Skill

Use Xarray when working with:

- **Climate and weather data** with dimensions like time, latitude, longitude, and altitude
- **Satellite and remote sensing imagery** with spatial and temporal dimensions
- **Oceanographic data** with depth, time, and spatial coordinates
- **Experimental measurements** with multiple parameters and conditions
- **Simulation outputs** with complex dimensional structures
- **Time series data** that varies across multiple spatial locations
- **Any data** where keeping track of dimensions and coordinates is critical
- **Large datasets** that benefit from lazy loading and Dask integration

## Core Concepts

### 1. DataArray: Labeled Multidimensional Arrays

A **DataArray** is Xarray's fundamental data structure - think of it as a NumPy array with labels and metadata.

**Anatomy of a DataArray:**
```python
import xarray as xr
import numpy as np

# Create a DataArray
temperature = xr.DataArray(
    data=np.array([[15.2, 16.1, 14.8],
                   [16.5, 17.2, 15.9],
                   [17.1, 18.0, 16.5]]),
    dims=["time", "location"],
    coords={
        "time": pd.date_range("2024-01-01", periods=3),
        "location": ["Station_A", "Station_B", "Station_C"],
        "lat": ("location", [40.7, 34.0, 41.8]),
        "lon": ("location", [-74.0, -118.2, -87.6])
    },
    attrs={
        "units": "Celsius",
        "description": "Daily average temperature"
    }
)
```

**Key components:**
- **data**: The actual NumPy array
- **dims**: Dimension names (like column names in Pandas)
- **coords**: Coordinate labels for each dimension
- **attrs**: Metadata dictionary

### 2. Dataset: Collection of DataArrays

A **Dataset** is like a dict of DataArrays that share dimensions - similar to a Pandas DataFrame but for N-dimensional data.

**Example:**
```python
# Create a Dataset
ds = xr.Dataset({
    "temperature": (["time", "location"], np.random.randn(3, 4)),
    "humidity": (["time", "location"], np.random.rand(3, 4) * 100),
    "pressure": (["time", "location"], 1013 + np.random.randn(3, 4) * 10)
},
coords={
    "time": pd.date_range("2024-01-01", periods=3),
    "location": ["A", "B", "C", "D"]
})
```

### 3. Coordinates: Dimension Labels

Coordinates provide meaningful labels for array dimensions and enable label-based indexing.

**Types of coordinates:**

**Dimension coordinates** (1D, same name as dimension):
```python
time_coord = pd.date_range("2024-01-01", periods=365)
```

**Non-dimension coordinates** (auxiliary information):
```python
# Latitude/longitude for each station
coords = {
    "time": time_coord,
    "station": ["A", "B", "C"],
    "lat": ("station", [40.7, 34.0, 41.8]),
    "lon": ("station", [-74.0, -118.2, -87.6])
}
```

### 4. Indexing and Selection

Xarray provides powerful label-based and position-based indexing.

**Label-based selection (.sel):**
```python
# Select by coordinate value
ds.sel(time="2024-01-15")
ds.sel(location="Station_A")

# Nearest neighbor selection
ds.sel(time="2024-01-15", method="nearest")

# Range selection
ds.sel(time=slice("2024-01-01", "2024-01-31"))
```

**Position-based selection (.isel):**
```python
# Select by integer position
ds.isel(time=0)
ds.isel(location=[0, 2])
```

**Boolean indexing (.where):**
```python
# Keep only values meeting condition
ds.where(ds["temperature"] > 15, drop=True)
```

### 5. DataTree: Hierarchical Data Organization

**DataTree** is Xarray's class for organizing hierarchical (tree-structured) data. Think of it as a filesystem for datasets, where each node can contain a dataset and child nodes.

**When to use DataTree:**

- Data at different resolutions or scales (multi-resolution imagery)
- Measurements from multiple sensor types on the same system
- Multi-model ensemble outputs with varying configurations
- Experimental data with multiple trials or parameter sweeps
- Heterogeneous data combining different domains or data types

**Creating a DataTree:**

```python
import xarray as xr

# From a dictionary of datasets
dt = xr.DataTree.from_dict({
    "/": xr.Dataset({"description": "Root metadata"}),
    "/observations": xr.Dataset({"temp": (["time"], [15.2, 16.1, 14.8])}),
    "/observations/station_a": xr.Dataset({"location": "New York"}),
    "/observations/station_b": xr.Dataset({"location": "Los Angeles"}),
    "/model_outputs": xr.Dataset({"predicted_temp": (["time"], [15.0, 16.0, 15.0])})
})

# Access nodes using filesystem-like paths
print(dt["/observations/station_a"])
print(dt["observations"]["station_a"])  # Equivalent
```

**Key DataTree operations:**

```python
# Navigate the tree
dt.parent  # Get parent node
dt.children  # Get child nodes dict
dt.subtree  # Iterate over all descendant nodes
dt.leaves  # Get all leaf nodes

# Apply operations across all datasets
dt.mean(dim="time")  # Apply to all nodes

# Map custom functions
dt.map_over_datasets(lambda ds: ds + 273.15)

# Filter nodes
dt.match("*/station_*")  # Pattern matching
dt.filter(lambda node: "temp" in node.ds.data_vars)  # Content-based filtering

# Coordinate inheritance (child nodes inherit parent coordinates)
# Define coordinates once at parent level, accessible in all children
```

**Combining DataTrees:**

```python
# Arithmetic operations on isomorphic trees
dt1 + dt2  # Add corresponding datasets at each node

# Check structure compatibility
dt1.isomorphic(dt2)  # Returns True if same structure
```

### 6. Ecosystem Extensions

Xarray has a rich ecosystem of extensions for domain-specific workflows. For geospatial data analysis, prioritize **rioxarray** over vanilla Xarray.

**Key geospatial extensions:**

**rioxarray** - Geospatial raster operations:
```python
import rioxarray

# Open raster with CRS (Coordinate Reference System) awareness
ds = rioxarray.open_rasterio("satellite_image.tif")

# Reproject to different CRS
ds_reprojected = ds.rio.reproject("EPSG:4326")

# Clip to bounding box
ds_clipped = ds.rio.clip_box(minx=-120, miny=35, maxx=-115, maxy=40)

# Write with CRS metadata
ds.rio.to_raster("output.tif")
```

**Other useful extensions:**

- **xESMF**: Universal regridder for geospatial data (grid transformations)
- **Geocube**: Convert vector data (GeoDataFrames) to raster (Xarray)
- **xarray-spatial**: Numba-accelerated raster analytics (NDVI, terrain analysis)
- **Salem**: Geolocation-based subsetting and masking

**When to use which:**

- **General geospatial rasters** → rioxarray
- **Regridding between different grids** → xESMF
- **Vector to raster conversion** → Geocube
- **Fast raster computations** → xarray-spatial
- **Geolocation operations** → Salem

## Patterns

See [references/PATTERNS.md](references/PATTERNS.md) for detailed patterns including:
- Creating DataArrays and Datasets
- Reading and writing data
- Selection and indexing
- Computation and aggregation
- Combining datasets
- Dask integration for large data
- Interpolation and regridding
- Custom functions with apply_ufunc
- Working with DataTree (hierarchical data)
- Geospatial operations with rioxarray

## Real-World Examples

See [references/EXAMPLES.md](references/EXAMPLES.md) for complete examples including:
- Climate data analysis
- Satellite data processing
- Oceanographic data analysis
- Multi-model ensemble analysis
- Time series decomposition
- Hierarchical climate model data with DataTree
- Geospatial satellite data processing with rioxarray

## Common Issues and Solutions

See [references/COMMON_ISSUES.md](references/COMMON_ISSUES.md) for solutions to:
- Memory errors with large datasets
- Misaligned coordinates
- Slow operations on chunked data
- Coordinate precision issues
- Dimension order confusion
- Broadcasting errors
- Encoding issues when saving
- Time coordinate parsing issues

## Best Practices Checklist

### Data Organization
- Use meaningful dimension and coordinate names
- Include units and descriptions in attrs
- Use standard dimension names (time, lat, lon, etc.) when applicable
- Keep coordinates sorted for better performance
- Use appropriate data types (float32 vs float64)

### Performance
- Chunk large datasets appropriately for your operations
- Use lazy loading with open_dataset(chunks=...)
- Avoid loading entire dataset into memory unnecessarily
- Use vectorized operations instead of loops
- Consider using float32 instead of float64 for large datasets

### File I/O
- Use NetCDF4 for general scientific data
- Use Zarr for cloud storage and parallel writes
- Include metadata (attrs) when saving
- Use compression for large datasets
- Document coordinate reference systems for geospatial data

### Code Quality
- Use .sel() for label-based indexing (more readable)
- Chain operations for clarity
- Use meaningful variable names
- Add type hints for function parameters
- Document expected dimensions in docstrings

### Computation
- Use built-in methods (.mean(), .sum()) over manual loops
- Leverage groupby for categorical aggregations
- Use .compute() explicitly with Dask
- Monitor memory usage with large datasets
- Use .persist() to cache intermediate results

## Resources and References

### Official Documentation
- **Xarray Documentation**: https://docs.xarray.dev/
- **Xarray Tutorial**: https://tutorial.xarray.dev/
- **API Reference**: https://docs.xarray.dev/en/stable/api.html
- **Hierarchical Data (DataTree)**: https://docs.xarray.dev/en/latest/user-guide/hierarchical-data.html
- **Ecosystem Extensions**: https://docs.xarray.dev/en/latest/user-guide/ecosystem.html

### File Formats
- **NetCDF**: https://www.unidata.ucar.edu/software/netcdf/
- **Zarr**: https://zarr.readthedocs.io/
- **HDF5**: https://www.hdfgroup.org/solutions/hdf5/

### Related Libraries
- **Dask**: https://docs.dask.org/ (parallel computing)
- **Pandas**: https://pandas.pydata.org/ (tabular data)
- **NumPy**: https://numpy.org/ (array operations)

### Geospatial Extensions
- **rioxarray**: https://corteva.github.io/rioxarray/ (geospatial raster operations)
- **xESMF**: https://xesmf.readthedocs.io/ (regridding)
- **Geocube**: https://corteva.github.io/geocube/ (vector to raster)
- **xarray-spatial**: https://xarray-spatial.readthedocs.io (spatial analytics)
- **Salem**: https://salem.readthedocs.io/ (geolocation operations)

### Domain-Specific Resources
- **Climate Data Operators (CDO)**: https://code.mpimet.mpg.de/projects/cdo
- **Pangeo**: https://pangeo.io/ (big data geoscience)

### Tutorials and Examples
- **Xarray Examples Gallery**: https://docs.xarray.dev/en/stable/gallery.html
- **Pangeo Gallery**: https://gallery.pangeo.io/
- **Earth and Environmental Data Science**: https://earth-env-data-science.github.io/

## Summary

Xarray is the go-to library for working with labeled multidimensional arrays in scientific Python. It combines the power of NumPy arrays with the convenience of Pandas labels, making it ideal for climate data, satellite imagery, experimental measurements, and any data with multiple dimensions.

**Key takeaways:**

- Use DataArrays for single variables, Datasets for collections
- Label-based indexing (.sel) is more readable than position-based
- Leverage automatic alignment for operations between datasets
- Use chunking and Dask for datasets larger than memory
- NetCDF and Zarr are the preferred formats for scientific data
- GroupBy and resample enable powerful temporal aggregations
- Xarray integrates seamlessly with NumPy, Pandas, and Dask

**Next steps:**

- Start with small datasets to learn the API
- Use .sel() and .isel() for intuitive data selection
- Explore groupby operations for categorical analysis
- Learn chunking strategies for your specific use case
- Integrate with domain-specific tools (Cartopy, Dask, etc.)

Xarray transforms complex multidimensional data analysis into intuitive, readable code while maintaining high performance and scalability.
