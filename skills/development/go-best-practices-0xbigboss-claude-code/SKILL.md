---
name: go-best-practices
description: Provides Go patterns for type-first development with custom types, interfaces, functional options, and error handling. Must use when reading or writing Go files.
---

# Go Best Practices

## Type-First Development

Types define the contract before implementation. Follow this workflow:

1. **Define data structures** - structs and interfaces first
2. **Define function signatures** - parameters, return types, and error conditions
3. **Implement to satisfy types** - let the compiler guide completeness
4. **Validate at boundaries** - check inputs where data enters the system

### Make Illegal States Unrepresentable

Use Go's type system to prevent invalid states at compile time.

**Structs for domain models:**
```go
// Define the data model first
type User struct {
    ID        UserID
    Email     string
    Name      string
    CreatedAt time.Time
}

type CreateUserRequest struct {
    Email string
    Name  string
}

// Functions follow from the types
func CreateUser(req CreateUserRequest) (*User, error) {
    // implementation
}
```

**Custom types for domain primitives:**
```go
// Distinct types prevent mixing up IDs
type UserID string
type OrderID string

func GetUser(id UserID) (*User, error) {
    // Compiler prevents passing OrderID here
}

func NewUserID(raw string) UserID {
    return UserID(raw)
}

// Methods attach behavior to the type
func (id UserID) String() string {
    return string(id)
}
```

**Interfaces for behavior contracts:**
```go
// Define what you need, not what you have
type Reader interface {
    Read(p []byte) (n int, err error)
}

type UserRepository interface {
    GetByID(ctx context.Context, id UserID) (*User, error)
    Save(ctx context.Context, user *User) error
}

// Accept interfaces, return structs
func ProcessInput(r Reader) ([]byte, error) {
    return io.ReadAll(r)
}
```

**Enums with iota:**
```go
type Status int

const (
    StatusActive Status = iota + 1
    StatusInactive
    StatusPending
)

func (s Status) String() string {
    switch s {
    case StatusActive:
        return "active"
    case StatusInactive:
        return "inactive"
    case StatusPending:
        return "pending"
    default:
        return fmt.Sprintf("Status(%d)", s)
    }
}

// Exhaustive handling in switch
func ProcessStatus(s Status) (string, error) {
    switch s {
    case StatusActive:
        return "processing", nil
    case StatusInactive:
        return "skipped", nil
    case StatusPending:
        return "waiting", nil
    default:
        return "", fmt.Errorf("unhandled status: %v", s)
    }
}
```

**Functional options for flexible construction:**
```go
type ServerOption func(*Server)

func WithPort(port int) ServerOption {
    return func(s *Server) {
        s.port = port
    }
}

func WithTimeout(d time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(opts ...ServerOption) *Server {
    s := &Server{
        port:    8080,    // sensible defaults
        timeout: 30 * time.Second,
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage: NewServer(WithPort(3000), WithTimeout(time.Minute))
```

**Embed for composition:**
```go
type Timestamps struct {
    CreatedAt time.Time
    UpdatedAt time.Time
}

type User struct {
    Timestamps  // embedded - User has CreatedAt, UpdatedAt
    ID    UserID
    Email string
}
```

## Module Structure

Prefer smaller files within packages: one type or concern per file. Split when a file handles multiple unrelated types or exceeds ~300 lines. Keep tests in `_test.go` files alongside implementation. Package boundaries define the API; internal organization is flexible.

## Functional Patterns

- Use value receivers when methods don't mutate state; reserve pointer receivers for mutation.
- Avoid package-level mutable variables; pass dependencies explicitly via function parameters.
- Return new structs/slices rather than mutating inputs; makes data flow explicit.
- Use closures and higher-order functions where they simplify code (e.g., `sort.Slice`, iterators).

## Instructions

- Return errors with context using `fmt.Errorf` and `%w` for wrapping. This preserves the error chain for debugging.
- Every function returns a value or an error; unimplemented paths return descriptive errors. Explicit failures are debuggable.
- Handle all branches in `switch` statements; include a `default` case that returns an error. Exhaustive handling prevents silent bugs.
- Pass `context.Context` to external calls with explicit timeouts. Runaway requests cause cascading failures.
- Reserve `panic` for truly unrecoverable situations; prefer returning errors. Panics crash the program.
- Add or update table-driven tests for new logic; cover edge cases (empty input, nil, boundaries).

## Examples

Explicit failure for unimplemented logic:
```go
func buildWidget(widgetType string) (*Widget, error) {
    return nil, fmt.Errorf("buildWidget not implemented for type: %s", widgetType)
}
```

Wrap errors with context to preserve the chain:
```go
out, err := client.Do(ctx, req)
if err != nil {
    return nil, fmt.Errorf("fetch widget failed: %w", err)
}
return out, nil
```

Exhaustive switch with default error:
```go
func processStatus(status string) (string, error) {
    switch status {
    case "active":
        return "processing", nil
    case "inactive":
        return "skipped", nil
    default:
        return "", fmt.Errorf("unhandled status: %s", status)
    }
}
```

Structured logging with slog:
```go
import "log/slog"

var log = slog.With("component", "widgets")

func createWidget(name string) (*Widget, error) {
    log.Debug("creating widget", "name", name)
    widget := &Widget{Name: name}
    log.Debug("created widget", "id", widget.ID)
    return widget, nil
}
```

## Configuration

- Load config from environment variables at startup; validate required values before use. Missing config should cause immediate exit.
- Define a Config struct as single source of truth; avoid `os.Getenv` scattered throughout code.
- Use sensible defaults for development; require explicit values for production secrets.

### Examples

Typed config struct:
```go
type Config struct {
    Port        int
    DatabaseURL string
    APIKey      string
    Env         string
}

func LoadConfig() (*Config, error) {
    dbURL := os.Getenv("DATABASE_URL")
    if dbURL == "" {
        return nil, fmt.Errorf("DATABASE_URL is required")
    }
    apiKey := os.Getenv("API_KEY")
    if apiKey == "" {
        return nil, fmt.Errorf("API_KEY is required")
    }
    port := 3000
    if p := os.Getenv("PORT"); p != "" {
        var err error
        port, err = strconv.Atoi(p)
        if err != nil {
            return nil, fmt.Errorf("invalid PORT: %w", err)
        }
    }
    return &Config{
        Port:        port,
        DatabaseURL: dbURL,
        APIKey:      apiKey,
        Env:         getEnvOrDefault("ENV", "development"),
    }, nil
}
```
