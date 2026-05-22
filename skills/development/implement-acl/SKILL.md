---
name: implement-acl
description: "Step-by-step guide for implementing Anti-Corruption Layers to shield your domain from external model pollution."
---

# Skill: Implement Anti-Corruption Layer

This skill teaches you how to implement Anti-Corruption Layers (ACL) following  architectural patterns. You'll learn to protect your domain model from external system pollution by translating external concepts at the boundary.

Anti-Corruption Layers are essential when integrating with external systems (third-party APIs, legacy systems, partner services) whose terminology and data structures differ from yours. Without an ACL, external models leak into your domain, coupling your core business logic to systems you don't control.

The ACL acts as a translator at your bounded context boundary, converting external schemas and concepts into your domain language. This ensures your domain remains clean, testable, and independent of external changes.

## Prerequisites

- Understanding of Clean Architecture and DDD concepts
- Familiarity with hexagonal architecture (ports and adapters)
- An external system to integrate with (API, legacy system, or partner service)
- Domain model already defined for your bounded context

## Overview

In this skill, you will:
1. Identify the external model and its concepts
2. Define your domain model (what you want)
3. Create the translation layer (ACL)
4. Implement the adapter using the ACL
5. Handle external errors and map them to domain errors
6. Test the ACL in isolation

## Step 1: Identify the External Model

Before implementing an ACL, you must understand the external system's data model. This includes studying API responses, data formats, naming conventions, and semantics.

### External API Example: Weather Provider

Consider integrating with a weather forecast provider for energy optimization. Their API returns data in their format:

```pseudocode
// external/weatherapi/types
// These types represent the external API's response format.
// DO NOT use these in your domain layer - they exist only for deserialization.

TYPE ForecastResponse
    location: LocationData
    predictions: List<PredictionData>
    units: String  // "C" or "F"
END TYPE

TYPE LocationData
    lat: Float
    long: Float
END TYPE

// PredictionData represents a single forecast point.
// The provider uses unix timestamps and their own naming conventions.
TYPE PredictionData
    timestamp: Integer      // Unix timestamp
    tempValue: Float        // Temperature in specified unit
    relHumidity: Integer    // 0-100
    cloudCover: Integer     // 0-100
    windSpeedMs: Float      // meters per second
    solarRadWm2: Float      // Global Horizontal Irradiance W/m²
    precipitation: Float    // millimeters
END TYPE
```

Key observations:
- Field names use abbreviated conventions (`ts`, `rh_percent`, `ghi`)
- Temperature unit is dynamic (Celsius or Fahrenheit)
- Timestamps are Unix integers, not structured time
- Semantics may differ (their "solar radiation" vs your "irradiance")

## Step 2: Define Your Domain Model

Define what you need in your domain language. This model should reflect your ubiquitous language, not the external system's terminology.

### Domain Value Objects

```pseudocode
// core/domain/forecast/temperature

CONSTANT ErrInvalidTemperature = "temperature must be between -80 and 60 Celsius"

// Temperature represents a validated temperature in Celsius.
// Always stored in Celsius regardless of source unit.
TYPE Temperature
    celsius: Float
END TYPE

CONSTRUCTOR NewTemperature(celsius: Float) RETURNS Result<Temperature, Error>
    IF celsius < -80 OR celsius > 60 THEN
        RETURN Error(ErrInvalidTemperature + ": got " + celsius)
    END IF
    RETURN Ok(Temperature{celsius: celsius})
END CONSTRUCTOR

METHOD Temperature.Celsius() RETURNS Float
    RETURN this.celsius
END METHOD


// core/domain/forecast/irradiance

CONSTANT ErrInvalidIrradiance = "solar irradiance cannot be negative"

// SolarIrradiance represents solar energy in W/m².
// Named using our domain language, not the provider's "GHI" term.
TYPE SolarIrradiance
    wattsPerM2: Float
END TYPE

CONSTRUCTOR NewSolarIrradiance(wattsPerM2: Float) RETURNS Result<SolarIrradiance, Error>
    IF wattsPerM2 < 0 THEN
        RETURN Error(ErrInvalidIrradiance + ": got " + wattsPerM2)
    END IF
    RETURN Ok(SolarIrradiance{wattsPerM2: wattsPerM2})
END CONSTRUCTOR

METHOD SolarIrradiance.WattsPerSquareMeter() RETURNS Float
    RETURN this.wattsPerM2
END METHOD
```

### Domain Aggregate

```pseudocode
// core/domain/forecast/weather_forecast

// WeatherForecast is our domain representation of forecast data.
// Uses our terminology, validated value objects, and domain time handling.
TYPE WeatherForecast
    validAt: DateTime
    temperature: Temperature
    humidity: Percentage
    cloudCover: Percentage
    irradiance: SolarIrradiance
    windSpeed: WindSpeed
END TYPE

CONSTRUCTOR NewWeatherForecast(
    validAt: DateTime,
    temp: Temperature,
    humidity: Percentage,
    cloudCover: Percentage,
    irradiance: SolarIrradiance,
    windSpeed: WindSpeed
) RETURNS WeatherForecast
    RETURN WeatherForecast{
        validAt: validAt,
        temperature: temp,
        humidity: humidity,
        cloudCover: cloudCover,
        irradiance: irradiance,
        windSpeed: windSpeed
    }
END CONSTRUCTOR

METHOD WeatherForecast.ValidAt() RETURNS DateTime
    RETURN this.validAt
END METHOD

METHOD WeatherForecast.Temperature() RETURNS Temperature
    RETURN this.temperature
END METHOD

METHOD WeatherForecast.SolarIrradiance() RETURNS SolarIrradiance
    RETURN this.irradiance
END METHOD

// IsGoodForSolarProduction indicates if conditions favor solar production.
// Business logic lives in domain, using domain concepts.
METHOD WeatherForecast.IsGoodForSolarProduction() RETURNS Boolean
    RETURN this.irradiance.WattsPerSquareMeter() > 200 AND
           this.cloudCover.Value() < 50
END METHOD
```

The domain model uses your ubiquitous language. Notice:
- `SolarIrradiance` instead of `GHI`
- `ValidAt` instead of `Timestamp`
- Business methods like `IsGoodForSolarProduction()` operate on domain concepts

## Step 3: Create the Translation Layer (ACL)

The ACL is responsible for translating external concepts to domain concepts. It lives in the adapters layer and contains all the mapping logic.

### ACL Interface

```pseudocode
// adapters/weather/acl

// ForecastACL translates external weather API responses to domain forecasts.
// This is the Anti-Corruption Layer - it shields the domain from external models.
TYPE ForecastACL
END TYPE

CONSTRUCTOR NewForecastACL() RETURNS ForecastACL
    RETURN ForecastACL{}
END CONSTRUCTOR
```

### Temperature Translation with Unit Conversion

```pseudocode
// adapters/weather/acl (continued)

// translateTemperature converts external temperature to domain Temperature.
// Handles unit conversion (Fahrenheit to Celsius if needed).
METHOD ForecastACL.translateTemperature(value: Float, unit: String) RETURNS Result<Temperature, Error>
    celsius: Float

    SWITCH unit
        CASE "F":
            // Convert Fahrenheit to Celsius: (F - 32) * 5/9
            celsius = (value - 32) * 5 / 9
        CASE "C":
            celsius = value
        DEFAULT:
            // Assume Celsius for unknown units, log warning in production
            celsius = value
    END SWITCH

    RETURN NewTemperature(celsius)
END METHOD
```

### Full Forecast Translation

```pseudocode
// adapters/weather/acl (continued)

// ToDomainForecasts translates the entire API response to domain forecasts.
// This is the main ACL method - external types go in, domain types come out.
METHOD ForecastACL.ToDomainForecasts(resp: ForecastResponse) RETURNS Result<List<WeatherForecast>, Error>
    forecasts = NEW List<WeatherForecast>()

    FOR EACH pred IN resp.predictions DO
        domainForecast = this.translatePrediction(pred, resp.units)
        IF domainForecast.IsError() THEN
            // Skip invalid predictions but log for observability
            CONTINUE
        END IF
        forecasts.Add(domainForecast.Value())
    END FOR

    IF forecasts.IsEmpty() THEN
        RETURN Error("no valid forecasts in response")
    END IF

    RETURN Ok(forecasts)
END METHOD

// translatePrediction converts a single prediction to domain model.
METHOD ForecastACL.translatePrediction(pred: PredictionData, unit: String) RETURNS Result<WeatherForecast, Error>
    // Translate timestamp: external uses Unix seconds, domain uses DateTime
    validAt = DateTime.FromUnixSeconds(pred.timestamp).ToUTC()

    // Translate temperature with unit conversion
    temp = this.translateTemperature(pred.tempValue, unit)
    IF temp.IsError() THEN
        RETURN Error("invalid temperature: " + temp.Error())
    END IF

    // Translate humidity: external uses int percent, domain uses Percentage value object
    humidity = NewPercentage(pred.relHumidity)
    IF humidity.IsError() THEN
        RETURN Error("invalid humidity: " + humidity.Error())
    END IF

    // Translate cloud cover
    cloudCover = NewPercentage(pred.cloudCover)
    IF cloudCover.IsError() THEN
        RETURN Error("invalid cloud cover: " + cloudCover.Error())
    END IF

    // Translate irradiance: external calls it "ghi", domain calls it SolarIrradiance
    irradiance = NewSolarIrradiance(pred.solarRadWm2)
    IF irradiance.IsError() THEN
        RETURN Error("invalid irradiance: " + irradiance.Error())
    END IF

    // Translate wind speed: external uses m/s, domain may use different unit
    windSpeed = NewWindSpeed(pred.windSpeedMs)
    IF windSpeed.IsError() THEN
        RETURN Error("invalid wind speed: " + windSpeed.Error())
    END IF

    RETURN Ok(NewWeatherForecast(
        validAt,
        temp.Value(),
        humidity.Value(),
        cloudCover.Value(),
        irradiance.Value(),
        windSpeed.Value()
    ))
END METHOD
```

Key ACL responsibilities:
- **Unit conversion**: Fahrenheit to Celsius
- **Type transformation**: Unix timestamp to `DateTime`
- **Naming translation**: `ghi` to `SolarIrradiance`
- **Validation**: Creating validated value objects
- **Semantic mapping**: External meanings to domain meanings

## Step 4: Implement the Adapter with ACL

The adapter uses the ACL to translate external API calls into domain operations. The adapter handles HTTP/networking; the ACL handles translation.

### Repository Port (Domain Layer)

```pseudocode
// core/domain/forecast/repository

// ForecastProvider is the port for obtaining weather forecasts.
// Defined in domain layer - implementations live in adapters.
INTERFACE ForecastProvider
    // GetForecast returns forecasts for a location and time range.
    // Parameters use domain concepts, not external API concepts.
    METHOD GetForecast(ctx: Context, lat: Float, lon: Float, from: DateTime, to: DateTime) RETURNS Result<List<WeatherForecast>, Error>
END INTERFACE
```

### Adapter Implementation

```pseudocode
// adapters/weather/provider

// WeatherAPIProvider implements ForecastProvider using the external API.
// It uses the ACL to translate responses to domain model.
TYPE WeatherAPIProvider
    httpClient: HttpClient
    baseURL: String
    apiKey: String
    acl: ForecastACL
END TYPE

CONSTRUCTOR NewWeatherAPIProvider(baseURL: String, apiKey: String) RETURNS WeatherAPIProvider
    RETURN WeatherAPIProvider{
        httpClient: NewHttpClient(timeout: 10 seconds),
        baseURL: baseURL,
        apiKey: apiKey,
        acl: NewForecastACL()
    }
END CONSTRUCTOR

// GetForecast fetches forecasts and translates them through the ACL.
METHOD WeatherAPIProvider.GetForecast(
    ctx: Context,
    lat: Float,
    lon: Float,
    from: DateTime,
    to: DateTime
) RETURNS Result<List<WeatherForecast>, Error>
    // Build external API request (using their parameter names)
    url = this.baseURL + "/forecast" +
          "?latitude=" + lat +
          "&longitude=" + lon +
          "&start_ts=" + from.ToUnixSeconds() +
          "&end_ts=" + to.ToUnixSeconds()

    request = NewHttpRequest(ctx, "GET", url)
    request.SetHeader("X-API-Key", this.apiKey)

    // Execute request
    response = this.httpClient.Do(request)
    IF response.IsError() THEN
        RETURN Error("failed to fetch forecast: " + response.Error())
    END IF
    DEFER response.Body.Close()

    // Handle external API errors (before ACL)
    IF response.StatusCode != 200 THEN
        RETURN this.translateHTTPError(response.StatusCode)
    END IF

    // Deserialize external response
    externalResp = Deserialize<ForecastResponse>(response.Body)
    IF externalResp.IsError() THEN
        RETURN Error("failed to decode response: " + externalResp.Error())
    END IF

    // ACL translates external response to domain model
    // This is where the anti-corruption happens
    domainForecasts = this.acl.ToDomainForecasts(externalResp.Value())
    IF domainForecasts.IsError() THEN
        RETURN Error("failed to translate forecast: " + domainForecasts.Error())
    END IF

    RETURN Ok(domainForecasts.Value())
END METHOD
```

Notice the clear separation:
- Adapter handles HTTP, authentication, serialization
- ACL handles translation to domain model
- Domain types never see external types

## Step 5: Handle External Errors

External systems have their own error codes and messages. The ACL should translate these to domain errors.

### Domain Errors

```pseudocode
// core/domain/forecast/errors

CONSTANT ErrForecastNotAvailable = "forecast not available for requested period"
CONSTANT ErrLocationNotSupported = "location not supported by forecast provider"
CONSTANT ErrProviderUnavailable = "forecast provider temporarily unavailable"
CONSTANT ErrProviderRateLimited = "forecast provider rate limit exceeded"
```

### Error Translation in Adapter

```pseudocode
// adapters/weather/provider (continued)

// translateHTTPError maps external HTTP errors to domain errors.
// This shields the domain from HTTP status codes and external error formats.
METHOD WeatherAPIProvider.translateHTTPError(statusCode: Integer) RETURNS Error
    SWITCH statusCode
        CASE 404:
            RETURN Error(ErrForecastNotAvailable)
        CASE 400:
            RETURN Error(ErrLocationNotSupported)
        CASE 429:
            RETURN Error(ErrProviderRateLimited)
        CASE 503, 502, 504:
            RETURN Error(ErrProviderUnavailable)
        DEFAULT:
            RETURN Error("unexpected error from forecast provider: status " + statusCode)
    END SWITCH
END METHOD

// translateAPIError maps external API error responses to domain errors.
METHOD WeatherAPIProvider.translateAPIError(apiError: ErrorResponse) RETURNS Error
    // External API uses error codes like "INVALID_LOCATION", "NO_DATA"
    SWITCH apiError.code
        CASE "INVALID_LOCATION", "UNSUPPORTED_REGION":
            RETURN Error(ErrLocationNotSupported)
        CASE "NO_DATA", "FORECAST_UNAVAILABLE":
            RETURN Error(ErrForecastNotAvailable)
        CASE "RATE_LIMIT_EXCEEDED":
            RETURN Error(ErrProviderRateLimited)
        DEFAULT:
            RETURN Error("provider error: " + apiError.message)
    END SWITCH
END METHOD
```

## Step 6: Test the ACL

ACL tests should verify translation logic in isolation, without hitting external services.

### Unit Tests for Temperature Translation

```pseudocode
// adapters/weather/acl_test

TEST ForecastACL_TemperatureConversion
    acl = NewForecastACL()

    testCases = [
        {name: "celsius passthrough", value: 25.0, unit: "C", wantCelsius: 25.0},
        {name: "fahrenheit to celsius", value: 77.0, unit: "F", wantCelsius: 25.0},
        {name: "freezing point fahrenheit", value: 32.0, unit: "F", wantCelsius: 0.0},
        {name: "negative celsius", value: -10.0, unit: "C", wantCelsius: -10.0}
    ]

    FOR EACH tc IN testCases DO
        TEST tc.name
            temp = acl.translateTemperature(tc.value, tc.unit)
            ASSERT temp.IsOk()
            ASSERT temp.Value().Celsius() == tc.wantCelsius
        END TEST
    END FOR
END TEST
```

### Integration Test with Mock External Response

```pseudocode
// adapters/weather/acl_test (continued)

TEST ForecastACL_ToDomainForecasts
    acl = NewForecastACL()

    // Simulate external API response
    externalResp = ForecastResponse{
        location: LocationData{lat: 59.3293, long: 18.0686},
        units: "C",
        predictions: [
            PredictionData{
                timestamp: 1706450400,  // 2024-01-28 14:00:00 UTC
                tempValue: 5.5,
                relHumidity: 75,
                cloudCover: 30,
                windSpeedMs: 3.5,
                solarRadWm2: 250.0,
                precipitation: 0.0
            },
            PredictionData{
                timestamp: 1706454000,  // 2024-01-28 15:00:00 UTC
                tempValue: 4.8,
                relHumidity: 78,
                cloudCover: 45,
                windSpeedMs: 4.2,
                solarRadWm2: 180.0,
                precipitation: 0.5
            }
        ]
    }

    // Translate through ACL
    forecasts = acl.ToDomainForecasts(externalResp)
    ASSERT forecasts.IsOk()

    // Verify domain model
    ASSERT forecasts.Value().Length() == 2

    // Check first forecast uses domain concepts
    first = forecasts.Value()[0]
    ASSERT first.Temperature().Celsius() == 5.5
    ASSERT first.SolarIrradiance().WattsPerSquareMeter() == 250.0

    // Verify domain business logic works
    ASSERT first.IsGoodForSolarProduction() == TRUE  // irradiance 250, cloud 30
    ASSERT forecasts.Value()[1].IsGoodForSolarProduction() == FALSE  // irradiance 180, cloud 45
END TEST
```

### Test Error Translation

```pseudocode
// adapters/weather/provider_test

TEST WeatherAPIProvider_ErrorTranslation
    provider = NewWeatherAPIProvider("http://example.com", "key")

    testCases = [
        {httpStatus: 404, wantError: ErrForecastNotAvailable},
        {httpStatus: 400, wantError: ErrLocationNotSupported},
        {httpStatus: 429, wantError: ErrProviderRateLimited},
        {httpStatus: 503, wantError: ErrProviderUnavailable}
    ]

    FOR EACH tc IN testCases DO
        TEST "HTTP " + tc.httpStatus
            err = provider.translateHTTPError(tc.httpStatus)
            ASSERT err.Message() == tc.wantError
        END TEST
    END FOR
END TEST
```

## Complete ACL File Structure

```
adapters/
  weather/
    acl                    # Translation logic (the ACL itself)
    acl_test               # ACL unit tests
    provider               # Adapter using the ACL
    provider_test          # Adapter tests with mocked HTTP

external/
  weatherapi/
    types                  # External API types (for deserialization only)

core/
  domain/
    forecast/
      errors               # Domain errors
      temperature          # Value objects
      irradiance
      weather_forecast     # Domain model
      repository           # Provider port
```

## Verification Checklist

After implementing your ACL, verify:

- [ ] External types are only used in the adapters layer
- [ ] Domain layer has no imports from external packages
- [ ] ACL handles all unit conversions (temperature, timestamps, etc.)
- [ ] External field names are mapped to domain terminology
- [ ] External semantics are translated to domain semantics
- [ ] Domain value objects validate translated data
- [ ] HTTP/API errors are translated to domain errors
- [ ] ACL can be tested without network access
- [ ] Business logic uses only domain types
- [ ] Changes to external API only affect the ACL and adapter
- [ ] ACL does not contain business logic (only translation)
- [ ] Provider port is defined in the domain layer
