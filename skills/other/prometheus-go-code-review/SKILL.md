---
name: prometheus-go-code-review
description: Reviews Prometheus instrumentation in Go code for proper metric types, labels, and patterns. Use when reviewing code with prometheus/client_golang metrics.
---

# Prometheus Go Code Review

## Review Checklist

- [ ] Metric types match measurement semantics (Counter/Gauge/Histogram)
- [ ] Labels have low cardinality (no user IDs, timestamps, paths)
- [ ] Metric names follow conventions (snake_case, unit suffix)
- [ ] Histograms use appropriate bucket boundaries
- [ ] Metrics registered once, not per-request
- [ ] Collectors don't panic on race conditions
- [ ] /metrics endpoint exposed and accessible

## Hard gates (sequenced)

Complete in order before recording a **finding**. Skip gates that clearly do not apply to the diff.

1. **Evidence scope** — Enumerate the files you are reviewing that touch Prometheus (`prometheus/client_golang`, `promauto`, `promhttp`, or `MustRegister`). **Pass:** you have a concrete path list (from the diff or an explicit file set); no repo-wide claim without at least one path.

2. **Label cardinality** — For each `*Vec` or labeled metric in scope, list label names and where values come from (constants, bounded codes, vs request-derived strings). **Pass:** no label uses unbounded values (e.g. raw `user_id`, full URL path, timestamps) unless the code uses a bounded mapping and you cite it.

3. **Registration lifecycle** — For metric definitions in scope, confirm constructors run once (package-level `var`, `init`, or `sync.Once`), not inside per-request handlers. **Pass:** no pattern that allocates/registers a new `Counter`/`Histogram`/`*Vec` on every request for the same logical metric.

4. **Finding shape** — Each finding names a file (and line or symbol where possible), states which gate (2 or 3) would fail if the issue is real, and ties to observed code. **Pass:** no standalone style nit when gates 2–3 are satisfied for that code.

## Metric Type Selection

| Measurement | Type | Example |
|-------------|------|---------|
| Requests processed | Counter | `requests_total` |
| Items in queue | Gauge | `queue_length` |
| Request duration | Histogram | `request_duration_seconds` |
| Concurrent connections | Gauge | `active_connections` |
| Errors since start | Counter | `errors_total` |
| Memory usage | Gauge | `memory_bytes` |

## Critical Anti-Patterns

### 1. High Cardinality Labels

```go
// BAD - unique per user/request
counter := promauto.NewCounterVec(
    prometheus.CounterOpts{Name: "requests_total"},
    []string{"user_id", "path"},  // millions of series!
)
counter.WithLabelValues(userID, request.URL.Path).Inc()

// GOOD - bounded label values
counter := promauto.NewCounterVec(
    prometheus.CounterOpts{Name: "requests_total"},
    []string{"method", "status_code"},  // <100 series
)
counter.WithLabelValues(r.Method, statusCode).Inc()
```

### 2. Wrong Metric Type

```go
// BAD - using gauge for monotonic value
requestCount := promauto.NewGauge(prometheus.GaugeOpts{
    Name: "http_requests",
})
requestCount.Inc()  // should be Counter!

// GOOD
requestCount := promauto.NewCounter(prometheus.CounterOpts{
    Name: "http_requests_total",
})
requestCount.Inc()
```

### 3. Registering Per-Request

```go
// BAD - new metric per request
func handler(w http.ResponseWriter, r *http.Request) {
    counter := prometheus.NewCounter(...)  // creates new each time!
    prometheus.MustRegister(counter)       // panics on duplicate!
}

// GOOD - register once
var requestCounter = promauto.NewCounter(prometheus.CounterOpts{
    Name: "http_requests_total",
})

func handler(w http.ResponseWriter, r *http.Request) {
    requestCounter.Inc()
}
```

### 4. Missing Unit Suffix

```go
// BAD
duration := promauto.NewHistogram(prometheus.HistogramOpts{
    Name: "request_duration",  // no unit!
})

// GOOD
duration := promauto.NewHistogram(prometheus.HistogramOpts{
    Name: "request_duration_seconds",  // unit in name
})
```

## Good Patterns

### Metric Definition

```go
var (
    httpRequests = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Namespace: "myapp",
            Subsystem: "http",
            Name:      "requests_total",
            Help:      "Total HTTP requests processed",
        },
        []string{"method", "status"},
    )

    httpDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Namespace: "myapp",
            Subsystem: "http",
            Name:      "request_duration_seconds",
            Help:      "HTTP request latencies",
            Buckets:   []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
        },
        []string{"method"},
    )
)
```

### Middleware Pattern

```go
func metricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        timer := prometheus.NewTimer(httpDuration.WithLabelValues(r.Method))
        defer timer.ObserveDuration()

        wrapped := &responseWriter{ResponseWriter: w, status: 200}
        next.ServeHTTP(wrapped, r)

        httpRequests.WithLabelValues(r.Method, strconv.Itoa(wrapped.status)).Inc()
    })
}
```

### Exposing Metrics

```go
import "github.com/prometheus/client_golang/prometheus/promhttp"

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.ListenAndServe(":9090", nil)
}
```

## Review Questions

1. Are metric types correct (Counter vs Gauge vs Histogram)?
2. Are label values bounded (no UUIDs, timestamps, paths)?
3. Do metric names include units (_seconds, _bytes)?
4. Are metrics registered once (not per-request)?
5. Is /metrics endpoint properly exposed?
