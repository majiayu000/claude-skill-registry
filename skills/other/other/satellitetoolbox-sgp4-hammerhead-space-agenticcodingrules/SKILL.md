---
name: satellitetoolbox-sgp4
description: SatelliteToolboxSgp4.jl implementing the SGP4/SDP4 orbit propagator for TLE-based orbit prediction. Use when propagating TLEs, fitting TLEs from osculating states, or updating TLE epochs.
---

# SatelliteToolboxSgp4.jl

SGP4/SDP4 orbit propagator for TLE-based prediction. Repo: [JuliaSpace/SatelliteToolboxSgp4.jl](https://github.com/JuliaSpace/SatelliteToolboxSgp4.jl)

## Basic Propagation

```julia
# One-shot: init + propagate
(r_teme, v_teme, sgp4d) = sgp4(t_min, tle)

# Two-step: init then propagate
sgp4d = sgp4_init(tle)
(r_teme, v_teme) = sgp4!(sgp4d, t_min)       # t_min = minutes from TLE epoch
```

## TLE Fitting

```julia
# Fit TLE from osculating state vectors
(fitted_tle, P) = fit_sgp4_tle(vjd, vr_teme, vv_teme;
    estimate_bstar=true, max_iterations=50, atol=1e-4, rtol=1e-4)

# In-place version
(fitted_tle, P) = fit_sgp4_tle!(sgp4d, vjd, vr_teme, vv_teme)
```

## Epoch Update

```julia
new_tle = update_sgp4_tle_epoch(tle, new_epoch_jd)
```

## Constants

```julia
sgp4c_wgs84       # WGS-84 Float64 (default)
sgp4c_wgs84_f32   # WGS-84 Float32
sgp4c_wgs72       # WGS-72 Float64
sgp4c_wgs72_f32   # WGS-72 Float32

sgp4d = sgp4_init(tle; sgp4c=sgp4c_wgs72)  # Use WGS-72
```

## Key Conventions
- Propagation time in **minutes** (not seconds!)
- Output: position in **km**, velocity in **km/s**
- Output frame: **TEME** (True Equator, Mean Equinox)
- Returns `SVector{3, T}`
- In-place `!` variants for reduced allocations
- Re-exports SatelliteToolboxBase and SatelliteToolboxTle
