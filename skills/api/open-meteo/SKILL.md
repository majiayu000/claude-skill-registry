---
name: open-meteo
description: "Integrate Open-Meteo Weather Forecast, Air Quality, and Geocoding APIs: query design, variable selection, timezone/timeformat/units, multi-location batching, and robust error handling. Keywords: Open-Meteo, /v1/forecast, /v1/air-quality, geocoding-api, hourly, daily, current, timezone=auto, timeformat=unixtime, models, WMO weather_code, CAMS, GeoNames, httpx, FastAPI, pytest."
version: "1.4.0"
release_date: "2024-12-31"
---

# Open Meteo

## When to use

- You need weather forecasts (hourly/daily/current) for coordinates.
- You need air quality / pollen forecasts (hourly/current) for coordinates.
- You need to resolve a user-provided place name to coordinates and timezone (geocoding).
- You need to support multi-location batching (comma-separated lat/lon lists).
- You need a deterministic checklist for Open-Meteo query parameters, response parsing, and error handling.

## Goal

Provide a reliable, production-friendly way to call Open-Meteo APIs (Forecast, Air Quality, Geocoding), choose variables, control time/units/timezone, and parse responses consistently.

## Steps

1. Pick the correct API and base URL

   - Forecast: `https://api.open-meteo.com/v1/forecast`
   - Air Quality: `https://air-quality-api.open-meteo.com/v1/air-quality`
   - Geocoding: `https://geocoding-api.open-meteo.com/v1/search`

2. Resolve coordinates (if you only have a name)

   - Call Geocoding with `name` and optional `language`, `countryCode`, `count`.
   - Use the returned `latitude`, `longitude`, and `timezone` for subsequent calls.

3. Design your time axis (timezone, timeformat, and range)

   - Prefer `timezone=auto` when results must align to local midnight.
   - If you request `daily=...`, set `timezone` (docs: daily requires timezone).
   - Choose `timeformat=iso8601` for readability, or `timeformat=unixtime` for compactness.
     - If using `unixtime`, remember timestamps are GMT+0 and you must apply `utc_offset_seconds` for correct local dates.
   - Choose range controls:
     - `forecast_days` and optional `past_days`, or
     - explicit `start_date`/`end_date` (YYYY-MM-DD), and for sub-daily `start_hour`/`end_hour`.

4. Choose variables minimally (avoid "download everything")

   - Forecast: request only the variables you need via `hourly=...`, `daily=...`, `current=...`.
   - Air Quality: request only the variables you need via `hourly=...`, `current=...`.
   - Keep variable names exact; typos return a JSON error with `error: true`.

5. Choose units and model selection deliberately

   - Forecast units:
     - `temperature_unit` (`celsius` / `fahrenheit`)
     - `wind_speed_unit` (`kmh` / `ms` / `mph` / `kn`)
     - `precipitation_unit` (`mm` / `inch`)
   - Forecast model selection:
     - default `models=auto` / “Best match” combines the best models.
     - you can explicitly request models via `models=...`.
     - provider-specific forecast endpoints also exist (provider implied by path). See `references/models.md` (section "Endpoints vs `models=`") for examples and doc links.
     - for provider/model-specific selection tradeoffs, see `references/models.md`.
   - Air Quality domain selection:
     - `domains=auto` (default) or `cams_europe` / `cams_global`.

6. Implement robust request/response handling

   - Treat HTTP errors and JSON-level errors separately.
   - JSON error format is:
     - `{"error": true, "reason": "..."}`
   - When requesting multiple locations (comma-separated coordinates), expect the JSON output shape to change to a list of structures.
   - Optionally use `format=csv` or `format=xlsx` when you need data export.

7. Validate correctness with a “known city” check
   - Geocode “Berlin” → Forecast `hourly=temperature_2m` for 1–2 days → verify timezone and array lengths.
   - Air Quality `hourly=pm10,pm2_5,european_aqi` → verify units and presence of `hourly_units`.

## Critical prohibitions

- Do not include out-of-scope APIs in this skill’s implementation guidance: Historical Weather, Ensemble Models, Seasonal Forecast, Climate Change, Marine, Satellite Radiation, Elevation, Flood.
- Do not omit `timezone` when requesting `daily` variables (per docs).
- Do not assume `unixtime` timestamps are local time; they are GMT+0 and require `utc_offset_seconds` adjustment.
- Do not silently ignore `{"error": true}` responses; fail fast with the provided `reason`.
- Do not request huge variable sets by default; keep queries minimal to reduce payload and avoid accidental overuse.

## Definition of done

- You can geocode a place name and obtain coordinates/timezone.
- You can fetch Forecast data with at least one `hourly`, one `daily` (with timezone), and one `current` variable.
- You can fetch Air Quality data for at least one pollutant and one AQI metric.
- Your client code handles both HTTP-level failures and JSON-level `error: true` with clear messages.
- Attribution requirements from the docs are captured for Air Quality (CAMS) and Geocoding (GeoNames).

## Links

- Official docs (in-scope):
  - https://open-meteo.com/en/docs
  - https://open-meteo.com/en/docs/air-quality-api
  - https://open-meteo.com/en/docs/geocoding-api
- Skill references:
  - `references/forecast-api.md`
  - `references/models.md`
  - `references/weather-codes.md`
  - `references/air-quality-api.md`
  - `references/geocoding-api.md`
  - `references/examples.md`
