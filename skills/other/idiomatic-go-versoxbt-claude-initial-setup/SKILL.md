---
name: idiomatic-go
description: >
  Write clean, idiomatic Go following community conventions and effective patterns.
  Use when the user writes Go code, designs packages, defines interfaces, uses
  struct embedding, writes receiver methods, organizes Go projects, or asks about
  Go best practices and conventions.
---

# Idiomatic Go

Write Go code that follows community conventions, leveraging interfaces, struct
embedding, and proper package organization for clean, maintainable projects.

## When to Use
- Starting a new Go project or package
- Designing interfaces and struct hierarchies
- Choosing between value and pointer receivers
- Organizing packages and project layout
- Reviewing Go code for idiom violations

## Core Patterns

### Pattern 1: Interface Design

Define small interfaces at the point of consumption, not at the implementation site.
The Go proverb: "The bigger the interface, the weaker the abstraction."

```go
// GOOD: small, focused interfaces defined by the consumer
package storage

// Reader is defined where it is used, not where it is implemented.
type Reader interface {
    Read(ctx context.Context, key string) ([]byte, error)
}

func NewCache(reader Reader, ttl time.Duration) *Cache {
    return &Cache{reader: reader, ttl: ttl}
}

// Accept interfaces, return structs
func ProcessData(r io.Reader) (*Result, error) {
    data, err := io.ReadAll(r)
    if err != nil {
        return nil, fmt.Errorf("reading data: %w", err)
    }
    return &Result{Data: data}, nil
}
```

### Pattern 2: Struct Embedding

Embed types to compose behavior without inheritance. Embedding promotes the
embedded type's methods to the outer struct.

```go
type Logger struct {
    prefix string
}

func (l *Logger) Log(msg string) {
    fmt.Printf("[%s] %s\n", l.prefix, msg)
}

type Server struct {
    Logger  // embed Logger -- Server now has a Log method
    addr string
}

func NewServer(addr string) *Server {
    return &Server{
        Logger: Logger{prefix: "server"},
        addr:   addr,
    }
}

// Usage
s := NewServer(":8080")
s.Log("starting") // promoted from Logger
```

### Pattern 3: Receiver Methods -- Value vs Pointer

Use pointer receivers when the method mutates state or the struct is large.
Use value receivers for small, immutable types.

```go
// Value receiver: small, immutable, safe to copy
type Point struct {
    X, Y float64
}

func (p Point) Distance(other Point) float64 {
    dx := p.X - other.X
    dy := p.Y - other.Y
    return math.Sqrt(dx*dx + dy*dy)
}

// Pointer receiver: mutates state
type Counter struct {
    mu    sync.Mutex
    count int64
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *Counter) Value() int64 {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

Rule: if any method on a type needs a pointer receiver, make all methods
use pointer receivers for consistency.

### Pattern 4: Package Organization

Follow the standard Go project layout conventions.

```
myapp/
  cmd/
    server/
      main.go        // entrypoint: flag parsing, wiring, server start
    worker/
      main.go
  internal/          // private packages, not importable by other modules
    user/
      user.go        // domain types
      service.go     // business logic
      repository.go  // data access interface
      postgres.go    // repository implementation
    order/
      order.go
  pkg/               // public library code (optional, use sparingly)
    httputil/
      middleware.go
  go.mod
  go.sum
```

Guidelines:
- Package names are short, lowercase, single-word (no underscores or mixedCase).
- Avoid `package util` or `package common` -- name packages by what they provide.
- Use `internal/` to prevent external imports of implementation details.
- One package per concept, not per file type.

### Pattern 5: Functional Options

Use the functional options pattern for configurable constructors with clean defaults.

```go
type Server struct {
    addr         string
    readTimeout  time.Duration
    writeTimeout time.Duration
    logger       *slog.Logger
}

type Option func(*Server)

func WithReadTimeout(d time.Duration) Option {
    return func(s *Server) { s.readTimeout = d }
}

func WithWriteTimeout(d time.Duration) Option {
    return func(s *Server) { s.writeTimeout = d }
}

func WithLogger(l *slog.Logger) Option {
    return func(s *Server) { s.logger = l }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{
        addr:         addr,
        readTimeout:  5 * time.Second,
        writeTimeout: 10 * time.Second,
        logger:       slog.Default(),
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer(":8080",
    WithReadTimeout(10*time.Second),
    WithLogger(customLogger),
)
```

## Anti-Patterns

- **Large interfaces defined at the implementation** -- Define interfaces where they are
  consumed. A 10-method interface is almost never needed.

- **`package utils`** -- This is a code smell in Go. Move functions to the package
  that uses them or name the package by its domain.

- **Getter prefixes** -- Go convention is `user.Name()`, not `user.GetName()`.
  Only use `Get` prefix when it disambiguates (e.g., HTTP handlers).

- **init() for complex logic** -- `init()` runs implicitly and makes testing hard.
  Use explicit initialization in `main()` or constructors.
  ```go
  // BAD
  var db *sql.DB
  func init() { db, _ = sql.Open("postgres", os.Getenv("DB_URL")) }

  // GOOD
  func NewDB(url string) (*sql.DB, error) { return sql.Open("postgres", url) }
  ```

- **Naked returns in long functions** -- Named returns are fine for documentation,
  but naked `return` in functions longer than a few lines hurts readability.

## Quick Reference

| Principle | Guideline |
|-----------|-----------|
| Interfaces | Small, consumer-defined, accept interfaces |
| Returns | Return concrete structs, not interfaces |
| Receivers | Pointer if mutating or large; value if small and immutable |
| Packages | Short names, by domain, use `internal/` |
| Constructors | `NewXxx` functions, functional options for config |
| Errors | Return `error` as last value, wrap with `%w` |
| Naming | MixedCaps, no underscores, short locals |
