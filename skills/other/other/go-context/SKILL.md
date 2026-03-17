---
name: go-context
description: Go context.Context usage patterns including parameter placement, avoiding struct embedding, and proper propagation. Use when working with context.Context in Go code for cancellation, deadlines, and request-scoped values.
---

# Go Context Usage

`context.Context` carries security credentials, tracing information, deadlines,
and cancellation signals across API and process boundaries. Go programs pass
contexts explicitly along the entire function call chain.

> Based on [Go Wiki CodeReviewComments - Contexts](https://github.com/golang/wiki/blob/master/CodeReviewComments.md#contexts).

---

## Context as First Parameter

Functions that use a Context should accept it as their **first parameter**:

```go
// Good: Context is first parameter
func F(ctx context.Context, /* other arguments */) error {
    // ...
}

func ProcessRequest(ctx context.Context, req *Request) (*Response, error) {
    // ...
}
```

This is a strong convention in Go that makes context flow visible and consistent
across codebases.

---

## Don't Store Context in Structs

Do not add a Context member to a struct type. Instead, pass `ctx` as a parameter
to each method that needs it:

```go
// Bad: Context stored in struct
type Worker struct {
    ctx context.Context  // Don't do this
    // ...
}

func (w *Worker) Process() error {
    // Uses w.ctx - context lifetime unclear
}
```

```go
// Good: Context passed to methods
type Worker struct {
    // ...
}

func (w *Worker) Process(ctx context.Context) error {
    // Context explicitly passed - lifetime clear
}
```

**Exception**: Methods whose signature must match an interface in the standard
library or a third-party library may need to work around this.

---

## Don't Create Custom Context Types

Do not create custom Context types or use interfaces other than `context.Context`
in function signatures:

```go
// Bad: Custom context type
type MyContext interface {
    context.Context
    GetUserID() string
}

func Process(ctx MyContext) error { ... }
```

```go
// Good: Use standard context.Context
func Process(ctx context.Context) error {
    userID := GetUserID(ctx)  // Extract from context value
    // ...
}
```

---

## Where to Put Application Data

If you have application data to pass around, consider these options in order of
preference:

1. **Function parameters** - Most explicit and type-safe
2. **Receiver** - For data that belongs to the type
3. **Globals** - For truly global configuration (use sparingly)
4. **Context value** - Only if it truly belongs there (request-scoped data)

```go
// Good: Explicit parameter
func ProcessOrder(ctx context.Context, userID string, order *Order) error {
    // userID is explicit
}

// Good: Context value for request-scoped data
func ProcessOrder(ctx context.Context, order *Order) error {
    // Request ID from context is appropriate - it's request-scoped
    reqID := RequestIDFromContext(ctx)
    // ...
}
```

Context values are appropriate for:
- Request IDs and trace IDs
- Authentication/authorization info that flows with requests
- Deadlines and cancellation signals

Context values are **not** appropriate for:
- Optional function parameters
- Data that could be passed explicitly
- Configuration that doesn't vary per-request

---

## Context Immutability

Contexts are immutable. It's safe to pass the same `ctx` to multiple calls that
share the same deadline, cancellation signal, credentials, and parent trace:

```go
// Good: Same context to multiple calls
func ProcessBatch(ctx context.Context, items []Item) error {
    for _, item := range items {
        // Safe to pass same ctx to each call
        if err := process(ctx, item); err != nil {
            return err
        }
    }
    return nil
}

// Good: Same context to concurrent calls
func ProcessConcurrently(ctx context.Context, a, b *Data) error {
    g, ctx := errgroup.WithContext(ctx)
    g.Go(func() error { return processA(ctx, a) })
    g.Go(func() error { return processB(ctx, b) })
    return g.Wait()
}
```

---

## When to Use context.Background()

Use `context.Background()` only for functions that are **never request-specific**:

```go
// Good: Main function or initialization
func main() {
    ctx := context.Background()
    if err := run(ctx); err != nil {
        log.Fatal(err)
    }
}

// Good: Top-level background task
func startBackgroundWorker() {
    ctx := context.Background()
    go worker(ctx)
}
```

**Default to passing a Context** even if you think you don't need to. Only use
`context.Background()` directly if you have a good reason why passing a context
would be a mistake:

```go
// Prefer: Accept context even for "simple" operations
func LoadConfig(ctx context.Context) (*Config, error) {
    // Even if not using ctx now, accepting it allows future
    // additions without API changes
}
```

---

## Common Patterns

### Deriving Contexts

```go
// Add timeout
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// Add cancellation
ctx, cancel := context.WithCancel(ctx)
defer cancel()

// Add deadline
ctx, cancel := context.WithDeadline(ctx, time.Now().Add(time.Hour))
defer cancel()

// Add value (use sparingly)
ctx = context.WithValue(ctx, requestIDKey, reqID)
```

### Checking Cancellation

```go
func LongRunningOperation(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            // Do work
        }
    }
}
```

### Respecting Cancellation in HTTP Handlers

```go
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    
    result, err := slowOperation(ctx)
    if err != nil {
        if errors.Is(err, context.Canceled) {
            // Client disconnected
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    json.NewEncoder(w).Encode(result)
}
```

---

## Quick Reference

| Pattern | Guidance |
|---------|----------|
| Parameter position | Always first: `func F(ctx context.Context, ...)` |
| Struct storage | Don't store in structs; pass to methods |
| Custom types | Don't create; use `context.Context` interface |
| Application data | Prefer parameters > receiver > globals > context values |
| Request-scoped data | Appropriate for context values |
| Sharing context | Safe - contexts are immutable |
| `context.Background()` | Only for non-request-specific code |
| Default | Pass context even if you think you don't need it |

---

## See Also

- **go-concurrency**: Goroutine patterns, cancellation, and coordination
- **go-error-handling**: Handling context cancellation errors
- **go-interfaces**: Interface design patterns for context-accepting APIs
