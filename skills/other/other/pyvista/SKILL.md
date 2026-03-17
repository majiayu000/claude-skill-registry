---
name: pyvista
description: |
  3D visualization and mesh analysis for geoscience data using PyVista/VTK.
  Use when Claude needs to: (1) Create 3D visualizations of geological models,
  (2) Render seismic volumes or voxel data, (3) Visualize point clouds or well
  paths, (4) Plot surfaces and meshes in 3D, (5) Read/write VTK, STL, OBJ files,
  (6) Create cross-sections through 3D models, (7) Export publication-quality
  figures or interactive HTML.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [3D Visualization, VTK, Mesh, Geological Models, Point Clouds]
dependencies: [pyvista>=0.42.0, numpy, vtk]
complements: [gempy, simpeg, verde, segyio, xarray]
workflow_role: visualization
---

# PyVista - 3D Visualization

## Quick Reference

```python
import pyvista as pv

mesh = pv.read('model.vtk')
plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars='property', cmap='viridis')
plotter.show()
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `pv.Plotter` | Main visualization window |
| `pv.PolyData` | Surface meshes, point clouds |
| `pv.StructuredGrid` | Regular 3D grids |
| `pv.UnstructuredGrid` | Irregular meshes |
| `pv.ImageData` | 3D voxel data (seismic) |

## Essential Operations

### Load and Display Mesh
```python
mesh = pv.read('model.vtk')
plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars='lithology', cmap='Set1')
plotter.show()
```

### Create Structured Grid (Surface)
```python
x, y = np.meshgrid(np.arange(-10, 10, 0.5), np.arange(-10, 10, 0.5))
z = np.sin(np.sqrt(x**2 + y**2))
grid = pv.StructuredGrid(x, y, z)
pv.Plotter().add_mesh(grid, scalars=z.ravel(), cmap='terrain').show()
```

### Visualize Point Cloud
```python
cloud = pv.PolyData(np.random.rand(1000, 3) * 100)
cloud['depth'] = cloud.points[:, 2]
pv.Plotter().add_mesh(cloud, scalars='depth', point_size=5,
                      render_points_as_spheres=True).show()
```

### Volume Rendering (Seismic)
```python
grid = pv.ImageData(dimensions=(nx+1, ny+1, nz+1), spacing=(25, 25, 10))
grid.cell_data['amplitude'] = data.ravel(order='F')
pv.Plotter().add_volume(grid, cmap='seismic', opacity='sigmoid').show()
```

### Slice Through Volume
```python
volume = pv.read('seismic.vti')
slice_x = volume.slice(normal='x', origin=volume.center)
pv.Plotter().add_mesh(slice_x, cmap='seismic').show()
```

### Well Path Visualization
```python
points = np.column_stack([x, y, z])  # Well trajectory
tube = pv.Spline(points, 500).tube(radius=5)
pv.Plotter().add_mesh(tube, color='brown', label='Well').add_legend().show()
```

### Combine Multiple Surfaces
```python
plotter = pv.Plotter()
plotter.add_mesh(horizon1, color='gold', opacity=0.7, label='Top')
plotter.add_mesh(horizon2, color='blue', opacity=0.7, label='Base')
plotter.add_mesh(fault, color='red', opacity=0.5, label='Fault')
plotter.add_legend().show()
```

### Export for Publication
```python
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(mesh, cmap='terrain')
plotter.screenshot('figure.png', scale=3)   # High-res image
plotter.export_html('model.html')           # Interactive HTML
```

## Color Maps

| Map | Use Case |
|-----|----------|
| `terrain` | Topography, elevation |
| `seismic` | Seismic amplitudes (diverging) |
| `viridis` | General scientific |
| `Set1`, `Set2` | Categorical (lithology) |

## Supported Formats

`.vtk`, `.vtu`, `.vti`, `.vtp`, `.stl`, `.obj`, `.ply` (read/write)

## When to Use vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **pyvista** | Pythonic 3D viz, VTK wrapper, mesh operations, scripting | Requires display or off-screen backend |
| **Mayavi** | Scientific 3D visualization, volume rendering | Heavier dependency, less active development |
| **ParaView** | Interactive GUI exploration of large 3D datasets | GUI-focused, scripting is secondary |
| **matplotlib 3D** | Simple 3D scatter/surface plots | Limited interactivity, not true 3D engine |

**Use pyvista when** you need programmatic 3D visualization of geological models,
meshes, or point clouds with VTK power but a Pythonic API.

**Consider alternatives when** you need a full GUI for exploring large models
(use ParaView), legacy scientific visualization (use Mayavi), or only need simple
3D scatter plots (use matplotlib 3D).

## Common Workflows

### Visualize 3D geological model with multiple surfaces
- [ ] Load mesh files with `pv.read()` for each surface/horizon
- [ ] Create plotter with `pv.Plotter()` (use `off_screen=True` for scripts)
- [ ] Add each surface with `plotter.add_mesh()` and distinct colors/opacity
- [ ] Add well paths as tubes with `pv.Spline().tube()`
- [ ] Add axes and legend with `plotter.add_axes()` and `plotter.add_legend()`
- [ ] Set camera position for desired view angle
- [ ] Export screenshot with `plotter.screenshot()` or HTML with `plotter.export_html()`

## Tips

- Use `off_screen=True` for batch processing
- Add axes with `plotter.add_axes()` for publication
- Export to HTML for interactive sharing
- Use opacity to show internal structure

## References

- **[Mesh Types](references/mesh_types.md)** - PyVista mesh classes and when to use each
- **[Plotting Options](references/plotting_options.md)** - Plotter settings and rendering options

## Scripts

- **[scripts/visualize_surface.py](scripts/visualize_surface.py)** - Visualize geological surfaces from file
