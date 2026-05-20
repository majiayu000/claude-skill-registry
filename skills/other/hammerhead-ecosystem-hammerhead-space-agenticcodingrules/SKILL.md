---
name: hammerhead-ecosystem
description: HAMMERHEAD-Space Julia astrodynamics ecosystem overview and cross-cutting patterns. Use when working on any HAMMERHEAD-Space repository, when asking about package interdependencies, or when creating new packages in the ecosystem.
---

# HAMMERHEAD-Space Astrodynamics Ecosystem

## Package Dependency Graph

```
QLaw.jl ──> AstroPropagators.jl ──> AstroForceModels.jl ──> AstroCoords.jl
                                                          ├─> SatelliteToolbox ecosystem
SimsFlanagan.jl ──> Lambert.jl ──> AstroCoords.jl
AstroMeasurements.jl ──> AstroCoords.jl
```

## Shared Conventions

| Convention | Standard |
|---|---|
| Julia versions | 1.10, 1.11 |
| Formatter | JuliaFormatter BlueStyle (`style = "blue"`) |
| Static arrays | `StaticArrays` / `StaticArraysCore` everywhere |
| AD support | ForwardDiff, Enzyme, Mooncake, Zygote, PolyesterForwardDiff |
| Allocation testing | AllocCheck.jl on all hot-path functions |
| Type stability | JET.jl on all packages |
| Package quality | Aqua.jl on all packages |
| Struct constructors | `@with_kw` from Parameters.jl |
| SciML interface | `solve(Problem, Algorithm)` pattern from SciMLBase |
| Default branch | `master` (not `main`) |

## Core Design Principles

1. **AD-first**: All code must be differentiable. Use `promote_type`, avoid mutation, use `SVector` returns.
2. **Zero allocations**: Hot-path functions (`acceleration`, `EOM`) must pass `@check_allocs`.
3. **Type stability**: All exported functions must pass JET analysis.
4. **SciML composability**: Follow Problem/Solution/Algorithm pattern.
5. **Multiple dispatch**: Use type dispatch over if/else branching.

## Standard State Representation

- Position/velocity: `[rx, ry, rz, vx, vy, vz]` km, km/s in J2000 ECI
- Parameters: `ComponentVector(; JD=epoch_jd, μ=gravitational_param)`
- Time: elapsed seconds since epoch; Julian Date = `p.JD + t / 86400.0`

## New Package Checklist

When creating a new package in this ecosystem:
- [ ] Add `.JuliaFormatter.toml` with `style = "blue"`
- [ ] Add `typos.toml` for spell checking
- [ ] Set up Aqua.jl, JET.jl, AllocCheck tests
- [ ] Use `StaticArraysCore` (not full `StaticArrays`) for minimal deps
- [ ] Support Julia 1.10+ in compat
- [ ] Follow `AbstractX` base type pattern
- [ ] Document with `# Arguments`, `# Returns`, `# References` sections
- [ ] Add AD differentiability tests against FiniteDiff
