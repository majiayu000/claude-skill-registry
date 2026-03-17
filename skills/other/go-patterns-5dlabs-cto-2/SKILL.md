---
name: go-patterns
description: Go backend patterns including chi router, gRPC, pgx, context handling, and concurrency.
agents: [grizz]
triggers: [go, golang, chi, grpc, pgx]
---

# Go Backend Patterns

Production Go patterns for backend services with focus on concurrency, error handling, and idiomatic Go.

## Core Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Language | Go 1.22+ | Backend development |
| Build | go build, go test | Compilation and testing |
| Linting | golangci-lint | Code quality |
| HTTP | chi router | RESTful APIs |
| RPC | grpc-go | Service communication |
| Database | pgx, sqlc | PostgreSQL |
| Cache | redis-go | Caching |
| Testing | testify, gomock | Test framework and mocking |
| Observability | OpenTelemetry | Tracing and metrics |

## Context7 Library IDs

Query these libraries for current best practices:

- **Chi Router**: `/go-chi/chi`
- **pgx**: `/jackc/pgx`
- **sqlc**: `/sqlc-dev/sqlc`
- **testify**: `/stretchr/testify`
- **OpenTelemetry Go**: `/open-telemetry/opentelemetry-go`

## Execution Rules

1. **golangci-lint always.** Run linting before commits
2. **No naked returns.** Always name return values in complex functions
3. **Error handling.** Wrap errors with context, don't discard them
4. **Documentation.** GoDoc comments on all exported items
5. **Tests.** Table-driven tests in `_test.go` files

## Error Handling

### Wrapping Errors with Context

```go
import (
    "fmt"
    "errors"
)

func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

### Checking Specific Errors

```go
if errors.Is(err, ErrNotFound) {
    return nil, status.Error(codes.NotFound, "user not found")
}
```

### Custom Error Types

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}
```

## Context Usage

### Timeouts and Cancellation

```go
func FetchData(ctx context.Context, url string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
    defer cancel()
    
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }
    
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("execute request: %w", err)
    }
    defer resp.Body.Close()
    
    return io.ReadAll(resp.Body)
}
```

### Context Values (Use Sparingly)

```go
type contextKey string

const userIDKey contextKey = "userID"

func WithUserID(ctx context.Context, userID string) context.Context {
    return context.WithValue(ctx, userIDKey, userID)
}

func UserIDFromContext(ctx context.Context) (string, bool) {
    userID, ok := ctx.Value(userIDKey).(string)
    return userID, ok
}
```

## Concurrency Patterns

### Graceful Goroutine Management

```go
func worker(ctx context.Context, jobs <-chan Job) {
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-jobs:
            if !ok {
                return
            }
            process(job)
        }
    }
}
```

### Worker Pool

```go
func StartWorkerPool(ctx context.Context, jobs <-chan Job, numWorkers int) {
    var wg sync.WaitGroup
    
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            worker(ctx, jobs)
        }()
    }
    
    wg.Wait()
}
```

### Mutex for Shared State

```go
type SafeCounter struct {
    mu    sync.RWMutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.count
}
```

## Structured Logging

```go
import (
    "log/slog"
    "context"
)

func ProcessRequest(ctx context.Context, id string) {
    logger := slog.With("request_id", id)
    logger.InfoContext(ctx, "processing request")
    
    // On error
    logger.ErrorContext(ctx, "failed to process",
        "error", err,
        "user_id", userID,
    )
}
```

## Chi Router Patterns

```go
import "github.com/go-chi/chi/v5"

func NewRouter() chi.Router {
    r := chi.NewRouter()
    
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.Timeout(30 * time.Second))
    
    r.Route("/api/v1", func(r chi.Router) {
        r.Get("/users/{id}", GetUser)
        r.Post("/users", CreateUser)
    })
    
    return r
}
```

## Table-Driven Tests

```go
func TestGetUser(t *testing.T) {
    tests := []struct {
        name    string
        userID  string
        want    *User
        wantErr bool
    }{
        {
            name:   "valid user",
            userID: "123",
            want:   &User{ID: "123", Name: "Test"},
        },
        {
            name:    "invalid user",
            userID:  "999",
            wantErr: true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := GetUser(tt.userID)
            if (err != nil) != tt.wantErr {
                t.Errorf("GetUser() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("GetUser() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Validation Commands

```bash
go fmt ./...
go vet ./...
golangci-lint run ./...
go test ./... -race -v
go build ./...
```

## Guidelines

- Keep functions small and focused
- Use interfaces for abstraction
- Handle errors explicitly, don't panic
- Prefer composition over inheritance
- Document exported functions and types
- Use context for cancellation and timeouts
- Leverage goroutines appropriately (not excessively)
