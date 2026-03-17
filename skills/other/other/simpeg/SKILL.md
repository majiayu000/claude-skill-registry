---
name: simpeg
description: |
  Simulation and Parameter Estimation in Geophysics. Framework for geophysical
  forward modeling and inversion. Use when Claude needs to: (1) Run geophysical
  inversions (DC resistivity, magnetics, gravity, EM), (2) Create forward models
  for potential fields or electromagnetic methods, (3) Build survey geometries
  and receiver configurations, (4) Design mesh discretizations for simulations,
  (5) Apply regularization and optimization to inverse problems, (6) Model
  subsurface physical properties from geophysical data.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Geophysical Inversion, DC Resistivity, Magnetics, Gravity, EM, Forward Modelling]
dependencies: [simpeg>=0.20.0, discretize, numpy]
complements: [pygimli, verde, pyvista]
workflow_role: modelling
---

# SimPEG - Geophysical Simulation & Inversion

## Quick Reference

```python
from discretize import TensorMesh
from simpeg.electromagnetics.static import resistivity as dc
from simpeg import maps, data_misfit, regularization, optimization
from simpeg import inverse_problem, inversion, directives
import numpy as np

# Create mesh
hx, hz = np.ones(100) * 10, np.ones(50) * 5
mesh = TensorMesh([hx, hz], origin='CN')

# Forward model
simulation = dc.Simulation2DNodal(mesh, survey=survey, sigmaMap=maps.ExpMap(mesh))
dpred = simulation.dpred(model)

# Inversion
dmis = data_misfit.L2DataMisfit(data=data, simulation=simulation)
reg = regularization.WeightedLeastSquares(mesh)
opt = optimization.InexactGaussNewton(maxIter=20)
inv_prob = inverse_problem.BaseInvProblem(dmis, reg, opt)
inv = inversion.BaseInversion(inv_prob, directiveList=[...])
mrec = inv.run(m0)
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `TensorMesh`, `TreeMesh` | Discretization (regular grid, adaptive octree) |
| `Survey` | Data acquisition geometry |
| `Simulation` | Forward modeling engine |
| `Data` | Observed/predicted data container |
| `InvProblem` | Combines misfit, regularization, optimization |

## Essential Operations

### Create Mesh
```python
from discretize import TensorMesh

# 2D mesh (x, z) - centered in x, top at z=0
hx, hz = np.ones(100) * 20, np.ones(50) * 10
mesh = TensorMesh([hx, hz], origin='CN')

# 3D mesh
mesh = TensorMesh([np.ones(50)*25, np.ones(50)*25, np.ones(30)*10], origin='CCN')
```

### DC Resistivity Survey
```python
from simpeg.electromagnetics.static import resistivity as dc

elec_locs = np.c_[np.linspace(-95, 95, 20), np.zeros(20)]
source_list = []
for i in range(17):  # dipole-dipole
    rx = dc.receivers.Dipole(elec_locs[[i+2]], elec_locs[[i+3]])
    src = dc.sources.Dipole([rx], elec_locs[i], elec_locs[i+1])
    source_list.append(src)
survey = dc.Survey(source_list)
```

### Forward Model
```python
model = np.ones(mesh.nC) * 100  # 100 ohm-m
simulation = dc.Simulation2DNodal(mesh, survey=survey, sigmaMap=maps.ExpMap(mesh))
dpred = simulation.dpred(np.log(1/model))  # input: log(conductivity)
```

### Inversion
```python
from simpeg import data_misfit, regularization, optimization
from simpeg import inverse_problem, inversion, directives, data

obs_data = data.Data(survey, dobs=dobs, standard_deviation=0.05*np.abs(dobs))
dmis = data_misfit.L2DataMisfit(data=obs_data, simulation=simulation)
reg = regularization.WeightedLeastSquares(mesh, alpha_s=1e-4, alpha_x=1, alpha_z=1)
opt = optimization.InexactGaussNewton(maxIter=20)
inv_prob = inverse_problem.BaseInvProblem(dmis, reg, opt)
dir_list = [directives.BetaSchedule(coolingFactor=2), directives.TargetMisfit()]
inv = inversion.BaseInversion(inv_prob, directiveList=dir_list)
mrec = inv.run(m0)
```

## Common Maps

| Map | Description | Use Case |
|-----|-------------|----------|
| `IdentityMap` | No transformation | Susceptibility, density |
| `ExpMap` | exp(m) | Log-parameterized conductivity |
| `ReciprocalMap` | 1/m | Resistivity to conductivity |
| `Wires` | Split model | Joint inversion |

## Physical Property Ranges

| Property | Typical Range | Units |
|----------|---------------|-------|
| Resistivity | 1 - 10000 | ohm-m |
| Conductivity | 0.0001 - 1 | S/m |
| Susceptibility | 0 - 0.1 | SI |
| Density contrast | -1 to 1 | g/cc |

## When to Use vs Alternatives

| Scenario | Recommendation |
|----------|---------------|
| Multi-method geophysical inversion (DC, magnetics, gravity, EM) | **SimPEG** - broadest method coverage |
| Near-surface ERT with standard arrays | **pyGIMLi** - simpler API, built-in array support |
| ERT-focused inversion with GUI export | **pyGIMLi** - better ERT-specific tooling |
| Custom forward modelling with flexible physics | **SimPEG** - modular design, easy to extend |
| Joint inversion of multiple geophysical datasets | **SimPEG** - built-in support via Wires maps |
| Commercial ERT processing | **Res2DInv / Res3DInv** - industry standard |

**Choose SimPEG when**: You need a unified framework for multiple geophysical methods,
custom forward operators, or research-grade flexibility. Its modular design
(mesh + survey + simulation + inversion) suits complex and non-standard problems.

**Avoid SimPEG when**: You only need standard ERT inversion (pyGIMLi is faster to set up),
or you need a turnkey commercial solution.

## Common Workflows

### Run DC resistivity inversion from survey data

- [ ] Define electrode locations and build dipole-dipole (or other) survey geometry
- [ ] Create `TensorMesh` or `TreeMesh` with appropriate cell sizes
- [ ] Set up `dc.Simulation2DNodal` with mesh, survey, and `ExpMap`
- [ ] Load observed data into `data.Data` with standard deviations
- [ ] Configure `L2DataMisfit`, `WeightedLeastSquares` regularization, and optimizer
- [ ] Set directives: `BetaSchedule`, `TargetMisfit`
- [ ] Build `BaseInvProblem` and `BaseInversion`
- [ ] Run inversion with `inv.run(m0)` using a homogeneous starting model
- [ ] Plot recovered model and compare observed vs predicted data
- [ ] Check data misfit convergence (target chi-squared ~ 1)

## Tips

1. **Use log parameters** for positive quantities (resistivity, susceptibility)
2. **Start with coarse mesh** and refine after initial tests
3. **Check data fit** by plotting observed vs predicted
4. **Tune regularization** to balance data fit and model smoothness
5. **Use TreeMesh** for 3D problems to improve efficiency

## References

- **[Survey Types](references/survey_types.md)** - Survey configurations and receiver types
- **[Mesh Types](references/mesh_types.md)** - Mesh discretization and refinement

## Scripts

- **[scripts/dc_inversion.py](scripts/dc_inversion.py)** - Complete DC resistivity inversion example
