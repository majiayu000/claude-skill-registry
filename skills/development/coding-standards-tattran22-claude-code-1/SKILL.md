---
skill_id: coding-standards
name: Go Coding Standards & Conventions
description: Go coding standards, best practices, and idioms - gofmt, error handling, naming conventions, interface design, and project organization
category: standards
tags: [go, standards, conventions, best-practices, gofmt]
applies_to: [go]
auto_trigger: ["go", "golang", "standards", "conventions"]
---

# Go Coding Standards & Conventions

Production-ready Go coding standards following official Go guidelines and community best practices.

## Core Principles

### 1. gofmt is Law
- **ALWAYS** run `gofmt` before committing
- **ALWAYS** run `goimports` to manage imports
- No exceptions, no debates
- Formatting is automatic, not a choice

### 2. Simplicity Over Cleverness
- Clear code > clever code
- Explicit > implicit
- Simple solutions > complex abstractions
- Readable by junior developers

### 3. Error Handling is Not Optional
- **ALWAYS** check errors
- **NEVER** use `_` to ignore errors
- Wrap errors with context
- Return errors, don't panic

### 4. Interfaces are Small
- One or two methods max (usually)
- Accept interfaces, return structs
- Define interfaces where used, not where implemented
- Composition over inheritance

---

## 1. Naming Conventions

### 1.1 Package Names

```go
// ✅ GOOD: Short, lowercase, no underscores
package user
package handler
package repository

// ❌ BAD: Mixed case, underscores, plural
package User
package user_service
package handlers
```

### 1.2 Variable Names

```go
// ✅ GOOD: MixedCaps (not snake_case)
var marketCount int
var isAuthenticated bool
var userID string           // ID, not Id
var httpClient *http.Client // HTTP, not Http

// ❌ BAD: snake_case, unclear
var market_count int
var flag bool
var x string
```

### 1.3 Function Names

```go
// ✅ GOOD: MixedCaps, verb-noun pattern
func GetMarket(id string) (*Market, error) {}
func CreateUser(name string) error {}
func IsValidEmail(email string) bool {}

// Exported: uppercase start
func FetchProducts() ([]Product, error) {}

// Unexported: lowercase start
func parseQuery(q string) map[string]string {}

// ❌ BAD: snake_case, unclear
func get_market(id string) {}
func market(id string) {}
```

### 1.4 Constant Names

```go
// ✅ GOOD: MixedCaps (not SCREAMING_SNAKE_CASE)
const MaxRetries = 3
const DefaultTimeout = 30 * time.Second
const APIVersion = "v1"

// Unexported constants
const maxConnections = 100

// ❌ BAD: SCREAMING_SNAKE_CASE (not Go style)
const MAX_RETRIES = 3
const DEFAULT_TIMEOUT = 30
```

### 1.5 Interface Names

```go
// ✅ GOOD: Single-method interfaces end in -er
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Validator interface {
    Validate() error
}

// Multi-method interfaces: descriptive names
type MarketRepository interface {
    FindByID(ctx context.Context, id string) (*Market, error)
    Create(ctx context.Context, market *Market) error
}

// ❌ BAD: Interface prefix (not Go style)
type IReader interface {}
type ReaderInterface interface {}
```

---

## 2. Error Handling (CRITICAL)

### 2.1 Always Check Errors

```go
// ✅ GOOD: Always check errors
data, err := json.Marshal(obj)
if err != nil {
    return fmt.Errorf("failed to marshal object: %w", err)
}

result, err := db.Query(ctx, query)
if err != nil {
    return fmt.Errorf("database query failed: %w", err)
}

// ❌ BAD: Ignoring errors (NEVER DO THIS)
data, _ := json.Marshal(obj)  // WRONG
db.Query(ctx, query)          // WRONG
```

### 2.2 Error Wrapping with Context

```go
// ✅ GOOD: Wrap errors with context using %w
func (r *Repository) FindByID(ctx context.Context, id string) (*Market, error) {
    var market Market
    err := r.db.QueryRow(ctx, query, id).Scan(&market.ID, &market.Name)
    if err == pgx.ErrNoRows {
        return nil, fmt.Errorf("market %s not found: %w", id, err)
    }
    if err != nil {
        return nil, fmt.Errorf("failed to query market %s: %w", id, err)
    }
    return &market, nil
}

// ❌ BAD: Generic error, no context
if err != nil {
    return nil, err  // WRONG: loses context
}

// ❌ BAD: Using %v instead of %w (breaks error unwrapping)
if err != nil {
    return nil, fmt.Errorf("error: %v", err)  // WRONG: use %w
}
```

### 2.3 Custom Error Types

```go
// ✅ GOOD: Custom error type
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %s", e.Field, e.Message)
}

// Usage
func ValidateMarket(m *Market) error {
    if m.Name == "" {
        return &ValidationError{Field: "name", Message: "required"}
    }
    return nil
}

// Check error type
if err != nil {
    var validationErr *ValidationError
    if errors.As(err, &validationErr) {
        // Handle validation error specifically
    }
}
```

### 2.4 Sentinel Errors

```go
// ✅ GOOD: Sentinel errors for expected conditions
var (
    ErrNotFound      = errors.New("not found")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrInvalidInput  = errors.New("invalid input")
)

func GetMarket(id string) (*Market, error) {
    if id == "" {
        return nil, ErrInvalidInput
    }
    // ...
}

// Check sentinel error
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // Handle not found case
    }
}
```

---

## 3. Function Design

### 3.1 Function Length

```go
// ✅ GOOD: Short, focused functions (< 30 lines)
func (s *Service) CreateMarket(ctx context.Context, name string) error {
    if err := s.validate(name); err != nil {
        return err
    }

    market := &Market{ID: uuid.NewString(), Name: name}

    if err := s.repo.Create(ctx, market); err != nil {
        return fmt.Errorf("failed to create market: %w", err)
    }

    return nil
}

func (s *Service) validate(name string) error {
    if name == "" {
        return ErrInvalidInput
    }
    return nil
}

// ❌ BAD: Long function (> 50 lines)
func CreateMarket() {
    // 100 lines of mixed logic
}
```

### 3.2 Function Parameters

```go
// ✅ GOOD: Context first, options last
func Query(ctx context.Context, query string, args ...interface{}) error {}

// ✅ GOOD: Use struct for many parameters
type CreateMarketOptions struct {
    Name        string
    Description string
    EndDate     time.Time
    Categories  []string
}

func CreateMarket(ctx context.Context, opts CreateMarketOptions) error {}

// ❌ BAD: Too many parameters
func CreateMarket(ctx context.Context, name, desc string, endDate time.Time, cats []string) error {}
```

### 3.3 Return Values

```go
// ✅ GOOD: Return error as last value
func FetchData() ([]byte, error) {}
func ParseJSON(data []byte) (*Result, error) {}

// ✅ GOOD: Named return values for documentation
func divide(a, b float64) (result float64, err error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// ❌ BAD: Error not last
func FetchData() (error, []byte) {}
```

---

## 4. Pointer vs Value Receivers

### 4.1 When to Use Pointer Receivers

```go
// ✅ Use pointer receiver if:
// 1. Method modifies the receiver
type Counter struct {
    count int
}

func (c *Counter) Increment() {
    c.count++
}

// 2. Receiver is large struct (avoid copying)
type LargeStruct struct {
    data [1000000]byte
}

func (l *LargeStruct) Process() {
    // Avoid copying 1MB
}

// 3. Receiver contains sync.Mutex or similar
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (s *SafeCounter) Increment() {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.count++
}
```

### 4.2 When to Use Value Receivers

```go
// ✅ Use value receiver if:
// 1. Method doesn't modify receiver
type Market struct {
    ID     string
    Status string
}

func (m Market) IsActive() bool {
    return m.Status == "active"
}

// 2. Receiver is small (few fields of basic types)
type Point struct {
    X, Y int
}

func (p Point) Distance() float64 {
    return math.Sqrt(float64(p.X*p.X + p.Y*p.Y))
}

// 3. Receiver is basic type, slice, or map
type MyInt int

func (i MyInt) Double() MyInt {
    return i * 2
}
```

### 4.3 Consistency Rule

```go
// ✅ GOOD: All methods use same receiver type
type Market struct {
    ID   string
    Name string
}

func (m *Market) Save() error { return nil }
func (m *Market) Delete() error { return nil }
func (m *Market) Update() error { return nil }

// ❌ BAD: Mixed pointer and value receivers
func (m *Market) Save() error { return nil }    // pointer
func (m Market) Delete() error { return nil }   // value - INCONSISTENT
```

---

## 5. Interface Design

### 5.1 Small Interfaces

```go
// ✅ GOOD: Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// Compose interfaces
type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

// ❌ BAD: Large interface (violates ISP)
type Repository interface {
    FindAll() ([]Market, error)
    FindByID(id string) (*Market, error)
    Create(m *Market) error
    Update(m *Market) error
    Delete(id string) error
    Search(query string) ([]Market, error)
    Count() (int, error)
    Exists(id string) (bool, error)
}
```

### 5.2 Accept Interfaces, Return Structs

```go
// ✅ GOOD: Accept interface parameter
func ProcessData(r io.Reader) error {
    data, err := io.ReadAll(r)
    // ...
}

// ✅ GOOD: Return concrete type
func NewMarketRepository(db *pgxpool.Pool) *MarketRepository {
    return &MarketRepository{db: db}
}

// ❌ BAD: Return interface (usually)
func NewMarketRepository(db *pgxpool.Pool) MarketRepository {
    return &marketRepository{db: db}
}
```

### 5.3 Define Interfaces Where Used

```go
// ✅ GOOD: Define interface in consumer package
// package handler
type MarketGetter interface {
    GetMarket(ctx context.Context, id string) (*Market, error)
}

type Handler struct {
    markets MarketGetter  // accepts any implementation
}

// ❌ BAD: Define interface in provider package
// package repository
type MarketRepository interface {
    GetMarket(ctx context.Context, id string) (*Market, error)
}
```

---

## 6. Package Organization

### 6.1 Standard Project Structure

```
project-root/
├── cmd/
│   ├── api/              # API server entry point
│   │   └── main.go
│   └── worker/           # Worker entry point
│       └── main.go
├── internal/             # Private application code
│   ├── domain/           # Business entities
│   │   ├── market.go
│   │   └── order.go
│   ├── repository/       # Data access
│   │   ├── market_postgres.go
│   │   └── market_cached.go
│   ├── service/          # Business logic
│   │   └── market_service.go
│   ├── handler/          # HTTP handlers
│   │   └── market_handler.go
│   └── middleware/       # HTTP middleware
│       └── auth.go
├── pkg/                  # Public libraries (optional)
│   └── validator/
│       └── validator.go
├── migrations/           # Database migrations
│   ├── 001_create_tables.up.sql
│   └── 001_create_tables.down.sql
├── scripts/              # Build/deploy scripts
├── go.mod
└── go.sum
```

### 6.2 Package Guidelines

```go
// ✅ GOOD: Package contains related functionality
// package user contains user-related types and functions
package user

type User struct {
    ID    string
    Email string
}

func ValidateEmail(email string) bool {}
func HashPassword(password string) string {}

// ❌ BAD: Package named "utils" or "helpers"
package utils  // TOO GENERIC

// ❌ BAD: Package contains unrelated functionality
package handler  // Don't mix user, market, order handlers
```

---

## 7. Concurrency Patterns

### 7.1 Goroutines

```go
// ✅ GOOD: Use goroutines for concurrent work
func ProcessItems(items []Item) {
    var wg sync.WaitGroup
    for _, item := range items {
        wg.Add(1)
        go func(i Item) {
            defer wg.Done()
            process(i)
        }(item)  // Pass as parameter to avoid closure issues
    }
    wg.Wait()
}

// ❌ BAD: Closure variable capture issue
for _, item := range items {
    go func() {
        process(item)  // WRONG: captures loop variable
    }()
}
```

### 7.2 Channels

```go
// ✅ GOOD: Use channels for communication
func ProduceNumbers(count int) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for i := 0; i < count; i++ {
            ch <- i
        }
    }()
    return ch
}

// ✅ GOOD: Use select for multiple channels
select {
case msg := <-ch1:
    handleMessage(msg)
case <-ctx.Done():
    return ctx.Err()
case <-time.After(5 * time.Second):
    return errors.New("timeout")
}
```

### 7.3 Context Usage

```go
// ✅ GOOD: Pass context as first parameter
func FetchData(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}

// ✅ GOOD: Check context cancellation
func LongOperation(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            // Continue processing
        }
    }
}

// ❌ BAD: Don't pass context in struct
type Handler struct {
    ctx context.Context  // WRONG
}
```

---

## 8. Code Organization

### 8.1 Import Groups

```go
// ✅ GOOD: Imports grouped and sorted by goimports
import (
    // Standard library
    "context"
    "encoding/json"
    "fmt"
    "time"

    // External packages
    "github.com/gofiber/fiber/v3"
    "github.com/jackc/pgx/v5/pgxpool"

    // Internal packages
    "yourapp/internal/domain"
    "yourapp/internal/repository"
)

// ❌ BAD: Mixed imports, not grouped
import (
    "github.com/gofiber/fiber/v3"
    "fmt"
    "yourapp/internal/domain"
    "context"
)
```

### 8.2 Variable Declarations

```go
// ✅ GOOD: Use := for local variables
func example() {
    name := "John"
    count := 42
}

// ✅ GOOD: Use var for zero values
var (
    count int
    name  string
    data  []byte
)

// ✅ GOOD: Group related var declarations
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

// ❌ BAD: Unnecessary var keyword
var name string = "John"  // Use name := "John"
```

---

## 9. Testing Standards

### 9.1 Table-Driven Tests

```go
// ✅ GOOD: Table-driven tests
func TestIsValidEmail(t *testing.T) {
    tests := []struct {
        name  string
        email string
        want  bool
    }{
        {
            name:  "valid email",
            email: "user@example.com",
            want:  true,
        },
        {
            name:  "missing @",
            email: "userexample.com",
            want:  false,
        },
        {
            name:  "empty email",
            email: "",
            want:  false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := IsValidEmail(tt.email)
            if got != tt.want {
                t.Errorf("IsValidEmail(%q) = %v, want %v", tt.email, got, tt.want)
            }
        })
    }
}
```

### 9.2 Test Helpers

```go
// ✅ GOOD: Use t.Helper() in test helpers
func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func assertEqual(t *testing.T, got, want interface{}) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

---

## 10. Best Practices Summary

### ✅ DO

```go
// ✅ Run gofmt and goimports
go fmt ./...
goimports -w .

// ✅ Always check errors
data, err := json.Marshal(obj)
if err != nil {
    return fmt.Errorf("marshal failed: %w", err)
}

// ✅ Use context for cancellation
func Fetch(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    }
}

// ✅ Defer cleanup
file, err := os.Open("file.txt")
if err != nil {
    return err
}
defer file.Close()

// ✅ Use meaningful names
marketCount := len(markets)
isAuthenticated := checkAuth()

// ✅ Keep functions small (< 30 lines)
func CreateMarket(ctx context.Context, name string) error {
    if err := validate(name); err != nil {
        return err
    }
    return save(ctx, name)
}

// ✅ Use table-driven tests
tests := []struct{ input, want string }{
    {"hello", "HELLO"},
    {"world", "WORLD"},
}

// ✅ Accept interfaces, return structs
func Process(r io.Reader) *Result {}

// ✅ Use pointer receivers consistently
func (m *Market) Save() error {}
func (m *Market) Delete() error {}
```

### ❌ DON'T

```go
// ❌ Never ignore errors
data, _ := json.Marshal(obj)  // WRONG

// ❌ Don't use snake_case
var user_id string  // WRONG

// ❌ Don't use SCREAMING_SNAKE_CASE for constants
const MAX_RETRIES = 3  // WRONG

// ❌ Don't use interface prefix
type IReader interface {}  // WRONG

// ❌ Don't panic in libraries (return errors)
if err != nil {
    panic(err)  // WRONG (except in init, main, or truly unrecoverable)
}

// ❌ Don't use generic package names
package utils   // WRONG
package helpers // WRONG
package common  // WRONG

// ❌ Don't mix pointer and value receivers
func (m *Market) Save() error {}   // pointer
func (m Market) Delete() error {}  // value - INCONSISTENT

// ❌ Don't pass context in struct
type Handler struct {
    ctx context.Context  // WRONG
}

// ❌ Don't use %v for error wrapping (use %w)
return fmt.Errorf("failed: %v", err)  // WRONG
return fmt.Errorf("failed: %w", err)  // CORRECT
```

---

## 11. Code Comments

### 11.1 Package Documentation

```go
// ✅ GOOD: Package comment before package declaration
// Package user provides user authentication and management.
//
// This package handles user registration, login, password hashing,
// and session management.
package user
```

### 11.2 Function Documentation (godoc)

```go
// ✅ GOOD: Document exported functions
// GetMarket retrieves a market by its ID.
// It returns ErrNotFound if the market doesn't exist.
func GetMarket(ctx context.Context, id string) (*Market, error) {
    // ...
}

// CreateMarket creates a new market with the given options.
// The market name must be unique and non-empty.
//
// Example:
//
//	market, err := CreateMarket(ctx, CreateMarketOptions{
//	    Name: "Election 2024",
//	    EndDate: time.Now().Add(30 * 24 * time.Hour),
//	})
func CreateMarket(ctx context.Context, opts CreateMarketOptions) (*Market, error) {
    // ...
}
```

### 11.3 When to Comment

```go
// ✅ GOOD: Explain WHY, not WHAT
// Use exponential backoff to avoid overwhelming the API during outages
delay := time.Duration(1<<uint(attempt)) * time.Second

// HACK: Workaround for upstream library bug (issue #123)
// Remove once fixed in v2.0
result = strings.TrimSpace(result)

// ❌ BAD: Stating the obvious
// Increment counter by 1
counter++

// Set name to user's name
name = user.Name
```

---

## Quick Reference

### File Header
```go
package user

import (
    "context"
    "errors"
)
```

### Error Handling
```go
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

### Naming
- Packages: `user`, `handler` (lowercase, no underscores)
- Variables: `marketCount`, `userID` (MixedCaps)
- Constants: `MaxRetries` (MixedCaps, not SCREAMING)
- Functions: `GetMarket`, `isValid` (exported: uppercase, unexported: lowercase)
- Interfaces: `Reader`, `Writer` (single method: -er suffix)

### Formatting
```bash
gofmt -w .
goimports -w .
```

---

## Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
- [Go Proverbs](https://go-proverbs.github.io/)

---

**Remember**: Go has strong conventions. Follow them. They're not suggestions—they're how Go code is written.
