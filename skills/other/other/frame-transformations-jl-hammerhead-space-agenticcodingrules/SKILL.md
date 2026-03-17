---
name: frame-transformations-jl
description: FrameTransformations.jl for building custom reference frame graphs and computing arbitrary point/axes transformations up to 4th order. Use when transforming between reference frames, building frame systems, or computing high-order state derivatives.
---

# FrameTransformations.jl

High-performance, extensible reference frame graph and transformation system. Repo: [JuliaSpaceMissionDesign/FrameTransformations.jl](https://github.com/JuliaSpaceMissionDesign/FrameTransformations.jl)

## Core Type

```julia
frames = FrameSystem{4, Float64}()       # Order 4 (through jerk), Float64, TDB timescale
frames = FrameSystem{2, Float64, TDB}()  # Explicit timescale
```

## Building the Frame Graph

### Pre-defined Frames
```julia
# Celestial/Inertial
add_axes_icrf!(frames)
add_axes_gcrf!(frames)
add_axes_eme2000!(frames)

# Terrestrial (IERS)
add_axes_itrf!(frames, iers2010b)
add_axes_cirf!(frames, iers2010b)
add_axes_mod!(frames, iers2010b)
add_axes_tod!(frames, iers2010b)
add_axes_pef!(frames, iers2010b)

# Planetary / Lunar
add_axes_bci2000!(frames, body)
add_axes_pa440!(frames)          # Moon principal axes DE440
add_axes_me421!(frames)          # Moon mean Earth DE421
```

### Custom Frames
```julia
add_axes_fixedoffset!(frames, :MyFrame, id, parent_id, dcm)
add_axes_rotating!(frames, :MyFrame, id, parent_id, fun, δfun, δ²fun, δ³fun)
add_point_fixedoffset!(frames, :MyPoint, id, parent_id, axes_id, offset)
add_point_dynamical!(frames, :MyPoint, id, parent_id, axes_id, fun)
add_point_ephemeris!(frames, eph, ...)
```

## Querying Transformations

### Point State Vectors
```julia
r    = vector3(frames, from, to, axes, epoch)     # SVector{3}  position
rv   = vector6(frames, from, to, axes, epoch)     # SVector{6}  pos + vel
rva  = vector9(frames, from, to, axes, epoch)     # SVector{9}  pos + vel + acc
rvaj = vector12(frames, from, to, axes, epoch)    # SVector{12} pos + vel + acc + jerk
```

### Axes Rotations
```julia
R  = rotation3(frames, from, to, epoch)    # Rotation{1} (DCM only)
R  = rotation6(frames, from, to, epoch)    # Rotation{2} (DCM + dDCM/dt)
R  = rotation9(frames, from, to, epoch)    # Rotation{3}
R  = rotation12(frames, from, to, epoch)   # Rotation{4}
```

## Key Types
- `Translation{S,T}` -- immutable container for S position derivative vectors
- `Rotation{S,T}` -- immutable container for S DCMs + derivatives. Supports `*`, `inv()`, and application to `Translation`

## Key Conventions
- Time: `Epoch{S}` from Tempo.jl or raw seconds since J2000
- Identifiers: integer IDs or Symbol names
- Auto-differentiates transformation functions via ForwardDiff if derivatives not provided
- Graph traversal finds paths automatically between any connected frames
- Ephemerides.jl loaded via package extension
