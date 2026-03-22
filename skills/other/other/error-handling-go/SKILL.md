---
name: error-handling-go
description: >
  Implement robust Go error handling with wrapping, sentinel errors, and custom types.
  Use when the user handles errors in Go, creates custom error types, wraps errors
  with fmt.Errorf and %w, uses errors.Is/As, or asks about Go error best practices
  and error propagation strategies.
---

# Go Error Handling

Handle errors in Go the idiomatic way: explicit checking, structured wrapping,
and type-safe error inspection for reliable, debuggable programs.

## When to Use
- Returning and checking errors in Go functions
- Creating custom error types for domain-specific failures
- Wrapping errors to add context as they propagate up the call stack
- Matching specific error conditions with errors.Is or errors.As
- Handling multiple errors from concurrent operations

## Core Patterns

### Pattern 1: Error Wrapping with fmt.Errorf %w

Add context at each call layer so the final error tells the full story.

```go
func GetUser(ctx context.Context, id string) (*User, error) {
    row := db.QueryRowContext(ctx, "SELECT name, email FROM users WHERE id = $1", id)

    var user User
    if err := row.Scan(&user.Name, &user.Email); err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("user %s not found: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("querying user %s: %w", id, err)
    }

    return &user, nil
}

func HandleGetUser(w http.ResponseWriter, r *http.Request) {
    user, err := GetUser(r.Context(), r.PathValue("id"))
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            http.Error(w, "user not found", http.StatusNotFound)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

### Pattern 2: Sentinel Errors

Define package-level errors for known, expected failure conditions.

```go
package user

import "errors"

var (
    ErrNotFound      = errors.New("user not found")
    ErrAlreadyExists = errors.New("user already exists")
    ErrInvalidEmail  = errors.New("invalid email address")
)

func Create(ctx context.Context, email string) (*User, error) {
    if !isValidEmail(email) {
        return nil, ErrInvalidEmail
    }

    existing, err := findByEmail(ctx, email)
    if err != nil && !errors.Is(err, ErrNotFound) {
        return nil, fmt.Errorf("checking existing user: %w", err)
    }
    if existing != nil {
        return nil, fmt.Errorf("email %s: %w", email, ErrAlreadyExists)
    }

    // ... create user
    return &User{Email: email}, nil
}
```

### Pattern 3: Custom Error Types

Use struct errors when you need to carry additional context (codes, fields, metadata).

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}

type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with id %s not found", e.Resource, e.ID)
}

// Check with errors.As
func handleError(err error) {
    var notFound *NotFoundError
    if errors.As(err, &notFound) {
        fmt.Printf("Could not find %s: %s\n", notFound.Resource, notFound.ID)
        return
    }

    var validationErr *ValidationError
    if errors.As(err, &validationErr) {
        fmt.Printf("Bad input for %s: %s\n", validationErr.Field, validationErr.Message)
        return
    }

    fmt.Printf("Unexpected error: %v\n", err)
}
```

### Pattern 4: errors.Is and errors.As

`errors.Is` checks the error chain for a specific value (sentinel).
`errors.As` checks the error chain for a specific type (struct error).

```go
// errors.Is -- value comparison through the wrap chain
func processOrder(ctx context.Context, id string) error {
    order, err := getOrder(ctx, id)
    if err != nil {
        // Works even if err was wrapped multiple times
        if errors.Is(err, sql.ErrNoRows) {
            return fmt.Errorf("order %s: %w", id, ErrNotFound)
        }
        return fmt.Errorf("fetching order %s: %w", id, err)
    }
    _ = order
    return nil
}

// errors.As -- type extraction through the wrap chain
func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if r := recover(); r != nil {
                http.Error(w, "internal error", 500)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

### Pattern 5: Error Groups for Concurrent Operations

Use errgroup to manage errors from multiple goroutines cleanly.

```go
import "golang.org/x/sync/errgroup"

func fetchAll(ctx context.Context, urls []string) ([]Response, error) {
    g, ctx := errgroup.WithContext(ctx)
    responses := make([]Response, len(urls))

    for i, url := range urls {
        g.Go(func() error {
            resp, err := fetch(ctx, url)
            if err != nil {
                return fmt.Errorf("fetching %s: %w", url, err)
            }
            responses[i] = resp
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, fmt.Errorf("fetching urls: %w", err)
    }

    return responses, nil
}
```

### Pattern 6: Multi-Error Aggregation

Collect multiple errors when you need to report all failures, not just the first.

```go
func validate(u User) error {
    var errs []error

    if u.Name == "" {
        errs = append(errs, &ValidationError{Field: "name", Message: "required"})
    }
    if u.Email == "" {
        errs = append(errs, &ValidationError{Field: "email", Message: "required"})
    }
    if u.Age < 0 || u.Age > 150 {
        errs = append(errs, &ValidationError{Field: "age", Message: "out of range"})
    }

    return errors.Join(errs...)
}

// Checking joined errors
err := validate(user)
if err != nil {
    var ve *ValidationError
    if errors.As(err, &ve) {
        // Gets the first matching ValidationError in the joined set
        fmt.Println(ve.Field, ve.Message)
    }
}
```

## Anti-Patterns

- **Ignoring errors with `_`** -- Every error should be checked or explicitly documented
  as intentionally ignored.
  ```go
  // BAD
  result, _ := riskyOperation()
  // GOOD
  result, err := riskyOperation()
  if err != nil { return fmt.Errorf("risky op: %w", err) }
  ```

- **Wrapping without `%w`** -- Using `%v` instead of `%w` breaks the error chain.
  `errors.Is` and `errors.As` will not find the original error.

- **Logging and returning** -- Choose one. Log at the top level; wrap and return everywhere else.
  Logging at every layer creates duplicate, noisy log entries.
  ```go
  // BAD
  if err != nil {
      log.Printf("failed: %v", err)  // logged here
      return err                       // AND propagated -- will be logged again
  }
  ```

- **Panicking for recoverable errors** -- Reserve `panic` for truly unrecoverable situations
  (programmer bugs, impossible states). Return errors for anything a caller can handle.

## Quick Reference

| Tool | Purpose |
|------|---------|
| `fmt.Errorf("context: %w", err)` | Wrap with context |
| `errors.New("message")` | Create sentinel error |
| `errors.Is(err, target)` | Check value in chain |
| `errors.As(err, &target)` | Extract type from chain |
| `errors.Join(errs...)` | Combine multiple errors |
| `errgroup.Group` | Concurrent error collection |

Wrapping rule: add context about WHAT was being done, not WHY it failed (the
wrapped error already says why).
