---
skill_id: backend-patterns
name: Go Backend Patterns with Fiber
description: Backend architecture patterns for Go with Fiber v3 framework - API design, repository pattern, PostgreSQL/Redis integration, middleware, context propagation, and error handling. High performance with prefork and zero-allocation.
category: backend
tags: [go, fiber, postgresql, redis, api, middleware, repository, fasthttp]
applies_to: [go]
auto_trigger: ["fiber", "router", "api", "middleware", "repository", "pgx", "sqlc"]
---

# Go Backend Patterns with Fiber

Production-ready backend patterns for Go with Fiber v3 (fasthttp-based), PostgreSQL (pgx/sqlc), Redis caching, structured logging, and error handling. Optimized for high performance with prefork mode and zero-allocation.

## Core Architecture

```
HTTP Request
     │
     ▼
Fiber App (Middleware Chain)
     │
     ├─> RequestID Middleware
     ├─> Logger Middleware
     ├─> Recover Middleware
     ├─> CORS Middleware
     ├─> Auth Middleware
     ├─> Rate Limit Middleware
     │
     ▼
HTTP Handler
     │
     ├─> Validator (validate request)
     ├─> Service (business logic)
     │     │
     │     ├─> Repository (data access)
     │     │     ├─> PostgreSQL (pgx/sqlc)
     │     │     └─> Redis (caching)
     │     │
     │     └─> External APIs
     │
     └─> Response (JSON)
```

---

## 1. Fiber Router Patterns

### 1.1 Basic Router Setup with High Performance

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

    "github.com/gofiber/fiber/v3"
    "github.com/gofiber/fiber/v3/middleware/cors"
    "github.com/gofiber/fiber/v3/middleware/limiter"
    "github.com/gofiber/fiber/v3/middleware/logger"
    "github.com/gofiber/fiber/v3/middleware/recover"
    "github.com/gofiber/fiber/v3/middleware/requestid"
    "github.com/gofiber/fiber/v3/middleware/timeout"
    "github.com/goccy/go-json"
)

func main() {
    // Create Fiber app with high-performance config
    app := fiber.New(fiber.Config{
        // Performance settings
        Prefork:       true, // Enable prefork (multi-process)
        StrictRouting: false,
        CaseSensitive: false,

        // Timeouts
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,

        // Buffer sizes (tune based on your payloads)
        ReadBufferSize:  8192,
        WriteBufferSize: 8192,

        // Use faster JSON encoder/decoder
        JSONEncoder: json.Marshal,
        JSONDecoder: json.Unmarshal,

        // Error handling
        ErrorHandler: customErrorHandler,
    })

    // Core middleware (order matters!)
    app.Use(requestid.New())
    app.Use(logger.New(logger.Config{
        Format:     "${time} | ${status} | ${latency} | ${ip} | ${method} | ${path} | ${error}\n",
        TimeFormat: "2006-01-02 15:04:05",
    }))
    app.Use(recover.New(recover.Config{
        EnableStackTrace: true,
    }))
    app.Use(timeout.New(timeout.Config{
        Timeout: 60 * time.Second,
    }))

    // CORS middleware
    app.Use(cors.New(cors.Config{
        AllowOrigins:     []string{"https://*", "http://*"},
        AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"},
        AllowHeaders:     []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
        ExposeHeaders:    []string{"Link"},
        AllowCredentials: true,
        MaxAge:           300,
    }))

    // Health check (before auth)
    app.Get("/health", handleHealth)

    // API routes
    api := app.Group("/api/v1")

    // Public routes
    api.Post("/auth/login", handleLogin)
    api.Post("/auth/register", handleRegister)

    // Protected routes (with auth middleware)
    protected := api.Group("", authMiddleware)

    // Markets routes
    markets := protected.Group("/markets")
    markets.Get("/", handleListMarkets)
    markets.Post("/", handleCreateMarket)
    markets.Get("/:id", handleGetMarket)
    markets.Put("/:id", handleUpdateMarket)
    markets.Delete("/:id", handleDeleteMarket)

    // Orders routes
    orders := protected.Group("/orders")
    orders.Get("/", handleListOrders)
    orders.Post("/", handleCreateOrder)

    // Start server in goroutine
    go func() {
        log.Printf("Server starting on :8080 (Prefork: %v)", app.Config().Prefork)
        if err := app.Listen(":8080"); err != nil {
            log.Fatalf("Server failed: %v", err)
        }
    }()

    // Graceful shutdown
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
    <-quit

    log.Println("Shutting down server...")

    if err := app.ShutdownWithTimeout(10 * time.Second); err != nil {
        log.Fatalf("Server forced to shutdown: %v", err)
    }

    log.Println("Server exited")
}

func handleHealth(c fiber.Ctx) error {
    return c.JSON(fiber.Map{
        "status": "healthy",
    })
}

func customErrorHandler(c fiber.Ctx, err error) error {
    code := fiber.StatusInternalServerError

    // Check if it's a Fiber error
    if e, ok := err.(*fiber.Error); ok {
        code = e.Code
    }

    return c.Status(code).JSON(fiber.Map{
        "success": false,
        "error":   err.Error(),
    })
}
```

### 1.2 Auth Middleware

```go
// internal/middleware/auth.go
package middleware

import (
    "fmt"
    "strings"

    "github.com/gofiber/fiber/v3"
    "github.com/golang-jwt/jwt/v5"
)

type contextKey string

const UserContextKey contextKey = "user"

type Claims struct {
    UserID string `json:"user_id"`
    Email  string `json:"email"`
    Role   string `json:"role"`
    jwt.RegisteredClaims
}

func Auth(jwtSecret string) fiber.Handler {
    return func(c fiber.Ctx) error {
        // Extract token from Authorization header
        authHeader := c.Get("Authorization")
        if authHeader == "" {
            return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
                "success": false,
                "error":   "missing authorization header",
            })
        }

        tokenString := strings.TrimPrefix(authHeader, "Bearer ")

        // Parse and validate JWT
        token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
            if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
                return nil, fmt.Errorf("unexpected signing method")
            }
            return []byte(jwtSecret), nil
        })

        if err != nil || !token.Valid {
            return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
                "success": false,
                "error":   "invalid token",
            })
        }

        claims, ok := token.Claims.(*Claims)
        if !ok {
            return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
                "success": false,
                "error":   "invalid token claims",
            })
        }

        // Store user in Locals (Fiber's context storage)
        c.Locals("user", claims)

        return c.Next()
    }
}

// GetUser retrieves user claims from Fiber context
func GetUser(c fiber.Ctx) *Claims {
    user, ok := c.Locals("user").(*Claims)
    if !ok {
        return nil
    }
    return user
}

// RequireRole middleware checks if user has required role
func RequireRole(role string) fiber.Handler {
    return func(c fiber.Ctx) error {
        claims := GetUser(c)
        if claims == nil {
            return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
                "success": false,
                "error":   "unauthorized",
            })
        }

        if claims.Role != role && claims.Role != "admin" {
            return c.Status(fiber.StatusForbidden).JSON(fiber.Map{
                "success": false,
                "error":   "insufficient permissions",
            })
        }

        return c.Next()
    }
}
```

### 1.3 Rate Limiting Middleware

```go
// internal/middleware/ratelimit.go
package middleware

import (
    "time"

    "github.com/gofiber/fiber/v3"
    "github.com/gofiber/fiber/v3/middleware/limiter"
)

// RateLimiter returns a configured rate limiting middleware
func RateLimiter(max int, expiration time.Duration) fiber.Handler {
    return limiter.New(limiter.Config{
        Max:        max,
        Expiration: expiration,

        // Use IP address as rate limit key
        KeyGenerator: func(c fiber.Ctx) string {
            return c.IP()
        },

        // Custom response when limit is reached
        LimitReached: func(c fiber.Ctx) error {
            return c.Status(fiber.StatusTooManyRequests).JSON(fiber.Map{
                "success": false,
                "error":   "rate limit exceeded",
            })
        },

        // Use sliding window algorithm
        LimiterMiddleware: limiter.SlidingWindow{},
    })
}

// Usage:
// app.Use(middleware.RateLimiter(100, 1*time.Minute))
```

### 1.4 Structured Logging Middleware

```go
// internal/middleware/logger.go
package middleware

import (
    "log/slog"
    "time"

    "github.com/gofiber/fiber/v3"
    "github.com/gofiber/fiber/v3/middleware/requestid"
)

func StructuredLogger(logger *slog.Logger) fiber.Handler {
    return func(c fiber.Ctx) error {
        start := time.Now()

        // Process request
        err := c.Next()

        // Log after response
        logger.Info("http request",
            slog.String("method", c.Method()),
            slog.String("path", c.Path()),
            slog.Int("status", c.Response().StatusCode()),
            slog.Int("bytes", len(c.Response().Body())),
            slog.Duration("duration", time.Since(start)),
            slog.String("request_id", requestid.FromContext(c)),
            slog.String("ip", c.IP()),
        )

        return err
    }
}
```

---

## 2. Repository Pattern with PostgreSQL

### 2.1 Repository Interface

```go
// internal/domain/market.go
package domain

import (
    "context"
    "time"
)

type Market struct {
    ID          string    `json:"id"`
    Name        string    `json:"name"`
    Description string    `json:"description"`
    Status      string    `json:"status"`
    Volume      float64   `json:"volume"`
    CreatedAt   time.Time `json:"created_at"`
    UpdatedAt   time.Time `json:"updated_at"`
}

type MarketFilters struct {
    Status *string
    Limit  int
    Offset int
}

// MarketRepository defines the interface for market data access
type MarketRepository interface {
    FindAll(ctx context.Context, filters MarketFilters) ([]Market, error)
    FindByID(ctx context.Context, id string) (*Market, error)
    Create(ctx context.Context, market *Market) error
    Update(ctx context.Context, id string, market *Market) error
    Delete(ctx context.Context, id string) error
}
```

### 2.2 PostgreSQL Repository with pgx

```go
// internal/repository/market_postgres.go
package repository

import (
    "context"
    "fmt"
    "time"

    "github.com/google/uuid"
    "github.com/jackc/pgx/v5"
    "github.com/jackc/pgx/v5/pgxpool"

    "yourapp/internal/domain"
)

type PostgresMarketRepository struct {
    db *pgxpool.Pool
}

func NewPostgresMarketRepository(db *pgxpool.Pool) *PostgresMarketRepository {
    return &PostgresMarketRepository{db: db}
}

func (r *PostgresMarketRepository) FindAll(ctx context.Context, filters domain.MarketFilters) ([]domain.Market, error) {
    query := `
        SELECT id, name, description, status, volume, created_at, updated_at
        FROM markets
        WHERE ($1::text IS NULL OR status = $1)
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
    `

    var status *string
    if filters.Status != nil {
        status = filters.Status
    }

    rows, err := r.db.Query(ctx, query, status, filters.Limit, filters.Offset)
    if err != nil {
        return nil, fmt.Errorf("query failed: %w", err)
    }
    defer rows.Close()

    var markets []domain.Market
    for rows.Next() {
        var m domain.Market
        if err := rows.Scan(
            &m.ID,
            &m.Name,
            &m.Description,
            &m.Status,
            &m.Volume,
            &m.CreatedAt,
            &m.UpdatedAt,
        ); err != nil {
            return nil, fmt.Errorf("scan failed: %w", err)
        }
        markets = append(markets, m)
    }

    if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("rows error: %w", err)
    }

    return markets, nil
}

func (r *PostgresMarketRepository) FindByID(ctx context.Context, id string) (*domain.Market, error) {
    query := `
        SELECT id, name, description, status, volume, created_at, updated_at
        FROM markets
        WHERE id = $1
    `

    var m domain.Market
    err := r.db.QueryRow(ctx, query, id).Scan(
        &m.ID,
        &m.Name,
        &m.Description,
        &m.Status,
        &m.Volume,
        &m.CreatedAt,
        &m.UpdatedAt,
    )

    if err == pgx.ErrNoRows {
        return nil, fmt.Errorf("market not found")
    }

    if err != nil {
        return nil, fmt.Errorf("query failed: %w", err)
    }

    return &m, nil
}

func (r *PostgresMarketRepository) Create(ctx context.Context, market *domain.Market) error {
    query := `
        INSERT INTO markets (id, name, description, status, volume, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    `

    market.ID = uuid.NewString()
    market.CreatedAt = time.Now()
    market.UpdatedAt = time.Now()

    _, err := r.db.Exec(ctx, query,
        market.ID,
        market.Name,
        market.Description,
        market.Status,
        market.Volume,
        market.CreatedAt,
        market.UpdatedAt,
    )

    if err != nil {
        return fmt.Errorf("insert failed: %w", err)
    }

    return nil
}

func (r *PostgresMarketRepository) Update(ctx context.Context, id string, market *domain.Market) error {
    query := `
        UPDATE markets
        SET name = $2, description = $3, status = $4, volume = $5, updated_at = $6
        WHERE id = $1
    `

    market.UpdatedAt = time.Now()

    result, err := r.db.Exec(ctx, query,
        id,
        market.Name,
        market.Description,
        market.Status,
        market.Volume,
        market.UpdatedAt,
    )

    if err != nil {
        return fmt.Errorf("update failed: %w", err)
    }

    if result.RowsAffected() == 0 {
        return fmt.Errorf("market not found")
    }

    return nil
}

func (r *PostgresMarketRepository) Delete(ctx context.Context, id string) error {
    query := `DELETE FROM markets WHERE id = $1`

    result, err := r.db.Exec(ctx, query, id)
    if err != nil {
        return fmt.Errorf("delete failed: %w", err)
    }

    if result.RowsAffected() == 0 {
        return fmt.Errorf("market not found")
    }

    return nil
}
```

### 2.3 Database Connection Pool

```go
// internal/database/postgres.go
package database

import (
    "context"
    "fmt"
    "time"

    "github.com/jackc/pgx/v5/pgxpool"
)

type Config struct {
    Host     string
    Port     int
    User     string
    Password string
    DBName   string
    SSLMode  string
}

func NewPostgresPool(ctx context.Context, cfg Config) (*pgxpool.Pool, error) {
    dsn := fmt.Sprintf(
        "host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
        cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.DBName, cfg.SSLMode,
    )

    config, err := pgxpool.ParseConfig(dsn)
    if err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }

    // Connection pool settings
    config.MaxConns = 25
    config.MinConns = 5
    config.MaxConnLifetime = time.Hour
    config.MaxConnIdleTime = 30 * time.Minute
    config.HealthCheckPeriod = time.Minute

    pool, err := pgxpool.NewWithConfig(ctx, config)
    if err != nil {
        return nil, fmt.Errorf("failed to create pool: %w", err)
    }

    // Test connection
    if err := pool.Ping(ctx); err != nil {
        return nil, fmt.Errorf("failed to ping database: %w", err)
    }

    return pool, nil
}
```

---

## 3. Redis Caching Pattern

### 3.1 Cached Repository (Cache-Aside Pattern)

```go
// internal/repository/market_cached.go
package repository

import (
    "context"
    "encoding/json"
    "fmt"
    "time"

    "github.com/redis/go-redis/v9"

    "yourapp/internal/domain"
)

type CachedMarketRepository struct {
    base  domain.MarketRepository
    redis *redis.Client
    ttl   time.Duration
}

func NewCachedMarketRepository(base domain.MarketRepository, redis *redis.Client, ttl time.Duration) *CachedMarketRepository {
    return &CachedMarketRepository{
        base:  base,
        redis: redis,
        ttl:   ttl,
    }
}

func (r *CachedMarketRepository) FindByID(ctx context.Context, id string) (*domain.Market, error) {
    cacheKey := fmt.Sprintf("market:%s", id)

    // Try cache first
    cached, err := r.redis.Get(ctx, cacheKey).Result()
    if err == nil {
        var market domain.Market
        if err := json.Unmarshal([]byte(cached), &market); err == nil {
            return &market, nil
        }
    }

    // Cache miss - fetch from database
    market, err := r.base.FindByID(ctx, id)
    if err != nil {
        return nil, err
    }

    // Update cache (fire and forget)
    go func() {
        data, err := json.Marshal(market)
        if err == nil {
            r.redis.Set(context.Background(), cacheKey, data, r.ttl)
        }
    }()

    return market, nil
}

func (r *CachedMarketRepository) Create(ctx context.Context, market *domain.Market) error {
    if err := r.base.Create(ctx, market); err != nil {
        return err
    }

    // Invalidate list cache
    r.redis.Del(ctx, "markets:list:*")

    return nil
}

func (r *CachedMarketRepository) Update(ctx context.Context, id string, market *domain.Market) error {
    if err := r.base.Update(ctx, id, market); err != nil {
        return err
    }

    // Invalidate cache
    cacheKey := fmt.Sprintf("market:%s", id)
    r.redis.Del(ctx, cacheKey)

    return nil
}

func (r *CachedMarketRepository) Delete(ctx context.Context, id string) error {
    if err := r.base.Delete(ctx, id); err != nil {
        return err
    }

    // Invalidate cache
    cacheKey := fmt.Sprintf("market:%s", id)
    r.redis.Del(ctx, cacheKey)

    return nil
}

func (r *CachedMarketRepository) FindAll(ctx context.Context, filters domain.MarketFilters) ([]domain.Market, error) {
    // For simplicity, bypass cache for list queries
    // In production, consider caching with filters as key
    return r.base.FindAll(ctx, filters)
}
```

### 3.2 Redis Client Setup

```go
// internal/cache/redis.go
package cache

import (
    "context"
    "fmt"

    "github.com/redis/go-redis/v9"
)

func NewRedisClient(addr, password string, db int) (*redis.Client, error) {
    client := redis.NewClient(&redis.Options{
        Addr:         addr,
        Password:     password,
        DB:           db,
        PoolSize:     10,
        MinIdleConns: 5,
    })

    // Test connection
    if err := client.Ping(context.Background()).Err(); err != nil {
        return nil, fmt.Errorf("failed to connect to Redis: %w", err)
    }

    return client, nil
}
```

---

## 4. Service Layer Pattern

### 4.1 Service with Business Logic

```go
// internal/service/market_service.go
package service

import (
    "context"
    "fmt"

    "yourapp/internal/domain"
)

type MarketService struct {
    repo domain.MarketRepository
}

func NewMarketService(repo domain.MarketRepository) *MarketService {
    return &MarketService{repo: repo}
}

func (s *MarketService) ListMarkets(ctx context.Context, filters domain.MarketFilters) ([]domain.Market, error) {
    // Apply business rules
    if filters.Limit <= 0 {
        filters.Limit = 20 // Default limit
    }

    if filters.Limit > 100 {
        filters.Limit = 100 // Max limit
    }

    return s.repo.FindAll(ctx, filters)
}

func (s *MarketService) GetMarket(ctx context.Context, id string) (*domain.Market, error) {
    market, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("failed to get market: %w", err)
    }

    return market, nil
}

func (s *MarketService) CreateMarket(ctx context.Context, market *domain.Market) error {
    // Validate business rules
    if market.Name == "" {
        return fmt.Errorf("market name is required")
    }

    if market.Status == "" {
        market.Status = "draft" // Default status
    }

    if err := s.repo.Create(ctx, market); err != nil {
        return fmt.Errorf("failed to create market: %w", err)
    }

    // Could trigger events here (e.g., publish to queue)

    return nil
}

func (s *MarketService) UpdateMarket(ctx context.Context, id string, market *domain.Market) error {
    // Check if market exists
    existing, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return fmt.Errorf("market not found: %w", err)
    }

    // Business logic: prevent status change from 'closed' to 'active'
    if existing.Status == "closed" && market.Status == "active" {
        return fmt.Errorf("cannot reopen closed market")
    }

    if err := s.repo.Update(ctx, id, market); err != nil {
        return fmt.Errorf("failed to update market: %w", err)
    }

    return nil
}

func (s *MarketService) DeleteMarket(ctx context.Context, id string) error {
    if err := s.repo.Delete(ctx, id); err != nil {
        return fmt.Errorf("failed to delete market: %w", err)
    }

    return nil
}
```

---

## 5. HTTP Handlers

### 5.1 RESTful Handler

```go
// internal/handler/market_handler.go
package handler

import (
    "github.com/gofiber/fiber/v3"

    "yourapp/internal/domain"
    "yourapp/internal/service"
)

type MarketHandler struct {
    service *service.MarketService
}

func NewMarketHandler(service *service.MarketService) *MarketHandler {
    return &MarketHandler{service: service}
}

func (h *MarketHandler) HandleListMarkets(c fiber.Ctx) error {
    // Parse query parameters
    filters := domain.MarketFilters{
        Limit:  20,
        Offset: 0,
    }

    if status := c.Query("status"); status != "" {
        filters.Status = &status
    }

    markets, err := h.service.ListMarkets(c.Context(), filters)
    if err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
            "success": false,
            "error":   "failed to list markets",
        })
    }

    return c.JSON(fiber.Map{
        "success": true,
        "data":    markets,
    })
}

func (h *MarketHandler) HandleGetMarket(c fiber.Ctx) error {
    id := c.Params("id")

    market, err := h.service.GetMarket(c.Context(), id)
    if err != nil {
        return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
            "success": false,
            "error":   "market not found",
        })
    }

    return c.JSON(fiber.Map{
        "success": true,
        "data":    market,
    })
}

func (h *MarketHandler) HandleCreateMarket(c fiber.Ctx) error {
    var market domain.Market
    if err := c.Bind().Body(&market); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "error":   "invalid request body",
        })
    }

    if err := h.service.CreateMarket(c.Context(), &market); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "error":   err.Error(),
        })
    }

    return c.Status(fiber.StatusCreated).JSON(fiber.Map{
        "success": true,
        "data":    market,
    })
}

func (h *MarketHandler) HandleUpdateMarket(c fiber.Ctx) error {
    id := c.Params("id")

    var market domain.Market
    if err := c.Bind().Body(&market); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "error":   "invalid request body",
        })
    }

    if err := h.service.UpdateMarket(c.Context(), id, &market); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "error":   err.Error(),
        })
    }

    return c.JSON(fiber.Map{
        "success": true,
        "data":    market,
    })
}

func (h *MarketHandler) HandleDeleteMarket(c fiber.Ctx) error {
    id := c.Params("id")

    if err := h.service.DeleteMarket(c.Context(), id); err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
            "success": false,
            "error":   err.Error(),
        })
    }

    return c.JSON(fiber.Map{
        "success": true,
        "message": "market deleted",
    })
}
```

---

## 6. Request Validation

### 6.1 Validator with go-playground/validator

```go
// internal/validator/validator.go
package validator

import (
    "fmt"

    "github.com/go-playground/validator/v10"
    "github.com/gofiber/fiber/v3"
)

type Validator struct {
    validate *validator.Validate
}

func New() *Validator {
    return &Validator{
        validate: validator.New(),
    }
}

func (v *Validator) Validate(data interface{}) error {
    if err := v.validate.Struct(data); err != nil {
        if validationErrors, ok := err.(validator.ValidationErrors); ok {
            return fmt.Errorf("validation failed: %v", validationErrors)
        }
        return err
    }
    return nil
}

// Example usage
type CreateMarketRequest struct {
    Name        string  `json:"name" validate:"required,min=3,max=100"`
    Description string  `json:"description" validate:"required,max=500"`
    Volume      float64 `json:"volume" validate:"gte=0"`
}

func (h *MarketHandler) HandleCreateMarketWithValidation(c fiber.Ctx) error {
    var req CreateMarketRequest
    if err := c.Bind().Body(&req); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "error":   "invalid request body",
        })
    }

    // Validate
    v := New()
    if err := v.Validate(req); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "success": false,
            "error":   err.Error(),
        })
    }

    // Process request...
    return nil
}
```

---

## 7. Error Handling Patterns

### 7.1 Custom Error Types

```go
// internal/errors/errors.go
package errors

import (
    "github.com/gofiber/fiber/v3"
)

type AppError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
    Status  int    `json:"-"`
}

func (e *AppError) Error() string {
    return e.Message
}

// Predefined errors
var (
    ErrNotFound = &AppError{
        Code:    "NOT_FOUND",
        Message: "resource not found",
        Status:  fiber.StatusNotFound,
    }

    ErrUnauthorized = &AppError{
        Code:    "UNAUTHORIZED",
        Message: "unauthorized",
        Status:  fiber.StatusUnauthorized,
    }

    ErrValidation = &AppError{
        Code:    "VALIDATION_ERROR",
        Message: "validation failed",
        Status:  fiber.StatusBadRequest,
    }

    ErrInternal = &AppError{
        Code:    "INTERNAL_ERROR",
        Message: "internal server error",
        Status:  fiber.StatusInternalServerError,
    }
)

func NewError(code, message string, status int) *AppError {
    return &AppError{
        Code:    code,
        Message: message,
        Status:  status,
    }
}

// ErrorHandler is a custom Fiber error handler
func ErrorHandler(c fiber.Ctx, err error) error {
    // Check for AppError
    if appErr, ok := err.(*AppError); ok {
        return c.Status(appErr.Status).JSON(fiber.Map{
            "success": false,
            "error": fiber.Map{
                "code":    appErr.Code,
                "message": appErr.Message,
            },
        })
    }

    // Check for Fiber error
    if fiberErr, ok := err.(*fiber.Error); ok {
        return c.Status(fiberErr.Code).JSON(fiber.Map{
            "success": false,
            "error":   fiberErr.Message,
        })
    }

    // Default internal error
    return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
        "success": false,
        "error":   "internal server error",
    })
}
```

### 7.2 Error Wrapping

```go
// Always wrap errors with context
func (r *PostgresMarketRepository) FindByID(ctx context.Context, id string) (*domain.Market, error) {
    var m domain.Market
    err := r.db.QueryRow(ctx, query, id).Scan(&m.ID, &m.Name, ...)

    if err == pgx.ErrNoRows {
        return nil, fmt.Errorf("market not found: %w", err)
    }

    if err != nil {
        return nil, fmt.Errorf("failed to query market: %w", err)
    }

    return &m, nil
}
```

---

## 8. Context Propagation

### 8.1 Context with Timeout

```go
func (h *MarketHandler) HandleCreateMarket(c fiber.Ctx) error {
    // Fiber Ctx implements context.Context in v3
    // Add timeout if needed
    ctx, cancel := context.WithTimeout(c.Context(), 5*time.Second)
    defer cancel()

    var market domain.Market
    if err := c.Bind().Body(&market); err != nil {
        return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
            "error": "invalid request",
        })
    }

    if err := h.service.CreateMarket(ctx, &market); err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
            "error": err.Error(),
        })
    }

    return c.Status(fiber.StatusCreated).JSON(market)
}
```

### 8.2 Context Values with Fiber Locals

```go
// Add request ID to context (in middleware)
func RequestIDMiddleware() fiber.Handler {
    return func(c fiber.Ctx) error {
        requestID := uuid.NewString()
        c.Locals("request_id", requestID)
        return c.Next()
    }
}

// Access request ID in handler
func (h *Handler) SomeHandler(c fiber.Ctx) error {
    requestID, _ := c.Locals("request_id").(string)
    log.Printf("Request ID: %s", requestID)
    return nil
}

// Type-safe access (Fiber v3)
func getRequestID(c fiber.Ctx) string {
    if id, ok := c.Locals("request_id").(string); ok {
        return id
    }
    return ""
}
```

---

## 9. Best Practices

### DO

```go
// Use Fiber's built-in context (implements context.Context)
func (s *Service) FetchData(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
        // Continue processing
    }
}

// Always check errors (NEVER ignore)
data, err := json.Marshal(obj)
if err != nil {
    return fmt.Errorf("failed to marshal: %w", err)
}

// Return errors from handlers
func handler(c fiber.Ctx) error {
    if err := doSomething(); err != nil {
        return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
            "error": err.Error(),
        })
    }
    return c.JSON(result)
}

// Use parameterized queries (pgx handles this)
query := "SELECT * FROM markets WHERE id = $1"
err := db.QueryRow(ctx, query, id).Scan(...)

// Close rows after use
rows, err := db.Query(ctx, query)
if err != nil {
    return err
}
defer rows.Close()

// Use structured logging
slog.Info("market created",
    slog.String("market_id", market.ID),
    slog.String("name", market.Name),
)

// Graceful shutdown with Fiber
quit := make(chan os.Signal, 1)
signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
<-quit
app.ShutdownWithTimeout(10 * time.Second)

// Copy strings in goroutines (zero-allocation mode)
id := c.Params("id")
idCopy := utils.CopyString(id) // or string([]byte(id))
go processAsync(idCopy)
```

### DON'T

```go
// Never ignore errors
data, _ := json.Marshal(obj) // WRONG

// Don't use SELECT * in production
query := "SELECT * FROM markets" // WRONG
query := "SELECT id, name, status FROM markets" // CORRECT

// Don't forget to defer Close()
rows, _ := db.Query(ctx, query)
// WRONG: Forgot defer rows.Close()

// Don't use string concatenation for SQL (SQL injection risk)
query := "SELECT * FROM markets WHERE id = '" + id + "'" // DANGEROUS
query := "SELECT * FROM markets WHERE id = $1" // CORRECT

// Don't pass context values to goroutines without copying (in zero-allocation mode)
id := c.Params("id")
go processAsync(id) // WRONG - id may be reused

// Don't block with fmt.Println in production
fmt.Println("Debug info") // WRONG
slog.Info("debug info") // CORRECT

// Don't create new connections per request
func handler(c fiber.Ctx) error {
    db, _ := sql.Open(...) // WRONG
}
```

---

## 10. Project Structure

```
project-root/
├── cmd/
│   ├── api/              # API server entry point
│   │   └── main.go
│   └── worker/           # Background worker entry point
│       └── main.go
├── internal/
│   ├── domain/           # Business entities
│   │   ├── market.go
│   │   └── order.go
│   ├── repository/       # Data access layer
│   │   ├── market_postgres.go
│   │   ├── market_cached.go
│   │   └── order_postgres.go
│   ├── service/          # Business logic
│   │   ├── market_service.go
│   │   └── order_service.go
│   ├── handler/          # HTTP handlers
│   │   ├── market_handler.go
│   │   └── order_handler.go
│   ├── middleware/       # Fiber middleware
│   │   ├── auth.go
│   │   ├── logger.go
│   │   └── ratelimit.go
│   ├── database/         # Database setup
│   │   └── postgres.go
│   ├── cache/            # Cache setup
│   │   └── redis.go
│   └── errors/           # Custom errors
│       └── errors.go
├── migrations/           # Database migrations
│   ├── 001_create_markets.up.sql
│   └── 001_create_markets.down.sql
├── pkg/                  # Public libraries (optional)
├── config/               # Configuration
│   └── config.go
├── go.mod
└── go.sum
```

---

## Quick Reference

### Fiber Router
```go
app := fiber.New(fiber.Config{Prefork: true})
app.Use(logger.New())
app.Get("/path", handler)
api := app.Group("/api")
api.Get("/users", getUsers)
```

### Fiber Handler Signature
```go
func handler(c fiber.Ctx) error {
    return c.JSON(data)
}
```

### Route Parameters
```go
id := c.Params("id")           // string
id := fiber.Params[int](c, "id") // typed (v3)
```

### Query Parameters
```go
status := c.Query("status")
page := c.QueryInt("page", 1) // with default
```

### Request Body
```go
var req MyStruct
if err := c.Bind().Body(&req); err != nil {
    return err
}
```

### JSON Response
```go
return c.JSON(data)
return c.Status(201).JSON(data)
return c.Status(400).JSON(fiber.Map{"error": "bad request"})
```

### PostgreSQL with pgx
```go
pool, _ := pgxpool.New(ctx, dsn)
rows, _ := pool.Query(ctx, "SELECT * FROM markets WHERE id = $1", id)
defer rows.Close()
```

### Redis Caching
```go
client := redis.NewClient(&redis.Options{Addr: "localhost:6379"})
client.Set(ctx, "key", "value", 5*time.Minute)
val, _ := client.Get(ctx, "key").Result()
```

### Error Wrapping
```go
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

---

## Resources

- [Fiber Documentation](https://docs.gofiber.io/)
- [Fiber v3 Migration Guide](https://docs.gofiber.io/next/guide/migration-v3)
- [pgx PostgreSQL Driver](https://github.com/jackc/pgx)
- [go-redis](https://github.com/redis/go-redis)
- [go-playground/validator](https://github.com/go-playground/validator)
- [Effective Go](https://go.dev/doc/effective_go)
