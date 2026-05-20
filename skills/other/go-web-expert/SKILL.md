---
name: go-web-expert
description: Comprehensive Go web development persona enforcing zero global state, explicit error handling, input validation, testability, and documentation conventions. Use when building Go web applications to ensure production-quality code from the start.
---

# Go Web Expert System

Five non-negotiable rules for production-quality Go web applications. Every handler, every service, every line of code must satisfy all five.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Validation tags, custom validators, nested structs, error formatting | [references/validation.md](references/validation.md) |
| httptest patterns, middleware testing, integration tests, fixtures | [references/testing-handlers.md](references/testing-handlers.md) |

## Rules of Engagement

| # | Rule | One-Liner |
|---|------|-----------|
| 1 | Zero Global State | All handlers are methods on a struct; no package-level `var` for mutable state |
| 2 | Explicit Error Handling | Every error is checked, wrapped with `fmt.Errorf("doing X: %w", err)` |
| 3 | Validation First | All incoming JSON validated with `go-playground/validator` at the boundary |
| 4 | Testability | Every handler has a `_test.go` using `httptest` with table-driven tests |
| 5 | Documentation | Every exported symbol has a Go doc comment starting with its name |

---

## Rule 1: Zero Global State

All handlers must be methods on a server struct. No package-level `var` for databases, loggers, clients, or any mutable state.

```go
// FORBIDDEN
var db *sql.DB
var logger *slog.Logger

func handleGetUser(w http.ResponseWriter, r *http.Request) {
    user, err := db.QueryRow(...)  // global state -- untestable, unsafe
}

// REQUIRED
type Server struct {
    db     *sql.DB
    logger *slog.Logger
    router *http.ServeMux
}

func (s *Server) handleGetUser(w http.ResponseWriter, r *http.Request) {
    user, err := s.db.QueryRow(...)  // explicit dependency
}
```

### What Is Allowed at Package Level

- **Constants** -- `const maxPageSize = 100`
- **Pure functions** -- functions with no side effects that depend only on their arguments
- **Sentinel errors** -- `var ErrNotFound = errors.New("not found")`
- **Validator instance** -- `var validate = validator.New()` (stateless after init)

### What Is Forbidden at Package Level

- Database connections (`*sql.DB`, `*pgxpool.Pool`)
- Loggers (`*slog.Logger`)
- HTTP clients configured with timeouts or transport
- Configuration structs read from environment
- Caches, rate limiters, or any mutable shared resource

### Constructor Pattern

```go
func NewServer(db *sql.DB, logger *slog.Logger) *Server {
    s := &Server{
        db:     db,
        logger: logger,
        router: http.NewServeMux(),
    }
    s.routes()
    return s
}

func (s *Server) routes() {
    s.router.HandleFunc("GET /api/users/{id}", s.handleGetUser)
    s.router.HandleFunc("POST /api/users", s.handleCreateUser)
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    s.router.ServeHTTP(w, r)
}
```

---

## Rule 2: Explicit Error Handling

Never ignore errors. Every error must be wrapped with context describing what was being attempted when the error occurred.

```go
// FORBIDDEN
result, _ := doSomething()
json.NewEncoder(w).Encode(data)  // error ignored

// REQUIRED
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doing something for user %s: %w", userID, err)
}

if err := json.NewEncoder(w).Encode(data); err != nil {
    s.logger.Error("encoding response", "err", err, "request_id", reqID)
}
```

### Error Wrapping Convention

Format: `"<verb>ing <noun>: %w"` -- lowercase, no period, provides call-chain context.

```go
// Good wrapping -- each layer adds context
return fmt.Errorf("creating user: %w", err)
return fmt.Errorf("inserting user into database: %w", err)
return fmt.Errorf("hashing password for user %s: %w", email, err)

// Bad wrapping
return fmt.Errorf("error: %w", err)           // no context
return fmt.Errorf("Failed to create user: %w", err) // uppercase, verbose
return err                                      // no wrapping at all
```

### Structured Error Type for HTTP APIs

```go
type AppError struct {
    Code    int    `json:"-"`
    Message string `json:"error"`
    Detail  string `json:"detail,omitempty"`
}

func (e *AppError) Error() string {
    return fmt.Sprintf("%d: %s", e.Code, e.Message)
}

// Map domain errors to HTTP errors in one place
func handleError(w http.ResponseWriter, r *http.Request, err error) {
    var appErr *AppError
    if errors.As(err, &appErr) {
        writeJSON(w, appErr.Code, appErr)
        return
    }

    slog.Error("unhandled error",
        "err", err,
        "path", r.URL.Path,
    )
    writeJSON(w, 500, map[string]string{"error": "internal server error"})
}
```

### Common Mistakes

```go
// MISTAKE: not checking Close errors on writers
defer f.Close()  // at minimum, log Close errors for writable resources

// BETTER for writable resources:
defer func() {
    if err := f.Close(); err != nil {
        s.logger.Error("closing file", "err", err)
    }
}()

// OK for read-only resources where Close rarely fails:
defer resp.Body.Close()
```

---

## Rule 3: Validation First

Use `go-playground/validator` for all incoming JSON. Validate at the boundary, trust internal data.

```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

type CreateUserRequest struct {
    Name  string `json:"name"  validate:"required,min=1,max=100"`
    Email string `json:"email" validate:"required,email"`
    Age   int    `json:"age"   validate:"omitempty,gte=0,lte=150"`
}

func (s *Server) handleCreateUser(w http.ResponseWriter, r *http.Request) error {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        return &AppError{Code: 400, Message: "invalid JSON", Detail: err.Error()}
    }

    if err := validate.Struct(req); err != nil {
        return &AppError{Code: 422, Message: "validation failed", Detail: formatValidationErrors(err)}
    }

    // From here, req is trusted
    user, err := s.userService.Create(r.Context(), req.Name, req.Email)
    if err != nil {
        return fmt.Errorf("creating user: %w", err)
    }

    writeJSON(w, http.StatusCreated, user)
    return nil
}
```

### Validation Error Formatting

```go
func formatValidationErrors(err error) string {
    var msgs []string
    for _, e := range err.(validator.ValidationErrors) {
        msgs = append(msgs, fmt.Sprintf("field '%s' failed on '%s'", e.Field(), e.Tag()))
    }
    return strings.Join(msgs, "; ")
}
```

### Validation Boundary Rule

- **Validate at the edge** -- HTTP handlers, message consumers, CLI input
- **Trust internal data** -- service layer receives already-validated types
- **Never validate twice** -- if the handler validated, the service does not re-validate the same fields

See [references/validation.md](references/validation.md) for custom validators, nested struct validation, slice validation, and cross-field validation.

---

## Rule 4: Testability

Every handler must have a corresponding `_test.go` file using `httptest`. Test through the HTTP layer, not by calling handler methods directly.

```go
func TestServer_handleGetUser(t *testing.T) {
    mockStore := &MockUserStore{
        GetUserFunc: func(ctx context.Context, id string) (*User, error) {
            if id == "123" {
                return &User{ID: "123", Name: "Alice"}, nil
            }
            return nil, ErrNotFound
        },
    }
    srv := NewServer(mockStore, slog.Default())

    tests := []struct {
        name       string
        path       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "existing user",
            path:       "/api/users/123",
            wantStatus: http.StatusOK,
            wantBody:   `"name":"Alice"`,
        },
        {
            name:       "not found",
            path:       "/api/users/999",
            wantStatus: http.StatusNotFound,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", tt.path, nil)
            w := httptest.NewRecorder()

            srv.ServeHTTP(w, req)

            if w.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", w.Code, tt.wantStatus)
            }
            if tt.wantBody != "" && !strings.Contains(w.Body.String(), tt.wantBody) {
                t.Errorf("body = %q, want to contain %q", w.Body.String(), tt.wantBody)
            }
        })
    }
}
```

### Key Testing Principles

- **Test through HTTP** -- use `httptest.NewRequest` and `httptest.NewRecorder`, call `srv.ServeHTTP`
- **Interface-based mocks** -- define narrow interfaces at the consumer, create mock implementations for tests
- **Table-driven tests** -- one `[]struct` with test cases, one `t.Run` loop
- **Error paths matter** -- test 400s, 404s, 422s, and 500s, not just 200s
- **No global test state** -- each test creates its own server with its own mocks

See [references/testing-handlers.md](references/testing-handlers.md) for middleware testing, integration tests with real databases, file upload testing, and streaming response testing.

---

## Rule 5: Documentation

Every exported function, type, method, and constant must have a Go doc comment following standard conventions.

```go
// CreateUser creates a new user with the given name and email.
// It returns ErrDuplicateEmail if a user with the same email already exists.
func (s *UserService) CreateUser(ctx context.Context, name, email string) (*User, error) {
    // ...
}

// Server handles HTTP requests for the user API.
type Server struct {
    // ...
}

// NewServer creates a Server with the given dependencies.
// The logger must not be nil.
func NewServer(store UserStore, logger *slog.Logger) *Server {
    // ...
}

// ErrNotFound is returned when a requested resource does not exist.
var ErrNotFound = errors.New("not found")
```

### Doc Comment Conventions

- **Start with the name** -- `// CreateUser creates...` not `// This function creates...`
- **First sentence is the summary** -- shown in `go doc` listings and IDE tooltips
- **Mention important error returns** -- callers need to know which errors to check
- **Don't document the obvious** -- `// SetName sets the name` adds no value
- **Document why, not what** -- when behavior is non-obvious, explain the reasoning

### Package Documentation

```go
// Package user provides user management for the application.
// It handles creation, retrieval, and deletion of user accounts,
// with email uniqueness enforced at the database level.
package user
```

---

## Cross-Cutting Concerns

The five rules reinforce each other. Here is how they interact.

### Zero Global State Enables Testability

Because all dependencies are on the struct, tests can inject mocks:

```go
// Production
srv := NewServer(realDB, prodLogger)

// Test
srv := NewServer(mockStore, slog.Default())
```

If `db` were a global `var`, tests would need to mutate package state, causing race conditions in parallel tests.

### Validation First Simplifies Error Handling

When handlers validate at the boundary, the service layer can assume valid input. This means service-layer errors are always unexpected (database failures, network issues), and error handling becomes simpler:

```go
func (s *UserService) Create(ctx context.Context, name, email string) (*User, error) {
    // No need to check if name is empty -- handler already validated
    user := &User{Name: name, Email: email}
    if err := s.store.Insert(ctx, user); err != nil {
        return nil, fmt.Errorf("inserting user: %w", err)
    }
    return user, nil
}
```

### Documentation Makes Error Handling Discoverable

Doc comments that mention error returns tell callers what to handle:

```go
// Delete removes a user by ID.
// It returns ErrNotFound if the user does not exist.
// It returns ErrHasActiveOrders if the user has unfinished orders.
func (s *UserService) Delete(ctx context.Context, id string) error {
```

---

## Self-Review Checklist

Before considering any handler or service complete, verify all five rules:

### Zero Global State
- [ ] No package-level `var` for mutable state (db, logger, clients)
- [ ] All handlers are methods on a struct
- [ ] Dependencies injected through constructor

### Explicit Error Handling
- [ ] No `_` ignoring returned errors
- [ ] All errors wrapped with `fmt.Errorf("doing X: %w", err)`
- [ ] `json.NewEncoder(w).Encode(...)` error checked or logged
- [ ] Structured `AppError` used for HTTP error responses

### Validation First
- [ ] All request structs have `validate` tags
- [ ] `validate.Struct(req)` called before any business logic
- [ ] Validation errors return 422 with field-level detail
- [ ] Service layer does not re-validate handler-validated data

### Testability
- [ ] `_test.go` file exists for every handler file
- [ ] Tests use `httptest.NewRequest` and `httptest.NewRecorder`
- [ ] Table-driven tests cover happy path and error paths
- [ ] Mocks implement narrow interfaces, not concrete types

### Documentation
- [ ] Every exported function has a doc comment starting with its name
- [ ] Error return values are documented
- [ ] Package has a doc comment

## When to Load References

Load **validation.md** when:
- Adding new request types with validation tags
- Creating custom validators
- Validating nested structs, slices, or maps
- Formatting validation errors for API responses

Load **testing-handlers.md** when:
- Writing handler tests for the first time in a project
- Testing middleware chains or authentication
- Setting up integration tests with a real database
- Testing file uploads or streaming responses
