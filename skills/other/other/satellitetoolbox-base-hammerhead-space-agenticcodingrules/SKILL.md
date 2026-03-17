---
name: satellitetoolbox-base
description: SatelliteToolboxBase.jl providing foundational types, constants, and orbit representations for the JuliaSpace ecosystem. Use when working with KeplerianElements, OrbitStateVector, anomaly conversions, Julian Date utilities, or SatelliteToolbox constants.
---

# SatelliteToolboxBase.jl

Foundation package for the JuliaSpace SatelliteToolbox ecosystem. Repo: [JuliaSpace/SatelliteToolboxBase.jl](https://github.com/JuliaSpace/SatelliteToolboxBase.jl)

## CRITICAL: Unit Convention

SatelliteToolbox uses **meters and m/s** throughout. HAMMERHEAD libraries use **km and km/s**. Always convert at interop boundaries (`* 1e3` or `/ 1e3`).

## Key Types

```julia
KeplerianElements{Tepoch, T}  # t [JD], a [m], e, i [rad], Ω [rad], ω [rad], f [rad]
OrbitStateVector{Tepoch, T}   # t [JD], r::SVector{3,T} [m], v::SVector{3,T} [m/s]
Ellipsoid{T}                  # a (semi-major), f (flattening) -> auto-computes b, e², el²
```

## Constants

| Constant | Value | Unit |
|---|---|---|
| `GM_EARTH` | 3.986004415e14 | m³/s² |
| `EARTH_EQUATORIAL_RADIUS` | 6378137.0 | m |
| `EARTH_ANGULAR_SPEED` | 7.292115e-5 | rad/s |
| `ASTRONOMICAL_UNIT` | 1.496e11 | m |
| `SUN_RADIUS` | 6.96342e8 | m |
| `JD_J2000` | 2451545.0 | Julian Day |
| `WGS84_ELLIPSOID` | Ellipsoid{Float64} | WGS-84 |

## Orbit Conversions

```julia
kepler_to_rv(orb)          # -> (r::SVector{3}, v::SVector{3}) in meters, m/s
kepler_to_sv(orb)          # -> OrbitStateVector
rv_to_kepler(t, r, v)      # -> KeplerianElements
sv_to_kepler(sv)           # -> KeplerianElements
```

## Anomaly Conversions (all radians, returns [0, 2π])

```julia
mean_to_eccentric_anomaly(e, M; max_iterations=10, tol=nothing)
mean_to_true_anomaly(e, M)
eccentric_to_true_anomaly(e, E)
true_to_eccentric_anomaly(e, f)
true_to_mean_anomaly(e, f)
```

## Time Utilities

```julia
date_to_jd(year, month, day, hour, min, sec)  # -> Julian Day
jd_to_date(JD)                                 # -> (year, month, day, hour, min, sec)
jd_to_gmst(JD)                                 # -> GMST [rad]
```
