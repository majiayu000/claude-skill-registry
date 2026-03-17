---
name: jsmd-ecosystem
description: JuliaSpaceMissionDesign (JSMD) ecosystem overview covering package dependencies, shared interfaces, utilities, and graph infrastructure. Use when working across multiple JSMD packages or understanding ecosystem architecture.
---

# JuliaSpaceMissionDesign Ecosystem

Open-source Julia packages for space mission analysis and design. Org: [JuliaSpaceMissionDesign](https://github.com/JuliaSpaceMissionDesign)

## Package Dependency Graph

```
JSMDInterfaces.jl (abstract types, @interface macro)
├── JSMDUtils.jl (math, file I/O, AD wrappers)
├── SMDGraphs.jl (graph data structures via Graphs.jl)
├── Tempo.jl (timescales, Epoch type)
├── Ephemerides.jl (SPK/PCK kernel reader)
├── CalcephEphemeris.jl (CALCEPH wrapper)
├── IERSConventions.jl (Earth orientation, precession, nutation)
├── AstroModels.jl (force models: gravity, SRP, drag)
└── FrameTransformations.jl (frame graph, state transformations)
```

## Shared Design Patterns

- **Order-parameterized**: All computations use `vector3/6/9/12` and `rotation3/6/9/12` for position through jerk (up to 4th order)
- **Graph-based**: Frames and timescales are directed graphs with automatic path-finding
- **AD-compatible**: ForwardDiff via `JSMDDiffTag` and `FunctionWrappersWrapper` with pre-baked dual-number types
- **Allocation-free**: StaticArrays, FunctionWrappers, PreallocationTools throughout
- **NAIF IDs**: Integer body/frame identifiers (399=Earth, 301=Moon, etc.)
- **Time**: Seconds since J2000 (TDB by default) via `Tempo.Epoch`

## JSMDInterfaces.jl (Foundation)

Defines abstract types and interface stubs via `@interface` macro:
- `JSMDInterfaces.Frames`: `vector3/6/9/12`, `rotation3/6/9/12`
- `JSMDInterfaces.Ephemeris`: `ephem_compute!`, `ephem_orient!`, `AbstractEphemerisProvider`
- `JSMDInterfaces.Graph`: `add_vertex!`, `add_edge!`, `get_path`, `has_path`
- `JSMDInterfaces.Models`: `parse_data`, `parse_model`, `compute_acceleration`
- `JSMDInterfaces.Bodies`: `body_rotational_elements` + derivatives

## JSMDUtils.jl (Utilities)

- **Math**: `unitvec`, `cross3/6/9/12`, angle conversions, Akima spline interpolation, rotation derivative helpers (`angle_to_δdcm`, `skew`)
- **AD**: `derivative`, `gradient!`, `jacobian!`, `hessian!` wrappers around ForwardDiff
- **File I/O**: `JSON`, `YAML`, `TXT` file type wrappers with `load()`

## SMDGraphs.jl (Graph Infrastructure)

Lightweight wrappers around Graphs.jl implementing the JSMDInterfaces.Graph interface. Provides `MappedGraphs` with Dijkstra path-finding used by Tempo and FrameTransformations.
