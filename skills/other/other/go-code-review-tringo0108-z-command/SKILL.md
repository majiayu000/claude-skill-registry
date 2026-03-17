---
name: go-code-review
description: Master Go code review patterns including error handling, goroutine management, race conditions, interface design, and testing. Use PROACTIVELY when reviewing Go PRs.
---

# Go Code Review

Comprehensive code review checklist and patterns for Go applications, focusing on error handling, concurrency, interface design, and idiomatic Go practices.

## When to Use This Skill

- Reviewing Go pull requests
- Establishing Go code review standards
- Training reviewers on Go-specific issues
- Catching concurrency bugs and race conditions
- Ensuring idiomatic Go patterns

## Quick Checklist

```markdown
## Go Review Checklist

- [ ] All errors checked or explicitly ignored with comment
- [ ] Errors wrapped with context using fmt.Errorf %w
- [ ] No goroutine leaks (context cancellation handled)
- [ ] Race conditions checked (run with -race flag)
- [ ] Defer not inside loops
- [ ] Interfaces are small and accepted, structs returned
- [ ] Table-driven tests used
- [ ] No naked returns in long functions
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Error Handling

### Ignoring Errors

```go
// ❌ Ignoring error silently - bugs go unnoticed
file, _ := os.Open(filename)
defer file.Close()

// ✅ Handle or explicitly ignore with comment
file, err := os.Open(filename)
if err != nil {
    return fmt.Errorf("opening file %s: %w", filename, err)
}
defer file.Close()

// ✅ If truly intentional, document why
_ = file.Close() // Intentionally ignored: already handled error on Write
```

### Errors Without Context

```go
// ❌ Error without context - hard to debug
func processOrder(orderID string) error {
    order, err := db.GetOrder(orderID)
    if err != nil {
        return err  // Which order? What operation?
    }
    // ...
}

// ✅ Wrap errors with context
func processOrder(orderID string) error {
    order, err := db.GetOrder(orderID)
    if err != nil {
        return fmt.Errorf("getting order %s: %w", orderID, err)
    }
    // ...
}
```

### Error Comparison

```go
// ❌ Direct error comparison - fails with wrapped errors
if err == sql.ErrNoRows {
    return nil
}

// ✅ Use errors.Is for wrapped errors
if errors.Is(err, sql.ErrNoRows) {
    return nil
}

// ✅ Use errors.As for type assertions
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    log.Printf("Path error on: %s", pathErr.Path)
}
```

### Nested Error Checks

```go
// ❌ Nested error checks hurt readability
if err := step1(); err == nil {
    if err := step2(); err == nil {
        if err := step3(); err == nil {
            return nil
        } else {
            return err
        }
    } else {
        return err
    }
} else {
    return err
}

// ✅ Early returns, happy path at minimal indent
if err := step1(); err != nil {
    return fmt.Errorf("step1: %w", err)
}
if err := step2(); err != nil {
    return fmt.Errorf("step2: %w", err)
}
if err := step3(); err != nil {
    return fmt.Errorf("step3: %w", err)
}
return nil
```

### Custom Error Types

```go
// ❌ String errors without additional context
func validate(name string) error {
    if name == "" {
        return errors.New("name is required")
    }
    return nil
}

// ✅ Custom error types for rich errors
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

func validate(name string) error {
    if name == "" {
        return &ValidationError{Field: "name", Message: "is required"}
    }
    return nil
}
```

---

## Concurrency Issues

### Goroutine Leaks

```go
// ❌ Goroutine leak - no way to stop
func startWorker() {
    go func() {
        for {
            processItem()  // Runs forever!
        }
    }()
}

// ✅ Use context for cancellation
func startWorker(ctx context.Context) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return  // Clean exit
            default:
                processItem()
            }
        }
    }()
}
```

### Race Conditions

```go
// ❌ Race condition - shared variable access
var counter int

func increment() {
    go func() { counter++ }()  // DATA RACE!
    go func() { counter++ }()
}

// ✅ Use mutex
var (
    counter int
    mu      sync.Mutex
)

func increment() {
    mu.Lock()
    counter++
    mu.Unlock()
}

// ✅ Or use atomic for simple operations
var counter int64

func incrementAtomic() {
    atomic.AddInt64(&counter, 1)
}
```

### RWMutex for Read-Heavy Workloads

```go
// ❌ Using Mutex for read-heavy workload
var (
    cache = make(map[string]string)
    mu    sync.Mutex
)

func get(key string) string {
    mu.Lock()  // Blocks other readers!
    defer mu.Unlock()
    return cache[key]
}

// ✅ Use RWMutex for better concurrency
var (
    cache = make(map[string]string)
    mu    sync.RWMutex
)

func get(key string) string {
    mu.RLock()  // Multiple readers allowed
    defer mu.RUnlock()
    return cache[key]
}

func set(key, value string) {
    mu.Lock()
    defer mu.Unlock()
    cache[key] = value
}
```

### Defer in Loops

```go
// ❌ Defer in loop - accumulates, runs at function end
func processFiles(files []string) error {
    for _, f := range files {
        file, _ := os.Open(f)
        defer file.Close()  // All close at END of function!
    }
    return nil
}

// ✅ Extract to function or close inline
func processFiles(files []string) error {
    for _, f := range files {
        if err := processFile(f); err != nil {
            return err
        }
    }
    return nil
}

func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close()  // Closes when this function returns
    // process...
    return nil
}
```

### Channel Operations

```go
// ❌ Sending on closed channel - panics!
func producer(ch chan int) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
    ch <- 11  // PANIC: send on closed channel
}

// ✅ Only sender closes, receiver uses range
func producer(ch chan<- int) {
    defer close(ch)  // Always close at end
    for i := 0; i < 10; i++ {
        ch <- i
    }
}

func consumer(ch <-chan int) {
    for v := range ch {  // Exits when channel closed
        process(v)
    }
}
```

### WaitGroup Misuse

```go
// ❌ WaitGroup counter wrong
func process(items []string) {
    var wg sync.WaitGroup
    wg.Add(1)  // Wrong count!

    for _, item := range items {
        go func(item string) {
            defer wg.Done()
            handle(item)
        }(item)
    }
    wg.Wait()  // Will panic or hang!
}

// ✅ Add for each goroutine
func process(items []string) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)  // Add before goroutine
        go func(item string) {
            defer wg.Done()
            handle(item)
        }(item)
    }
    wg.Wait()
}
```

### Loop Variable Capture

```go
// ❌ Loop variable captured by reference (Go < 1.22)
for _, item := range items {
    go func() {
        process(item)  // All goroutines see same item!
    }()
}

// ✅ Pass as argument (required before Go 1.22)
for _, item := range items {
    go func(item string) {
        process(item)
    }(item)
}

// Note: Go 1.22+ fixes this with per-iteration loop variables
```

---

## Interface Design

### Large Interfaces

```go
// ❌ Large interface - hard to implement/mock
type UserService interface {
    GetUser(id string) (*User, error)
    CreateUser(u *User) error
    UpdateUser(u *User) error
    DeleteUser(id string) error
    ListUsers() ([]*User, error)
    GetUserByEmail(email string) (*User, error)
    ValidateUser(u *User) error
    // ... 10 more methods
}

// ✅ Small, focused interfaces
type UserGetter interface {
    GetUser(id string) (*User, error)
}

type UserCreator interface {
    CreateUser(u *User) error
}

// Compose when needed
type UserRepository interface {
    UserGetter
    UserCreator
}
```

### Returning Interfaces

```go
// ❌ Return interface - hides implementation details
func NewCache() Cache {
    return &memoryCache{}  // Caller can't access implementation
}

// ✅ Accept interfaces, return structs
func NewMemoryCache() *MemoryCache {
    return &MemoryCache{}
}

// Consumer uses interface
func ProcessWithCache(cache Cache) {
    // ...
}
```

### Interface Placement

```go
// ❌ Interface defined by implementer (Java style)
// In package: userservice
type UserService interface {
    GetUser(id string) (*User, error)
}

type userServiceImpl struct{}

func (s *userServiceImpl) GetUser(id string) (*User, error) { ... }

// ✅ Interface defined by consumer (Go style)
// In package: handler
type UserGetter interface {  // Only methods handler needs
    GetUser(id string) (*domain.User, error)
}

type Handler struct {
    users UserGetter  // Any impl with GetUser works
}
```

---

## Testing Patterns

### Table-Driven Tests

```go
// ❌ Repetitive tests
func TestAdd(t *testing.T) {
    if Add(1, 2) != 3 {
        t.Error("1+2 should be 3")
    }
    if Add(0, 0) != 0 {
        t.Error("0+0 should be 0")
    }
    if Add(-1, 1) != 0 {
        t.Error("-1+1 should be 0")
    }
}

// ✅ Table-driven tests
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 1, 2, 3},
        {"zeros", 0, 0, 0},
        {"negative and positive", -1, 1, 0},
        {"large numbers", 1000000, 1000000, 2000000},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Subtest Parallel Execution

```go
// ✅ Parallel subtests for faster execution
func TestUserService(t *testing.T) {
    tests := []struct {
        name string
        // ...
    }{
        {"create user", /* ... */},
        {"delete user", /* ... */},
    }

    for _, tt := range tests {
        tt := tt  // Capture range variable (Go < 1.22)
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()  // Run subtests in parallel
            // test logic...
        })
    }
}
```

### Test Helpers

```go
// ❌ Repetitive test setup
func TestGetUser(t *testing.T) {
    db, err := sql.Open("postgres", "...")
    if err != nil {
        t.Fatal(err)
    }
    defer db.Close()
    // test...
}

func TestCreateUser(t *testing.T) {
    db, err := sql.Open("postgres", "...")  // Duplicated!
    if err != nil {
        t.Fatal(err)
    }
    defer db.Close()
    // test...
}

// ✅ Test helper function
func setupDB(t *testing.T) *sql.DB {
    t.Helper()  // Marks as helper for better error reporting

    db, err := sql.Open("postgres", "...")
    if err != nil {
        t.Fatal(err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}

func TestGetUser(t *testing.T) {
    db := setupDB(t)
    // test...
}
```

---

## Code Style

### Naked Returns

```go
// ❌ Naked returns in long functions - hard to follow
func process(data []byte) (result string, err error) {
    // ... 50 lines of code ...

    if condition {
        result = "value"
        return  // What's being returned?
    }

    // ... 20 more lines ...
    return
}

// ✅ Explicit returns for clarity
func process(data []byte) (string, error) {
    // ... 50 lines of code ...

    if condition {
        return "value", nil
    }

    // ... 20 more lines ...
    return result, nil
}
```

### Variable Shadowing

```go
// ❌ Variable shadowing - confusing
func process(err error) error {
    if condition {
        err := doSomething()  // Shadows outer err!
        if err != nil {
            return err
        }
    }
    return err  // Returns original err, not inner one!
}

// ✅ Use different names or explicit assignment
func process(err error) error {
    if condition {
        innerErr := doSomething()
        if innerErr != nil {
            return innerErr
        }
    }
    return err
}
```

### Package Naming

```go
// ❌ Stuttering - package name repeated in type
package user

type UserService struct{}  // user.UserService

// ✅ Don't repeat package name
package user

type Service struct{}  // user.Service
```

---

## Common Pitfalls

| Pitfall               | Problem           | Solution                  |
| --------------------- | ----------------- | ------------------------- |
| Ignored error         | Silent failures   | Check all errors          |
| No error context      | Hard to debug     | Wrap with `%w`            |
| Goroutine leak        | Memory leak       | Use context cancellation  |
| Defer in loop         | Resource leak     | Extract to function       |
| Send on closed chan   | Panic             | Only sender closes        |
| Large interfaces      | Hard to implement | Small, focused interfaces |
| Loop variable capture | Wrong value       | Pass as argument          |
| Naked returns         | Hard to read      | Explicit returns          |

## Best Practices Summary

1. **Handle All Errors** - Never `_` an error without comment
2. **Wrap Errors** - Add context with `fmt.Errorf("%w")`
3. **Use Context** - For cancellation and timeouts
4. **Small Interfaces** - 1-3 methods max
5. **Table-Driven Tests** - For comprehensive coverage
6. **Early Returns** - Keep happy path at minimal indent
7. **Run Race Detector** - `go test -race`
8. **Document Why** - Not what (code shows what)


## Parent Hub
- [_backend-mastery](../_backend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
