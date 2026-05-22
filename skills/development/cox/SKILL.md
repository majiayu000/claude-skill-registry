---
name: cox-tooling-excellence
description: Write Go code in the style of Russ Cox, Go tech lead. Emphasizes tooling, module design, correctness, and backward compatibility. Use when designing packages, modules, or tools that others will depend on.
---

# Russ Cox Style Guide

## Overview

Russ Cox is the tech lead of Go at Google. He designed the Go module system, maintains critical tools, and writes extensively about correctness and compatibility. His work on regular expressions (RE2) and the Go toolchain sets the standard for quality.

## Core Philosophy

> "Compatibility is about people, not just code."

> "The goal is not to be fast. The goal is to be correct and then fast."

Cox believes in **correctness first**, then performance. He also champions the **Go 1 compatibility promise**: code written for Go 1.0 should still work.

## Design Principles

1. **Correctness First**: Get it right before getting it fast.

2. **Compatibility Matters**: Breaking changes hurt real people.

3. **Tooling is Product**: `go mod`, `go vet`, `gofmt` are as important as the language.

4. **Reproducibility**: Builds should be reproducible, dependencies explicit.

## When Writing Code

### Always

- Use `go mod` for dependency management
- Run `go vet` and address all warnings
- Write reproducible builds (pin dependencies)
- Maintain backward compatibility in public APIs
- Use semantic versioning correctly
- Document breaking changes clearly

### Never

- Break existing API contracts
- Publish v0 code as v1
- Ignore module versioning rules
- Use `replace` directives in published modules
- Import packages with `_` prefix

### Prefer

- Stable APIs over flexible ones
- Explicit imports over dot imports
- Internal packages for private code
- Minimal dependencies
- Standard library when possible

## Code Patterns

### Module Design

```go
// go.mod - clean, minimal
module github.com/example/myproject

go 1.21

require (
    golang.org/x/sync v0.5.0
)

// Avoid unnecessary dependencies
// Every dependency is a liability
```

### API Stability with Options Pattern

```go
// Extensible API without breaking changes

// Public, stable struct (fields are API)
type Config struct {
    Timeout time.Duration
    // Adding fields is safe
}

// Options pattern for flexibility
type Option func(*clientOptions)

type clientOptions struct {
    timeout    time.Duration
    retries    int
    logger     Logger
}

func WithTimeout(d time.Duration) Option {
    return func(o *clientOptions) {
        o.timeout = d
    }
}

func WithRetries(n int) Option {
    return func(o *clientOptions) {
        o.retries = n
    }
}

// Adding new options doesn't break existing code
func NewClient(opts ...Option) *Client {
    options := clientOptions{
        timeout: 30 * time.Second,  // sensible defaults
        retries: 3,
    }
    for _, opt := range opts {
        opt(&options)
    }
    return &Client{options: options}
}

// Usage (existing code keeps working as options are added)
client := NewClient(WithTimeout(10 * time.Second))
```

### Internal Packages

```go
// Project structure with internal packages

// myproject/
// ├── go.mod
// ├── client.go         (public API)
// ├── internal/
// │   ├── parser/       (private: can change freely)
// │   └── protocol/     (private: can change freely)
// └── cmd/
//     └── mytool/       (command)

// internal/ packages can only be imported by parent
// This allows free refactoring without breaking users
```

### Semantic Versioning

```go
// v0.x.x - No compatibility guarantees
// Breaking changes are fine

// v1.x.x - Compatibility guaranteed
// v1.1.0 adds features, v1.1.1 fixes bugs
// NEVER break API

// v2.x.x - New major version, new import path
// github.com/example/myproject/v2

// go.mod for v2:
module github.com/example/myproject/v2

go 1.21

// Import path includes version:
import "github.com/example/myproject/v2/pkg"
```

### Deprecation Without Breaking

```go
// Add new function, deprecate old
// Old code keeps working

// Deprecated: Use NewFoo instead.
func Foo() *Widget {
    return NewFoo(DefaultOptions)
}

// New function with more flexibility
func NewFoo(opts Options) *Widget {
    // ...
}

// Godoc shows deprecation, go vet can warn
```

### Correct Concurrent Code

```go
// From Russ Cox's concurrency patterns

// Correct synchronization
type Cache struct {
    mu    sync.RWMutex
    items map[string]Item
}

func (c *Cache) Get(key string) (Item, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    item, ok := c.items[key]
    return item, ok
}

func (c *Cache) Set(key string, item Item) {
    c.mu.Lock()
    defer c.mu.Unlock()
    if c.items == nil {
        c.items = make(map[string]Item)
    }
    c.items[key] = item
}

// Graceful shutdown pattern
func serve(ctx context.Context, addr string, handler http.Handler) error {
    srv := &http.Server{Addr: addr, Handler: handler}
    
    errCh := make(chan error, 1)
    go func() {
        errCh <- srv.ListenAndServe()
    }()
    
    select {
    case err := <-errCh:
        return err
    case <-ctx.Done():
        // Graceful shutdown
        shutdownCtx, cancel := context.WithTimeout(
            context.Background(), 
            5*time.Second,
        )
        defer cancel()
        return srv.Shutdown(shutdownCtx)
    }
}
```

### Testing Best Practices

```go
// Table-driven tests
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Result
        wantErr bool
    }{
        {"empty", "", Result{}, false},
        {"simple", "foo", Result{Value: "foo"}, false},
        {"invalid", "!!!", Result{}, true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Parse() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("Parse() = %v, want %v", got, tt.want)
            }
        })
    }
}

// Test helpers
func newTestServer(t *testing.T) *Server {
    t.Helper()
    srv := &Server{}
    t.Cleanup(func() { srv.Close() })
    return srv
}
```

## Mental Model

Cox approaches design by asking:

1. **Is it correct?** Prove it works before optimizing.
2. **Is it compatible?** Will existing code break?
3. **Is it reproducible?** Same inputs → same outputs?
4. **Is it maintainable?** Will this be regretted in 5 years?

## The Compatibility Contract

| Change | Safe? |
|--------|-------|
| Add function | ✅ Yes |
| Add method to interface | ❌ No (breaks implementers) |
| Add field to struct | ⚠️ Maybe (if not compared) |
| Add optional parameter | ✅ Yes (via options pattern) |
| Change function signature | ❌ No |
| Rename exported symbol | ❌ No |

