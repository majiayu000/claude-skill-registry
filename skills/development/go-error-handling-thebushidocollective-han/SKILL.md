---
name: go-error-handling
description: Use when Go error handling with error wrapping, sentinel errors, and custom error types. Use when handling errors in Go applications.
allowed-tools:
  - Bash
  - Read
---

# Go Error Handling

Master Go's error handling patterns including error wrapping, sentinel
errors, custom error types, and the errors package for robust applications.

## Basic Error Handling

**Creating and returning errors:**

```go
package main

import (
    "errors"
    "fmt"
)

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}
```

**Using fmt.Errorf:**

```go
func processFile(filename string) error {
    if filename == "" {
        return fmt.Errorf("filename cannot be empty")
    }
    // Process file...
    return nil
}
```

## Error Wrapping

**Wrapping errors with context (Go 1.13+):**

```go
import (
    "errors"
    "fmt"
    "os"
)

func readConfig(path string) error {
    _, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("failed to read config: %w", err)
    }
    return nil
}

func main() {
    err := readConfig("config.json")
    if err != nil {
        fmt.Println(err)
        // Output: failed to read config: open config.json: no such file
    }
}
```

**Unwrapping errors:**

```go
func handleError(err error) {
    // Unwrap one level
    unwrapped := errors.Unwrap(err)
    if unwrapped != nil {
        fmt.Println("Unwrapped:", unwrapped)
    }

    // Check if specific error is in chain
    if errors.Is(err, os.ErrNotExist) {
        fmt.Println("File does not exist")
    }
}
```

## Sentinel Errors

**Defining and using sentinel errors:**

```go
package main

import (
    "errors"
    "fmt"
)

var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
    ErrInvalidInput = errors.New("invalid input")
)

func getUser(id int) (string, error) {
    if id < 0 {
        return "", ErrInvalidInput
    }
    if id == 0 {
        return "", ErrNotFound
    }
    return fmt.Sprintf("user-%d", id), nil
}

func main() {
    _, err := getUser(0)
    if errors.Is(err, ErrNotFound) {
        fmt.Println("User not found")
    }
}
```

## Custom Error Types

**Implementing error interface:**

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

func validateAge(age int) error {
    if age < 0 {
        return &ValidationError{
            Field:   "age",
            Message: "must be positive",
        }
    }
    if age > 150 {
        return &ValidationError{
            Field:   "age",
            Message: "must be less than 150",
        }
    }
    return nil
}

func main() {
    err := validateAge(-5)
    if err != nil {
        fmt.Println(err)
    }
}
```

**Type assertions with errors.As:**

```go
func handleValidation(err error) {
    var validationErr *ValidationError
    if errors.As(err, &validationErr) {
        fmt.Printf("Field '%s' failed: %s\n",
            validationErr.Field,
            validationErr.Message,
        )
    }
}
```

## Multi-Error Handling

**Collecting multiple errors:**

```go
type MultiError struct {
    Errors []error
}

func (m *MultiError) Error() string {
    if len(m.Errors) == 0 {
        return "no errors"
    }
    if len(m.Errors) == 1 {
        return m.Errors[0].Error()
    }
    return fmt.Sprintf("%d errors occurred: %v", len(m.Errors), m.Errors)
}

func (m *MultiError) Add(err error) {
    if err != nil {
        m.Errors = append(m.Errors, err)
    }
}

func validateUser(name, email string, age int) error {
    errs := &MultiError{}

    if name == "" {
        errs.Add(errors.New("name is required"))
    }
    if email == "" {
        errs.Add(errors.New("email is required"))
    }
    if age < 0 {
        errs.Add(errors.New("age must be positive"))
    }

    if len(errs.Errors) > 0 {
        return errs
    }
    return nil
}
```

## Panic and Recover

**When to use panic:**

```go
// Panic for unrecoverable errors
func mustConnect(dsn string) *DB {
    db, err := connect(dsn)
    if err != nil {
        panic(fmt.Sprintf("failed to connect to database: %v", err))
    }
    return db
}

// Recover from panics
func safeExecute(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()

    fn()
    return nil
}
```

## Error Handling Patterns

**Early return pattern:**

```go
func processRequest(id int) error {
    user, err := fetchUser(id)
    if err != nil {
        return fmt.Errorf("fetch user: %w", err)
    }

    if err := validateUser(user); err != nil {
        return fmt.Errorf("validate user: %w", err)
    }

    if err := saveUser(user); err != nil {
        return fmt.Errorf("save user: %w", err)
    }

    return nil
}
```

**Error variable naming:**

```go
// Good: specific error names
errDB := connectDB()
if errDB != nil {
    return fmt.Errorf("db connection: %w", errDB)
}

errCache := connectCache()
if errCache != nil {
    return fmt.Errorf("cache connection: %w", errCache)
}

// Avoid: reusing 'err' everywhere makes debugging harder
```

## pkg/errors Pattern (Legacy)

**Using github.com/pkg/errors:**

```go
import (
    "github.com/pkg/errors"
)

func loadConfig() error {
    _, err := os.Open("config.json")
    if err != nil {
        return errors.Wrap(err, "failed to load config")
    }
    return nil
}

func init() {
    if err := loadConfig(); err != nil {
        // Print stack trace
        fmt.Printf("%+v\n", err)
    }
}
```

## Error Logging

**Structured error logging:**

```go
import (
    "log/slog"
)

func processOrder(orderID string) error {
    order, err := fetchOrder(orderID)
    if err != nil {
        slog.Error("failed to fetch order",
            "orderID", orderID,
            "error", err,
        )
        return fmt.Errorf("fetch order %s: %w", orderID, err)
    }

    if err := validateOrder(order); err != nil {
        slog.Warn("order validation failed",
            "orderID", orderID,
            "error", err,
        )
        return fmt.Errorf("validate order: %w", err)
    }

    return nil
}
```

## HTTP Error Handling

**Handling HTTP errors:**

```go
import (
    "encoding/json"
    "net/http"
)

type APIError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
}

func (e *APIError) Error() string {
    return e.Message
}

func writeError(w http.ResponseWriter, err error) {
    var apiErr *APIError
    if errors.As(err, &apiErr) {
        w.WriteHeader(apiErr.Code)
        json.NewEncoder(w).Encode(apiErr)
        return
    }

    // Default error
    w.WriteHeader(http.StatusInternalServerError)
    json.NewEncoder(w).Encode(APIError{
        Code:    http.StatusInternalServerError,
        Message: "Internal server error",
    })
}

func handler(w http.ResponseWriter, r *http.Request) {
    err := processRequest(r)
    if err != nil {
        writeError(w, err)
        return
    }

    w.WriteHeader(http.StatusOK)
}
```

## Error Context

**Adding context to errors:**

```go
type ContextError struct {
    Op      string // Operation
    Path    string // File path, URL, etc.
    Err     error  // Underlying error
}

func (e *ContextError) Error() string {
    return fmt.Sprintf("%s %s: %v", e.Op, e.Path, e.Err)
}

func (e *ContextError) Unwrap() error {
    return e.Err
}

func readFile(path string) error {
    _, err := os.ReadFile(path)
    if err != nil {
        return &ContextError{
            Op:   "read",
            Path: path,
            Err:  err,
        }
    }
    return nil
}
```

## Testing Error Cases

**Testing error conditions:**

```go
package main

import (
    "errors"
    "testing"
)

func TestDivideByZero(t *testing.T) {
    _, err := divide(10, 0)
    if err == nil {
        t.Fatal("expected error, got nil")
    }

    expected := "division by zero"
    if err.Error() != expected {
        t.Errorf("expected %q, got %q", expected, err.Error())
    }
}

func TestErrorWrapping(t *testing.T) {
    err := readConfig("missing.json")
    if err == nil {
        t.Fatal("expected error")
    }

    if !errors.Is(err, os.ErrNotExist) {
        t.Error("expected wrapped ErrNotExist")
    }
}

func TestCustomError(t *testing.T) {
    err := validateAge(-1)

    var validationErr *ValidationError
    if !errors.As(err, &validationErr) {
        t.Fatal("expected ValidationError")
    }

    if validationErr.Field != "age" {
        t.Errorf("expected field 'age', got %q", validationErr.Field)
    }
}
```

## When to Use This Skill

Use go-error-handling when you need to:

- Handle errors in Go applications properly
- Add context to errors without losing information
- Define domain-specific error types
- Check for specific error conditions
- Wrap errors with additional context
- Log errors with appropriate detail
- Return errors from HTTP handlers
- Test error conditions thoroughly
- Build error-resilient systems
- Implement retry logic based on error types

## Best Practices

- Always check errors, never ignore them
- Return errors instead of logging and continuing
- Use fmt.Errorf with %w to wrap errors
- Use errors.Is for comparing sentinel errors
- Use errors.As for type assertions
- Provide context in error messages
- Use custom error types for domain errors
- Don't panic in libraries, return errors
- Log errors at appropriate levels
- Test error paths as thoroughly as happy paths

## Common Pitfalls

- Ignoring errors with _ assignment
- Not wrapping errors (losing context)
- Using == for error comparison
- Panicking instead of returning errors
- Not handling all error cases
- Creating too many custom error types
- Poorly formatted error messages
- Not testing error conditions
- Swallowing errors in goroutines
- Not providing enough context in errors

## Resources

- [Go Blog - Error Handling](https://go.dev/blog/error-handling-and-go)
- [Go Blog - Working with Errors](https://go.dev/blog/go1.13-errors)
- [Effective Go - Errors](https://go.dev/doc/effective_go#errors)
- [errors Package](https://pkg.go.dev/errors)
- [Error Handling in Go](https://go.dev/doc/tutorial/handle-errors)
