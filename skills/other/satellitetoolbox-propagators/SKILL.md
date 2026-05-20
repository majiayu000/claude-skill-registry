---
name: satellitetoolbox-propagators
description: SatelliteToolboxPropagators.jl providing a unified API for analytical orbit propagators (TwoBody, J2, J4, SGP4). Use when propagating orbits with analytical models, fitting mean elements, or comparing propagator outputs.
---

# SatelliteToolboxPropagators.jl

Unified API for analytical orbit propagators. Repo: [JuliaSpace/SatelliteToolboxPropagators.jl](https://github.com/JuliaSpace/SatelliteToolboxPropagators.jl)

## Available Propagators

| Symbol | Type | Description |
|---|---|---|
| `:TwoBody` | `OrbitPropagatorTwoBody` | Keplerian two-body |
| `:J2` | `OrbitPropagatorJ2` | J2 mean elements |
| `:J2osc` | `OrbitPropagatorJ2Osculating` | J2 with osculating output |
| `:J4` | `OrbitPropagatorJ4` | J4 mean elements |
| `:J4osc` | `OrbitPropagatorJ4Osculating` | J4 with osculating output |
| `:SGP4` | `OrbitPropagatorSgp4` | SGP4/SDP4 from TLE |

## Initialize and Propagate

```julia
# Init from KeplerianElements or orbital parameters
orbp = Propagators.init(Val(:J2), orb)
orbp = Propagators.init(Val(:J2), epoch_jd, a, e, i, Ω, ω, f)

# Init from TLE (SGP4 only)
orbp = Propagators.init(Val(:SGP4), tle)

# Propagate by Δt seconds from epoch
(r_i, v_i) = Propagators.propagate!(orbp, Δt)

# Propagate to a specific epoch
(r_i, v_i) = Propagators.propagate_to_epoch!(orbp, jd)

# Step from current time (not epoch)
(r_i, v_i) = Propagators.step!(orbp, Δt)

# One-shot: init + propagate
(r_i, v_i, orbp) = Propagators.propagate(Val(:J2), Δt, epoch_jd, a, e, i, Ω, ω, f)
```

## Return as OrbitStateVector

```julia
sv = Propagators.propagate!(orbp, Δt, OrbitStateVector)
```

## Vectorized Propagation

```julia
(vr, vv) = Propagators.propagate!(orbp, [0.0, 60.0, 120.0]; ntasks=4)
```

## Fitting Mean Elements

```julia
mean_elements = Propagators.fit_mean_elements(Val(:J2), vjd, vr_i, vv_i)
```

## Query Propagator State

```julia
Propagators.epoch(orbp)            # Epoch [JD]
Propagators.last_instant(orbp)     # Last propagation time [s]
Propagators.mean_elements(orbp)    # Current mean elements
Propagators.name(orbp)             # Propagator name string
```

## Key Conventions
- Units: **meters**, **m/s**, **seconds** for Δt, **Julian Day** for epochs
- Propagator selection via `Val(:Symbol)` dispatch
- `Dates.Period` inputs auto-converted to seconds
- Output frame: inertial (ECI) for analytical propagators, TEME for SGP4
- Re-exports SatelliteToolboxBase and SatelliteToolboxSgp4
