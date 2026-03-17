---
name: satellitetoolbox-tle
description: SatelliteToolboxTle.jl for parsing, creating, fetching, and converting TLE (Two-Line Element) data. Use when reading TLE files, fetching TLEs from CelesTrak, or constructing TLE objects.
---

# SatelliteToolboxTle.jl

TLE parsing, creation, fetching, and conversion. Repo: [JuliaSpace/SatelliteToolboxTle.jl](https://github.com/JuliaSpace/SatelliteToolboxTle.jl)

## Parsing TLEs

```julia
# From string macros
tle = tle"
1 25544U 98067A   24005.50000000  .00000000  00000+0  00000+0 0    09
2 25544  51.6400 100.0000 0001000  90.0000 270.0000 15.50000000    04
"

# From strings
tle = read_tle(tle_string)
tle = read_tle(line1, line2; name="ISS")
tles = read_tles(multi_tle_string)
tles = read_tles_from_file("tles.txt")

# Without checksum verification
tle = tle_nc"..."
```

## Fetching from CelesTrak

```julia
fetcher = create_tle_fetcher(CelestrakTleFetcher)
tles = fetch_tles(fetcher; satellite_name="ISS")
tles = fetch_tles(fetcher; satellite_number=25544)
tles = fetch_tles(fetcher; international_designator="98067A")
```

## TLE Fields

| Field | Unit | Description |
|---|---|---|
| `inclination` | degrees | Orbital inclination |
| `raan` | degrees | Right ascension of ascending node |
| `eccentricity` | -- | Orbital eccentricity |
| `argument_of_perigee` | degrees | Argument of perigee |
| `mean_anomaly` | degrees | Mean anomaly |
| `mean_motion` | rev/day | Mean motion |
| `bstar` | 1/Earth radii | BSTAR drag term |
| `epoch_year`, `epoch_day` | -- | Epoch |

## Utilities

```julia
jd = tle_epoch(tle)                    # Julian Day of epoch
dt = tle_epoch(DateTime, tle)          # DateTime of epoch
str = convert(String, tle)             # Back to TLE string format
chk = tle_line_checksum(line)          # Compute line checksum
```

## Key Conventions
- TLE angles in **degrees** (TLE standard), mean motion in **rev/day**
- Search precedence: satellite_number > international_designator > satellite_name
- `@kwdef` constructor: required fields are `epoch_year`, `epoch_day`, `inclination`, `raan`, `eccentricity`, `argument_of_perigee`, `mean_anomaly`, `mean_motion`
