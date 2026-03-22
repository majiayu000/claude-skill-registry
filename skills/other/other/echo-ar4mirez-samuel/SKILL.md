---
name: echo
description: |
  Echo framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Echo projects, or when the user mentions Echo framework.
  Provides middleware patterns, routing, context handling, and REST API guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: go
  extensions: ".go"
---

# Echo Framework Guide

> **Applies to**: Echo v4+, REST APIs, Microservices, High-Performance Web Applications
> **Language Guide**: @.claude/skills/go-guide/SKILL.md

## Overview

Echo is a high-performance, extensible, minimalist Go web framework. It features an optimized HTTP router, middleware support, data binding, and rendering.

**Use Echo when:**
- You need high performance with minimal overhead
- You want a clean, intuitive API
- Built-in middleware matters (JWT, CORS, Gzip, etc.)
- You prefer automatic TLS via Let's Encrypt

**Consider alternatives when:**
- You want the most popular framework (use Gin)
- You need WebSocket support built-in (use Fiber)
- Maximum community resources are needed (use Gin)

## Project Structure

```
myproject/
├── cmd/
│   └── api/
│       └── main.go           # Entry point
├── internal/
│   ├── config/
│   │   └── config.go         # Configuration
│   ├── handler/
│   │   ├── handler.go        # Handler container
│   │   ├── user.go           # User handlers
│   │   └── auth.go           # Auth handlers
│   ├── middleware/
│   │   ├── auth.go           # JWT middleware
│   │   └── custom.go         # Custom middleware
│   ├── model/
│   │   ├── user.go           # User model
│   │   └── response.go       # Response models
│   ├── repository/
│   │   ├── repository.go     # Repository interface
│   │   └── user.go           # User repository
│   ├── service/
│   │   ├── service.go        # Service container
│   │   └── user.go           # User service
│   └── validator/
│       └── validator.go      # Custom validators
├── pkg/
│   └── response/
│       └── response.go       # Response helpers
├── migrations/
├── .env.example
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

- `cmd/` for entry points; one `main.go` per binary
- `internal/` for private application code; not importable externally
- `handler/` contains Echo handler functions, thin HTTP layer only
- `service/` holds business logic; no Echo or HTTP dependencies
- `repository/` encapsulates data access; accepts `context.Context`
- `model/` defines domain structs, request/response DTOs
- `middleware/` for custom Echo middleware functions
- `validator/` for custom validation rules via go-playground/validator

## Application Setup

```go
e := echo.New()
e.HideBanner = true
e.Validator = validator.NewCustomValidator()

// Global middleware (order matters)
e.Use(echoMw.Recover())   // First: catch panics
e.Use(echoMw.Logger())    // Second: log all requests
e.Use(echoMw.RequestID()) // Third: trace IDs
e.Use(echoMw.CORSWithConfig(echoMw.CORSConfig{
    AllowOrigins: cfg.CORSOrigins,
    AllowMethods: []string{http.MethodGet, http.MethodPost,
        http.MethodPut, http.MethodPatch, http.MethodDelete},
    AllowHeaders: []string{echo.HeaderOrigin,
        echo.HeaderContentType, echo.HeaderAccept,
        echo.HeaderAuthorization},
}))
```

**Setup guidelines:**
- Set `e.HideBanner = true` in production
- Register `Recover()` first to catch panics in all handlers
- Use `RequestID()` for distributed tracing
- Always implement graceful shutdown with `e.Shutdown(ctx)`
- See [references/patterns.md](references/patterns.md) for full `main.go` with graceful shutdown

## Routing

### Route Groups and Versioning

```go
func setupRoutes(e *echo.Echo, h *handler.Handlers, authMw *middleware.AuthMiddleware) {
    // Health check (ungrouped)
    e.GET("/health", func(c echo.Context) error {
        return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
    })

    // API v1
    v1 := e.Group("/api/v1")

    // Public routes
    auth := v1.Group("/auth")
    auth.POST("/login", h.Auth.Login)
    auth.POST("/register", h.Auth.Register)
    auth.POST("/refresh", h.Auth.Refresh)

    // Protected routes
    users := v1.Group("/users")
    users.POST("", h.User.Create)
    users.Use(authMw.Authenticate)
    users.GET("", h.User.GetAll)
    users.GET("/me", h.User.GetCurrent)
    users.GET("/:id", h.User.GetByID)
    users.PUT("/:id", h.User.Update)
    users.DELETE("/:id", h.User.Delete, authMw.RequireAdmin)
}
```

**Routing guidelines:**
- Group routes by resource and version (`/api/v1/users`)
- Apply middleware at group level, not per-route when possible
- Use `/:param` for path parameters (e.g., `/:id`)
- Append per-route middleware as extra handler args (e.g., `RequireAdmin`)
- Keep health check outside API groups for monitoring tools

## Middleware

### Built-in Middleware (use these first)

| Middleware | Purpose |
|-----------|---------|
| `Recover()` | Catch panics, return 500 |
| `Logger()` | Request logging |
| `RequestID()` | Unique request IDs |
| `CORS()` | Cross-origin requests |
| `Gzip()` | Response compression |
| `RateLimiter()` | Rate limiting |
| `Secure()` | Security headers |
| `BodyLimit()` | Request size limits |

### Custom Middleware Pattern

```go
// Middleware that injects request-scoped values
func RequestTimerMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        start := time.Now()
        err := next(c)
        duration := time.Since(start)
        c.Response().Header().Set("X-Response-Time",
            duration.String())
        return err
    }
}

// Middleware with configuration
type RateLimitConfig struct {
    Rate  int
    Burst int
}

func RateLimitMiddleware(cfg RateLimitConfig) echo.MiddlewareFunc {
    limiter := rate.NewLimiter(
        rate.Limit(cfg.Rate), cfg.Burst,
    )
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            if !limiter.Allow() {
                return c.JSON(http.StatusTooManyRequests,
                    model.ErrorResponse("rate limit exceeded"))
            }
            return next(c)
        }
    }
}
```

**Middleware guidelines:**
- Return `echo.HandlerFunc` from middleware
- Call `next(c)` to continue the chain; skip to short-circuit
- Configurable middleware returns `echo.MiddlewareFunc`
- Order matters: register `Recover()` first, then logging, then auth

## Echo Context

### Reading Values

```go
func handler(c echo.Context) error {
    // Path params
    id := c.Param("id")

    // Query params
    page := c.QueryParam("page")
    search := c.QueryParam("q")

    // Form values
    name := c.FormValue("name")

    // Headers
    token := c.Request().Header.Get("Authorization")

    // Request-scoped values (set by middleware)
    userID, ok := c.Get("user_id").(uint)

    // Real IP (respects X-Forwarded-For)
    ip := c.RealIP()

    // Underlying context.Context for DB/service calls
    ctx := c.Request().Context()

    return c.JSON(http.StatusOK, data)
}
```

**Context guidelines:**
- Use `c.Request().Context()` when passing to services/repositories
- Use `c.Get()`/`c.Set()` for request-scoped values between middleware and handlers
- Type-assert values from `c.Get()` with `ok` check
- Never store `echo.Context` beyond the request lifecycle

## Request Binding and Validation

### Binding

```go
type CreateUserRequest struct {
    Email     string `json:"email" validate:"required,email"`
    Password  string `json:"password" validate:"required,min=8"`
    FirstName string `json:"first_name" validate:"required,min=1,max=100"`
    LastName  string `json:"last_name" validate:"required,min=1,max=100"`
}

func (h *UserHandler) Create(c echo.Context) error {
    var req CreateUserRequest
    if err := c.Bind(&req); err != nil {
        return c.JSON(http.StatusBadRequest,
            model.ErrorResponse(err.Error()))
    }
    if err := c.Validate(&req); err != nil {
        return err // Custom validator returns HTTPError
    }
    // Process valid request...
}
```

### Custom Validator

```go
type CustomValidator struct {
    validator *validator.Validate
}

func NewCustomValidator() *CustomValidator {
    v := validator.New()
    v.RegisterTagNameFunc(func(fld reflect.StructField) string {
        name := strings.SplitN(fld.Tag.Get("json"), ",", 2)[0]
        if name == "-" {
            return ""
        }
        return name
    })
    return &CustomValidator{validator: v}
}

func (cv *CustomValidator) Validate(i interface{}) error {
    if err := cv.validator.Struct(i); err != nil {
        return echo.NewHTTPError(
            http.StatusBadRequest,
            formatValidationErrors(err),
        )
    }
    return nil
}
```

**Binding guidelines:**
- Always `Bind` then `Validate` as separate steps
- Use struct tags: `json` for binding, `validate` for rules
- Register custom validator on `e.Validator` at startup
- Return structured validation errors, not raw messages
- Use pointer fields for optional/partial updates (`*string`)

## Response Patterns

Use a consistent JSON envelope across all endpoints:

```go
// Success: c.JSON(http.StatusOK, SuccessResponse(data))
// Error:   c.JSON(http.StatusNotFound, ErrorResponse("not found"))
// Delete:  c.NoContent(http.StatusNoContent)

type Response struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
}

func SuccessResponse(data interface{}) *Response {
    return &Response{Success: true, Data: data}
}

func ErrorResponse(msg string) *Response {
    return &Response{Success: false, Error: msg}
}
```

- Use response DTOs; never expose domain models directly (omit passwords, internal IDs)
- For paginated responses, include `meta` with page/total counts
- See [references/patterns.md](references/patterns.md) for `PaginatedResponse` struct

## Error Handling

### Domain Errors

```go
var (
    ErrUserNotFound       = errors.New("user not found")
    ErrUserAlreadyExists  = errors.New("user already exists")
    ErrInvalidCredentials = errors.New("invalid credentials")
)
```

### Handler Error Mapping

```go
func (h *UserHandler) GetByID(c echo.Context) error {
    id, err := strconv.ParseUint(c.Param("id"), 10, 32)
    if err != nil {
        return c.JSON(http.StatusBadRequest,
            model.ErrorResponse("invalid user ID"))
    }

    user, err := h.userService.GetByID(
        c.Request().Context(), uint(id),
    )
    if err != nil {
        if errors.Is(err, service.ErrUserNotFound) {
            return c.JSON(http.StatusNotFound,
                model.ErrorResponse(err.Error()))
        }
        return c.JSON(http.StatusInternalServerError,
            model.ErrorResponse(err.Error()))
    }

    return c.JSON(http.StatusOK,
        model.SuccessResponse(user.ToResponse()))
}
```

**Error handling guidelines:**
- Define domain errors as sentinel values in the service layer
- Map domain errors to HTTP status codes in handlers only
- Use `errors.Is()` / `errors.As()` for error checking
- Never expose internal errors to clients in production
- Log detailed errors server-side; return safe messages to clients

## Configuration

- Load from environment variables (12-factor app) via `godotenv`
- Provide sensible defaults for development only
- Never hardcode secrets; use empty defaults to force explicit config
- Parse durations and validate at startup, not at use time
- See [references/patterns.md](references/patterns.md) for full config struct example

## Commands Reference

```bash
# Initialize project
go mod init myproject

# Install dependencies
go mod tidy

# Run development server
go run cmd/api/main.go

# Build binary
go build -o bin/api cmd/api/main.go

# Run tests
go test ./...
go test -v -cover ./...

# Run with race detection
go test -race ./...

# Lint
golangci-lint run

# Database migrations (golang-migrate)
migrate -path migrations -database "$DATABASE_URL" up
migrate -path migrations -database "$DATABASE_URL" down
```

## Dependencies

```go
// Core
github.com/labstack/echo/v4          // Web framework
github.com/go-playground/validator/v10 // Validation
github.com/golang-jwt/jwt/v5          // JWT auth
github.com/joho/godotenv              // Env loading

// Database
gorm.io/gorm                          // ORM
gorm.io/driver/postgres               // PostgreSQL driver

// Crypto
golang.org/x/crypto                    // bcrypt, etc.

// Testing
github.com/stretchr/testify           // Assertions and mocks
```

## Best Practices Checklist

### Echo-Specific
- Use custom validator with `go-playground/validator`
- Use `echo.Context` for request handling only (not in services)
- Use middleware groups for route organization
- Return errors from handlers for centralized handling
- Use `echo.Bind` for request binding
- Configure proper timeouts and graceful shutdown
- Set `e.HideBanner = true` in production

### Performance
- Configure database connection pooling (`SetMaxOpenConns`, etc.)
- Implement pagination for list endpoints
- Use `Gzip()` middleware for response compression
- Implement request logging middleware for observability
- Use `BodyLimit()` to prevent oversized requests

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Handler examples, database repository, authentication, WebSocket, testing patterns

## External References

- [Echo Documentation](https://echo.labstack.com/)
- [Echo GitHub](https://github.com/labstack/echo)
- [Echo Cookbook](https://github.com/labstack/echo/tree/master/cookbook)
- [GORM Documentation](https://gorm.io/docs/)
- [go-playground/validator](https://github.com/go-playground/validator)
