---
name: astromodels-jl
description: AstroModels.jl providing astrodynamics force models (gravity, SRP, drag) for the JSMD ecosystem. Use when computing gravitational acceleration, solar radiation pressure, atmospheric drag, or building force model compositions for orbit propagation.
---

# AstroModels.jl

Astrodynamics force models for the JSMD ecosystem. Repo: [JuliaSpaceMissionDesign/AstroModels.jl](https://github.com/JuliaSpaceMissionDesign/AstroModels.jl)

## Type Hierarchy

```
AbstractAccelerationModel
├── AbstractGravityModel{T}
│   ├── Point mass (central body)
│   ├── Third-body gravity
│   ├── Relativistic corrections
│   ├── Spherical harmonics (ICGEM/PDS)
│   ├── Polyhedron
│   ├── Mascons
│   └── PINN (neural network)
└── AbstractSolarPressureModel{T}
    ├── Cannonball SRP
    └── Flat plate SRP
```

Shadow models: Conical, Cylindrical

## Core API

```julia
# All models implement this interface
a = compute_acceleration(model, args...)

# Gravity models also implement
U = compute_potential(model, args...)
```

## Loading Gravity Models

```julia
# Parse coefficient data from ICGEM or PDS format files
data = parse_data(Float64, DataType, filename; kwargs...)
model = parse_model(Float64, ModelType, DataType, args...)
```

## Key Conventions
- Implements `AbstractAccelerationModel` interface from JSMDInterfaces
- Uses `PreallocationTools` for cache buffers in mutable model types
- Third-body positions resolved via `JSMDInterfaces.Frames.vector3` (frame graph lookup)
- Depends on Tempo.jl for time handling
- StaticArrays for return types
