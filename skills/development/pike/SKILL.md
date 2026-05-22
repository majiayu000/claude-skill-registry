---
name: pike-simplicity-first
description: Write Go code in the style of Rob Pike, co-creator of Go. Emphasizes radical simplicity, concurrency through communication, and composition over inheritance. Use when writing Go that should be clear, concurrent, and maintainable.
---

# Rob Pike Style Guide

## Overview

Rob Pike co-created Go at Google with Ken Thompson and Robert Griesemer. He also created Plan 9, Acme, sam, and co-invented UTF-8. His central thesis: **simplicity is the ultimate sophistication**, and most software is far too complex.

## Core Philosophy

> "Simplicity is complicated."

> "Don't communicate by sharing memory; share memory by communicating."

> "Clear is better than clever."

Pike believes that **complexity is the enemy**, and Go was designed as an antidote to the bloat of C++ and Java. Every feature in Go earned its place by being essential.

## Design Principles

1. **Simplicity Above All**: If you can remove something without breaking functionality, remove it.

2. **Composition Over Inheritance**: Embed types, implement interfaces implicitly.

3. **Concurrency as First-Class**: Goroutines and channels, not threads and locks.

4. **Orthogonality**: Features should be independent and composable.

## When Writing Code

### Always

- Use `gofmt` — no exceptions, no debates
- Keep functions short and focused
- Use interfaces for abstraction, keep them small
- Handle errors explicitly at the call site
- Use goroutines freely, they're cheap
- Communicate via channels, not shared memory
- Name things clearly—`userCount` not `uc`

### Never

- Fight `gofmt`
- Create deep inheritance hierarchies (Go doesn't have them anyway)
- Use `interface{}` without good reason
- Ignore errors with `_`
- Use `panic` for normal error handling
- Create goroutines without knowing how they'll stop

### Prefer

- Small interfaces (1-2 methods ideal)
- Returning errors over panicking
- Channels over mutexes for coordination
- Composition over embedding over "inheritance"
- Standard library over third-party when possible
- Table-driven tests

## Code Patterns

### Composition via Embedding

```go
// NOT inheritance — composition
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose interfaces
type ReadWriter interface {
    Reader
    Writer
}

// Embed structs for composition
type CountingWriter struct {
    io.Writer        // Embedded — gets all Writer methods
    count int64
}

func (cw *CountingWriter) Write(p []byte) (int, error) {
    n, err := cw.Writer.Write(p)  // Delegate to embedded
    cw.count += int64(n)
    return n, err
}
```

### Concurrency: Share by Communicating

```go
// BAD: Sharing memory, communicating by locking
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    c.value++
    c.mu.Unlock()
}

// GOOD: Communicate via channels
func Counter() (inc func(), value func() int) {
    ch := make(chan int)
    go func() {
        count := 0
        for delta := range ch {
            if delta == 0 {
                ch <- count  // Request for value
            } else {
                count += delta
            }
        }
    }()
    return func() { ch <- 1 }, 
           func() int { ch <- 0; return <-ch }
}

// Even better: channel as work queue
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        results <- process(job)
    }
}

func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)
    
    // Start workers
    for i := 0; i < 4; i++ {
        go worker(jobs, results)
    }
    
    // Send jobs, collect results...
}
```

### Small Interfaces

```go
// BAD: Large interface
type Repository interface {
    Create(user User) error
    Read(id string) (User, error)
    Update(user User) error
    Delete(id string) error
    List() ([]User, error)
    Search(query string) ([]User, error)
    // ... and 20 more methods
}

// GOOD: Small, focused interfaces
type UserReader interface {
    Read(id string) (User, error)
}

type UserWriter interface {
    Write(user User) error
}

type UserDeleter interface {
    Delete(id string) error
}

// Compose when needed
type UserStore interface {
    UserReader
    UserWriter
}

// Functions accept minimal interface
func ProcessUser(r UserReader, id string) error {
    user, err := r.Read(id)
    // ...
}
```

### Error Handling

```go
// Errors are values — handle them
func readConfig(path string) (*Config, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, fmt.Errorf("open config: %w", err)
    }
    defer f.Close()
    
    var cfg Config
    if err := json.NewDecoder(f).Decode(&cfg); err != nil {
        return nil, fmt.Errorf("decode config: %w", err)
    }
    
    return &cfg, nil
}

// Sentinel errors for checking
var ErrNotFound = errors.New("not found")

func Find(id string) (*Item, error) {
    item, ok := store[id]
    if !ok {
        return nil, ErrNotFound
    }
    return item, nil
}

// Caller can check:
if errors.Is(err, ErrNotFound) {
    // handle not found
}
```

### Make the Zero Value Useful

```go
// BAD: Requires initialization
type Buffer struct {
    data []byte
}

func NewBuffer() *Buffer {
    return &Buffer{data: make([]byte, 0, 1024)}
}

// GOOD: Zero value works
type Buffer struct {
    data []byte
}

func (b *Buffer) Write(p []byte) (int, error) {
    b.data = append(b.data, p...)  // nil slice append works!
    return len(p), nil
}

// Can use immediately:
var buf Buffer
buf.Write([]byte("hello"))

// sync.Mutex zero value is unlocked
// sync.WaitGroup zero value is ready
// etc.
```

## Mental Model

Pike approaches software by asking:

1. **Is this necessary?** Remove anything that isn't essential
2. **Is this simple?** Can someone understand it in 30 seconds?
3. **Is this orthogonal?** Does it compose with other features?
4. **How does it fail?** Design for failure cases explicitly

## The Go Way

- No generics (until Go 1.18) — and that was intentional restraint
- No exceptions — errors are values
- No inheritance — composition only
- No operator overloading — `+` always means numeric addition
- No implicit conversions — explicit is better

Each "missing" feature is a deliberate choice for simplicity.
