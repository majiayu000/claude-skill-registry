---
name: satellitetoolbox-atmosphere
description: SatelliteToolboxAtmosphericModels.jl for computing atmospheric density and temperature using empirical models (Exponential, JR1971, JB2008, NRLMSISE-00). Use when computing atmospheric drag, looking up density at altitude, or working with atmospheric models for orbit propagation.
---

# SatelliteToolboxAtmosphericModels.jl

Atmospheric density and temperature models. Repo: [JuliaSpace/SatelliteToolboxAtmosphericModels.jl](https://github.com/JuliaSpace/SatelliteToolboxAtmosphericModels.jl)

## Models

All functions accessed via `AtmosphericModels.` submodule prefix.

### Exponential (simplest, no space indices needed)
```julia
ρ = AtmosphericModels.exponential(h)  # h [m] -> density [kg/m³]
```

### Jacchia-Roberts 1971
```julia
out = AtmosphericModels.jr1971(jd, ϕ_gd, λ, h)        # auto-fetches indices
out = AtmosphericModels.jr1971(jd, ϕ_gd, λ, h, F10, F10ₐ, Kp)  # manual indices
out.total_density      # [kg/m³]
out.temperature        # [K]
out.exospheric_temperature  # [K]
```

### Jacchia-Bowman 2008
```julia
out = AtmosphericModels.jb2008(jd, ϕ_gd, λ, h)  # auto-fetches indices
out = AtmosphericModels.jb2008(jd, ϕ_gd, λ, h, F10, F10ₐ, S10, S10ₐ, M10, M10ₐ, Y10, Y10ₐ, DstΔTc)
```

### NRLMSISE-00
```julia
# NOTE: argument order differs! (time, altitude, lat, lon)
out = AtmosphericModels.nrlmsise00(jd, h, ϕ_gd, λ)          # auto-fetches
out = AtmosphericModels.nrlmsise00(jd, h, ϕ_gd, λ, F10ₐ, F10, ap)
```

## Output Fields (all models)
- `total_density` [kg/m³], `temperature` [K], `exospheric_temperature` [K]
- Species number densities [1/m³]: `N2_number_density`, `O2_number_density`, `O_number_density`, `He_number_density`, `H_number_density`, `Ar_number_density`

## Prerequisites
```julia
SpaceIndices.init()  # Required before auto-fetching indices
```

## Key Conventions
- Altitude in **meters**, angles in **radians**
- Time as Julian Day (`Number`) or `DateTime`
- JR1971/JB2008: args are `(time, lat, lon, alt)`. NRLMSISE-00: args are `(time, alt, lat, lon)`
- AD support via ForwardDiff, Mooncake, and Zygote extensions
- Pass `P` keyword to NRLMSISE-00 for pre-allocated Legendre buffer
