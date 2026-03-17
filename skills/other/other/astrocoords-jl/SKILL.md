---
name: astrocoords-jl
description: Develop and maintain AstroCoords.jl, a Julia library for orbital coordinate representations and transformations. Use when working on AstroCoords.jl, adding new coordinate sets, implementing coordinate transformations, or converting between orbital elements.
---

# AstroCoords.jl

High-performance, non-allocating Julia library for orbital coordinate representations and transformations. Repo: [HAMMERHEAD-Space/AstroCoords.jl](https://github.com/HAMMERHEAD-Space/AstroCoords.jl)

## Architecture

### Type Hierarchy
```
Coordinate{N,T} <: StaticVector{N,T}
├── AstroCoord{N,T}           # Orbital coordinate sets
│   ├── Cartesian{T}          # (x, y, z, dx, dy, dz)
│   ├── Keplerian{T}          # (a, e, i, RAAN, ω, ν)
│   ├── Delaunay{T}
│   ├── ModEq{T}              # Modified equinoctial
│   ├── ModEqN{T}             # Generalized modified equinoctial
│   ├── Spherical{T}
│   ├── Cylindrical{T}
│   ├── USM7{T}, USM6{T}, USMEM{T}  # Unified State Models
│   ├── Milankovich{T}
│   ├── J2EqOE{T}             # J2 modified equinoctial
│   ├── EDromo{T}
│   ├── KustaanheimoStiefel{T}
│   └── StiefelScheifele{T}
└── AttitudeCoord{N,T}        # Attitude coordinates
```

All coordinates are `StaticVector` subtypes -- they support indexing, broadcasting, and all `StaticArrays` operations.

### Source Layout
```
src/
  AstroCoords.jl             # Module, includes, exports, alias dictionary
  core_types.jl              # Abstract types, Transformation hierarchy
  anomalies.jl               # Kepler solver, true/eccentric/mean anomaly conversions
  quantities.jl              # meanMotion, orbitalPeriod, orbitalNRG, angularMomentum
  regularized_config.jl      # Config for regularized coords (EDromo, KS, SS)
  transformations.jl         # BFS graph, macro-generated transformation pairs
  utils.jl
  coordinate_sets/           # One file per coordinate type
  coordinate_changes/        # Conversion math between coordinate systems
ext/
  AstroCoordsZygoteExt.jl   # Zygote AD extension
```

## Key Patterns

### Coordinate Construction (3 forms per type)
```julia
# Field-by-field
cart = Cartesian(x, y, z, dx, dy, dz)

# From vector
cart = Cartesian(vec)

# Convert from another coordinate (auto-finds path via BFS graph)
cart = Cartesian(kep, μ)
```

### Extract Raw Data
```julia
params(cart)   # -> SVector{6,T}
cart.r          # -> SVector{3,T} position (Cartesian only)
cart.v          # -> SVector{3,T} velocity (Cartesian only)
```

### Transformation System
- `@define_transformation_pair` macro generates forward/inverse transforms
- BFS graph finds shortest conversion path between any two coordinate types
- Transformations composable via `compose()` / `Base.:∘`
- All transforms: `(coord, μ, args...)` signature

### Orbital Quantities
```julia
meanMotion(a, μ)          # or meanMotion(kep, μ)
orbitalPeriod(a, μ)
orbitalNRG(a, μ)
angularMomentumVector(cart, μ)
```

Note: functions use `camelCase` (project convention for orbital quantities).

### Anomaly Conversions
```julia
KeplerSolver(M, e)  # Mean -> Eccentric anomaly
```

## Adding a New Coordinate Set

1. Create `src/coordinate_sets/newcoord.jl` with `struct NewCoord{T} <: AstroCoord{N,T}`
2. Implement `Tuple(::Type{NewCoord})` for field names
3. Add transformations in `src/coordinate_changes/` to/from at least Cartesian
4. Register with `@define_transformation_pair` in `transformations.jl`
5. Add to `_COORDINATE_SETS` test array
6. Tests: construction, round-trip conversions, AD with all backends, `@check_allocs`

## Dependencies
- `LinearAlgebra` (stdlib), `StaticArrays` 1.9
- Weak dep: `Zygote` (0.6, 0.7) via package extension
- Julia 1.10, 1.11
