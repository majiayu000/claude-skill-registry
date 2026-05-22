---
name: cheney-practical-go
description: Write Go code in the style of Dave Cheney, Go community leader. Emphasizes practical patterns, clear error handling, and performance awareness. Use when writing production Go that needs to be maintainable and performant.
---

# Dave Cheney Style Guide

## Overview

Dave Cheney is a Go contributor, prolific blogger, and author of "Practical Go." His talks and writing focus on real-world Go patterns, error handling philosophy, and performance optimization without sacrificing readability.

## Core Philosophy

> "Clear is better than clever."

> "Errors are just values."

> "Make the zero value useful."

Cheney believes in **practical, production-ready code**. His approach: write clear code first, understand the performance characteristics, optimize only what matters.

## Design Principles

1. **Errors Are Values**: Handle them, wrap them, or return them—but never ignore them.

2. **Clear Over Clever**: If it needs a comment, rewrite it.

3. **Performance Awareness**: Know the cost of operations, but don't prematurely optimize.

4. **Package Design**: Small, focused packages with clear responsibilities.

## When Writing Code

### Always

- Handle every error explicitly
- Wrap errors with context using `fmt.Errorf` and `%w`
- Use structured logging
- Write benchmarks for hot paths
- Keep packages focused and small
- Document exported symbols

### Never

- Use `_` to ignore errors (except in specific cases)
- `panic` for expected error conditions
- Create "utils" or "common" packages
- Use package-level variables for state
- Log and return an error (do one or the other)

### Prefer

- `errors.Is` and `errors.As` over type assertions
- Wrapping errors over creating new ones
- Returning early over deep nesting
- Small interfaces (1-3 methods)
- Dependency injection over globals

## Code Patterns

### Error Handling Philosophy

```go
// BAD: Ignoring errors
data, _ := ioutil.ReadFile(filename)

// BAD: Log and return (double handling)
if err != nil {
    log.Printf("failed to read: %v", err)
    return err
}

// GOOD: Add context and return
if err != nil {
    return fmt.Errorf("read config %s: %w", filename, err)
}

// GOOD: Handle completely (don't return)
if err != nil {
    log.Printf("failed to read %s, using defaults: %v", filename, err)
    return defaultConfig()
}
```

### Error Wrapping Strategy

```go
// Build error chains with context
func LoadUser(id string) (*User, error) {
    data, err := db.Query(id)
    if err != nil {
        return nil, fmt.Errorf("load user %s: %w", id, err)
    }
    
    user, err := parseUser(data)
    if err != nil {
        return nil, fmt.Errorf("load user %s: %w", id, err)
    }
    
    return user, nil
}

// Callers can check for specific errors
user, err := LoadUser(id)
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrUserNotFound
}

// Or extract error types
var queryErr *QueryError
if errors.As(err, &queryErr) {
    log.Printf("query failed: %s", queryErr.Query)
}
```

### Sentinel Errors Done Right

```go
// Define sentinel errors at package level
var (
    ErrNotFound   = errors.New("not found")
    ErrPermission = errors.New("permission denied")
    ErrTimeout    = errors.New("operation timed out")
)

// Wrap them with context
func GetItem(id string) (*Item, error) {
    item, ok := store[id]
    if !ok {
        return nil, fmt.Errorf("item %s: %w", id, ErrNotFound)
    }
    return item, nil
}

// Callers check with errors.Is (handles wrapping)
if errors.Is(err, ErrNotFound) {
    // handle not found
}
```

### Package Organization

```go
// BAD: Kitchen sink packages
package utils
package common
package helpers

// GOOD: Focused packages by responsibility
package user      // User domain logic
package storage   // Storage abstraction
package http      // HTTP handlers

// Package should have ONE primary type or purpose
// user/user.go
package user

type User struct { ... }
type Service struct { ... }
func New(...) *Service { ... }
```

### Dependency Injection

```go
// BAD: Hard-coded dependencies
type Server struct{}

func (s *Server) HandleUser(w http.ResponseWriter, r *http.Request) {
    user, err := db.GetUser(r.Context(), userID)  // Global db!
    // ...
}

// GOOD: Injected dependencies
type Server struct {
    users  UserStore
    logger Logger
}

type UserStore interface {
    Get(ctx context.Context, id string) (*User, error)
}

func NewServer(users UserStore, logger Logger) *Server {
    return &Server{users: users, logger: logger}
}

func (s *Server) HandleUser(w http.ResponseWriter, r *http.Request) {
    user, err := s.users.Get(r.Context(), userID)
    // ...
}

// Testing is now trivial
func TestHandleUser(t *testing.T) {
    mock := &MockUserStore{}
    srv := NewServer(mock, testLogger)
    // ...
}
```

### Performance-Aware Code

```go
// Know the cost: string concatenation
// BAD: Creates many allocations
func join(items []string) string {
    result := ""
    for _, item := range items {
        result += item + ","  // Allocates each time!
    }
    return result
}

// GOOD: Pre-allocate with strings.Builder
func join(items []string) string {
    var b strings.Builder
    for i, item := range items {
        if i > 0 {
            b.WriteString(",")
        }
        b.WriteString(item)
    }
    return b.String()
}

// Know the cost: slice operations
// BAD: May cause unexpected allocations
func process(items []Item) {
    filtered := items[:0]  // Reuses backing array - be careful!
    for _, item := range items {
        if item.Valid {
            filtered = append(filtered, item)
        }
    }
}

// GOOD: Clear intent
func process(items []Item) []Item {
    filtered := make([]Item, 0, len(items))
    for _, item := range items {
        if item.Valid {
            filtered = append(filtered, item)
        }
    }
    return filtered
}
```

### Functional Options with Validation

```go
type serverOptions struct {
    addr         string
    readTimeout  time.Duration
    writeTimeout time.Duration
}

type ServerOption func(*serverOptions) error

func WithAddr(addr string) ServerOption {
    return func(o *serverOptions) error {
        if addr == "" {
            return errors.New("addr cannot be empty")
        }
        o.addr = addr
        return nil
    }
}

func WithTimeouts(read, write time.Duration) ServerOption {
    return func(o *serverOptions) error {
        if read <= 0 || write <= 0 {
            return errors.New("timeouts must be positive")
        }
        o.readTimeout = read
        o.writeTimeout = write
        return nil
    }
}

func NewServer(opts ...ServerOption) (*Server, error) {
    options := serverOptions{
        addr:         ":8080",
        readTimeout:  30 * time.Second,
        writeTimeout: 30 * time.Second,
    }
    
    for _, opt := range opts {
        if err := opt(&options); err != nil {
            return nil, fmt.Errorf("invalid option: %w", err)
        }
    }
    
    return &Server{options: options}, nil
}
```

## Mental Model

Cheney writes code by asking:

1. **How does this fail?** Handle that case explicitly.
2. **What's the cost?** Know allocations, copies, syscalls.
3. **Is this clear?** Would a new team member understand it?
4. **Is this testable?** Can I inject dependencies?

## Cheney's Laws

1. Don't log and return an error—do one or the other
2. Wrap errors with context, don't just return them
3. If a function can fail, it should return an error
4. Small interfaces are better than large ones
5. Accept interfaces, return structs

