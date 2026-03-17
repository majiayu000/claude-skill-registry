---
name: telemetry-analysis
description: TelemetryAnalysis.jl providing an API framework for satellite telemetry packet processing. Use when fetching, unpacking, or processing satellite telemetry data, defining transfer functions, or building telemetry databases.
---

# TelemetryAnalysis.jl

API framework for satellite telemetry processing. Repo: [JuliaSpace/TelemetryAnalysis.jl](https://github.com/JuliaSpace/TelemetryAnalysis.jl)

## Key Types

- `TelemetrySource` -- Abstract type for telemetry data sources (subtype to implement)
- `TelemetryPacket` -- Container for a raw telemetry packet
- `TelemetryDatabase` -- Variable definitions, transfer functions, and dependencies

## API Pattern

```julia
# Initialize a telemetry source
source = init_telemetry_source(MySource, args...)

# Fetch packets in a time range
packets = get_telemetry(source, start_time, end_time)

# Create a telemetry database
db = create_telemetry_database(:my_label;
    get_telemetry_timestamp=ts_func,
    unpack_telemetry=unpack_func)

# Register variables with transfer function pipeline
add_variable!(db, :temperature, position, size, tf;
    alias=:temp, description="Board temp", endianess=:big)
```

## Transfer Function Pipeline

```
Raw Bytes -> Bit Transfer Function (btf) -> Raw Value -> Raw Transfer Function (rtf) -> Transfer Function (tf) -> Processed Value
```

## Implementing a Source

```julia
struct MySource <: TelemetrySource ... end
TelemetryAnalysis._api_init_telemetry_source(::Type{MySource}, args...) = ...
TelemetryAnalysis._api_get_telemetry(source::MySource, t0, t1) = ...
```

## Key Conventions
- Framework package: requires companion packages for concrete implementations
- Variables extracted by byte `position` + `size` + `endianess`
- Dependencies between variables supported (chained processing)
- Uses Unitful time units: `d`, `h`, `m`, `s`
- DataFrames for tabular output
