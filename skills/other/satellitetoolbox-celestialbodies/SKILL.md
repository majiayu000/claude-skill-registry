---
name: satellitetoolbox-celestialbodies
description: SatelliteToolboxCelestialBodies.jl for computing Sun and Moon positions and velocities in the MOD frame. Use when computing third-body positions, Sun/Moon ephemeris, or eclipse geometry.
---

# SatelliteToolboxCelestialBodies.jl

Analytical Sun and Moon position/velocity in the Mean-Of-Date (MOD) reference frame. Repo: [JuliaSpace/SatelliteToolboxCelestialBodies.jl](https://github.com/JuliaSpace/SatelliteToolboxCelestialBodies.jl)

## Sun

```julia
r_sun = sun_position_mod(jd_tdb)          # -> SVector{3, Float64} [km]
r_sun = sun_position_mod(date_tdb)        # DateTime input
v_sun = sun_velocity_mod(jd_tdb)          # -> SVector{3, Float64} [km/s]
```

## Moon

```julia
r_moon = moon_position_mod(jd_tdb)                    # Default: Meeus algorithm (~10" accuracy)
r_moon = moon_position_mod(jd_tdb, Val(:Vallado))     # Faster, lower accuracy (~0.3°)
r_moon = moon_position_mod(jd_tdb, Val(:Meeus))       # Explicit high-accuracy
```

## Key Conventions
- Time must be in **TDB** (Barycentric Dynamical Time) as Julian Day or `DateTime`
- Output frame: **MOD** (Mean-Of-Date) -- apply precession/nutation for J2000/GCRF
- Positions in **km**, velocities in **km/s** (note: unlike other SatelliteToolbox packages)
- Returns `SVector{3, Float64}`
- Model selection via `Val(:symbol)` dispatch
