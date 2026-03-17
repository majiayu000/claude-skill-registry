---
name: satellite-analysis
description: SatelliteAnalysis.jl for high-level satellite mission analysis including beta angle, eclipse time, frozen orbits, Sun-synchronous orbit design, ground tracks, and visibility analysis. Use when designing orbits, computing coverage, analyzing lighting conditions, or generating ground tracks.
---

# SatelliteAnalysis.jl

High-level satellite mission analysis. Repo: [JuliaSpace/SatelliteAnalysis.jl](https://github.com/JuliaSpace/SatelliteAnalysis.jl)

## Beta Angle & Eclipse

```julia
β = beta_angle(orb, Δjd; perturbation=:J2)    # Beta angle [rad]
```

## Frozen Orbit Design

```julia
(e, ω) = frozen_orbit(a, i; gravity_model=nothing, max_degree=53)
```

## Sun-Synchronous Orbit Design

```julia
# From angular velocity
(a, i, converged) = sun_sync_orbit_from_angular_velocity(angvel, e)

# From inclination -> semi-major axis
(a, converged) = sun_sync_orbit_semi_major_axis(i, e)

# From semi-major axis -> inclination
(i, converged) = sun_sync_orbit_inclination(a, e)
```

## Ground-Repeating Orbits

```julia
# Design table of Sun-sync ground-repeating orbits
df = design_sun_sync_ground_repeating_orbit(min_rep, max_rep; kwargs...)

# Adjacent track spacing
d = ground_repeating_orbit_adjacent_track_distance(a, e, i, orbit_cycle)
θ = ground_repeating_orbit_adjacent_track_angle(a, e, i, orbit_cycle)
```

## Key Conventions
- Units: **meters**, **radians**, **seconds** (SI)
- `perturbation` keyword: `:J0`, `:J2`, `:J4`
- Newton-Raphson solvers return `(value, converged::Bool)` tuples
- DataFrames output with configurable display units via keywords
- GeoMakie plotting via package extension
- Re-exports SatelliteToolbox meta-package and DataFrames
