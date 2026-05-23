---
name: free-weather-data
description: "Get current weather, forecasts, and historical data using free Open-Meteo and wttr.in APIs. Use when: (1) Fetching weather conditions, (2) Weather alerts and monitoring, (3) Forecast data for planning, or (4) Climate analysis."
---

# Free Weather Data API — Open-Meteo & wttr.in

Get current weather, forecasts, and historical weather data using free APIs. No API keys required. Privacy-respecting alternative to paid weather APIs ($5-100/month).

## Why This Replaces Paid Weather APIs

**💰 Cost savings:**
- ✅ **100% free** — no API keys, no rate limits
- ✅ **Comprehensive data** — current, forecast, historical weather
- ✅ **Open source** — Open-Meteo is fully open-source
- ✅ **Privacy-first** — no tracking or data collection

**Perfect for AI agents that need:**
- Weather conditions for location-based decisions
- Forecast data for planning and scheduling
- Historical weather data for analysis
- Weather alerts and monitoring

## Quick comparison

| Service | Cost | Rate limit | API key required | Privacy |
|---------|------|------------|------------------|---------|
| OpenWeatherMap | $0-180/month | 60 calls/min free | ✅ Yes | ❌ Tracked |
| WeatherAPI | $0-70/month | 1M calls/month free | ✅ Yes | ❌ Tracked |
| **Open-Meteo** | **Free** | **10k req/day** | **❌ No** | **✅ Private** |
| **wttr.in** | **Free** | **Unlimited** | **❌ No** | **✅ Private** |

## Skills

### get_current_weather_open_meteo

Get current weather using Open-Meteo (most accurate and comprehensive).

```bash
# Current weather by coordinates
LAT=40.7128
LON=-74.0060

curl -s "https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&temperature_unit=fahrenheit" \
  | jq '{
    temperature: .current.temperature_2m,
    feels_like: .current.apparent_temperature,
    humidity: .current.relative_humidity_2m,
    wind_speed: .current.wind_speed_10m,
    precipitation: .current.precipitation,
    weather_code: .current.weather_code
  }'

# With timezone
curl -s "https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,weather_code&timezone=America/New_York" \
  | jq '{temperature: .current.temperature_2m, time: .current.time}'
```

**Node.js:**

```javascript
async function getCurrentWeather(lat, lon, unit = 'fahrenheit') {
  const params = new URLSearchParams({
    latitude: lat.toString(),
    longitude: lon.toString(),
    current: 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
    temperature_unit: unit
  });
  
  const res = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`);
  
  if (!res.ok) {
    throw new Error(`Weather API failed: ${res.status}`);
  }
  
  const data = await res.json();
  
  return {
    temperature: data.current.temperature_2m,
    feelsLike: data.current.apparent_temperature,
    humidity: data.current.relative_humidity_2m,
    windSpeed: data.current.wind_speed_10m,
    windDirection: data.current.wind_direction_10m,
    precipitation: data.current.precipitation,
    weatherCode: data.current.weather_code,
    time: data.current.time,
    unit: data.current_units.temperature_2m
  };
}

// Usage
// getCurrentWeather(40.7128, -74.0060, 'fahrenheit')
//   .then(weather => {
//     console.log(`Temperature: ${weather.temperature}°${weather.unit}`);
//     console.log(`Feels like: ${weather.feelsLike}°${weather.unit}`);
//     console.log(`Humidity: ${weather.humidity}%`);
//     console.log(`Wind: ${weather.windSpeed} mph`);
//   });
```

### get_weather_forecast

Get weather forecast for the next 7-16 days.

```bash
# 7-day forecast
LAT=37.7749
LON=-122.4194

curl -s "https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code&temperature_unit=fahrenheit&timezone=America/Los_Angeles" \
  | jq '{
    dates: .daily.time,
    max_temp: .daily.temperature_2m_max,
    min_temp: .daily.temperature_2m_min,
    precipitation: .daily.precipitation_sum
  }'

# Hourly forecast for next 24 hours
curl -s "https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&hourly=temperature_2m,precipitation,weather_code&forecast_days=1" \
  | jq '{hourly: [.hourly.time, .hourly.temperature_2m, .hourly.precipitation] | transpose | map({time: .[0], temp: .[1], precip: .[2]})}'
```

**Node.js:**

```javascript
async function getWeatherForecast(lat, lon, days = 7, unit = 'fahrenheit') {
  const params = new URLSearchParams({
    latitude: lat.toString(),
    longitude: lon.toString(),
    daily: 'temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code,wind_speed_10m_max',
    temperature_unit: unit,
    forecast_days: days.toString()
  });
  
  const res = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`);
  
  if (!res.ok) {
    throw new Error(`Forecast API failed: ${res.status}`);
  }
  
  const data = await res.json();
  
  return data.daily.time.map((date, i) => ({
    date,
    maxTemp: data.daily.temperature_2m_max[i],
    minTemp: data.daily.temperature_2m_min[i],
    precipitation: data.daily.precipitation_sum[i],
    precipitationProbability: data.daily.precipitation_probability_max[i],
    maxWindSpeed: data.daily.wind_speed_10m_max[i],
    weatherCode: data.daily.weather_code[i]
  }));
}

// Usage
// getWeatherForecast(37.7749, -122.4194, 7, 'fahrenheit')
//   .then(forecast => {
//     forecast.forEach(day => {
//       console.log(`${day.date}: ${day.minTemp}°-${day.maxTemp}°, ${day.precipitationProbability}% rain`);
//     });
//   });
```

### get_weather_wttr_simple

Get simple weather using wttr.in (human-readable, very fast).

```bash
# Get weather by city name (plain text)
curl -s "https://wttr.in/London?format=3"
# Output: London: ☀️ +22°C

# Get detailed weather report
curl -s "https://wttr.in/Paris"

# JSON format
curl -s "https://wttr.in/Tokyo?format=j1" | jq '.current_condition[0] | {
  temp_f: .temp_F,
  humidity: .humidity,
  description: .weatherDesc[0].value,
  wind_mph: .windspeedMiles
}'

# Custom format (temperature and condition)
curl -s "https://wttr.in/NewYork?format=%C+%t"
# Output: Clear +75°F

# Get weather by coordinates
curl -s "https://wttr.in/40.7128,-74.0060?format=%l:+%C+%t"
```

**Node.js:**

```javascript
async function getWeatherWttr(location) {
  // location can be city name or "lat,lon"
  const res = await fetch(`https://wttr.in/${encodeURIComponent(location)}?format=j1`);
  
  if (!res.ok) {
    throw new Error(`Weather API failed: ${res.status}`);
  }
  
  const data = await res.json();
  const current = data.current_condition[0];
  
  return {
    location: data.nearest_area[0]?.areaName[0]?.value || location,
    tempF: parseInt(current.temp_F),
    tempC: parseInt(current.temp_C),
    feelsLikeF: parseInt(current.FeelsLikeF),
    feelsLikeC: parseInt(current.FeelsLikeC),
    humidity: parseInt(current.humidity),
    description: current.weatherDesc[0].value,
    windMph: parseInt(current.windspeedMiles),
    windKmh: parseInt(current.windspeedKmph),
    precipMM: parseFloat(current.precipMM),
    uvIndex: parseInt(current.uvIndex)
  };
}

// Usage
// getWeatherWttr('San Francisco')
//   .then(weather => {
//     console.log(`${weather.location}: ${weather.description}`);
//     console.log(`Temperature: ${weather.tempF}°F (feels like ${weather.feelsLikeF}°F)`);
//     console.log(`Humidity: ${weather.humidity}%`);
//   });
```

### get_historical_weather

Get historical weather data (past dates).

```bash
# Historical weather for specific date range
LAT=51.5074
LON=-0.1278
START_DATE="2024-01-01"
END_DATE="2024-01-31"

curl -s "https://archive-api.open-meteo.com/v1/archive?latitude=${LAT}&longitude=${LON}&start_date=${START_DATE}&end_date=${END_DATE}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum" \
  | jq '{
    dates: .daily.time,
    max_temps: .daily.temperature_2m_max,
    min_temps: .daily.temperature_2m_min,
    precipitation: .daily.precipitation_sum
  }'

# Historical average for a month
curl -s "https://archive-api.open-meteo.com/v1/archive?latitude=${LAT}&longitude=${LON}&start_date=2024-01-01&end_date=2024-01-31&daily=temperature_2m_mean" \
  | jq '[.daily.temperature_2m_mean[]] | add / length'
```

**Node.js:**

```javascript
async function getHistoricalWeather(lat, lon, startDate, endDate) {
  const params = new URLSearchParams({
    latitude: lat.toString(),
    longitude: lon.toString(),
    start_date: startDate, // Format: YYYY-MM-DD
    end_date: endDate,
    daily: 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code'
  });
  
  const res = await fetch(`https://archive-api.open-meteo.com/v1/archive?${params}`);
  
  if (!res.ok) {
    throw new Error(`Historical weather API failed: ${res.status}`);
  }
  
  const data = await res.json();
  
  return data.daily.time.map((date, i) => ({
    date,
    maxTemp: data.daily.temperature_2m_max[i],
    minTemp: data.daily.temperature_2m_min[i],
    precipitation: data.daily.precipitation_sum[i],
    weatherCode: data.daily.weather_code[i]
  }));
}

// Usage
// getHistoricalWeather(40.7128, -74.0060, '2024-01-01', '2024-01-31')
//   .then(history => {
//     const avgTemp = history.reduce((sum, day) => 
//       sum + (day.maxTemp + day.minTemp) / 2, 0) / history.length;
//     console.log(`Average temperature in January: ${avgTemp.toFixed(1)}°C`);
//   });
```

### decode_weather_code

Decode Open-Meteo weather codes into human-readable descriptions.

```bash
# Weather code reference
decode_weather_code() {
  case $1 in
    0) echo "Clear sky" ;;
    1|2|3) echo "Partly cloudy" ;;
    45|48) echo "Foggy" ;;
    51|53|55) echo "Drizzle" ;;
    61|63|65) echo "Rain" ;;
    71|73|75) echo "Snow" ;;
    77) echo "Snow grains" ;;
    80|81|82) echo "Rain showers" ;;
    85|86) echo "Snow showers" ;;
    95) echo "Thunderstorm" ;;
    96|99) echo "Thunderstorm with hail" ;;
    *) echo "Unknown" ;;
  esac
}

# Usage
decode_weather_code 61  # Output: Rain
```

**Node.js:**

```javascript
function decodeWeatherCode(code) {
  const weatherCodes = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Foggy',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Light freezing rain',
    67: 'Heavy freezing rain',
    71: 'Slight snow fall',
    73: 'Moderate snow fall',
    75: 'Heavy snow fall',
    77: 'Snow grains',
    80: 'Slight rain showers',
    81: 'Moderate rain showers',
    82: 'Violent rain showers',
    85: 'Slight snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail'
  };
  
  return weatherCodes[code] || 'Unknown';
}

// Usage
// console.log(decodeWeatherCode(61)); // Output: Slight rain
```

### weather_alerts_and_monitoring

Check weather conditions and generate alerts.

**Node.js:**

```javascript
async function checkWeatherAlerts(lat, lon, thresholds) {
  const {
    maxTemp = 95,      // °F
    minTemp = 32,      // °F
    maxWindSpeed = 30, // mph
    maxPrecip = 2      // inches
  } = thresholds;
  
  const weather = await getCurrentWeather(lat, lon, 'fahrenheit');
  const forecast = await getWeatherForecast(lat, lon, 3, 'fahrenheit');
  
  const alerts = [];
  
  // Current condition alerts
  if (weather.temperature >= maxTemp) {
    alerts.push({
      type: 'high_temp',
      severity: 'warning',
      message: `High temperature: ${weather.temperature}°F`
    });
  }
  
  if (weather.temperature <= minTemp) {
    alerts.push({
      type: 'low_temp',
      severity: 'warning',
      message: `Low temperature: ${weather.temperature}°F`
    });
  }
  
  if (weather.windSpeed >= maxWindSpeed) {
    alerts.push({
      type: 'high_wind',
      severity: 'warning',
      message: `High wind speed: ${weather.windSpeed} mph`
    });
  }
  
  // Forecast alerts
  forecast.forEach(day => {
    if (day.precipitation >= maxPrecip) {
      alerts.push({
        type: 'heavy_rain',
        severity: 'watch',
        message: `Heavy rain expected on ${day.date}: ${day.precipitation} inches`,
        date: day.date
      });
    }
  });
  
  return {
    currentWeather: weather,
    forecast: forecast,
    alerts: alerts,
    hasAlerts: alerts.length > 0
  };
}

// Usage
// checkWeatherAlerts(40.7128, -74.0060, {
//   maxTemp: 90,
//   minTemp: 32,
//   maxWindSpeed: 25,
//   maxPrecip: 1.5
// }).then(result => {
//   console.log(`Current: ${result.currentWeather.temperature}°F`);
//   if (result.hasAlerts) {
//     console.log('⚠️ Weather Alerts:');
//     result.alerts.forEach(alert => 
//       console.log(`  - ${alert.severity.toUpperCase()}: ${alert.message}`)
//     );
//   } else {
//     console.log('✅ No weather alerts');
//   }
// });
```

## Agent prompt

```text
You have access to free weather APIs (Open-Meteo and wttr.in). When you need weather data:

1. For current weather and forecasts, use Open-Meteo:
   - Current: https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code
   - Forecast: Add &daily=temperature_2m_max,temperature_2m_min,precipitation_sum
   - Historical: https://archive-api.open-meteo.com/v1/archive

2. For quick weather checks, use wttr.in:
   - Simple: https://wttr.in/{city}?format=3
   - JSON: https://wttr.in/{city}?format=j1
   - Works with city names or coordinates

3. Weather parameters available:
   - Temperature (current, feels-like, max/min)
   - Humidity, precipitation, wind speed/direction
   - Weather codes (0=clear, 61=rain, 71=snow, 95=thunderstorm)
   - UV index, cloud cover, visibility

4. Temperature units:
   - Open-Meteo: Add &temperature_unit=fahrenheit (default: celsius)
   - wttr.in: Returns both Celsius and Fahrenheit

5. Best practices:
   - Cache weather data for 15-30 minutes
   - Use coordinates for accuracy (get from geocoding)
   - Decode weather codes to human-readable descriptions
   - Set reasonable alert thresholds for monitoring

No API keys required. Unlimited requests within fair use.
```

## Cost analysis: Open-Meteo vs. paid APIs

**Scenario: AI agent checking weather 1,000 times/month**

| Provider | Monthly cost | Rate limits | API key required |
|----------|--------------|-------------|------------------|
| OpenWeatherMap | **$15-50** | 60 calls/min | ✅ Yes |
| WeatherAPI | **$0-10** | 1M calls/month free | ✅ Yes |
| **Open-Meteo** | **$0** | **10k req/day** | **❌ No** |
| **wttr.in** | **$0** | **Unlimited** | **❌ No** |

**Annual savings with Open-Meteo: $180-$600**

## Rate limits / Best practices

- ✅ **Open-Meteo: 10,000 requests/day** — Very generous for typical use
- ✅ **wttr.in: Unlimited** — Community service with fair use
- ✅ **Cache weather data** — Weather doesn't change frequently (15-30 min cache)
- ✅ **Use coordinates** — More accurate than city names
- ✅ **Decode weather codes** — Convert numeric codes to descriptions
- ✅ **Set timeouts** — 10-second timeout for weather requests
- ⚠️ **Self-host for critical apps** — Open-Meteo is self-hostable
- ⚠️ **Don't poll continuously** — Weather updates hourly, not every second

## Troubleshooting

**Error: "Invalid coordinates"**
- Symptom: API returns error for lat/lon
- Solution: Validate lat ∈ [-90, 90], lon ∈ [-180, 180]

**No data returned:**
- Symptom: API returns empty or null values
- Solution: Check if location has weather station coverage; try nearby coordinates

**Historical data missing:**
- Symptom: Archive API returns no data for date range
- Solution: Open-Meteo archive starts from 1940; check date format is YYYY-MM-DD

**Weather code not recognized:**
- Symptom: Unknown weather code number
- Solution: Refer to WMO weather code standard; codes 0-99 are defined

**wttr.in returns HTML instead of JSON:**
- Symptom: Response is HTML page
- Solution: Ensure you add ?format=j1 to get JSON response

**Temperature unit confusion:**
- Symptom: Unexpected temperature values
- Solution: Open-Meteo defaults to Celsius; add &temperature_unit=fahrenheit if needed

## See also

- [../free-geocoding-and-maps/SKILL.md](../free-geocoding-and-maps/SKILL.md) — Get coordinates for weather lookups
- [../send-email-programmatically/SKILL.md](../send-email-programmatically/SKILL.md) — Send weather alerts via email
- [../using-telegram-bot/SKILL.md](../using-telegram-bot/SKILL.md) — Send weather updates via Telegram
