---
name: weather
description: Get weather information for locations using Open-Meteo API. Use when user asks about weather, temperature, or forecasts.
version: 1.0.0
author: Workshop Team
---

# Weather Skill

Provides weather information for locations around the world using the free Open-Meteo API.

## When to Use

- User asks about current weather
- User asks about temperature
- User asks about weather forecasts
- User mentions weather-related queries

## Available Operations

1. **Get Current Weather**: Retrieve current conditions for a location
2. **Format Weather Data**: Present weather in a user-friendly format

## Instructions

When a user asks about weather:

1. Identify the location from the user's query
2. Look up the latitude and longitude for that location (common cities below)
3. Use the Open-Meteo API to get weather data
4. Present the weather information in a friendly format

### Common City Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| New York | 40.71 | -74.01 |
| Los Angeles | 34.05 | -118.24 |
| London | 51.51 | -0.13 |
| Paris | 48.85 | 2.35 |
| Tokyo | 35.69 | 139.69 |
| Sydney | -33.87 | 151.21 |
| Miami | 25.76 | -80.19 |
| Chicago | 41.88 | -87.63 |
| San Francisco | 37.77 | -122.42 |
| Berlin | 52.52 | 13.41 |

### Weather Code Meanings

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1, 2, 3 | Mainly clear, partly cloudy, overcast |
| 45, 48 | Fog |
| 51, 53, 55 | Drizzle (light, moderate, dense) |
| 61, 63, 65 | Rain (slight, moderate, heavy) |
| 71, 73, 75 | Snow fall (slight, moderate, heavy) |
| 80, 81, 82 | Rain showers (slight, moderate, violent) |
| 95 | Thunderstorm |
| 96, 99 | Thunderstorm with hail |

## Resources

ALWAYS read this documentation before making an API request so you have the right parameters:
- `references/api_reference.md` - Complete Open-Meteo API documentation

## Examples

### Example 1: Simple Query
User asks: "What's the weather in New York?"
Response: Use coordinates (40.71, -74.01), call Open-Meteo API, format response with temperature and conditions.

### Example 2: Temperature Query
User asks: "How hot is it in Miami?"
Response: Use coordinates (25.76, -80.19), get temperature_2m, convert to Fahrenheit if needed.

## Notes

- Open-Meteo is free and requires NO API key
- Temperature is in Celsius by default (add temperature_unit=fahrenheit for F)
- All times are in the specified timezone
