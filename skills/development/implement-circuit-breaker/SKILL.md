---
name: implement-circuit-breaker
description: "Step-by-step guide for implementing circuit breakers to protect against unstable dependencies following resilience patterns."
---

# Skill: Implement Circuit Breaker

This skill teaches you how to implement circuit breakers following  resilience patterns. You'll learn to protect your services from cascading failures by detecting unhealthy dependencies and failing fast when they're unavailable.

Circuit breakers are essential for building resilient distributed systems. When a dependency becomes slow or unresponsive, continuing to call it wastes resources and delays failure detection. A circuit breaker "opens" after repeated failures, immediately rejecting requests without attempting the call, giving the dependency time to recover.

The pattern follows three states: CLOSED (normal operation), OPEN (fail fast), and HALF-OPEN (testing recovery).

## Prerequisites

- Understanding of distributed system failure modes
- Familiarity with HTTP clients and context timeouts
- A service with external dependencies (APIs, databases, third-party services)
- Basic understanding of Clean Architecture patterns

## Overview

In this skill, you will:
1. Identify dependencies that need circuit breaker protection
2. Configure circuit breaker settings (thresholds, timeouts, intervals)
3. Implement circuit breakers
4. Create fallback strategies for graceful degradation
5. Add observability for circuit state monitoring
6. Test failure scenarios to validate the implementation

## Step 1: Identify Dependencies Needing Protection

Before implementing circuit breakers, analyze your service to identify which dependencies warrant protection. Not every call needs a circuit breaker - focus on external or unreliable dependencies.

### When to Use Circuit Breakers

Circuit breakers are appropriate for:
- External HTTP APIs (weather services, payment providers, third-party integrations)
- Cross-service calls within your system (especially across bounded contexts)
- Database operations on remote or shared databases
- Any dependency with variable latency or availability

Circuit breakers are NOT needed for:
- Local in-memory operations
- Highly reliable local resources (local cache, local file system)
- Operations where immediate retry is always safe and fast

### Dependency Analysis

```pseudocode
// Pattern: Port Interface for External Dependency
// This external dependency is a prime candidate for circuit breaker protection:
// - External API with variable latency
// - Not under our control
// - Non-critical for core functionality (can use cached/fallback data)

INTERFACE WeatherClient
    // GetCurrentWeather fetches current weather for a location
    // May fail due to network issues, API rate limits, or service outages
    METHOD GetCurrentWeather(ctx: Context, locationId: String) RETURNS Result<WeatherReading, Error>
END INTERFACE

TYPE WeatherReading
    temperatureCelsius: Float
    humidity: Float
    timestamp: String
END TYPE

// Dependency Analysis for External Weather API:
//
// Failure Modes:
//   - Network timeouts (2-5% of requests during peak)
//   - API rate limiting (429 responses during high load)
//   - Service outages (occasional multi-minute outages)
//
// Impact of Failure:
//   - Medium: Weather data enhances optimization but is not critical
//   - Can use cached data up to 1 hour old
//   - Can use regional average as fallback
//
// Circuit Breaker Recommendation:
//   - Threshold: 5 failures in 10 seconds
//   - Timeout: 30 seconds in OPEN state
//   - MaxRequests in HALF-OPEN: 3
```

## Step 2: Configure Circuit Breaker Settings

The circuit breaker's effectiveness depends on proper configuration. Configure thresholds based on your dependency's characteristics and your service's requirements.

### Circuit Breaker Settings

```pseudocode
// Pattern: Configuration Value Object
// CircuitBreakerConfig holds configuration for the circuit breaker

TYPE CircuitBreakerConfig
    // Name identifies the circuit breaker in logs and metrics
    name: String

    // MaxRequests is the maximum number of requests allowed in HALF-OPEN state
    // When the circuit is half-open, only this many requests are allowed through
    // to test if the dependency has recovered. If they succeed, circuit closes.
    // If any fail, circuit opens again.
    // Recommended: 1-5 depending on how quickly you want to recover.
    maxRequests: Integer

    // Interval is the cyclic time period for clearing internal counts while CLOSED
    // If set to 0, internal counts are never cleared while CLOSED.
    // This controls the window for counting failures toward the threshold.
    // Recommended: 10-60 seconds for most use cases.
    interval: Duration

    // Timeout is how long the circuit stays OPEN before transitioning to HALF-OPEN
    // After this duration, the circuit breaker allows test requests through.
    // Too short: You'll hammer a recovering dependency.
    // Too long: You'll reject requests longer than necessary.
    // Recommended: 15-60 seconds depending on expected recovery time.
    timeout: Duration

    // FailureThreshold is the number of failures that triggers OPEN state
    failureThreshold: Integer

    // SuccessThreshold is successes needed to close circuit from HALF-OPEN
    successThreshold: Integer
END TYPE

// Pattern: Factory Function with Sensible Defaults
FUNCTION DefaultWeatherConfig() RETURNS CircuitBreakerConfig
    RETURN CircuitBreakerConfig{
        name: "weather-api",
        maxRequests: 3,                     // Allow 3 test requests in half-open
        interval: 10 * Seconds,             // Count failures over 10-second windows
        timeout: 30 * Seconds,              // Stay open for 30 seconds
        failureThreshold: 5,                // Open after 5 failures
        successThreshold: 3                 // Need 3 successes to close
    }
END FUNCTION
```

### Create the Circuit Breaker

```pseudocode
// Pattern: State Machine Pattern
// CircuitState represents the three states

TYPE CircuitState
    CONSTANT Closed = "CLOSED"
    CONSTANT Open = "OPEN"
    CONSTANT HalfOpen = "HALF_OPEN"
END TYPE

// Pattern: Statistics Tracking
// Counts tracks request statistics

TYPE Counts
    requests: Integer
    totalSuccesses: Integer
    totalFailures: Integer
    consecutiveSuccesses: Integer
    consecutiveFailures: Integer
END TYPE

// Pattern: Circuit Breaker Core Implementation
TYPE CircuitBreaker
    name: String
    config: CircuitBreakerConfig
    state: CircuitState
    counts: Counts
    expiry: Timestamp
    mutex: Mutex
END TYPE

CONSTRUCTOR NewCircuitBreaker(config: CircuitBreakerConfig) RETURNS CircuitBreaker
    RETURN CircuitBreaker{
        name: config.name,
        config: config,
        state: CircuitState.Closed,
        counts: Counts{},
        expiry: Timestamp.Zero(),
        mutex: Mutex.New()
    }
END CONSTRUCTOR

// Pattern: Execute with Protection
METHOD CircuitBreaker.Execute<T>(operation: Function<Result<T, Error>>) RETURNS Result<T, Error>
    this.mutex.Lock()

    // Check if we should allow this request
    IF NOT this.allowRequest() THEN
        this.mutex.Unlock()
        RETURN Error(ErrCircuitOpen)
    END IF

    this.mutex.Unlock()

    // Execute the operation
    result = operation()

    this.mutex.Lock()
    this.recordResult(result.IsOk())
    this.mutex.Unlock()

    RETURN result
END METHOD

METHOD CircuitBreaker.allowRequest() RETURNS Boolean
    now = CurrentTimestamp()

    MATCH this.state
        CASE CircuitState.Closed:
            RETURN true
        CASE CircuitState.Open:
            IF now.After(this.expiry) THEN
                this.toHalfOpen()
                RETURN true
            END IF
            RETURN false
        CASE CircuitState.HalfOpen:
            RETURN this.counts.requests < this.config.maxRequests
    END MATCH

    RETURN false
END METHOD

METHOD CircuitBreaker.recordResult(success: Boolean)
    this.counts.requests = this.counts.requests + 1

    IF success THEN
        this.counts.totalSuccesses = this.counts.totalSuccesses + 1
        this.counts.consecutiveSuccesses = this.counts.consecutiveSuccesses + 1
        this.counts.consecutiveFailures = 0

        IF this.state == CircuitState.HalfOpen AND
           this.counts.consecutiveSuccesses >= this.config.successThreshold THEN
            this.toClosed()
        END IF
    ELSE
        this.counts.totalFailures = this.counts.totalFailures + 1
        this.counts.consecutiveFailures = this.counts.consecutiveFailures + 1
        this.counts.consecutiveSuccesses = 0

        IF this.shouldTrip() THEN
            this.toOpen()
        END IF
    END IF
END METHOD

METHOD CircuitBreaker.shouldTrip() RETURNS Boolean
    IF this.state == CircuitState.HalfOpen THEN
        RETURN true
    END IF

    failureRatio = this.counts.totalFailures / this.counts.requests
    thresholdExceeded = this.counts.consecutiveFailures >= this.config.failureThreshold

    // Open if we have enough samples and high failure ratio
    // OR if we hit consecutive failure threshold
    IF this.counts.requests >= 5 AND failureRatio >= 0.5 THEN
        RETURN true
    END IF

    RETURN thresholdExceeded
END METHOD

// Pattern: State Transitions with Logging
METHOD CircuitBreaker.toOpen()
    this.state = CircuitState.Open
    this.expiry = CurrentTimestamp().Add(this.config.timeout)
    this.counts = Counts{}
    Logger.Warn("circuit breaker opened", "name", this.name)
END METHOD

METHOD CircuitBreaker.toHalfOpen()
    this.state = CircuitState.HalfOpen
    this.counts = Counts{}
    Logger.Info("circuit breaker half-open", "name", this.name)
END METHOD

METHOD CircuitBreaker.toClosed()
    this.state = CircuitState.Closed
    this.counts = Counts{}
    Logger.Info("circuit breaker closed", "name", this.name)
END METHOD

METHOD CircuitBreaker.State() RETURNS CircuitState
    RETURN this.state
END METHOD

METHOD CircuitBreaker.Counts() RETURNS Counts
    RETURN this.counts
END METHOD

// Error for open circuit
CONSTANT ErrCircuitOpen = Error("circuit breaker is open")
```

## Step 3: Implement Circuit Breaker with HTTP Client

Wrap your external client with the circuit breaker.

```pseudocode
// Pattern: Adapter with Circuit Breaker Protection
// Client implements WeatherClient with circuit breaker protection

TYPE Client
    httpClient: HTTPClient
    baseURL: String
    cb: CircuitBreaker
    logger: Logger
END TYPE

CONSTRUCTOR NewClient(baseURL: String, config: CircuitBreakerConfig, logger: Logger) RETURNS Client
    RETURN Client{
        httpClient: HTTPClient{timeout: 5 * Seconds},
        baseURL: baseURL,
        cb: NewCircuitBreaker(config),
        logger: logger
    }
END CONSTRUCTOR

// GetCurrentWeather fetches weather data, protected by circuit breaker
METHOD Client.GetCurrentWeather(ctx: Context, locationId: String) RETURNS Result<WeatherReading, Error>
    // Execute request through circuit breaker
    // If circuit is OPEN, this returns immediately with ErrCircuitOpen
    // If circuit is CLOSED or HALF-OPEN, the function is executed
    result = this.cb.Execute(FUNCTION() RETURNS Result<WeatherReading, Error>
        RETURN this.doRequest(ctx, locationId)
    END FUNCTION)

    IF result.IsError() THEN
        // Check if error is due to open circuit
        IF result.Error() == ErrCircuitOpen THEN
            this.logger.Warn("circuit breaker is open, request rejected",
                "location_id", locationId
            )
            RETURN Error("weather service unavailable: " + result.Error())
        END IF
        RETURN Error("weather request failed: " + result.Error())
    END IF

    RETURN result
END METHOD

// doRequest performs the actual HTTP request to the weather API
METHOD Client.doRequest(ctx: Context, locationId: String) RETURNS Result<WeatherReading, Error>
    url = this.baseURL + "/weather/" + locationId

    response = this.httpClient.GET(ctx, url)
    IF response.IsError() THEN
        RETURN Error("http request failed: " + response.Error())
    END IF

    IF response.StatusCode != 200 THEN
        RETURN Error("unexpected status code: " + ToString(response.StatusCode))
    END IF

    reading = DeserializeJSON<WeatherReading>(response.Body)
    RETURN Ok(reading)
END METHOD

METHOD Client.State() RETURNS CircuitState
    RETURN this.cb.State()
END METHOD

METHOD Client.Counts() RETURNS Counts
    RETURN this.cb.Counts()
END METHOD
```

The circuit breaker wraps the HTTP call, so:
- When CLOSED: Requests pass through normally
- When OPEN: Requests fail immediately with `ErrCircuitOpen`
- When HALF-OPEN: Limited requests pass through to test recovery

## Step 4: Add Fallback Strategies

When the circuit is open, provide graceful degradation instead of just failing. Fallback strategies maintain partial functionality during outages.

```pseudocode
// Pattern: Graceful Degradation with Fallback Chain
// ErrNoFallbackAvailable indicates no cached or default data is available

CONSTANT ErrNoFallbackAvailable = Error("no fallback data available")

// Pattern: Decorator with Fallback
// FallbackClient wraps the circuit breaker client with fallback strategies

TYPE FallbackClient
    primary: Client
    cache: WeatherCache
    logger: Logger
    defaultReading: WeatherReading
END TYPE

// Pattern: Cache with TTL
// WeatherCache stores recent weather readings for fallback

TYPE WeatherCache
    readings: Map<String, CachedReading>
    maxAge: Duration
    mutex: RWMutex
END TYPE

TYPE CachedReading
    data: WeatherReading
    fetchedAt: Timestamp
END TYPE

CONSTRUCTOR NewFallbackClient(primary: Client, cacheMaxAge: Duration, defaultTemp: Float, logger: Logger) RETURNS FallbackClient
    RETURN FallbackClient{
        primary: primary,
        cache: WeatherCache{
            readings: {},
            maxAge: cacheMaxAge,
            mutex: RWMutex.New()
        },
        logger: logger,
        defaultReading: WeatherReading{
            temperatureCelsius: defaultTemp,
            humidity: 50.0,
            timestamp: "fallback-default"
        }
    }
END CONSTRUCTOR

// Pattern: Fallback Chain (Primary -> Cache -> Default)
// GetCurrentWeather attempts primary, then cache, then default fallback
METHOD FallbackClient.GetCurrentWeather(ctx: Context, locationId: String) RETURNS Result<WeatherReading, Error>
    // Strategy 1: Try the primary circuit-breaker-protected client
    readingResult = this.primary.GetCurrentWeather(ctx, locationId)
    IF readingResult.IsOk() THEN
        // Success: update cache and return
        this.cache.Set(locationId, readingResult.Value())
        RETURN readingResult
    END IF

    this.logger.Warn("primary weather request failed, trying fallback",
        "location_id", locationId,
        "error", readingResult.Error()
    )

    // Strategy 2: Try cached data (if not too stale)
    cachedResult = this.cache.Get(locationId)
    IF cachedResult.IsOk() THEN
        this.logger.Info("using cached weather data",
            "location_id", locationId,
            "cached_at", cachedResult.Value().timestamp
        )
        RETURN cachedResult
    END IF

    // Strategy 3: Check if this is a circuit breaker rejection
    IF readingResult.Error() == ErrCircuitOpen THEN
        // Circuit is open - dependency is known to be unhealthy
        // Return default reading to allow system to continue functioning
        this.logger.Warn("circuit open, using default weather reading",
            "location_id", locationId
        )
        RETURN Ok(this.defaultReading)
    END IF

    // All strategies exhausted
    RETURN Error("all weather strategies failed: " + readingResult.Error())
END METHOD

METHOD WeatherCache.Set(locationId: String, reading: WeatherReading)
    this.mutex.Lock()
    this.readings[locationId] = CachedReading{
        data: reading,
        fetchedAt: CurrentTimestamp()
    }
    this.mutex.Unlock()
END METHOD

METHOD WeatherCache.Get(locationId: String) RETURNS Result<WeatherReading, Error>
    this.mutex.RLock()
    cached = this.readings[locationId]
    this.mutex.RUnlock()

    IF cached == NULL THEN
        RETURN Error("not cached")
    END IF

    // Check if cached data is too stale
    IF CurrentTimestamp().Sub(cached.fetchedAt) > this.maxAge THEN
        RETURN Error("cache expired")
    END IF

    RETURN Ok(cached.data)
END METHOD
```

### Fallback Strategy Guidelines

The fallback approach should match business requirements:

- **Cache fallback**: Use recently fetched data (appropriate when stale data is acceptable)
- **Default values**: Use sensible defaults (appropriate for non-critical features)
- **Degraded response**: Return partial data or indicate degraded mode to caller
- **Alternative source**: Try a backup API or secondary data source

## Step 5: Monitor Circuit State

Observability is critical for circuit breakers. You need to know when circuits open, how often they trip, and how long recovery takes.

```pseudocode
// Pattern: Metrics Port Interface
// Metrics defines the interface for circuit breaker observability

INTERFACE Metrics
    // RecordStateChange records when circuit state changes
    METHOD RecordStateChange(name: String, from: String, to: String)

    // RecordRequest records a request through the circuit breaker
    METHOD RecordRequest(name: String, success: Boolean, duration: Duration)

    // RecordFallbackUsed records when a fallback strategy was used
    METHOD RecordFallbackUsed(name: String, strategy: String)
END INTERFACE

// Pattern: Decorator for Observability
// InstrumentedClient adds metrics to the fallback client

TYPE InstrumentedClient
    fallbackClient: FallbackClient
    metrics: Metrics
    name: String
END TYPE

CONSTRUCTOR NewInstrumentedClient(client: FallbackClient, metrics: Metrics, name: String) RETURNS InstrumentedClient
    RETURN InstrumentedClient{
        fallbackClient: client,
        metrics: metrics,
        name: name
    }
END CONSTRUCTOR

// GetCurrentWeather with instrumentation
METHOD InstrumentedClient.GetCurrentWeather(ctx: Context, locationId: String) RETURNS Result<WeatherReading, Error>
    start = CurrentTimestamp()

    readingResult = this.fallbackClient.GetCurrentWeather(ctx, locationId)

    duration = CurrentTimestamp().Sub(start)
    success = readingResult.IsOk()

    this.metrics.RecordRequest(this.name, success, duration)

    // Track if we used a fallback (check if timestamp indicates fallback)
    IF readingResult.IsOk() AND readingResult.Value().timestamp == "fallback-default" THEN
        this.metrics.RecordFallbackUsed(this.name, "default")
    END IF

    RETURN readingResult
END METHOD
```

## Step 6: Test Failure Scenarios

Validate your circuit breaker implementation with comprehensive tests that simulate various failure modes.

```pseudocode
// Pattern: Unit Test for State Transitions
// Test: Circuit opens after failures

TEST CircuitBreaker_OpensAfterFailures
    // Create a server that always fails
    failCount = 0
    server = MockServer(FUNCTION(request) RETURNS Response
        failCount = failCount + 1
        RETURN Response{statusCode: 500}
    END FUNCTION)

    config = CircuitBreakerConfig{
        name: "test-breaker",
        maxRequests: 1,
        interval: 1 * Second,
        timeout: 5 * Seconds,
        failureThreshold: 3
    }

    client = NewClient(server.URL, config, TestLogger)

    // Make requests until circuit opens
    ctx = Context.Background()
    FOR i = 0; i < 5; i++ DO
        client.GetCurrentWeather(ctx, "loc-1")
    END FOR

    // Verify circuit is now open
    ASSERT client.State() == CircuitState.Open

    // Verify requests are rejected immediately
    result = client.GetCurrentWeather(ctx, "loc-1")
    ASSERT result.Error() == ErrCircuitOpen

    // Verify server wasn't called after circuit opened
    // (should be 3-5 calls, not more)
    ASSERT failCount <= 5
END TEST

// Pattern: Recovery Test
// Test: Circuit recovers through half-open

TEST CircuitBreaker_RecoversThroughHalfOpen
    // Create a server that fails initially, then recovers
    callCount = 0
    recovered = false

    server = MockServer(FUNCTION(request) RETURNS Response
        callCount = callCount + 1
        IF NOT recovered THEN
            RETURN Response{statusCode: 500}
        END IF
        RETURN Response{
            statusCode: 200,
            body: '{"temperature_celsius": 20.5, "humidity": 65.0}'
        }
    END FUNCTION)

    config = CircuitBreakerConfig{
        name: "test-breaker",
        maxRequests: 1,
        interval: 1 * Second,
        timeout: 100 * Milliseconds,    // Short timeout for testing
        failureThreshold: 2
    }

    client = NewClient(server.URL, config, TestLogger)
    ctx = Context.Background()

    // Trigger circuit open
    FOR i = 0; i < 3; i++ DO
        client.GetCurrentWeather(ctx, "loc-1")
    END FOR

    ASSERT client.State() == CircuitState.Open

    // Simulate recovery
    recovered = true

    // Wait for timeout to transition to half-open
    Sleep(150 * Milliseconds)

    // Next request should go through and succeed
    readingResult = client.GetCurrentWeather(ctx, "loc-1")
    ASSERT readingResult.IsOk()
    ASSERT readingResult.Value().temperatureCelsius == 20.5

    // Circuit should now be closed
    ASSERT client.State() == CircuitState.Closed
END TEST

// Pattern: Fallback Test
// Test: Fallback uses cache when primary fails

TEST FallbackClient_UsesCacheWhenPrimaryFails
    // Create a server that succeeds once, then fails
    requestCount = 0

    server = MockServer(FUNCTION(request) RETURNS Response
        requestCount = requestCount + 1
        IF requestCount == 1 THEN
            RETURN Response{
                statusCode: 200,
                body: '{"temperature_celsius": 15.0, "humidity": 70.0}'
            }
        END IF
        RETURN Response{statusCode: 500}
    END FUNCTION)

    config = DefaultWeatherConfig()
    config.timeout = 50 * Milliseconds

    primary = NewClient(server.URL, config, TestLogger)
    fallback = NewFallbackClient(primary, 1 * Hour, 10.0, TestLogger)

    ctx = Context.Background()

    // First request succeeds and caches
    reading1Result = fallback.GetCurrentWeather(ctx, "loc-1")
    ASSERT reading1Result.IsOk()
    ASSERT reading1Result.Value().temperatureCelsius == 15.0

    // Second request fails but uses cache
    reading2Result = fallback.GetCurrentWeather(ctx, "loc-1")
    ASSERT reading2Result.IsOk()
    ASSERT reading2Result.Value().temperatureCelsius == 15.0
END TEST

// Pattern: Chaos/Integration Test
// Test: Circuit breaker under chaos

TEST CircuitBreaker_UnderChaos
    totalRequests = 0
    successRequests = 0
    failedRequests = 0

    // Server with 30% failure rate
    server = MockServer(FUNCTION(request) RETURNS Response
        totalRequests = totalRequests + 1
        IF Random() < 0.3 THEN
            failedRequests = failedRequests + 1
            RETURN Response{statusCode: 503}
        END IF
        successRequests = successRequests + 1
        RETURN Response{
            statusCode: 200,
            body: '{"temperature_celsius": 18.0, "humidity": 55.0}'
        }
    END FUNCTION)

    config = CircuitBreakerConfig{
        name: "chaos-test",
        maxRequests: 3,
        interval: 1 * Second,
        timeout: 500 * Milliseconds,
        failureThreshold: 5
    }

    primary = NewClient(server.URL, config, TestLogger)
    client = NewFallbackClient(primary, 10 * Minutes, 20.0, TestLogger)

    ctx = Context.Background()

    // Simulate sustained load
    clientSuccesses = 0
    clientFailures = 0

    FOR i = 0; i < 100; i++ DO
        result = client.GetCurrentWeather(ctx, "loc-1")
        IF result.IsOk() THEN
            clientSuccesses = clientSuccesses + 1
        ELSE
            clientFailures = clientFailures + 1
        END IF
        Sleep(10 * Milliseconds)
    END FOR

    // With fallback, client should succeed most of the time
    successRate = clientSuccesses / (clientSuccesses + clientFailures)
    ASSERT successRate >= 0.9, "expected >90% client success rate with fallback"
END TEST
```

## Verification Checklist

After implementing circuit breakers, verify:

- [ ] Dependencies are analyzed for circuit breaker suitability
- [ ] Circuit breaker settings match dependency characteristics (timeout, threshold, interval)
- [ ] ReadyToTrip function uses appropriate failure threshold logic
- [ ] OnStateChange logs state transitions for observability
- [ ] Fallback strategy provides graceful degradation
- [ ] Cache fallback has appropriate max age
- [ ] Default fallback values are sensible for business logic
- [ ] Metrics are emitted for circuit state changes
- [ ] Metrics are emitted for fallback usage
- [ ] Unit tests verify circuit opens after threshold failures
- [ ] Unit tests verify circuit recovers through half-open state
- [ ] Tests verify fallback strategies work correctly
- [ ] No business logic in the circuit breaker adapter (keep it thin)
