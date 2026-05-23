---
name: space-indices
description: SpaceIndices.jl for fetching and querying space weather indices (F10.7, Ap, Kp, Dst). Use when initializing space indices, querying solar flux or geomagnetic activity data, or setting up atmospheric model inputs.
---

# SpaceIndices.jl

Fetch, cache, and query space environment indices. Repo: [JuliaSpace/SpaceIndices.jl](https://github.com/JuliaSpace/SpaceIndices.jl)

## Initialization (required before any queries)

```julia
using SpaceIndices
SpaceIndices.init()       # Downloads/caches all registered index files
# ... use indices ...
SpaceIndices.destroy()    # Cleanup (optional)
```

## Querying Indices

```julia
space_index(Val(:F10obs), DateTime(2024, 1, 5))          # Observed F10.7
space_index(Val(:F10adj_avg_center81), jd)                # 81-day centered avg F10.7
space_index(Val(:Ap), DateTime(2024, 1, 5, 12, 0, 0))    # 3-hourly Ap
space_index(Val(:Kp_daily), DateTime(2024, 1, 5))         # Daily Kp
space_index(Val(:Dst), DateTime(2024, 1, 5))              # Dst index
```

## Available Indices

**Solar Flux:** `:F10obs`, `:F10adj`, `:F10obs_avg_center81`, `:F10adj_avg_center81`, `:F10obs_avg_last81`, `:F10adj_avg_last81`
**Geomagnetic (Celestrak):** `:Ap`, `:Ap_daily`, `:Kp`, `:Kp_daily`, `:Cp`, `:C9`, `:ISN`, `:BSRN`, `:ND`
**JB2008 Indices:** `:DTC`, `:S10`, `:M10`, `:Y10`, `:S81a`, `:M81a`, `:Y81a`
**High-cadence Geomagnetic:** `:Hp30`, `:ap30`, `:Hp60`, `:ap60`
**Storm-time:** `:Dst`, `:DTC_Dst`

## Extension API (custom index sets)

```julia
struct MyIndex <: SpaceIndexSet end
SpaceIndices.urls(::Type{MyIndex}) = ["https://..."]
SpaceIndices.expiry_periods(::Type{MyIndex}) = [Day(7)]
SpaceIndices.parse_files(::Type{MyIndex}, paths) = ...
SpaceIndices.@register MyIndex
```

## Key Conventions
- Val-type dispatch: `space_index(Val(:Symbol), time)`
- Accepts both `DateTime` and Julian Day `Number`
- Auto-downloads with configurable expiry (default 1 day)
- Must call `init()` before queries; atmospheric models call it implicitly if needed
