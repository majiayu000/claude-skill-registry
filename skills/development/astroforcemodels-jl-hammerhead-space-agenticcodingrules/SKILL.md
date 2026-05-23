---
name: astroforcemodels-jl
description: Develop and maintain AstroForceModels.jl, a Julia library for astrodynamics force modeling (gravity, drag, SRP, third-body, relativity). Use when working on AstroForceModels.jl, adding new force models, or computing orbital perturbation accelerations.
---

# AstroForceModels.jl

Julia package for modeling astrodynamics perturbation forces. Repo: [HAMMERHEAD-Space/AstroForceModels.jl](https://github.com/HAMMERHEAD-Space/AstroForceModels.jl)

## Architecture

### Type Hierarchy
```
AbstractAstroForceModel
├── AbstractPotentialBasedForce
│   └── AbstractGravityAstroModel
│       ├── GravityHarmonicsAstroModel   # Spherical harmonics (EGM96 etc.)
│       └── KeplerianGravityAstroModel   # Two-body point mass
└── AbstractNonPotentialBasedForce
    ├── DragAstroModel                   # Atmospheric drag
    ├── SRPAstroModel                    # Solar radiation pressure
    ├── ThirdBodyModel                   # Sun, Moon, planets
    └── RelativityModel                  # GR corrections

AbstractDynamicsModel
└── CentralBodyDynamicsModel{N,GT,PT}   # Gravity + N perturbations
```

### Source Layout
```
src/
  AstroForceModels.jl        # Module entry, abstract types, exports
  constants.jl                # Physical constants (R_EARTH, μ_SUN, etc.)
  utils.jl                    # angle_between_vectors()
  dynamics_builder.jl         # CentralBodyDynamicsModel, build_dynamics_model
  force_models/
    drag/                     # satellite_shape_model.jl, density_calculator.jl, drag_accel.jl
    gravity/                  # utils.jl, gravity_accel.jl
    relativity/               # relativity_accel.jl
    solar_radiation_pressure/ # satellite_shape_model.jl, shadow_models.jl, srp_accel.jl
    third_body/               # celestial_body.jl, third_body_model.jl, third_body_accel.jl
```

## Key Patterns

### Unified Acceleration Interface
Every force model implements the same 4-argument signature:

```julia
@inline function acceleration(
    u::AbstractVector, p::ComponentVector, t::Number, model::SomeForceModel
)::SVector{3}
    # ... compute and return acceleration in km/s^2 ...
end
```

Gravity models additionally implement:
- `potential(u, p, t, model) -> Number`
- `potential_time_derivative(u, p, t, model) -> Number`

### Force Composition
```julia
grav = GravityHarmonicsAstroModel(; gravity_model=..., eop_data=..., order=36, degree=36)
sun = ThirdBodyModel(; body=SunBody(), eop_data=eop_data)
moon = ThirdBodyModel(; body=MoonBody(), eop_data=eop_data)
srp = SRPAstroModel(; satellite_srp_model=CannonballFixedSRP(0.2), ...)
drag = DragAstroModel(; satellite_drag_model=CannonballFixedDrag(0.2), ...)

model = CentralBodyDynamicsModel(grav, (sun, moon, srp, drag))
accel = build_dynamics_model(u, p, t, model)  # Returns SVector{3}
```

`sum_accelerations` uses compile-time tuple recursion (`first`/`Base.tail`) for zero-overhead force summation.

### Satellite Shape Models
- **Drag**: `CannonballFixedDrag(area_mass_ratio)`, `StateDragModel(f)`
- **SRP**: `CannonballFixedSRP(area_mass_ratio)`, `StateSRPModel(f)`
- **Shadow**: `Conical()`, `Cylindrical()`, `No_Shadow()`

### Atmospheric Density
`compute_density()` dispatches on atmosphere model type: `JB2008`, `JR1971`, `MSIS2000`, `ExpAtmo`, `NoDensityModel`.

### Units Convention
- Input/output: km, km/s, km/s^2 (J2000 ECI)
- Internal SatelliteToolbox calls: convert to/from meters (`* 1E3`, `/ 1E3`)

## Adding a New Force Model

1. Create struct `<: AbstractNonPotentialBasedForce` (or `AbstractPotentialBasedForce`)
2. Implement `acceleration(u, p, t, model)` returning `SVector{3}`
3. Use `@inline`, return `SVector{3}`, use `promote_type` for AD
4. Add to `CentralBodyDynamicsModel` perturbation tuple
5. Tests: correctness against reference, AD with all 5 backends, `@check_allocs`

## Dependencies
- `ComponentArrays` 0.15, `Parameters` 0.12, `StaticArraysCore` 1.4
- SatelliteToolbox: atmospheric, gravity, celestial bodies, transformations
- `SpaceIndices` 2 for space weather data
