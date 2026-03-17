---
name: geological-modelling
skill_type: workflow
description: |
  3D geological modelling workflow from spatial data preparation through
  implicit surface modelling and 3D visualization. Use when building
  geological models from surface data, boreholes, or GIS inputs.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geological Modelling, 3D, Implicit Surfaces, GIS, Workflow]
dependencies: [gemgis, gempy, pyvista]
complements: [gemgis, gempy, loopstructural, pyvista]
workflow_role: modelling
---

# Geological Modelling Workflow

End-to-end pipeline for building 3D geological models from spatial data,
covering GIS data preparation, implicit surface modelling, and 3D visualization.

## Skill Chain

```text
gemgis              gempy / loopstructural       pyvista
[GIS Preprocessing] --> [Implicit Modelling]     --> [3D Visualization]
  |                      |                           |
  Shapefile parsing      Surface interpolation       Volume render
  Raster extraction      Fault modelling             Cross-sections
  Borehole to points     Unconformities              Mesh export
  CRS transforms         Scalar field solving        Interactive pick
```

## Decision Points: GemPy vs LoopStructural

| Criterion | GemPy | LoopStructural |
|-----------|-------|----------------|
| Standard layer-cake geology | Preferred | Works |
| Complex folding (refolded folds) | Limited | Preferred (structural frames) |
| Fault networks | Good | Good |
| Built-in gravity forward model | Yes | No |
| Learning curve | Gentler | Steeper |
| Data input | Points + orientations | Points + orientations + fold constraints |
| Unconformities | ERODE / ONLAP types | Supported |
| API style | Functional (`gp.compute_model`) | Object-oriented (`model.update()`) |

**Rule of thumb**: Use GemPy for standard structural geology with faults and
unconformities. Use LoopStructural when fold geometry is the primary control
on model architecture.

## Step-by-Step Orchestration

### Stage 1: Spatial Data Preparation (gemgis)

```python
import gemgis as gg
import geopandas as gpd
import rasterio

# Load geological map (shapefile)
contacts = gpd.read_file('geological_contacts.shp')
orientations = gpd.read_file('orientations.shp')

# Extract surface points from GIS contacts with DEM
with rasterio.open('dem.tif') as dem:
    surface_points = gg.vector.extract_xyz(contacts, dem=dem)

# Extract orientations with elevation
orientation_pts = gg.vector.extract_xyz(orientations, dem=dem)

# Extract borehole data
boreholes = gpd.read_file('boreholes.shp')
bh_points = gg.vector.extract_xyz_from_cross_sections(boreholes)

# Define model extent from data bounds
extent = gg.utils.set_extent(
    gdf=surface_points,
    z_min=-500, z_max=1000
)
```

### Stage 2a: Implicit Modelling with GemPy

```python
import gempy as gp

# Create model
geo_model = gp.create_geomodel(
    project_name='RegionalModel',
    extent=extent,
    resolution=[50, 50, 30]
)

# Add data from GemGIS output
gp.add_surface_points(
    geo_model,
    x=surface_points['X'], y=surface_points['Y'],
    z=surface_points['Z'], surface=surface_points['formation']
)
gp.add_orientations(
    geo_model,
    x=orientation_pts['X'], y=orientation_pts['Y'],
    z=orientation_pts['Z'],
    dip=orientation_pts['dip'],
    azimuth=orientation_pts['azimuth'],
    surface=orientation_pts['formation']
)

# Define stratigraphic relationships
gp.map_stack_to_surfaces(geo_model, mapping={
    'Cover': ['Alluvium'],
    'Sedimentary': ['Sandstone', 'Shale', 'Limestone'],
    'Basement': ['Granite']
})
geo_model.structural_frame.structural_groups[0].structural_relation = \
    gp.data.StackRelationType.ERODE

# Add faults
gp.map_stack_to_surfaces(geo_model, mapping={
    'Fault_Series': ['MainFault'],
    'Cover': ['Alluvium'],
    'Sedimentary': ['Sandstone', 'Shale', 'Limestone'],
    'Basement': ['Granite']
})
geo_model.structural_frame.structural_groups[0].structural_relation = \
    gp.data.StackRelationType.FAULT

# Compute and validate
gp.set_interpolator(geo_model)
sol = gp.compute_model(geo_model)
gp.plot_2d(geo_model, cell_number=[25], direction='y', show_data=True)
```

### Stage 2b: Implicit Modelling with LoopStructural (alternative)

```python
from LoopStructural import GeologicalModel
import pandas as pd

# Prepare input DataFrames
data = pd.DataFrame({
    'X': x_coords, 'Y': y_coords, 'Z': z_coords,
    'feature_name': formation_names,
    'val': stratigraphic_values,     # Scalar values for interface position
    'gx': gradient_x, 'gy': gradient_y, 'gz': gradient_z  # Orientation
})

# Build model
model = GeologicalModel(
    origin=[extent[0], extent[2], extent[4]],
    maximum=[extent[1], extent[3], extent[5]]
)
model.data = data

# Add features
model.create_and_add_foliation('Stratigraphy', interpolatortype='FDI')
model.create_and_add_fault('MainFault', displacement=100)

# Update and access
model.update()
lithology = model.evaluate_model(model.regular_grid())
```

### Stage 3: Visualization (pyvista)

```python
import pyvista as pv

# GemPy model to PyVista
lith_block = sol.raw_arrays.lith_block
grid_3d = lith_block.reshape(geo_model.grid.regular_grid.resolution)

grid = pv.ImageData(dimensions=geo_model.grid.regular_grid.resolution)
grid.point_data['lithology'] = lith_block.flatten(order='F')

# 3D visualization with cross-section
plotter = pv.Plotter()
plotter.add_volume(grid, scalars='lithology', cmap='tab10', opacity='sigmoid')
sliced = grid.slice(normal='y', origin=grid.center)
plotter.add_mesh(sliced, scalars='lithology', cmap='tab10')
plotter.show()

# Export to VTK for external tools
grid.save('geological_model.vtk')
```

## Common Pipelines

### Standard 3D Geological Model
```
- [ ] Gather input data: geological map, DEM, borehole logs, structural measurements
- [ ] Load shapefiles and rasters with geopandas and rasterio
- [ ] Extract surface contact points with elevation using gemgis
- [ ] Extract orientation data (dip, azimuth) with gemgis
- [ ] Define model extent and resolution (cover data + buffer)
- [ ] Create GemPy GeoModel with extent and resolution
- [ ] Add surface points and orientations
- [ ] Define stratigraphic pile and structural relationships (ERODE, ONLAP)
- [ ] Add fault surfaces if present
- [ ] Set interpolator and compute model
- [ ] Validate with 2D cross-sections through known data points
- [ ] Visualize 3D result with pyvista
- [ ] Export to VTK or numpy for downstream use
```

### Borehole-Based Model
```
- [ ] Load borehole data (collar, survey, lithology intervals)
- [ ] Convert lithology picks to surface contact points at formation boundaries
- [ ] Estimate orientations from multi-well dip calculation or assign regional dip
- [ ] Build model with GemPy (minimum 2 points + 1 orientation per surface)
- [ ] Validate: check model honours borehole intersections
- [ ] Iterate: add more data or adjust orientations to fix artifacts
```

### GIS-to-Model Pipeline
```
- [ ] Load geological map polygons and structural measurements from shapefiles
- [ ] Reproject to common CRS with geopandas
- [ ] Extract formation boundary polylines from polygon contacts
- [ ] Sample points along polylines with gemgis
- [ ] Drape points onto DEM to get 3D coordinates
- [ ] Build GemPy model from extracted points and orientations
- [ ] Compare model surface traces with original geological map
```

## When to Use

Use the geological modelling workflow when:

- Building 3D geological models from surface mapping, boreholes, or GIS data
- Converting GIS spatial data into implicit geological surfaces
- Modelling faults, unconformities, or intrusions in 3D
- Creating subsurface models for downstream geophysical or engineering use

Use individual domain skills when:
- Only converting GIS data formats (use `gemgis` alone)
- Only building a model with data already prepared (use `gempy` alone)
- Only visualizing existing VTK meshes (use `pyvista` alone)

## Common Issues

| Issue | Solution |
|-------|----------|
| Model artifacts at edges | Extend model extent 10-20% beyond data coverage |
| GemPy needs min 2 points per surface | Add interpolated or projected points from known geology |
| Fault offset direction wrong | Reverse pole_vector or swap footwall/hangingwall points |
| CRS mismatch between datasets | Reproject all data to common projected CRS with geopandas |
| LoopStructural fold not honoured | Add fold axis orientation and wavelength constraints |
| Resolution too coarse | Increase grid resolution but watch memory (50^3 = 125k cells) |
