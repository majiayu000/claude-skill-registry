---
name: fiber
description: |
  Fiber framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Fiber projects, or when the user mentions Fiber framework.
  Provides Express-style routing, middleware, high-performance patterns, and REST API guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: go
  extensions: ".go"
---

# Fiber Framework Guide

> Applies to: Fiber v2.50+, Go 1.21+, High-Performance REST APIs, Microservices

## Overview

Fiber is an Express-inspired web framework built on top of Fasthttp, the fastest HTTP engine for Go. It is designed for ease of use with zero memory allocation and performance in mind.

**Key Features**:
- Express-like API (familiar to Node.js developers)
- Built on Fasthttp (10x faster than net/http)
- Zero memory allocation in hot paths
- Built-in middleware collection
- WebSocket support, rate limiting, template engines

**When to use Fiber**:
- High-throughput APIs requiring maximum performance
- Teams familiar with Express.js migrating to Go
- Real-time applications with WebSockets
- Microservices requiring low latency

## Project Structure

```
myapi/
├── cmd/
│   └── api/
│       └── main.go              # Application entry point
├── internal/
│   ├── config/
│   │   └── config.go            # Configuration management
│   ├── handler/
│   │   ├── handler.go           # Handler container
│   │   ├── user_handler.go      # User handlers
│   │   └── health_handler.go    # Health check handlers
│   ├── middleware/
│   │   ├── auth.go              # JWT authentication
│   │   ├── logger.go            # Request logging
│   │   └── recover.go           # Panic recovery
│   ├── model/
│   │   ├── user.go              # User model
│   │   └── dto.go               # Data transfer objects
│   ├── repository/
│   │   ├── repository.go        # Repository interface
│   │   └── user_repository.go   # User repository
│   ├── service/
│   │   ├── service.go           # Service container
│   │   ├── user_service.go      # User business logic
│   │   └── auth_service.go      # Authentication service
│   └── router/
│       └── router.go            # Route definitions
├── pkg/
│   ├── validator/
│   │   └── validator.go         # Custom validator
│   └── response/
│       └── response.go          # Response helpers
├── go.mod
├── go.sum
└── README.md
```

- `internal/` for private application code (not importable externally)
- `pkg/` for reusable shared libraries
- `cmd/` for application entry points
- Handlers are thin; business logic lives in services
- Data access isolated in repositories

## Application Setup

```go
// cmd/api/main.go
package main

import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/cors"
    "github.com/gofiber/fiber/v2/middleware/helmet"
    "github.com/gofiber/fiber/v2/middleware/limiter"
    "github.com/gofiber/fiber/v2/middleware/requestid"

    "myapi/internal/config"
    "myapi/internal/handler"
    "myapi/internal/middleware"
    "myapi/internal/repository"
    "myapi/internal/router"
    "myapi/internal/service"
)

func main() {
    cfg, err := config.Load()
    if err != nil {
        log.Fatalf("Failed to load config: %v", err)
    }

    db, err := config.NewDatabase(cfg)
    if err != nil {
        log.Fatalf("Failed to connect to database: %v", err)
    }

    app := fiber.New(fiber.Config{
        AppName:      cfg.AppName,
        ReadTimeout:  cfg.ReadTimeout,
        WriteTimeout: cfg.WriteTimeout,
        IdleTimeout:  cfg.IdleTimeout,
        BodyLimit:    cfg.BodyLimit,
        Prefork:      cfg.Prefork,
        ErrorHandler: customErrorHandler,
    })

    // Global middleware stack
    app.Use(requestid.New())
    app.Use(middleware.Logger())
    app.Use(middleware.Recover())
    app.Use(cors.New(cors.Config{
        AllowOrigins:     cfg.CORSAllowOrigins,
        AllowMethods:     "GET,POST,PUT,DELETE,PATCH,OPTIONS",
        AllowHeaders:     "Origin,Content-Type,Accept,Authorization",
        AllowCredentials: true,
    }))
    app.Use(helmet.New())
    app.Use(limiter.New(limiter.Config{
        Max:        cfg.RateLimitMax,
        Expiration: cfg.RateLimitExpiration,
        KeyGenerator: func(c *fiber.Ctx) string {
            return c.IP()
        },
        LimitReached: func(c *fiber.Ctx) error {
            return c.Status(fiber.StatusTooManyRequests).JSON(fiber.Map{
                "error": "Rate limit exceeded",
            })
        },
    }))

    // Initialize layers (dependency injection)
    repos := repository.NewRepositories(db)
    services := service.NewServices(repos, cfg)
    handlers := handler.NewHandlers(services)

    router.Setup(app, handlers, services.Auth)

    // Graceful shutdown
    go func() {
        if err := app.Listen(":" + cfg.Port); err != nil {
            log.Fatalf("Failed to start server: %v", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := app.ShutdownWithContext(ctx); err != nil {
        log.Fatalf("Server forced to shutdown: %v", err)
    }

    sqlDB, _ := db.DB()
    sqlDB.Close()
}

func customErrorHandler(c *fiber.Ctx, err error) error {
    code := fiber.StatusInternalServerError
    message := "Internal Server Error"

    if e, ok := err.(*fiber.Error); ok {
        code = e.Code
        message = e.Message
    }

    return c.Status(code).JSON(fiber.Map{
        "error":   message,
        "code":    code,
        "request": c.Locals("requestid"),
    })
}
```

## Routing and Grouping

```go
// internal/router/router.go
func Setup(app *fiber.App, h *handler.Handlers, authService service.AuthService) {
    // Health checks (public)
    app.Get("/health", h.Health.Health)
    app.Get("/ready", h.Health.Ready)

    // API v1
    v1 := app.Group("/api/v1")

    // Auth routes (public)
    auth := v1.Group("/auth")
    auth.Post("/login", h.User.Login)
    auth.Post("/register", h.User.Create)

    // Protected auth routes
    authProtected := auth.Group("", middleware.Auth(authService))
    authProtected.Get("/profile", h.User.GetProfile)

    // User routes (protected)
    users := v1.Group("/users", middleware.Auth(authService))
    users.Get("/", h.User.GetAll)
    users.Get("/:id", h.User.GetByID)
    users.Put("/:id", h.User.Update)
    users.Delete("/:id", middleware.RequireRole("admin"), h.User.Delete)
}
```

**Routing rules**:
- Group routes by resource and version (`/api/v1/users`)
- Apply auth middleware at the group level, not per-route
- Use role-based middleware for fine-grained access control
- Health and readiness checks always public, at root level

## Middleware

### Authentication Middleware

```go
func Auth(authService service.AuthService) fiber.Handler {
    return func(c *fiber.Ctx) error {
        authHeader := c.Get("Authorization")
        if authHeader == "" {
            return fiber.NewError(fiber.StatusUnauthorized, "Missing authorization header")
        }

        parts := strings.SplitN(authHeader, " ", 2)
        if len(parts) != 2 || parts[0] != "Bearer" {
            return fiber.NewError(fiber.StatusUnauthorized, "Invalid authorization format")
        }

        claims, err := authService.ValidateToken(parts[1])
        if err != nil {
            return fiber.NewError(fiber.StatusUnauthorized, "Invalid token")
        }

        c.Locals("userID", claims.UserID)
        c.Locals("userEmail", claims.Email)
        c.Locals("userRole", claims.Role)

        return c.Next()
    }
}
```

### Role-Based Access

```go
func RequireRole(roles ...string) fiber.Handler {
    return func(c *fiber.Ctx) error {
        userRole, ok := c.Locals("userRole").(string)
        if !ok {
            return fiber.NewError(fiber.StatusForbidden, "Access denied")
        }

        for _, role := range roles {
            if userRole == role {
                return c.Next()
            }
        }

        return fiber.NewError(fiber.StatusForbidden, "Insufficient permissions")
    }
}
```

### Custom Logger and Recovery

```go
func Logger() fiber.Handler {
    return func(c *fiber.Ctx) error {
        start := time.Now()
        err := c.Next()
        log.Printf("[%s] %s %s %d %s",
            c.Method(), c.Path(), c.IP(),
            c.Response().StatusCode(), time.Since(start))
        return err
    }
}

func Recover() fiber.Handler {
    return func(c *fiber.Ctx) error {
        defer func() {
            if r := recover(); r != nil {
                log.Printf("Panic recovered: %v\n%s", r, debug.Stack())
                c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
                    "error": "Internal server error",
                })
            }
        }()
        return c.Next()
    }
}
```

## Request Handling and Validation

### Generic Body Validator

```go
func ValidateBody[T any](c *fiber.Ctx, v *CustomValidator) (*T, error) {
    var body T
    if err := c.BodyParser(&body); err != nil {
        return nil, fiber.NewError(fiber.StatusBadRequest, "Invalid request body")
    }
    if err := v.Validate(&body); err != nil {
        return nil, err
    }
    return &body, nil
}
```

### DTO Pattern with Validation Tags

```go
type CreateUserRequest struct {
    Email    string `json:"email" validate:"required,email,max=255"`
    Password string `json:"password" validate:"required,min=8,max=72"`
    Name     string `json:"name" validate:"required,min=2,max=100"`
}

type UpdateUserRequest struct {
    Email string `json:"email" validate:"omitempty,email,max=255"`
    Name  string `json:"name" validate:"omitempty,min=2,max=100"`
}
```

### Response Helpers

```go
func Success(c *fiber.Ctx, data interface{}) error {
    return c.JSON(fiber.Map{"success": true, "data": data})
}

func Created(c *fiber.Ctx, data interface{}) error {
    return c.Status(fiber.StatusCreated).JSON(fiber.Map{"success": true, "data": data})
}

func Error(c *fiber.Ctx, code int, message string) error {
    return c.Status(code).JSON(fiber.Map{"success": false, "error": message})
}

func Paginated(c *fiber.Ctx, data interface{}, page, pageSize int, total int64) error {
    totalPages := int(total) / pageSize
    if int(total)%pageSize > 0 {
        totalPages++
    }
    return c.JSON(fiber.Map{
        "success": true,
        "data":    data,
        "meta": fiber.Map{
            "page": page, "page_size": pageSize,
            "total_items": total, "total_pages": totalPages,
        },
    })
}
```

## Error Handling

- Use `fiber.NewError(code, message)` for HTTP errors in handlers
- Implement a custom `ErrorHandler` on the app for consistent responses
- Return domain errors from services; map them to HTTP codes in handlers
- Never expose internal error details to clients

```go
func (h *UserHandler) Create(c *fiber.Ctx) error {
    req, err := validator.ValidateBody[model.CreateUserRequest](c, h.validator)
    if err != nil {
        if _, ok := err.(*fiber.Error); ok {
            return err
        }
        return response.ValidationError(c, err)
    }

    user, err := h.service.Create(c.Context(), req)
    if err != nil {
        if errors.Is(err, service.ErrUserAlreadyExists) {
            return response.Error(c, fiber.StatusConflict, "User already exists")
        }
        return err // Falls through to custom error handler
    }

    return response.Created(c, user.ToResponse())
}
```

## Best Practices

### Performance
- Enable `Prefork` for multi-core utilization in production
- Use Fasthttp's zero-allocation patterns
- Configure appropriate read/write/idle timeouts
- Use connection pooling for databases (25 max open, 5 min lifetime)
- Use `fiber.Ctx.Context()` for request-scoped context

### Security
- Use `helmet` middleware for security headers
- Implement rate limiting per IP (built-in `limiter` middleware)
- Validate all inputs via `go-playground/validator`
- Use CORS middleware with explicit origins in production
- Hash passwords with bcrypt; use JWT HS256 for tokens

### Code Organization
- Follow clean architecture: handler -> service -> repository
- Use dependency injection (no global state)
- Keep handlers thin (parse, validate, delegate, respond)
- Define interfaces where consumed, not where implemented
- Use DTO structs for request/response serialization

### Error Handling
- Use a custom error handler on the Fiber app
- Return consistent JSON error responses with `success`, `error`, `code`
- Log errors with request context (request ID, method, path)
- Do not expose stack traces or internal details to clients

## Commands

```bash
# Development
go run cmd/api/main.go

# Build
go build -o bin/api cmd/api/main.go

# Production build
CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o bin/api cmd/api/main.go

# Tests
go test ./...
go test -cover ./...
go test -race ./...

# Swagger docs (with swag)
swag init -g cmd/api/main.go

# Database migrations (with golang-migrate)
migrate -path migrations -database "$DATABASE_URL" up
migrate -path migrations -database "$DATABASE_URL" down 1

# Lint
golangci-lint run
```

## Dependencies

Core: `fiber/v2`, `gofiber/swagger` | Database: `gorm`, `gorm/driver/postgres` | Validation: `go-playground/validator/v10` | Auth: `golang-jwt/jwt/v5`, `x/crypto/bcrypt` | Testing: `stretchr/testify` | Docs: `swaggo/swag`

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Handler examples, database, WebSocket, testing, and performance patterns

## External References

- [Fiber Documentation](https://docs.gofiber.io/)
- [Fiber GitHub](https://github.com/gofiber/fiber)
- [Fasthttp](https://github.com/valyala/fasthttp)
- [Fiber Recipes](https://github.com/gofiber/recipes)
- [Fiber Awesome List](https://github.com/gofiber/awesome-fiber)
