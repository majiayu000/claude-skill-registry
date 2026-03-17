---
name: satellitetoolbox-odm
description: SatelliteToolboxOrbitDataMessages.jl for parsing and creating CCSDS Orbit Data Messages (OMM, NDM). Use when working with OMM XML files, fetching orbit messages from CelesTrak/SpaceTrack, or converting between OMM and TLE formats.
---

# SatelliteToolboxOrbitDataMessages.jl

CCSDS Orbit Data Messages (ODM) following the 502.0-B-3 standard. Repo: [JuliaSpace/SatelliteToolboxOrbitDataMessages.jl](https://github.com/JuliaSpace/SatelliteToolboxOrbitDataMessages.jl)

## Supported Message Types
- **OMM** -- Orbit Mean-Elements Message (primary)
- **NDM** -- Navigation Data Message (container for multiple OMMs)

## Structure

```
OrbitMeanElementsMessage
├── version::String
├── header::OmmHeader           # creation_date, originator
└── body::OmmBody
    └── segment::OmmSegment
        ├── metadata::OmmMetadata   # object_name, ref_frame, time_system
        └── data::OmmData           # epoch, elements, bstar, etc.
```

## Key Fields (OmmData)
- `epoch`, `semi_major_axis`, `mean_motion`, `eccentricity`
- `inclination`, `raan`, `arg_of_pericenter`, `mean_anomaly`
- `bstar`, `norad_cat_id`, `classification_type`

## Key Conventions
- XML format for read/write
- `@kwdef` structs with `Union{T, Nothing}` for optional fields
- Copy-with-modifications: `OrbitMeanElementsMessage(existing_omm; field=new_value)`
- TLE conversion via weak dependency on SatelliteToolboxTle
- Uses NanoDates for high-precision timestamps
- Still early version (v0.0.1)
