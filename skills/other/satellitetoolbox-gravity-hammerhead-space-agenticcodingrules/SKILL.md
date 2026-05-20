---
name: satellitetoolbox-gravity
description: SatelliteToolboxGravityModels.jl for spherical harmonic gravity field computation. Use when loading gravity models (EGM96, EGM2008), computing gravitational acceleration or potential, or working with ICGEM gravity field files.
---

# SatelliteToolboxGravityModels.jl

Spherical harmonic gravity field modeling. Repo: [JuliaSpace/SatelliteToolboxGravityModels.jl](https://github.com/JuliaSpace/SatelliteToolboxGravityModels.jl)

## Loading a Model

```julia
using SatelliteToolboxGravityModels

# Load from ICGEM file (downloads and caches automatically)
model = GravityModels.load(IcgemFile, fetch_icgem_file(:EGM96))
model = GravityModels.load(IcgemFile, fetch_icgem_file(:EGM2008))
```

## Computing Accelerations

All positions must be in **ITRF (body-fixed frame)** in **meters**.

```julia
# Gravitational acceleration (mass-attraction only) -> SVector{3} [m/s²]
a = GravityModels.gravitational_acceleration(model, r_itrf; max_degree=70, max_order=70)

# Gravity acceleration (includes centrifugal) -> SVector{3} [m/s²]
g = GravityModels.gravity_acceleration(model, r_itrf; max_degree=70)

# Gravitational potential -> scalar [J/kg]
U = GravityModels.gravitational_potential(model, r_itrf; max_degree=70)

# Field derivative in spherical coords -> (dU/dr, dU/dϕ, dU/dλ)
fd = GravityModels.gravitational_field_derivative(model, r_itrf; max_degree=70)
```

## Pre-allocated Legendre Buffers (for hot-path performance)

```julia
P  = LowerTriangularStorage{RowMajor, Float64}(max_degree + 1)
dP = LowerTriangularStorage{RowMajor, Float64}(max_degree + 1)
a  = GravityModels.gravitational_acceleration(model, r; max_degree=70, P=P, dP=dP)
```

## Model Queries

```julia
GravityModels.gravity_constant(model)       # μ [m³/s²]
GravityModels.radius(model)                 # Reference radius [m]
GravityModels.maximum_degree(model)         # Max available degree
GravityModels.coefficients(model, n, m)     # (Clm, Slm) at degree n, order m
GravityModels.coefficient_norm(model)       # :full, :schmidt, or :unnormalized
```

## Key Conventions
- Positions in **ITRF, meters**. Returns in **m/s²**.
- `max_degree` and `max_order` keywords truncate the expansion
- Time-varying coefficients supported (pass `time` argument as seconds since J2000 or `DateTime`)
- AD support via ForwardDiff/Zygote package extension
- Uses `LowerTriangularStorage{RowMajor}` from SatelliteToolboxBase for efficient coefficient storage
