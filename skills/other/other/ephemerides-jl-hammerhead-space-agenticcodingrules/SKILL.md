---
name: ephemerides-jl
description: Ephemerides.jl for reading JPL binary SPK and PCK ephemeris kernels. Use when loading SPICE kernels, computing celestial body positions/velocities, or querying ephemeris data for orbit propagation.
---

# Ephemerides.jl

Pure-Julia, allocation-free, thread-safe reader for JPL binary SPK and PCK ephemeris kernels. Repo: [JuliaSpaceMissionDesign/Ephemerides.jl](https://github.com/JuliaSpaceMissionDesign/Ephemerides.jl)

Note: This package only *reads* kernel data. For frame transformations, use FrameTransformations.jl.

## Loading Kernels

```julia
eph = EphemerisProvider("de440.bsp")
eph = EphemerisProvider(["de440.bsp", "moon_pa_de440.bpc"])
```

## State Vector Queries

```julia
# from/to are NAIF integer IDs, time is TDB seconds since J2000
r     = ephem_vector3(eph, from, to, time)    # SVector{3}  position
rv    = ephem_vector6(eph, from, to, time)    # SVector{6}  pos + vel
rva   = ephem_vector9(eph, from, to, time)    # SVector{9}  pos + vel + acc
rvaj  = ephem_vector12(eph, from, to, time)   # SVector{12} pos + vel + acc + jerk
```

## Orientation Queries

```julia
ang   = ephem_rotation3(eph, from, to, time)   # SVector{3}  angles
angd  = ephem_rotation6(eph, from, to, time)   # SVector{6}  angles + rates
angdd = ephem_rotation9(eph, from, to, time)   # SVector{9}
```

## Kernel Inspection

```julia
ephem_get_points(eph)        # Available NAIF IDs
ephem_get_axes(eph)          # Available frame IDs
ephem_timescale_id(eph)      # 1=TDB, 2=TCB
ephem_spk_records(eph)       # Vector{EphemRecordSPK}
ephem_spk_timespan(eph)      # (first_time, last_time, continuity)
```

## Key Conventions
- Time: **TDB seconds since J2000**
- Bodies: **NAIF integer IDs** (399=Earth, 301=Moon, 10=Sun, etc.)
- Returns `SVector` -- allocation-free
- AD-compatible (ForwardDiff)
- SPK segment types: 1, 2, 3, 5, 8, 9, 12, 13, 14, 15, 17, 18, 19, 20, 21
- Interpolation: Chebyshev, Hermite, and Lagrange internally
