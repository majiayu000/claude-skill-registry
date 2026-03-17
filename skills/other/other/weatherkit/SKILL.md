---
name: weatherkit
description: Access Apple WeatherKit REST API for detailed weather forecasts using JWT authentication.
homepage: https://developer.apple.com/documentation/weatherkitrestapi/
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "env": ["APPLE_TEAM_ID", "APPLE_KEY_ID", "APPLE_WEATHERKIT_KEY_PATH", "APPLE_SERVICE_ID"] },
      },
  }
---

# Apple WeatherKit Skill

## Why WeatherKit?

While simpler weather tools can provide quick forecasts, the `weatherkit` skill leverages Apple's robust WeatherKit REST API to deliver:

-   **Highly Detailed Data:** Access to granular data points like UV Index, humidity, wind gusts, sunrise/sunset times, and more.
-   **Longer Forecast Horizons:** Provides forecasts for up to 10 days, exceeding many free command-line tools.
-   **Reliable Data Source:** Powered by Apple Weather, offering timely and hyperlocal information.
-   **Programmatic Access:** Ideal for integrating detailed weather data into automated workflows and decision-making processes.

This skill allows you to fetch current weather and detailed weather forecasts using Apple's WeatherKit REST API. It authenticates using JSON Web Tokens (JWT) based on your Apple Developer Team ID, Key ID, Service ID, and a private key file.

## Configuration

This skill requires the following environment variables to be set:

-   `APPLE_TEAM_ID`: Your Apple Developer Team ID.
-   `APPLE_KEY_ID`: Your WeatherKit API Key ID.
-   `APPLE_WEATHERKIT_KEY_PATH`: The absolute path to your WeatherKit private key file (`.p8`).
-   `APPLE_SERVICE_ID`: The Bundle ID / Service ID associated with your WeatherKit access (e.g., `net.free-sky.weatherkit`).

## Actions

### `weatherkit.get_forecast`

Retrieves a detailed weather forecast for a specified location and date range.

**Parameters:**

-   `latitude`: (Required, float) The latitude of the location.
-   `longitude`: (Required, float) The longitude of the location.
-   `start_date`: (Optional, YYYY-MM-DD string) The start date for the forecast. Defaults to today.
-   `end_date`: (Optional, YYYY-MM-DD string) The end date for the forecast. Defaults to `start_date` + 5 days.
-   `timezone`: (Optional, string) The IANA timezone name (e.g., "America/Los_Angeles"). Defaults to "auto".
-   `data_sets`: (Optional, list of strings) Which data sets to return (e.g., ["forecastDaily", "forecastHourly"]). Defaults to ["forecastDaily", "currentWeather"].
-   `country_code`: (Optional, string) The ISO 3166-1 alpha-2 country code (e.g., "US", "GB"). Defaults to "US".

**Example Usage:**

```tool_code
exec {
  command: "skills/weatherkit/venv/bin/python3 skills/weatherkit/weatherkit.py get_forecast --latitude 33.8121 --longitude -117.9190 --start-date 2026-02-12 --end-date 2026-02-15 --country-code US --timezone America/Los_Angeles"
}
```
