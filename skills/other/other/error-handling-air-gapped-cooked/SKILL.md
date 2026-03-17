---
name: error-handling
description: Error handling patterns for Go 1.20+. Multi-error wrapping, performance traps, slog integration.
---

# Error Handling

This skill covers Go 1.20+ error patterns and project-specific conventions. Assumes you know basic `if err != nil`.

---

## Go 1.20+: Multi-Error Support

### errors.Join (Go 1.20+)

Combine multiple errors without losing any:

```go
// Collecting errors from goroutines
var errs []error
for result := range results {
    if result.err != nil {
        errs = append(errs, result.err)
    }
}
return errors.Join(errs...)  // Returns nil if all nil
```

### Multiple %w in fmt.Errorf (Go 1.20+)

Wrap multiple errors with context:

```go
err := fmt.Errorf("operation failed: %w and %w", err1, err2)
```

Both `errors.Is(err, err1)` and `errors.Is(err, err2)` return true.

### Critical: Unwrap Behavior Change

```go
// Old pattern - BROKEN with multi-errors
wrapped := errors.Unwrap(joinedErr)  // Returns nil!

// New pattern - works with multi-errors
if errors.Is(joinedErr, targetErr) { ... }  // Works
if errors.As(joinedErr, &typedErr) { ... }  // Works
```

`errors.Unwrap()` returns nil for multi-wrapped errors. Always use `errors.Is`/`errors.As`.

Sources: [Go 1.20 Multi-Error Wrapping](https://lukas.zapletalovi.com/posts/2022/wrapping-multiple-errors/), [errors package](https://pkg.go.dev/errors)

---

## Performance: Sentinel Errors Are Slow

Benchmarks from [DoltHub](https://www.dolthub.com/blog/2024-05-31-benchmarking-go-error-handling/):

| Pattern | ns/op | vs baseline |
|---------|-------|-------------|
| Boolean return | 3.4 | 1x |
| Direct `==` check | 7.4 | 2x |
| `errors.Is()` | 19.4 | **6x** |
| Wrapped sentinel through stack | 1,374 | **117x** |

### When Performance Matters

**Don't use sentinel errors for expected conditions:**

```go
// SLOW - sentinel for "not found"
var ErrNotFound = errors.New("not found")
func Get(key string) (Value, error) {
    if !exists {
        return Value{}, ErrNotFound  // Allocates, slow
    }
}

// FAST - boolean for expected condition
func Get(key string) (Value, bool) {
    if !exists {
        return Value{}, false  // No allocation
    }
}
```

**Reserve errors for unexpected failures.** Expected outcomes (not found, empty, EOF) should use booleans or special values.

### If You Must Use Sentinel Errors

Check nil first to avoid `errors.Is` overhead:

```go
if err != nil {
    if errors.Is(err, ErrSpecific) {
        // handle
    }
}
```

---

## Project Patterns

### Error Message Format

Use lowercase, action-oriented prefixes:

```go
// Pattern: "action: description"
return fmt.Errorf("upstream fetch: %w", err)
return fmt.Errorf("render markdown: %w", err)
return fmt.Errorf("parse upstream url: %w", err)
return fmt.Errorf("cache store: %w", err)
return fmt.Errorf("read response body: size exceeds %d bytes", maxSize)
```

When wrapping, preserve the context chain:

```go
if err := fetchUpstream(url); err != nil {
    return fmt.Errorf("render %s: %w", url, err)
    // Chains: "render https://...: upstream fetch: connection refused"
}
```

### slog Error Logging

Always use `"error"` as the key, error as value:

```go
slog.Error("upstream fetch failed", "error", err, "upstream", url)
slog.Warn("cache eviction", "error", err, "key", cacheKey)
```

Never stringify the error:

```go
// WRONG
slog.Error("failed", "error", err.Error())

// RIGHT
slog.Error("failed", "error", err)
```

### HTTP Error Responses

cooked returns styled HTML error pages:

```go
func renderError(w http.ResponseWriter, status int, errType, message string) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.WriteHeader(status)
    // Execute error template
}
```

### Type Assertions with errors.As

For stdlib error types:

```go
var maxBytesErr *http.MaxBytesError
if errors.As(err, &maxBytesErr) {
    // Request body too large
}
```

---

## Decision Tree

### Returning Errors

```
Is the condition expected (not found, empty, no match)?
  YES → Return (value, bool) or special value, not error
  NO  → Continue

Need to add context?
  YES → fmt.Errorf("context: %w", err)
  NO  → return err

Multiple errors to combine?
  YES → errors.Join(errs...) or fmt.Errorf("%w and %w", e1, e2)
```

### Checking Errors

```
Need to check specific error type?
  YES → errors.As(err, &typed)

Need to check sentinel error?
  YES → if err != nil && errors.Is(err, sentinel)

Just need to know if error occurred?
  YES → if err != nil
```

### Logging vs Returning

```
Can the caller handle this error?
  YES → Return it, don't log
  NO  → Log it, then either:
        - Return a wrapped/sanitized error
        - Handle and continue

At system boundary (HTTP handler, main)?
  YES → Log with full context, return user-safe message
```

---

## Error Types vs Sentinels

| Use | When |
|-----|------|
| **Sentinel** (`var ErrX = errors.New(...)`) | Well-known conditions: `io.EOF`, `context.Canceled` |
| **Error type** (`type MyError struct{...}`) | Error carries structured data callers need |
| **Wrapped sentinel** (`fmt.Errorf("...: %w", ErrX)`) | Need both context and identifiable cause |
| **Plain error** (`fmt.Errorf("...")`) | Caller doesn't need to distinguish error types |

Default to plain errors. Only add sentinels/types when callers need to handle specifically.

---

## Defer Cleanup Pattern

Handle errors from deferred cleanup:

```go
func DoWork() (err error) {  // Named return
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer func() {
        if cerr := f.Close(); cerr != nil && err == nil {
            err = cerr  // Only set if no prior error
        }
    }()

    // ... work with f
    return nil
}
```

---

## What NOT to Do

| Don't | Why |
|-------|-----|
| `errors.Unwrap()` with multi-errors | Returns nil — use `errors.Is`/`errors.As` |
| Sentinel errors for expected outcomes | 6-117x slower than booleans |
| `slog.Error("msg", "error", err.Error())` | Loses error chain — pass error directly |
| Log AND return the same error | Causes duplicate logs up the stack |
| `panic` for recoverable errors | Reserve for truly unrecoverable state |
| Ignore deferred Close() errors | Can mask the real failure |
