---
name: astropropagators-jl
description: Develop and maintain AstroPropagators.jl, a Julia library for high-fidelity orbit propagation with multiple formulations. Use when working on AstroPropagators.jl, implementing new propagators, or integrating orbit propagation with AstroForceModels.jl.
---

# AstroPropagators.jl

Julia library for high-fidelity astrodynamics orbit propagation. Repo: [HAMMERHEAD-Space/AstroPropagators.jl](https://github.com/HAMMERHEAD-Space/AstroPropagators.jl)

## Architecture

### Type Hierarchy
```
AbstractPropType (singleton base)
├── CowellPropagator         # Cartesian state
├── GaussVEPropagator        # Gauss Variational Equations
├── EDromoPropagator          # Regularized EDromo elements
├── KustaanheimoStiefelPropagator  # KS transform
├── MilankovichPropagator     # Milankovich elements
├── StiefelScheifelePropagator     # Stiefel-Scheifele
├── USM7Propagator            # Unified State Model (7-element)
├── USM6Propagator            # Unified State Model (6-element)
└── USMEMPropagator           # Unified State Model (exponential map)
```

### Source Layout
```
src/
  AstroPropagators.jl       # Module entry point
  api.jl                    # propagate() public API
  auxiliary/util.jl          # skew_sym, quaternions2DCM, RTN_frame
  propagators/               # One file per propagator (EOM + EOM!)
  events/impulsive_maneuvers.jl  # Impulsive burn callbacks
```

## Key Patterns

### Dual-Form EOM Pattern
Every propagator must implement both forms:

```julia
# Out-of-place (returns SVector, zero-allocation)
function Cowell_EOM(u, p, t, model_list)
    # ... compute accelerations ...
    return SVector{6}(du1, du2, du3, du4, du5, du6)
end

# In-place (calls out-of-place, assigns with .=)
function Cowell_EOM!(du, u, p, t, model_list)
    du .= Cowell_EOM(u, p, t, model_list)
    return nothing
end
```

### Primary API - `propagate()`
```julia
sol = propagate(
    u0, p, models, tspan;
    prop_type=CowellPropagator(),
    config=nothing,                    # RegularizedCoordinateConfig for EDromo/KS/SS
    ODE_solver=VCABM(),
    abstol=1E-13, reltol=1E-13,
)
```

### Lower-Level Usage
```julia
EOM!(du, u, p, t) = Cowell_EOM!(du, u, p, t, model_list)
prob = ODEProblem(EOM!, u0, tspan, p)
sol = solve(prob, VCABM(); abstol=1e-13, reltol=1e-13)
```

### Force Model Setup (from AstroForceModels)
```julia
grav = GravityHarmonicsAstroModel(; gravity_model=..., eop_data=..., order=36, degree=36)
sun = ThirdBodyModel(; body=SunBody(), eop_data=eop_data)
moon = ThirdBodyModel(; body=MoonBody(), eop_data=eop_data)
model_list = CentralBodyDynamicsModel(grav, (sun, moon, srp, drag))
```

### Regularized Coordinate Config
EDromo, KS, and Stiefel-Scheifele propagators require a `RegularizedCoordinateConfig` specifying the time element type: `PhysicalTime`, `ConstantTime`, or `LinearTime`.

### Event Callbacks (Regularized)
```julia
end_EDromo_integration(stop_time, config)       # ContinuousCallback for termination
EDromo_burn(burn_time, ΔV, config)              # ContinuousCallback for impulsive burn
```

## Adding a New Propagator

1. Create `src/propagators/NewName.jl` with `NewName_EOM` and `NewName_EOM!`
2. Add `NewNamePropagator <: AbstractPropType` singleton struct
3. Add dispatch in `api.jl` for `propagate()` with the new type
4. Add coordinate conversions in AstroCoords.jl if needed
5. Add tests: `test/propagators/test_newname.jl` (Keplerian + high-fidelity)
6. Add AD tests: `test/differentiability/test_newname.jl` (all 5 backends)
7. Add allocation test in `test/test_performance.jl`

## Dependencies
- `AstroCoords` 0.3, `AstroForceModels` 0.3, `ComponentArrays` 0.15
- `OrdinaryDiffEqAdamsBashforthMoulton` 1.1, `OrdinaryDiffEqCore` 1.6
- `SciMLBase` 2.58, `StaticArraysCore` 1
- SatelliteToolbox ecosystem (atmospheric, gravity, transformations, space indices)
