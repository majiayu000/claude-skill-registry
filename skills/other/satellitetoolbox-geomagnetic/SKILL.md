---
name: satellitetoolbox-geomagnetic
description: SatelliteToolboxGeomagneticField.jl for computing Earth's geomagnetic field using IGRF and dipole models. Use when computing magnetic field vectors, IGRF field values, or geomagnetic torques on spacecraft.
---

# SatelliteToolboxGeomagneticField.jl

Earth's geomagnetic field computation. Repo: [JuliaSpace/SatelliteToolboxGeomagneticField.jl](https://github.com/JuliaSpace/SatelliteToolboxGeomagneticField.jl)

## IGRF Model

```julia
# Angles in radians
B = igrf(date, r, λ, Ω; max_degree=13)                     # Geocentric (default)
B = igrf(date, h, λ, Ω, Val(:geodetic); max_degree=13)     # Geodetic

# Angles in degrees (d suffix)
B = igrfd(date, r, λ_deg, Ω_deg; max_degree=13)
B = igrfd(date, h, λ_deg, Ω_deg, Val(:geodetic))
```

## Simplified Dipole Model

```julia
B = geomagnetic_dipole_field(r_ecef, year)   # r_ecef in meters, returns B in ECEF [nT]
```

## Pre-allocated Legendre Buffers

```julia
B = igrf(date, r, λ, Ω; P=P_matrix, dP=dP_matrix)
```

## Key Conventions
- `date` as decimal year (e.g., `2024.5`), valid range: 1900-2035
- `igrf`: angles in **radians**. `igrfd`: angles in **degrees**
- Altitude/distance in **meters**
- Output: geomagnetic field in **nT** in NED (North-East-Down) frame
- Position reference: `Val(:geocentric)` (default) or `Val(:geodetic)`
- IGRF v14, spherical harmonics up to degree 13
