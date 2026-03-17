---
name: Go Ecosystem
description: This skill should be used when the user asks to "write go", "golang", "go.mod", "go module", "go test", "go build", or works with Go language development. Provides comprehensive Go ecosystem patterns and best practices.
version: 0.2.0
---

# Go Ecosystem

## Core Concepts

- **Errors are values**: Handle explicitly with `if err != nil`; use `%w` to wrap for `errors.Is`/`errors.As`
- **Interfaces**: Accept interfaces, return concrete types; define where used, not implemented; keep small (1-3 methods)
- **Concurrency**: Goroutines for concurrency, channels for communication, `context.Context` for cancellation
- **Zero values**: Design types so zero value is useful (`var buf bytes.Buffer` ready to use)

## Naming Conventions

- Packages: lowercase, single-word (no underscores)
- Exported: PascalCase; Unexported: camelCase
- Single-method interfaces: method name + "er" (Reader, Writer, Handler)
- Acronyms uppercase: `HTTPClient`, `userID`
- No "Get" prefix for getters: `func (u *User) Name() string`

## Error Handling

```go
// Wrap with context
if err != nil {
    return fmt.Errorf("processing user %s: %w", userID, err)
}

// Sentinel errors
var ErrNotFound = errors.New("not found")

// Custom error type
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}

// Go 1.20+ multiple errors
err := errors.Join(err1, err2, err3)
```

## Project Structure

```
cmd/myapp/main.go    # Minimal - call into internal packages
internal/            # Private, cannot be imported externally
pkg/                 # Public library (optional)
testdata/            # Test fixtures (ignored by go build)
```

## Testing

```go
// Table-driven tests
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}

// Test helpers
func setupTestDB(t *testing.T) *DB {
    t.Helper()
    db := NewDB()
    t.Cleanup(func() { db.Close() })
    return db
}
```

## Concurrency

```go
// Context for cancellation
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// Channel select
select {
case msg := <-ch1:
    handle(msg)
case <-ctx.Done():
    return ctx.Err()
}

// WaitGroup
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(item Item) {
        defer wg.Done()
        process(item)
    }(item)
}
wg.Wait()
```

## Anti-Patterns

- **init() overuse**: Prefer explicit initialization functions
- **Global state**: Pass dependencies explicitly
- **Interface pollution**: Define interfaces when needed, not prematurely
- **Naked returns**: Use explicit returns in long functions
- **Goroutine leaks**: Use context or done channels for cancellation

## Commands

- `go build` / `go build -o name` - Compile
- `go test ./... -v -race` - Test with race detector
- `go vet ./...` - Static analysis
- `go fmt ./...` - Format
- `go mod tidy` - Clean dependencies
- `GOOS=linux GOARCH=amd64 go build` - Cross-compile

## Context7 Reference

Library ID: `/golang/website`
