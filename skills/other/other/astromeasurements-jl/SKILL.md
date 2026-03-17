---
name: astromeasurements-jl
description: Develop and maintain AstroMeasurements.jl, a Julia library for computing astrodynamics measurements from observers. Use when working on AstroMeasurements.jl, implementing observation models, computing measurement Jacobians, or simulating orbit determination observations.
---

# AstroMeasurements.jl

Julia library for computing astrodynamic measurements from various observer types. Repo: [HAMMERHEAD-Space/AstroMeasurements.jl](https://github.com/HAMMERHEAD-Space/AstroMeasurements.jl)

## Architecture

### Observer Types
| Type | Measurements | Description |
|------|-------------|-------------|
| `Radar` | rho, rho_dot, alpha, delta | Range, range-rate, RA, Dec |
| `RangeOnly` | rho, rho_dot | Range and range-rate only |
| `Optical` | alpha, delta, alpha_dot, delta_dot | Angles and angular rates |
| `AngleOnly` | alpha, delta | RA and Dec only |
| `GNSSType` | x,y,z,vx,vy,vz | Full state from GNSS |
| `FullStateType` | x,y,z,vx,vy,vz | Perfect state observation (simulation) |

### Source Layout
```
src/
  AstroMeasurements.jl          # Module entry, exports, includes
  constants.jl                   # Physical constants
  observer_types.jl              # Observer type definitions
  observer_functions.jl          # Shared observer utilities
  get_measurement.jl             # Core measurement computation
  get_measurement_jacobian.jl    # Analytical Jacobians
  radar.jl                       # Radar-specific logic
  optical.jl                     # Optical-specific logic
  gnss.jl                        # GNSS-specific logic
  fullstate.jl                   # Full-state observer logic
```

## Key Patterns

### Core API
```julia
# Compute measurement from observer
meas = get_measurement(observer, state, params...)

# Compute analytical Jacobian
H = get_measurement_jacobian(observer, state, params...)
```

Multiple dispatch on observer type selects the correct measurement model.

### Analytical Jacobians
Hand-derived Jacobians verified against ForwardDiff in tests. This provides:
- Better performance than AD for orbit determination inner loops
- Validated correctness against automatic differentiation

### Features
- **Light-time correction**: Optional for ground station observations
- **Elevation masking**: Configurable elevation masks for visibility checking
- **Frame transformations**: Uses `SatelliteToolboxTransformations` for ECI/ECEF conversion

## Adding a New Observer Type

1. Define observer struct in `observer_types.jl`
2. Implement `get_measurement()` dispatch for the new type
3. Derive and implement analytical Jacobian in `get_measurement_jacobian.jl`
4. Validate Jacobian against ForwardDiff in tests
5. Add `@check_allocs` test for measurement computation

## Dependencies
- `AstroCoords` 0.3, `Parameters` 0.12, `StaticArraysCore` 1
- `SatelliteToolboxTransformations` 1 (frame transformations)
- Test: `AllocCheck`, `Aqua`, `ForwardDiff`, `JET`
