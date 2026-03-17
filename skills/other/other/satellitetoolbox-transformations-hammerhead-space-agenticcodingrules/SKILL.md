---
name: satellitetoolbox-transformations
description: SatelliteToolboxTransformations.jl for reference frame rotations (ECI/ECEF), geodetic/geocentric conversions, time epoch conversions, and Earth Orientation Parameters. Use when transforming between reference frames (GCRF, J2000, TOD, MOD, TEME, ITRF, PEF), converting geodetic coordinates, or handling EOP data.
---

# SatelliteToolboxTransformations.jl

Reference frame transformations, geodetic/geocentric conversions, and time epoch handling. Repo: [JuliaSpace/SatelliteToolboxTransformations.jl](https://github.com/JuliaSpace/SatelliteToolboxTransformations.jl)

## Frame Selectors (zero-arg functions returning Val singletons)

**IAU-76/FK5 ECI:** `GCRF()`, `J2000()`, `TOD()`, `MOD()`, `TEME()`
**IAU-76/FK5 ECEF:** `ITRF()`, `PEF()`
**IAU-2006/2010 ECI:** `CIRS()`, `TIRS()`, `ERS()`, `MOD06()`, `MJ2000()`

Do NOT mix IAU-76/FK5 and IAU-2006/2010 frames in one transformation.

## Frame Rotations

```julia
# Get rotation matrix (DCM by default, or Quaternion)
D = r_eci_to_ecef(GCRF(), ITRF(), jd_utc, eop)
D = r_ecef_to_eci(ITRF(), J2000(), jd_utc, eop)
D = r_eci_to_eci(J2000(), MOD(), jd_utc)
Q = r_eci_to_ecef(Quaternion, GCRF(), ITRF(), jd_utc, eop)

# Transform state vectors and orbits directly
sv_ecef = sv_eci_to_ecef(sv, GCRF(), ITRF(), jd_utc, eop)
sv_eci  = sv_ecef_to_eci(sv, ITRF(), J2000(), jd_utc, eop)
orb_mod = orb_eci_to_eci(orb, J2000(), MOD(), jd_utc)
```

EOP is optional for some frame pairs but required for ITRF transformations.

## EOP Data

```julia
eop = fetch_iers_eop()                # IAU-1980 (default)
eop = fetch_iers_eop(Val(:IAU2000A))  # IAU-2000A
```

## Geodetic/Geocentric Conversions

All positions in **meters**, angles in **radians**.

```julia
(lat, lon, h) = ecef_to_geodetic(r_ecef)                    # rad, rad, m
r_ecef        = geodetic_to_ecef(lat, lon, h)                # -> SVector{3}
(lat, lon, r) = ecef_to_geocentric(r_ecef)                   # rad, rad, m
r_ecef        = geocentric_to_ecef(lat, lon, r)              # -> SVector{3}
(phi_gc, r)   = geodetic_to_geocentric(phi_gd, h)
(phi_gd, h)   = geocentric_to_geodetic(phi_gc, r)
```

## Time Conversions

```julia
jd_ut1 = jd_utc_to_ut1(jd_utc, eop)
jd_tt  = jd_utc_to_tt(jd_utc)
DeltaAT = get_Deltaat(jd)   # Accumulated leap seconds
```

## Key Conventions
- Units: **meters**, **m/s**, **radians**, Julian Day
- Re-exports SatelliteToolboxBase (all base types/constants available)
- DCM output by default; pass `Quaternion` as first arg for quaternion output
