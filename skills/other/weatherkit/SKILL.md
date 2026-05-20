---
name: weatherkit
description: "Fetch current, hourly, and daily weather forecasts and display required attribution using WeatherKit. Use when integrating weather data, showing forecasts, handling weather alerts, displaying Apple Weather attribution, or querying historical weather statistics in iOS apps."
---

# WeatherKit

Fetch current conditions, hourly and daily forecasts, weather alerts, and
historical statistics using `WeatherService`. Display required Apple Weather
attribution. Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Fetching Current Weather](#fetching-current-weather)
- [Forecasts](#forecasts)
- [Weather Alerts](#weather-alerts)
- [Selective Queries](#selective-queries)
- [Attribution](#attribution)
- [Availability](#availability)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Project Configuration

1. Enable the **WeatherKit** capability in Xcode (adds the entitlement)
2. Enable WeatherKit for your App ID in the Apple Developer portal
3. Add `NSLocationWhenInUseUsageDescription` to Info.plist if using device location
4. WeatherKit requires an active Apple Developer Program membership

### Import

```swift
import WeatherKit
import CoreLocation
```

### Creating the Service

Use the shared singleton or create an instance. The service is `Sendable` and
thread-safe.

```swift
let weatherService = WeatherService.shared
// or
let weatherService = WeatherService()
```

## Fetching Current Weather

Fetch current conditions for a location. Returns a `Weather` object with all
available datasets.

```swift
func fetchCurrentWeather(for location: CLLocation) async throws -> CurrentWeather {
    let weather = try await weatherService.weather(for: location)
    return weather.currentWeather
}

// Using the result
func displayCurrent(_ current: CurrentWeather) {
    let temp = current.temperature  // Measurement<UnitTemperature>
    let condition = current.condition  // WeatherCondition enum
    let symbol = current.symbolName  // SF Symbol name
    let humidity = current.humidity  // Double (0-1)
    let wind = current.wind  // Wind (speed, direction, gust)
    let uvIndex = current.uvIndex  // UVIndex

    print("\(condition): \(temp.formatted())")
}
```

## Forecasts

### Hourly Forecast

Returns 25 contiguous hours starting from the current hour by default.

```swift
func fetchHourlyForecast(for location: CLLocation) async throws -> Forecast<HourWeather> {
    let weather = try await weatherService.weather(for: location)
    return weather.hourlyForecast
}

// Iterate hours
for hour in hourlyForecast {
    print("\(hour.date): \(hour.temperature.formatted()), \(hour.condition)")
}
```

### Daily Forecast

Returns 10 contiguous days starting from the current day by default.

```swift
func fetchDailyForecast(for location: CLLocation) async throws -> Forecast<DayWeather> {
    let weather = try await weatherService.weather(for: location)
    return weather.dailyForecast
}

// Iterate days
for day in dailyForecast {
    print("\(day.date): \(day.lowTemperature.formatted()) - \(day.highTemperature.formatted())")
    print("  Condition: \(day.condition), Precipitation: \(day.precipitationChance)")
}
```

### Custom Date Range

Request forecasts for specific date ranges using `WeatherQuery`.

```swift
func fetchExtendedForecast(for location: CLLocation) async throws -> Forecast<DayWeather> {
    let startDate = Date.now
    let endDate = Calendar.current.date(byAdding: .day, value: 10, to: startDate)!

    let forecast = try await weatherService.weather(
        for: location,
        including: .daily(startDate: startDate, endDate: endDate)
    )
    return forecast
}
```

## Weather Alerts

Fetch active weather alerts for a location. Alerts include severity, summary,
and affected regions.

```swift
func fetchAlerts(for location: CLLocation) async throws -> [WeatherAlert]? {
    let weather = try await weatherService.weather(for: location)
    return weather.weatherAlerts
}

// Process alerts
if let alerts = weatherAlerts {
    for alert in alerts {
        print("Alert: \(alert.summary)")
        print("Severity: \(alert.severity)")
        print("Region: \(alert.region)")
        if let detailsURL = alert.detailsURL {
            // Link to full alert details
        }
    }
}
```

## Selective Queries

Fetch only the datasets you need to minimize API usage and response size. Each
`WeatherQuery` type maps to one dataset.

### Single Dataset

```swift
let current = try await weatherService.weather(
    for: location,
    including: .current
)
// current is CurrentWeather
```

### Multiple Datasets

```swift
let (current, hourly, daily) = try await weatherService.weather(
    for: location,
    including: .current, .hourly, .daily
)
// current: CurrentWeather, hourly: Forecast<HourWeather>, daily: Forecast<DayWeather>
```

### Minute Forecast

Available in limited regions. Returns precipitation forecasts at minute
granularity for the next hour.

```swift
let minuteForecast = try await weatherService.weather(
    for: location,
    including: .minute
)
// minuteForecast: Forecast<MinuteWeather>?  (nil if unavailable)
```

### Available Query Types

| Query | Return Type | Description |
|---|---|---|
| `.current` | `CurrentWeather` | Current observed conditions |
| `.hourly` | `Forecast<HourWeather>` | 25 hours from current hour |
| `.daily` | `Forecast<DayWeather>` | 10 days from today |
| `.minute` | `Forecast<MinuteWeather>?` | Next-hour precipitation (limited regions) |
| `.alerts` | `[WeatherAlert]?` | Active weather alerts |
| `.availability` | `WeatherAvailability` | Dataset availability for location |

## Attribution

Apple requires apps using WeatherKit to display attribution. This is a
legal requirement.

### Fetching Attribution

```swift
func fetchAttribution() async throws -> WeatherAttribution {
    return try await weatherService.attribution
}
```

### Displaying Attribution in SwiftUI

```swift
import SwiftUI
import WeatherKit

struct WeatherAttributionView: View {
    let attribution: WeatherAttribution
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack(spacing: 8) {
            // Display the Apple Weather mark
            AsyncImage(url: markURL) { image in
                image
                    .resizable()
                    .scaledToFit()
                    .frame(height: 20)
            } placeholder: {
                EmptyView()
            }

            // Link to the legal attribution page
            Link("Weather data sources", destination: attribution.legalPageURL)
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
    }

    private var markURL: URL {
        colorScheme == .dark
            ? attribution.combinedMarkDarkURL
            : attribution.combinedMarkLightURL
    }
}
```

### Attribution Properties

| Property | Use |
|---|---|
| `combinedMarkLightURL` | Apple Weather mark for light backgrounds |
| `combinedMarkDarkURL` | Apple Weather mark for dark backgrounds |
| `squareMarkURL` | Square Apple Weather logo |
| `legalPageURL` | URL to the legal attribution web page |
| `legalAttributionText` | Text alternative when a web view is not feasible |
| `serviceName` | Weather data provider name |

## Availability

Check which weather datasets are available for a given location. Not all datasets
are available in all countries.

```swift
func checkAvailability(for location: CLLocation) async throws {
    let availability = try await weatherService.weather(
        for: location,
        including: .availability
    )

    // Check specific dataset availability
    if availability.alertAvailability == .available {
        // Safe to fetch alerts
    }

    if availability.minuteAvailability == .available {
        // Minute forecast available for this region
    }
}
```

## Common Mistakes

### DON'T: Ship without Apple Weather attribution

Omitting attribution violates the WeatherKit terms of service and risks App Review
rejection.

```swift
// WRONG: Show weather data without attribution
VStack {
    Text("72F, Sunny")
}

// CORRECT: Always include attribution
VStack {
    Text("72F, Sunny")
    WeatherAttributionView(attribution: attribution)
}
```

### DON'T: Fetch all datasets when you only need current conditions

Each dataset query counts against your API quota. Fetch only what you display.

```swift
// WRONG: Fetches everything
let weather = try await weatherService.weather(for: location)
let temp = weather.currentWeather.temperature

// CORRECT: Fetch only current conditions
let current = try await weatherService.weather(
    for: location,
    including: .current
)
let temp = current.temperature
```

### DON'T: Ignore minute forecast unavailability

Minute forecasts return `nil` in unsupported regions. Force-unwrapping crashes.

```swift
// WRONG: Force-unwrap minute forecast
let minutes = try await weatherService.weather(for: location, including: .minute)
for m in minutes! { ... } // Crash in unsupported regions

// CORRECT: Handle nil
if let minutes = try await weatherService.weather(for: location, including: .minute) {
    for m in minutes { ... }
} else {
    // Minute forecast not available for this region
}
```

### DON'T: Forget the WeatherKit entitlement

Without the capability enabled, `WeatherService` calls throw at runtime.

```swift
// WRONG: No WeatherKit capability configured
let weather = try await weatherService.weather(for: location) // Throws

// CORRECT: Enable WeatherKit in Xcode Signing & Capabilities
// and in the Apple Developer portal for your App ID
```

### DON'T: Make repeated requests without caching

Weather data updates every few minutes, not every second. Cache responses
to stay within API quotas and improve performance.

```swift
// WRONG: Fetch on every view appearance
.task {
    let weather = try? await fetchWeather()
}

// CORRECT: Cache with a staleness interval
actor WeatherCache {
    private var cached: CurrentWeather?
    private var lastFetch: Date?

    func current(for location: CLLocation) async throws -> CurrentWeather {
        if let cached, let lastFetch,
           Date.now.timeIntervalSince(lastFetch) < 600 {
            return cached
        }
        let fresh = try await WeatherService.shared.weather(
            for: location, including: .current
        )
        cached = fresh
        lastFetch = .now
        return fresh
    }
}
```

## Review Checklist

- [ ] WeatherKit capability enabled in Xcode and Apple Developer portal
- [ ] Active Apple Developer Program membership (required for WeatherKit)
- [ ] Apple Weather attribution displayed wherever weather data appears
- [ ] Attribution mark uses correct color scheme variant (light/dark)
- [ ] Legal attribution page linked or `legalAttributionText` displayed
- [ ] Only needed `WeatherQuery` datasets fetched (not full `weather(for:)` when unnecessary)
- [ ] Minute forecast handled as optional (nil in unsupported regions)
- [ ] Weather alerts checked for nil before iteration
- [ ] Responses cached with a reasonable staleness interval (5-15 minutes)
- [ ] `WeatherAvailability` checked before fetching region-limited datasets
- [ ] Location permission requested before passing `CLLocation` to service
- [ ] Temperature and measurements formatted with `Measurement.formatted()` for locale

## References

- Extended patterns (SwiftUI dashboard, charts integration, historical statistics): `references/weatherkit-patterns.md`
- [WeatherKit framework](https://sosumi.ai/documentation/weatherkit)
- [WeatherService](https://sosumi.ai/documentation/weatherkit/weatherservice)
- [WeatherAttribution](https://sosumi.ai/documentation/weatherkit/weatherattribution)
- [WeatherQuery](https://sosumi.ai/documentation/weatherkit/weatherquery)
- [CurrentWeather](https://sosumi.ai/documentation/weatherkit/currentweather)
- [Forecast](https://sosumi.ai/documentation/weatherkit/forecast)
- [HourWeather](https://sosumi.ai/documentation/weatherkit/hourweather)
- [DayWeather](https://sosumi.ai/documentation/weatherkit/dayweather)
- [WeatherAlert](https://sosumi.ai/documentation/weatherkit/weatheralert)
- [WeatherAvailability](https://sosumi.ai/documentation/weatherkit/weatheravailability)
- [Fetching weather forecasts with WeatherKit](https://sosumi.ai/documentation/weatherkit/fetching_weather_forecasts_with_weatherkit)
