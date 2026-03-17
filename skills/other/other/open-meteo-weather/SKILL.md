---
name: open-meteo-weather
description: Get current weather using the Open-Meteo API. Use for requests like “current weather in Boston,” “get weather for Medford, MA,” or any task that needs a quick current_weather lookup via Open-Meteo (by location name or lat/lon). Use when the user wants a direct API call or a tiny CLI flow to fetch current conditions.
---

# Open-Meteo Weather

## Overview
Fetch current weather from Open-Meteo with a tiny, deterministic flow. Prefer the script for repeatable calls; fall back to raw URL construction when asked for a direct API call.

## Quick Start
- Use the script for location names:

```bash
/Users/ivancampos/.codex/skills/open-meteo-weather/scripts/open_meteo_current.py --location "Boston, MA"
```

- Use the script for explicit coordinates:

```bash
/Users/ivancampos/.codex/skills/open-meteo-weather/scripts/open_meteo_current.py --lat 42.3601 --lon -71.0589
```

- Provide a direct API call when the user requests a raw URL:

```text
https://api.open-meteo.com/v1/forecast?latitude=42.3601&longitude=-71.0589&current_weather=true&timezone=auto
```

## Workflow
1. Determine input type: location name or lat/lon.
2. If location name is provided, geocode first (use the Open-Meteo geocoding API).
3. Call the forecast endpoint with `current_weather=true` and `timezone=auto`.
4. Return JSON with `location` and a normalized `current_weather` object.
   - Include both `temperature_c` and `temperature_f`.
   - Use keys: `windspeed_kmh`, `winddirection_deg`, `weathercode`, `is_day`, `time`, `interval`.

## Examples
- “Get current weather in Boston” → geocode, then call forecast.
- “Use this URL for Medford, MA” → provide direct forecast URL with given lat/lon.

## Resources
### scripts/
- `open_meteo_current.py`: CLI for location or lat/lon; prints JSON with `location` and `current_weather`.

### references/
- `open_meteo.md`: endpoint and parameter quick reference.
