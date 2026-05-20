---
name: go-middleware
description: Idiomatic Go HTTP middleware patterns with context propagation, structured logging via slog, centralized error handling, and panic recovery. Use when writing middleware, adding request tracing, or implementing cross-cutting concerns.
---

# Go HTTP Middleware

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Context keys, request IDs, user metadata | [references/context-propagation.md](references/context-propagation.md) |
| slog setup, logging middleware, child loggers | [references/structured-logging.md](references/structured-logging.md) |
| AppHandler pattern, domain errors, recovery | [references/error-handling-middleware.md](references/error-handling-middleware.md) |

## Middleware Signature

All middleware follows the standard `func(http.Handler) http.Handler` pattern. This is the composable building block for cross-cutting concerns in Go HTTP servers.

```go
// Standard middleware signature
func RequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := r.Header.Get("X-Request-ID")
        if id == "" {
            id = uuid.New().String()
        }
        ctx := context.WithValue(r.Context(), requestIDKey, id)
        w.Header().Set("X-Request-ID", id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Type-safe context keys
type contextKey string
const requestIDKey contextKey = "request_id"

func RequestIDFromContext(ctx context.Context) string {
    id, _ := ctx.Value(requestIDKey).(string)
    return id
}
```

Key points:
- Accept `http.Handler`, return `http.Handler` -- always
- Call `next.ServeHTTP(w, r)` to pass control to the next handler
- Work before the call (pre-processing) or after (post-processing) or both
- Use `r.WithContext(ctx)` to propagate new context values downstream

## Context Propagation

Use `context.WithValue` for request-scoped data that crosses API boundaries (request IDs, authenticated users, tenant IDs). Always use typed keys to avoid collisions.

```go
type contextKey string

const (
    requestIDKey contextKey = "request_id"
    userKey      contextKey = "user"
)
```

Provide typed helper functions for extraction:

```go
func RequestIDFromContext(ctx context.Context) string {
    id, _ := ctx.Value(requestIDKey).(string)
    return id
}
```

See [references/context-propagation.md](references/context-propagation.md) for user metadata patterns, downstream propagation, and timeouts.

## Structured Logging

Use `slog` (standard library, Go 1.21+) for structured logging in middleware. Wrap `http.ResponseWriter` to capture the status code.

```go
func Logger(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            wrapped := &statusWriter{ResponseWriter: w, status: http.StatusOK}

            next.ServeHTTP(wrapped, r)

            logger.Info("request completed",
                "method", r.Method,
                "path", r.URL.Path,
                "status", wrapped.status,
                "duration_ms", time.Since(start).Milliseconds(),
                "request_id", RequestIDFromContext(r.Context()),
            )
        })
    }
}
```

See [references/structured-logging.md](references/structured-logging.md) for JSON/text handler setup, log levels, and child loggers.

## Centralized Error Handling

Define a custom handler type that returns `error` so handlers don't need to write error responses themselves:

```go
type AppHandler func(w http.ResponseWriter, r *http.Request) error

func (fn AppHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if err := fn(w, r); err != nil {
        handleError(w, r, err)
    }
}
```

Map domain errors to HTTP status codes in a single `handleError` function. Never leak internal error details to clients.

See [references/error-handling-middleware.md](references/error-handling-middleware.md) for the full pattern with `AppError`, `errors.As`, and JSON responses.

## Recovery Middleware

Catch panics to prevent a single bad request from crashing the server:

```go
func Recovery(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                slog.Error("panic recovered",
                    "panic", rec,
                    "stack", string(debug.Stack()),
                    "request_id", RequestIDFromContext(r.Context()),
                )
                writeJSON(w, 500, map[string]string{"error": "internal server error"})
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

Recovery must be the **outermost** middleware so it catches panics from all inner middleware and handlers. See [references/error-handling-middleware.md](references/error-handling-middleware.md) for details.

## Middleware Chain Ordering

Apply middleware outermost-first. The first middleware in the chain wraps all others.

```go
// Nested style (outermost first)
handler := Recovery(
    RequestID(
        Logger(
            Auth(
                router,
            ),
        ),
    ),
)

// Or with a chain helper
func Chain(h http.Handler, middleware ...func(http.Handler) http.Handler) http.Handler {
    for i := len(middleware) - 1; i >= 0; i-- {
        h = middleware[i](h)
    }
    return h
}

handler := Chain(router, Recovery, RequestID, Logger(slog.Default()), Auth)
```

### Recommended Order

1. **Recovery** -- outermost; catches panics from all inner middleware
2. **RequestID** -- assign early so all subsequent middleware can reference it
3. **Logger** -- logs the completed request with ID and status
4. **Auth** -- after logging so failed auth attempts are recorded
5. **Application-specific middleware** -- rate limiting, CORS, etc.

## Anti-patterns

### Using string or int context keys
```go
// BAD: collisions with other packages
ctx = context.WithValue(ctx, "user", user)

// GOOD: unexported typed key
type contextKey string
const userKey contextKey = "user"
ctx = context.WithValue(ctx, userKey, user)
```

### Writing response before calling next
```go
// BAD: writes response then continues chain
func Bad(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK) // too early!
        next.ServeHTTP(w, r)
    })
}
```

### Forgetting to call next.ServeHTTP
```go
// BAD: swallows the request
func Bad(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Println("got request")
        // forgot next.ServeHTTP(w, r)
    })
}
```

### Storing large objects in context
Context values should be small, request-scoped metadata (IDs, tokens, user structs). Never store database connections, file handles, or large payloads.

### Using context.WithValue for function parameters
If a function needs a value to do its job, pass it as an explicit parameter. Context is for cross-cutting metadata that passes through APIs, not for avoiding function signatures.

### Recovery middleware in the wrong position
If recovery is not the outermost middleware, panics in outer middleware will crash the server. Always apply recovery first.
