---
name: golang-patterns
description: Idiomatic Go patterns and policies. Use when writing, reviewing, or refactoring Go application code. Do NOT use for test code -- use golang-testing instead.
durability: encoded-preference
---

# Go Development Patterns

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Simplicity > Cleverness** | Code should be obvious and easy to read |
| **Zero value useful** | Types should work without initialization |
| **Accept interfaces, return structs** | Functions accept interface params, return concrete types |
| **Errors are values** | Handle errors explicitly, never ignore |
| **Clear > Clever** | Prioritize readability |

## Error Handling (CRITICAL)

### Always Wrap with Context

```go
if err != nil {
    return nil, fmt.Errorf("load config %s: %w", path, err)
}
```

### Use errors.Is and errors.As

```go
if errors.Is(err, sql.ErrNoRows) { /* specific error */ }

var validationErr *ValidationError
if errors.As(err, &validationErr) { /* error type */ }
```

### Never Ignore Errors

```go
// BAD
result, _ := doSomething()

// GOOD
result, err := doSomething()
if err != nil {
    return err
}
```

## Interface Design

### Define Where Used (Consumer Package)

```go
// In service package, NOT in repository package
type UserStore interface {
    GetUser(id string) (*User, error)
}
```

### Small, Focused Interfaces

Prefer single-method interfaces — enables composition and testing flexibility. Compose as needed.

## Concurrency Policies

### Context Rules

- Context is ALWAYS first parameter
- Never store context in structs
- Use `context.WithTimeout` for external calls

### Avoid Goroutine Leaks

```go
// Use buffered channel or select with ctx.Done()
ch := make(chan []byte, 1)
select {
case ch <- data:
case <-ctx.Done():
}
```

### Use errgroup for Coordinated Goroutines

```go
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { /* ... */ })
if err := g.Wait(); err != nil { /* ... */ }
```

## Package Organization

```text
myproject/
├── cmd/myapp/main.go    # Entry point
├── internal/            # Private packages
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/                 # Public packages
└── Makefile
```

### Package Naming

- Short, lowercase, no underscores
- No redundant suffixes (`user` not `userService`)

### No Package-Level State

Use dependency injection, not global variables.

## Struct Design

### Functional Options for Configurability

```go
func NewServer(addr string, opts ...Option) *Server

// Usage
server := NewServer(":8080", WithTimeout(60*time.Second))
```

## Performance Policies

| Policy | Why |
|--------|-----|
| Preallocate slices | `make([]T, 0, len)` avoids reallocations |
| Use strings.Builder | Avoid `+=` in loops |
| Use sync.Pool | For frequent allocations |

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Naked returns in long functions | Explicit returns |
| panic for control flow | Return errors |
| Context in struct | Context as first param |
| Mixed receivers | Consistent value OR pointer |
| Ignoring errors with `_` | Handle or explicitly document |

## Commands

**See `makefile-first` skill** for command execution policy.
