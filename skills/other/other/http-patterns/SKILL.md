---
name: http-patterns
description: HTTP handler patterns for Go 1.22+. Method routing, middleware, graceful shutdown.
---

# HTTP Patterns

Go 1.22+ patterns and project-specific conventions for HTTP handlers.

---

## Go 1.22: ServeMux Method Routing

No more manual method checks. Register with HTTP verb prefix:

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /healthz", healthHandler)
mux.HandleFunc("GET /_cooked/{path...}", assetHandler)
mux.HandleFunc("GET /{upstream...}", renderHandler)
```

### Path Parameters

```go
func renderHandler(w http.ResponseWriter, r *http.Request) {
    upstream := r.PathValue("upstream")  // NEW in Go 1.22
    // ...
}
```

### Special Patterns

| Pattern | Matches |
|---------|---------|
| `/posts/{id}` | `/posts/123` (single segment) |
| `/files/{path...}` | `/files/a/b/c` (remainder of path) |
| `/posts/{$}` | `/posts/` only (not `/posts` or `/posts/x`) |

### Precedence

More specific wins:
- `/healthz` beats `/{upstream...}`
- `GET /posts/{id}` beats `/posts/{id}`

**Conflicting patterns panic at registration:**
```go
mux.HandleFunc("GET /posts/{id}", h1)
mux.HandleFunc("GET /{resource}/latest", h2)  // PANIC - both match /posts/latest
```

### Automatic 405

Unmatched methods return `405 Method Not Allowed` with `Allow` header.

### go.mod Requirement

Go 1.22+ patterns require `go 1.22` or later in `go.mod`. Without it, patterns are treated literally (braces aren't wildcards).

Sources: [Go Blog: Routing Enhancements](https://go.dev/blog/routing-enhancements), [Eli Bendersky](https://eli.thegreenplace.net/2023/better-http-server-routing-in-go-122/)

---

## Middleware Pattern

This project uses the standard wrapper pattern:

```go
func RequestLogger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        wrapped := &byteCountingWriter{ResponseWriter: w}
        next.ServeHTTP(wrapped, r)
        slog.Info("request",
            "method", r.Method,
            "path", r.URL.Path,
            "status", wrapped.statusCode,
            "bytes", wrapped.bytes,
            "total_ms", time.Since(start).Milliseconds(),
        )
    })
}

// Composable
var handler http.Handler = mux
handler = RequestLogger(handler)
handler = RecoveryMiddleware(handler)

srv := &http.Server{Handler: handler}
```

---

## Request Context

Store request-scoped values using typed keys:

```go
// Define typed key (prevents collisions)
type contextKey string
const loggerKey contextKey = "logger"

// Set in middleware
ctx := context.WithValue(r.Context(), loggerKey, logger)
next.ServeHTTP(w, r.WithContext(ctx))

// Retrieve in handlers
func Logger(ctx context.Context) *slog.Logger {
    if l, ok := ctx.Value(loggerKey).(*slog.Logger); ok {
        return l
    }
    return slog.Default()
}
```

---

## ResponseWriter Wrapping

Wrap to capture bytes and status:

```go
type byteCountingWriter struct {
    http.ResponseWriter
    bytes      int64
    statusCode int
}

func (w *byteCountingWriter) WriteHeader(code int) {
    w.statusCode = code
    w.ResponseWriter.WriteHeader(code)
}

func (w *byteCountingWriter) Write(b []byte) (int, error) {
    if w.statusCode == 0 {
        w.statusCode = 200  // Default if WriteHeader not called
    }
    n, err := w.ResponseWriter.Write(b)
    w.bytes += int64(n)
    return n, err
}
```

---

## Graceful Shutdown

### Standard Pattern

```go
srv := &http.Server{
    Addr:    ":8080",
    Handler: mux,
}

// Start server
go func() {
    if err := srv.ListenAndServe(); !errors.Is(err, http.ErrServerClosed) {
        log.Fatal(err)
    }
}()

// Wait for signal
<-ctx.Done()

// Graceful shutdown with timeout
shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

if err := srv.Shutdown(shutdownCtx); err != nil {
    log.Printf("shutdown error: %v", err)
}
```

### What Shutdown() Does

1. Stops accepting new connections immediately
2. Closes idle connections
3. Waits for active requests to complete
4. Returns when all handlers finish OR context expires

### Kubernetes Considerations

Add a health endpoint that fails during shutdown:

```go
healthService.MarkShuttingDown()  // Called before Shutdown()
// Readiness probe now returns 503
```

Sources: [VictoriaMetrics](https://victoriametrics.com/blog/go-graceful-shutdown/), [DEV Community](https://dev.to/mokiat/proper-http-shutdown-in-go-3fji)

---

## Error Responses

cooked returns HTML error pages, not JSON:

```go
func renderError(w http.ResponseWriter, r *http.Request, status int, errType, message string) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.WriteHeader(status)
    // Render error template with same theming as content pages
}
```

Error pages use the same HTML template with:
- Proper theming (respects user's theme choice)
- `#cooked-error` element with `data-error-type` and `data-status-code`
- Direct link to the upstream URL

---

## Handler Naming

| Pattern | Returns | Example |
|---------|---------|---------|
| `FeatureHandler(deps)` | `http.HandlerFunc` | `RenderHandler(deps)` |
| `FeatureMiddleware(next)` | `http.Handler` | `RequestLogger(next)` |

---

## What NOT to Do

| Don't | Why |
|-------|-----|
| Check method with `if r.Method != "GET"` | Use Go 1.22+ method routing |
| Call `w.Write` after handler returns | Causes panic or writes to wrong response |
| Use `string` context keys | Collisions — use typed keys |
| Ignore `http.ErrServerClosed` | It's expected from `Shutdown()` |
| Release resources before shutdown completes | Handlers may still be using them |
