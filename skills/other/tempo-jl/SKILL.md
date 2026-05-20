---
name: tempo-jl
description: Tempo.jl for efficient astronomical time representations and transformations between timescales. Use when working with Epoch types, converting between timescales (TDB, TT, UTC, TAI, UT1), or defining custom timescales.
---

# Tempo.jl

Astronomical time transformations with split-second precision. Repo: [JuliaSpaceMissionDesign/Tempo.jl](https://github.com/JuliaSpaceMissionDesign/Tempo.jl)

## Core Types

```julia
Epoch{S, T}    # Time in timescale S with numeric type T
Duration{T}    # Integer seconds + fractional seconds (split for precision)
DateTime{T}    # Calendar date + time wrapper
```

## Creating Epochs

```julia
ep = Epoch(0.0, TDB)                          # J2000 in TDB
ep = Epoch(86400.0, TT)                        # 1 day after J2000 in TT
ep = Epoch("2024-01-05T12:00:00.000 TDB")     # ISO string
ep = Epoch("JD 2460000.5 TDB")                # Julian Date
ep = Epoch("MJD 58849.0 TDB")                 # Modified Julian Date
ep = Epoch{TDB}(seconds)                       # Typed constructor
```

## Timescale Conversion

```julia
ep_tt = convert(TT, ep_tdb)        # TDB -> TT
ep_utc = convert(UTC, ep_tt)       # TT -> UTC
```

## Available Timescales

`TDB`, `TT`, `TAI`, `UTC`, `TCG`, `TCB`, `UT1`, `TDBH`, `GPS`

## Epoch Accessors

```julia
value(ep)         # Seconds since J2000
j2000(ep)         # Days since J2000
j2000s(ep)        # Seconds since J2000
j2000c(ep)        # Centuries since J2000
timescale(ep)     # Get the timescale
doy(ep)           # Day of year
```

## Epoch Arithmetic

```julia
ep2 = ep + 3600.0       # Advance by seconds
ep3 = ep - 86400.0      # Go back by seconds
dt = ep2 - ep1          # Duration between (same timescale only)
range = ep1:60.0:ep2    # Range of epochs
ep1 < ep2               # Comparison
```

## Custom Timescales

```julia
@timescale NTS 100 NewTimeScale              # Define a new timescale
add_timescale!(TIMESCALES, NTS, offset_fun)  # Connect to graph
```

## Key Conventions
- Internal representation: split integer + fractional seconds since J2000
- Default timescale: TDB (Barycentric Dynamical Time)
- Graph-based: timescales are nodes, offset functions are edges
- Leap seconds handled automatically (UTC<->TAI)
- AD-compatible via FunctionWrappersWrapper
- `DJ2000 = 2451545` (J2000 Julian Date constant)
