---
name: iers-conventions-jl
description: IERSConventions.jl implementing IERS Conventions (1996, 2003, 2010) for Earth orientation, precession, nutation, and terrestrial reference frame rotations. Use when computing Earth rotation matrices, polar motion, sidereal time, or CIO/equinox-based frame transformations.
---

# IERSConventions.jl

IERS Conventions for Earth orientation computations. Repo: [JuliaSpaceMissionDesign/IERSConventions.jl](https://github.com/JuliaSpaceMissionDesign/IERSConventions.jl)

## Available Models

| Singleton | Convention | Description |
|---|---|---|
| `iers1996` | IERS 1996 | Legacy |
| `iers2003a` | IERS 2003A | High precision |
| `iers2003b` | IERS 2003B | Reduced precision |
| `iers2010a` | IERS 2010A | Current, high precision |
| `iers2010b` | IERS 2010B | Current, reduced precision |

## Frame Rotations

```julia
# GCRF -> other frames (pass IERS model as first arg)
D = iers_rot3_gcrf_to_itrf(iers2010b, tt_s)     # DCM
D = iers_rot3_gcrf_to_mod(iers2010b, tt_s)
D = iers_rot3_gcrf_to_tod(iers2010b, tt_s)
D = iers_rot3_gcrf_to_pef(iers2010b, tt_s)
D = iers_rot3_gcrf_to_cirf(iers2010b, tt_s)
D = iers_rot3_gcrf_to_tirf(iers2010b, tt_s)
D = iers_rot3_gcrf_to_gtod(iers2010b, tt_s)

# Higher-order derivatives
D, dD       = iers_rot6_gcrf_to_itrf(iers2010b, tt_s)
D, dD, ddD  = iers_rot9_gcrf_to_itrf(iers2010b, tt_s)

# Inverse rotations
D = iers_rot3_itrf_to_cirf(iers2010b, tt_s)
D = iers_rot3_itrf_to_mod(iers2010b, tt_s)
```

## EOP Data Access

```julia
eop_xp(model, tt_c)       # Polar motion x [rad]
eop_yp(model, tt_c)       # Polar motion y [rad]
eop_lod(model, tt_c)      # Length of day [s]
eop_δX(model, tt_c)       # CIP correction X [rad]
eop_δY(model, tt_c)       # CIP correction Y [rad]
```

## Internal Functions

```julia
iers_obliquity(model, tt_c)     # Mean obliquity
iers_gmst(model, tt_s)          # Greenwich Mean Sidereal Time
iers_gast(model, tt_s)          # Greenwich Apparent Sidereal Time
iers_earth_rot_rate(model, tt_c) # Earth rotation rate
```

## Key Conventions
- Time: **TT seconds since J2000** (internally converted to centuries where needed)
- `rot3/6/9/12` naming: rotation + Nth-order derivative
- Returns DCM from ReferenceFrameRotations.jl
- Registers UT1 timescale with Tempo.jl on package init
- EOP data interpolated via Akima splines from JSMDUtils
