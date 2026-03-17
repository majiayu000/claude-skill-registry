---
name: go-defensive
description: Defensive programming patterns in Go including interface verification, slice/map copying at boundaries, time handling, avoiding globals, and defer for cleanup. Use when writing robust, production-quality Go code.
---

# Go Defensive Programming Patterns

## Verify Interface Compliance

> **Source**: Uber Go Style Guide

Verify interface compliance at compile time using zero-value assertions.

**Bad**
```go
type Handler struct{}

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  // ...
}
```

**Good**
```go
type Handler struct{}

var _ http.Handler = (*Handler)(nil)

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  // ...
}
```

Use `nil` for pointer types, slices, maps; empty struct `{}` for value receivers.

## Copy Slices and Maps at Boundaries

> **Source**: Uber Go Style Guide

Slices and maps contain pointers. Copy at API boundaries to prevent unintended modifications.

### Receiving

**Bad**
```go
func (d *Driver) SetTrips(trips []Trip) {
  d.trips = trips  // caller can still modify d.trips
}
```

**Good**
```go
func (d *Driver) SetTrips(trips []Trip) {
  d.trips = make([]Trip, len(trips))
  copy(d.trips, trips)
}
```

### Returning

**Bad**
```go
func (s *Stats) Snapshot() map[string]int {
  s.mu.Lock()
  defer s.mu.Unlock()
  return s.counters  // exposes internal state!
}
```

**Good**
```go
func (s *Stats) Snapshot() map[string]int {
  s.mu.Lock()
  defer s.mu.Unlock()
  result := make(map[string]int, len(s.counters))
  for k, v := range s.counters {
    result[k] = v
  }
  return result
}
```

## Defer to Clean Up

> **Source**: Uber Go Style Guide, Effective Go

Use `defer` to clean up resources (files, locks). Avoids missed cleanup on multiple returns.

**Bad**
```go
p.Lock()
if p.count < 10 {
  p.Unlock()
  return p.count
}
p.count++
newCount := p.count
p.Unlock()
return newCount  // easy to miss unlocks
```

**Good**
```go
p.Lock()
defer p.Unlock()

if p.count < 10 {
  return p.count
}
p.count++
return p.count
```

Defer overhead is negligible. Only avoid in nanosecond-critical paths.

### Defer for File Operations

Place `defer f.Close()` immediately after opening a file for clarity:

```go
func Contents(filename string) (string, error) {
    f, err := os.Open(filename)
    if err != nil {
        return "", err
    }
    defer f.Close()  // Close sits near Open - much clearer

    var result []byte
    buf := make([]byte, 100)
    for {
        n, err := f.Read(buf[0:])
        result = append(result, buf[0:n]...)
        if err != nil {
            if err == io.EOF {
                break
            }
            return "", err  // f will be closed
        }
    }
    return string(result), nil  // f will be closed
}
```

### Defer Argument Evaluation

Arguments to deferred functions are evaluated when `defer` executes, not when the
deferred function runs:

```go
for i := 0; i < 5; i++ {
    defer fmt.Printf("%d ", i)
}
// Prints: 4 3 2 1 0 (LIFO order, values captured at defer time)
```

### Defer LIFO Order

Multiple defers execute in Last-In-First-Out order:

```go
func trace(s string) string {
    fmt.Println("entering:", s)
    return s
}

func un(s string) {
    fmt.Println("leaving:", s)
}

func a() {
    defer un(trace("a"))  // trace() runs now, un() runs at return
    fmt.Println("in a")
}
// Output: entering: a, in a, leaving: a
```

## Start Enums at One

> **Source**: Uber Go Style Guide

Start enums at non-zero to distinguish uninitialized from valid values.

**Bad**
```go
const (
  Add Operation = iota  // Add=0, zero value looks valid
  Subtract
  Multiply
)
```

**Good**
```go
const (
  Add Operation = iota + 1  // Add=1, zero value = uninitialized
  Subtract
  Multiply
)
```

**Exception**: When zero is the sensible default (e.g., `LogToStdout = iota`).

## Use time.Time and time.Duration

> **Source**: Uber Go Style Guide

Always use the `time` package. Avoid raw `int` for time values.

### Instants

**Bad**
```go
func isActive(now, start, stop int) bool {
  return start <= now && now < stop
}
```

**Good**
```go
func isActive(now, start, stop time.Time) bool {
  return (start.Before(now) || start.Equal(now)) && now.Before(stop)
}
```

### Durations

**Bad**
```go
func poll(delay int) {
  time.Sleep(time.Duration(delay) * time.Millisecond)
}
poll(10)  // seconds? milliseconds?
```

**Good**
```go
func poll(delay time.Duration) {
  time.Sleep(delay)
}
poll(10 * time.Second)
```

### JSON Fields

When `time.Duration` isn't possible, include unit in field name:

**Bad**
```go
type Config struct {
  Interval int `json:"interval"`
}
```

**Good**
```go
type Config struct {
  IntervalMillis int `json:"intervalMillis"`
}
```

## Avoid Mutable Globals

> **Source**: Uber Go Style Guide

Use dependency injection instead of mutable globals.

**Bad**
```go
var _timeNow = time.Now

func sign(msg string) string {
  now := _timeNow()
  return signWithTime(msg, now)
}

// Test requires save/restore of global
func TestSign(t *testing.T) {
  oldTimeNow := _timeNow
  _timeNow = func() time.Time { return someFixedTime }
  defer func() { _timeNow = oldTimeNow }()
  assert.Equal(t, want, sign(give))
}
```

**Good**
```go
type signer struct {
  now func() time.Time
}

func newSigner() *signer {
  return &signer{now: time.Now}
}

func (s *signer) Sign(msg string) string {
  now := s.now()
  return signWithTime(msg, now)
}

// Test injects dependency cleanly
func TestSigner(t *testing.T) {
  s := newSigner()
  s.now = func() time.Time { return someFixedTime }
  assert.Equal(t, want, s.Sign(give))
}
```

## Avoid Embedding Types in Public Structs

> **Source**: Uber Go Style Guide

Embedded types leak implementation details and inhibit type evolution.

**Bad**
```go
type ConcreteList struct {
  *AbstractList
}
```

**Good**
```go
type ConcreteList struct {
  list *AbstractList
}

func (l *ConcreteList) Add(e Entity) {
  l.list.Add(e)
}

func (l *ConcreteList) Remove(e Entity) {
  l.list.Remove(e)
}
```

Embedding problems:
- Adding methods to embedded interface is a breaking change
- Removing methods from embedded struct is a breaking change
- Replacing the embedded type is a breaking change

## Use Field Tags in Marshaled Structs

> **Source**: Uber Go Style Guide

Always use explicit field tags for JSON, YAML, etc.

**Bad**
```go
type Stock struct {
  Price int
  Name  string
}
```

**Good**
```go
type Stock struct {
  Price int    `json:"price"`
  Name  string `json:"name"`
  // Safe to rename Name to Symbol
}
```

Tags make the serialization contract explicit and safe to refactor.

---

## Crypto Rand

> **Source**: Go Wiki CodeReviewComments (Normative)

Do not use `math/rand` or `math/rand/v2` to generate keys, even throwaway ones. This is a **security concern**.

Unseeded or time-seeded random generators have predictable output:
- `Time.Nanoseconds()` provides only a few bits of entropy
- Keys generated this way can be guessed by attackers

**Use `crypto/rand` instead:**

```go
import (
	"crypto/rand"
)

func Key() string {
	return rand.Text()
}
```

For text output:
- Use `crypto/rand.Text` directly (preferred)
- Or encode random bytes with `encoding/hex` or `encoding/base64`

---

## Panic and Recover

> **Source**: Effective Go

Use `panic` only for truly unrecoverable situations. Library functions should avoid panic—if the problem can be worked around, let things continue rather than taking down the whole program.

Use `recover` to regain control of a panicking goroutine (only works inside deferred functions):

```go
func safelyDo(work *Work) {
    defer func() {
        if err := recover(); err != nil {
            log.Println("work failed:", err)
        }
    }()
    do(work)
}
```

**Key rules:**
- Never expose panics across package boundaries—always convert to errors
- Acceptable to panic in `init()` if a library truly cannot set itself up
- Use recover to isolate panics in server goroutine handlers

For detailed patterns including server protection and package-internal panic/recover, see [references/PANIC-RECOVER.md](references/PANIC-RECOVER.md).

---

## Quick Reference

| Pattern | Rule |
|---------|------|
| Interface compliance | `var _ Interface = (*Type)(nil)` |
| Receiving slices/maps | Copy before storing |
| Returning slices/maps | Return a copy |
| Resource cleanup | Use `defer` |
| Defer argument timing | Evaluated at defer, not call time |
| Enums | Start at `iota + 1` |
| Time instants | Use `time.Time` |
| Time durations | Use `time.Duration` |
| Mutable globals | Use dependency injection |
| Type embedding | Use explicit delegation |
| Serialization | Always use field tags |
| Key generation | Use `crypto/rand`, never `math/rand` |
| Panic usage | Only for truly unrecoverable situations |
| Recover pattern | Use in defer; convert to error at API boundary |

## See Also

- `go-style-core` - Core Go style principles
- `go-concurrency` - Goroutine and channel patterns
- `go-error-handling` - Error handling best practices
