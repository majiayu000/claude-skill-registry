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
