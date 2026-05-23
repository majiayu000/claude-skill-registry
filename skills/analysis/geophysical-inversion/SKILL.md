---
name: geophysical-inversion
skill_type: workflow
description: |
  Geophysical data inversion workflow from data loading through mesh
  creation, forward modelling, inversion, and result visualization.
  Use when inverting ERT, magnetics, gravity, or EM survey data.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geophysical Inversion, ERT, Magnetics, Gravity, EM, Workflow]
dependencies: [simpeg, pygimli, verde, pyvista]
complements: [simpeg, pygimli, verde, pyvista]
workflow_role: modelling
---

# Geophysical Inversion Workflow

End-to-end pipeline for inverting geophysical data, from survey data loading
through mesh creation, forward modelling, inversion, gridding, and 3D
visualization of recovered physical property models.

## Skill Chain

```text
simpeg / pygimli      verde            pyvista
[Mesh + Inversion] --> [Gridding]    --> [3D Visualization]
  |                     |                |
  Survey geometry       Interpolate      Volume render
  Forward model         Grid to raster   Slice views
  Misfit + reg          Trend removal    Overlay data
  Recover model         Cross-validate   Export mesh
```

## Decision Points: SimPEG vs pyGIMLi

| Criterion | SimPEG | pyGIMLi |
|-----------|--------|---------|
| DC resistivity / ERT | Yes | Yes (simpler API) |
| Magnetics | Yes | Limited |
| Gravity | Yes | Limited |
| Electromagnetics (TDEM, FDEM) | Yes | No |
| Seismic refraction (SRT) | No | Yes |
| Induced polarization | Yes | Yes |
| Built-in electrode arrays | Manual setup | Built-in (Wenner, Schlumberger, etc.) |
| Mesh types | TensorMesh, TreeMesh, CurvilinearMesh | Triangular, tetrahedral, structured |
| Joint inversion | Yes (Wires maps) | Limited |
| API complexity | More boilerplate, more flexible | Less boilerplate, opinionated |

**Rule of thumb**: Use pyGIMLi for standard near-surface ERT/SRT surveys with
conventional arrays. Use SimPEG for multi-physics, EM methods, potential fields,
or research-grade custom inversions.

## Step-by-Step Orchestration

### Stage 1a: Inversion with SimPEG (DC Resistivity Example)

```python
import numpy as np
from discretize import TensorMesh
from simpeg.electromagnetics.static import resistivity as dc
from simpeg import maps, data, data_misfit, regularization
from simpeg import optimization, inverse_problem, inversion, directives

# 1. Create mesh
hx = np.ones(80) * 5.0
hz = np.ones(40) * 2.5
mesh = TensorMesh([hx, hz], origin='CN')

# 2. Build survey (dipole-dipole)
n_electrodes = 24
electrode_spacing = 5.0
elec_x = np.arange(n_electrodes) * electrode_spacing
elec_locs = np.c_[elec_x, np.zeros(n_electrodes)]

source_list = []
for i in range(n_electrodes - 3):
    rx = dc.receivers.Dipole(elec_locs[[i+2]], elec_locs[[i+3]])
    src = dc.sources.Dipole([rx], elec_locs[i], elec_locs[i+1])
    source_list.append(src)
survey = dc.Survey(source_list)

# 3. Forward model (for synthetic test)
sigma_true = np.ones(mesh.nC) * 0.01  # 100 ohm-m background
sigma_true[mesh.cell_centers[:, 1] < -20] = 0.1  # Conductive layer
simulation = dc.Simulation2DNodal(
    mesh, survey=survey, sigmaMap=maps.ExpMap(mesh)
)
dobs = simulation.dpred(np.log(sigma_true))
dobs += 0.02 * np.abs(dobs) * np.random.randn(len(dobs))  # Add noise

# 4. Set up inversion
obs_data = data.Data(survey, dobs=dobs,
                     standard_deviation=0.05 * np.abs(dobs))
dmis = data_misfit.L2DataMisfit(data=obs_data, simulation=simulation)
reg = regularization.WeightedLeastSquares(
    mesh, alpha_s=1e-4, alpha_x=1, alpha_z=1
)
opt = optimization.InexactGaussNewton(maxIter=20)
inv_prob = inverse_problem.BaseInvProblem(dmis, reg, opt)
dir_list = [
    directives.BetaSchedule(coolingFactor=2),
    directives.TargetMisfit()
]
inv = inversion.BaseInversion(inv_prob, directiveList=dir_list)

# 5. Run inversion
m0 = np.log(np.ones(mesh.nC) * 0.01)  # Starting model
mrec = inv.run(m0)
sigma_rec = np.exp(mrec)  # Recovered conductivity
```

### Stage 1b: Inversion with pyGIMLi (ERT Example)

```python
import pygimli as pg
from pygimli.physics import ert

# 1. Load or create data
data = ert.load('ert_survey.dat')
# Or create synthetic: data = ert.simulate(mesh, res, scheme)

# 2. Check and filter data
print(data)
data.remove(data['rhoa'] <= 0)  # Remove negative apparent resistivity

# 3. Create mesh and run inversion
mgr = ert.ERTManager(data)
model = mgr.invert(lam=20, verbose=True)

# 4. Visualize
mgr.showResult()
mgr.showFit()
```

### Stage 2: Gridding and Interpolation (verde)

```python
import verde as vd

# Grid scattered inversion results to regular raster
coordinates = (mesh.cell_centers[:, 0], mesh.cell_centers[:, 1])
region = vd.get_region(coordinates)

# Spline gridding
spline = vd.Spline(mindist=10, damping=1e-3)
spline.fit(coordinates, data=np.log10(1.0 / sigma_rec))

grid = spline.grid(spacing=2.5, region=region,
                   data_names=['log_resistivity'])
```

### Stage 3: Visualization (pyvista)

```python
import pyvista as pv

# SimPEG mesh to PyVista
resistivity = 1.0 / sigma_rec  # Convert to resistivity
grid_pv = pv.ImageData(
    dimensions=(mesh.shape_cells[0]+1, mesh.shape_cells[1]+1, 1),
    spacing=(mesh.h[0][0], mesh.h[1][0], 1),
    origin=(mesh.origin[0], mesh.origin[1], 0)
)
grid_pv.cell_data['resistivity'] = resistivity

plotter = pv.Plotter()
plotter.add_mesh(grid_pv, scalars='resistivity', cmap='Spectral',
                 log_scale=True, clim=[10, 1000])
plotter.add_scalar_bar('Resistivity (ohm-m)')
plotter.show()
```

## Common Pipelines

### Standard ERT Inversion
```
- [ ] Load ERT data (electrode positions, configurations, apparent resistivity)
- [ ] QC data: remove negative rhoa, check reciprocals, filter by error threshold
- [ ] Choose framework: pyGIMLi for standard arrays, SimPEG for custom setups
- [ ] Create mesh appropriate for electrode layout and target depth
- [ ] Set up forward simulation with survey geometry
- [ ] Configure inversion: data misfit, regularization weight, starting model
- [ ] Run inversion, monitor convergence (target chi-squared ~ 1)
- [ ] Plot recovered resistivity model
- [ ] Overlay electrode positions and data fit
- [ ] Export model to VTK or gridded raster
```

### Gravity or Magnetics Inversion (SimPEG)
```
- [ ] Load survey data (station locations, observed field, regional correction)
- [ ] Remove regional trend if needed (polynomial or upward continuation)
- [ ] Create TensorMesh or TreeMesh covering survey area and target depth
- [ ] Build survey object with receiver locations and source field
- [ ] Set up Simulation3DIntegral with appropriate physical property map
- [ ] Configure L2 data misfit and Tikhonov regularization
- [ ] Add depth weighting to counteract resolution decay
- [ ] Run inversion from homogeneous starting model
- [ ] Visualize recovered density/susceptibility with pyvista
- [ ] Validate against known geology or borehole constraints
```

### Synthetic Study (Forward + Inversion)
```
- [ ] Define true model with target anomaly on mesh
- [ ] Create survey geometry matching planned field layout
- [ ] Run forward simulation to generate synthetic data
- [ ] Add realistic noise (percentage + floor)
- [ ] Run inversion on noisy synthetic data
- [ ] Compare recovered model to true model
- [ ] Test sensitivity to regularization parameters
- [ ] Assess resolution by varying survey design
```

## When to Use

Use the geophysical inversion workflow when:

- Inverting ERT, magnetics, gravity, or EM survey data for subsurface models
- Designing geophysical surveys through synthetic forward-inversion studies
- Processing and visualizing inverted physical property models
- Comparing results from different inversion parameters or methods

Use individual domain skills when:
- Only creating meshes or survey geometries (use `simpeg` or `pygimli` alone)
- Only gridding scattered data (use `verde` alone)
- Only visualizing existing model files (use `pyvista` alone)

## Common Issues

| Issue | Solution |
|-------|----------|
| Inversion does not converge | Check data uncertainties; increase regularization (`lam` or `alpha_s`) |
| Artifacts near surface | Add depth weighting or refine mesh near electrodes |
| Memory error on 3D mesh | Use TreeMesh (SimPEG) with adaptive refinement near sources |
| Negative apparent resistivity | Remove bad data points before inversion |
| Over-fitting (chi-squared << 1) | Increase trade-off parameter; check noise estimates |
| Model too smooth | Reduce regularization weight; try sparse norms (L1) |
| pyGIMLi mesh too coarse | Increase `quality` parameter in mesh generation |
