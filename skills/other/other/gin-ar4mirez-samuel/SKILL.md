---
name: gin
description: |
  Gin framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Gin projects, or when the user mentions Gin framework.
  Provides middleware patterns, routing, validation, error handling, and REST API guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: go
  extensions: ".go"
---

# Gin Framework Guide

> Applies to: Gin 1.9+, REST APIs, Microservices, Web Applications
> Language Guide: @.claude/skills/go-guide/SKILL.md

## Overview

Gin is a high-performance HTTP web framework written in Go featuring a martini-like API with performance up to 40x faster. It is the most popular Go web framework, ideal for building REST APIs and microservices.

**Use Gin when:**
- Building high-performance REST APIs
- You need a mature, well-documented framework
- Middleware ecosystem is important
- You want a balanced approach (not too minimal, not too heavy)

**Consider alternatives when:**
- You need maximum minimalism (use standard library)
- You want built-in WebSocket support (use Fiber)
- You prefer a different API style (use Echo)

## Guardrails

### Gin-Specific Rules

- Use application factory pattern for testability
- Group routes with versioning (`/api/v1`)
- Use middleware for cross-cutting concerns (auth, logging, CORS)
- Use `gin.Context` for request-scoped data only
- Use binding tags for input validation
- Return consistent JSON response structure across all endpoints
- Use proper HTTP status codes
- Set `gin.ReleaseMode` in production
- Configure proper server timeouts (read, write, idle)
- Implement graceful shutdown for all servers
- Use connection pooling for database access
- Use pagination for all list endpoints

### Anti-Patterns

- Do not use `gin.Default()` in production without understanding its middleware
- Do not store business logic in handlers (use service layer)
- Do not return raw error messages to clients
- Do not skip input validation on any endpoint
- Do not use global state; use dependency injection

## Project Structure

```
myproject/
├── cmd/
│   └── api/
│       └── main.go           # Entry point, server setup, graceful shutdown
├── internal/
│   ├── config/
│   │   └── config.go         # Configuration from env vars
│   ├── handler/
│   │   ├── handler.go        # Handler registry struct
│   │   ├── user.go           # User handlers
│   │   └── auth.go           # Auth handlers
│   ├── middleware/
│   │   ├── auth.go           # JWT/Bearer auth middleware
│   │   ├── cors.go           # CORS middleware
│   │   └── logger.go         # Request logging middleware
│   ├── model/
│   │   ├── user.go           # Domain model + request/response DTOs
│   │   └── response.go       # Standardized response wrappers
│   ├── repository/
│   │   ├── repository.go     # Repository registry (interfaces)
│   │   └── user.go           # User repository implementation
│   ├── service/
│   │   ├── service.go        # Service registry (interfaces)
│   │   └── user.go           # User business logic
│   └── router/
│       └── router.go         # Route definitions and grouping
├── pkg/
│   ├── validator/
│   │   └── validator.go      # Custom validators
│   └── response/
│       └── response.go       # Shared response helpers
├── migrations/
├── .env.example
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

**Layer responsibilities:**
- `handler/` — HTTP concerns only: parse request, call service, write response
- `service/` — Business logic, validation, orchestration
- `repository/` — Data access, database queries
- `model/` — Domain types, request/response DTOs, validation tags
- `middleware/` — Cross-cutting: auth, logging, CORS, rate limiting
- `router/` — Route registration, grouping, middleware attachment

## Routing

### Route Groups and Versioning

```go
func Setup(handlers *handler.Handlers, mw *middleware.Middleware) *gin.Engine {
    r := gin.New()

    // Global middleware
    r.Use(gin.Recovery())
    r.Use(middleware.Logger())
    r.Use(middleware.CORS())

    // Health check (always public)
    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{"status": "ok"})
    })

    // API v1 routes
    v1 := r.Group("/api/v1")
    {
        // Public routes
        auth := v1.Group("/auth")
        {
            auth.POST("/login", handlers.Auth.Login)
            auth.POST("/refresh", handlers.Auth.Refresh)
        }

        // Protected routes
        users := v1.Group("/users")
        {
            users.POST("", handlers.User.CreateUser)        // Public
            users.Use(mw.Auth())                             // Auth from here down
            users.GET("", handlers.User.GetUsers)
            users.GET("/me", handlers.User.GetCurrentUser)
            users.GET("/:id", handlers.User.GetUser)
            users.PATCH("/:id", handlers.User.UpdateUser)
            users.DELETE("/:id", mw.AdminOnly(), handlers.User.DeleteUser)
        }
    }

    return r
}
```

**Routing conventions:**
- Always use `gin.New()` (not `gin.Default()`) and add middleware explicitly
- Group public and protected routes separately
- Apply auth middleware at the group level, not per-route
- Use per-route middleware for fine-grained access (e.g., `mw.AdminOnly()`)
- Always include a `/health` endpoint

## Middleware

### Auth Middleware (JWT Bearer)

```go
func (m *Middleware) Auth() gin.HandlerFunc {
    return func(c *gin.Context) {
        header := c.GetHeader("Authorization")
        if header == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized,
                model.NewErrorResponse("missing authorization header"))
            return
        }

        parts := strings.Split(header, " ")
        if len(parts) != 2 || parts[0] != "Bearer" {
            c.AbortWithStatusJSON(http.StatusUnauthorized,
                model.NewErrorResponse("invalid authorization header"))
            return
        }

        claims, err := m.authService.ValidateToken(parts[1])
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized,
                model.NewErrorResponse("invalid token"))
            return
        }

        // Set user context for downstream handlers
        c.Set("user_id", claims.UserID)
        c.Set("is_admin", claims.IsAdmin)
        c.Next()
    }
}
```

### Role-Based Access

```go
func (m *Middleware) AdminOnly() gin.HandlerFunc {
    return func(c *gin.Context) {
        isAdmin, exists := c.Get("is_admin")
        if !exists || !isAdmin.(bool) {
            c.AbortWithStatusJSON(http.StatusForbidden,
                model.NewErrorResponse("admin access required"))
            return
        }
        c.Next()
    }
}
```

### Request Logger

```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path
        query := c.Request.URL.RawQuery

        c.Next()

        if query != "" {
            path = path + "?" + query
        }

        log.Printf("[GIN] %3d | %13v | %15s | %-7s %s",
            c.Writer.Status(), time.Since(start),
            c.ClientIP(), c.Request.Method, path)
    }
}
```

## Request Binding and Validation

### Binding Tags

Gin uses `binding` struct tags for request validation (backed by `go-playground/validator`).

```go
// Create request — all fields required
type CreateUserRequest struct {
    Email     string `json:"email" binding:"required,email"`
    Password  string `json:"password" binding:"required,min=8"`
    FirstName string `json:"first_name" binding:"required,min=1,max=100"`
    LastName  string `json:"last_name" binding:"required,min=1,max=100"`
}

// Update request — all fields optional (pointer types)
type UpdateUserRequest struct {
    FirstName *string `json:"first_name" binding:"omitempty,min=1,max=100"`
    LastName  *string `json:"last_name" binding:"omitempty,min=1,max=100"`
    IsActive  *bool   `json:"is_active"`
}
```

### Handler Binding Pattern

```go
func (h *UserHandler) CreateUser(c *gin.Context) {
    var req model.CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, model.NewErrorResponse(err.Error()))
        return
    }

    user, err := h.userService.Create(c.Request.Context(), &req)
    if err != nil {
        handleServiceError(c, err)
        return
    }

    c.JSON(http.StatusCreated, model.NewSuccessResponse(user.ToResponse()))
}
```

**Binding conventions:**
- Use `ShouldBindJSON` (not `BindJSON`) to control error responses yourself
- Use pointer fields for optional/partial update DTOs
- Always validate before passing to service layer
- Separate request DTOs from domain models

### Query Parameter Binding

```go
func (h *UserHandler) GetUsers(c *gin.Context) {
    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    perPage, _ := strconv.Atoi(c.DefaultQuery("per_page", "20"))

    users, total, err := h.userService.GetAll(c.Request.Context(), page, perPage)
    if err != nil {
        c.JSON(http.StatusInternalServerError, model.NewErrorResponse(err.Error()))
        return
    }

    responses := make([]*model.UserResponse, len(users))
    for i, user := range users {
        responses[i] = user.ToResponse()
    }

    c.JSON(http.StatusOK, model.NewPaginatedResponse(responses, page, perPage, total))
}
```

## Error Handling

### Standardized Response Models

```go
type Response struct {
    Success bool        `json:"success"`
    Message string      `json:"message,omitempty"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
}

type PaginatedResponse struct {
    Success bool        `json:"success"`
    Data    interface{} `json:"data"`
    Meta    *PageMeta   `json:"meta"`
}

type PageMeta struct {
    Page       int   `json:"page"`
    PerPage    int   `json:"per_page"`
    Total      int64 `json:"total"`
    TotalPages int   `json:"total_pages"`
}

func NewSuccessResponse(data interface{}) *Response {
    return &Response{Success: true, Data: data}
}

func NewErrorResponse(message string) *Response {
    return &Response{Success: false, Error: message}
}
```

### Service Error Mapping

Define domain errors in the service layer, map them to HTTP status in handlers:

```go
// service layer
var (
    ErrUserNotFound      = errors.New("user not found")
    ErrUserAlreadyExists = errors.New("user already exists")
    ErrInvalidCredentials = errors.New("invalid credentials")
)

// handler helper
func handleServiceError(c *gin.Context, err error) {
    switch {
    case errors.Is(err, service.ErrUserNotFound):
        c.JSON(http.StatusNotFound, model.NewErrorResponse(err.Error()))
    case errors.Is(err, service.ErrUserAlreadyExists):
        c.JSON(http.StatusConflict, model.NewErrorResponse(err.Error()))
    case errors.Is(err, service.ErrInvalidCredentials):
        c.JSON(http.StatusUnauthorized, model.NewErrorResponse(err.Error()))
    default:
        c.JSON(http.StatusInternalServerError, model.NewErrorResponse("internal server error"))
    }
}
```

**Error handling rules:**
- Never expose internal errors to clients in production
- Map domain errors to appropriate HTTP status codes
- Use `errors.Is` for sentinel errors, `errors.As` for typed errors
- Always return the standardized `Response` structure

## Application Setup

### Server with Graceful Shutdown

```go
func main() {
    cfg, err := config.Load()
    if err != nil {
        log.Fatalf("Failed to load config: %v", err)
    }

    if cfg.Environment == "production" {
        gin.SetMode(gin.ReleaseMode)
    }

    // Wire layers: repo -> service -> handler
    db, err := initDB(cfg.DatabaseURL)
    if err != nil {
        log.Fatalf("Failed to connect to database: %v", err)
    }

    repos := repository.NewRepositories(db)
    services := service.NewServices(repos, cfg)
    handlers := handler.NewHandlers(services)
    r := router.Setup(handlers, middleware.NewMiddleware(cfg))

    srv := &http.Server{
        Addr:         ":" + cfg.Port,
        Handler:      r,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("Server failed: %v", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatalf("Server forced to shutdown: %v", err)
    }
}
```

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

# Generate Swagger docs (with swaggo)
swag init -g cmd/api/main.go

# Database migrations (using golang-migrate)
migrate -path migrations -database "$DATABASE_URL" up
migrate -path migrations -database "$DATABASE_URL" down
```

## Dependencies

```go
// Core
github.com/gin-gonic/gin v1.9.1

// Auth
github.com/golang-jwt/jwt/v5 v5.0.0
golang.org/x/crypto v0.14.0

// Database
gorm.io/gorm v1.25.5
gorm.io/driver/postgres v1.5.4

// Config
github.com/joho/godotenv v1.5.1

// Testing
github.com/stretchr/testify v1.8.4

// Docs
github.com/swaggo/gin-swagger v1.6.0
github.com/swaggo/swag v1.16.2
```

## Advanced Topics

For detailed patterns and full implementation examples, see:

- [references/patterns.md](references/patterns.md) -- Handler implementations, database integration, authentication service, testing patterns, performance tuning

## External References

- [Gin Documentation](https://gin-gonic.com/docs/)
- [Gin GitHub](https://github.com/gin-gonic/gin)
- [GORM Documentation](https://gorm.io/docs/)
- [Go Project Layout](https://github.com/golang-standards/project-layout)
