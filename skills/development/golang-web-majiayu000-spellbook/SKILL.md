---
name: golang-web
description: Modern Go Web application architecture guide. Use when creating new Go web projects, APIs, or microservices. Covers project structure, tech stack selection, and best practices based on Go standards.
---
# Go Web Architecture

## Core Principles

- **Standard layout** — Follow cmd/internal/pkg convention
- **Explicit dependencies** — Wire dependencies in main.go, no globals
- **Interface-driven** — Define interfaces where you use them, not where you implement
- **Error wrapping** — Wrap errors with context, use error codes
- **No backwards compatibility** — Delete, don't deprecate. Change directly
- **LiteLLM for LLM APIs** — Use LiteLLM proxy for all LLM integrations

---

## No Backwards Compatibility

> **Delete unused code. Change directly. No compatibility layers.**

```go
// ❌ BAD: Deprecated function kept around
// Deprecated: Use NewUserService instead
func CreateUserService() *UserService { ... }

// ❌ BAD: Alias for renamed types
type OldName = NewName // "for backwards compatibility"

// ❌ BAD: Unused parameters
func Process(_ context.Context, data Data) { ... }

// ✅ GOOD: Just delete and update all usages
func NewUserService(repo UserRepository) *UserService { ... }
```

---

## LiteLLM for LLM APIs

> **Use LiteLLM proxy. Don't call provider APIs directly.**

```go
// adapters/llm/client.go
package llm

import (
    "github.com/sashabaranov/go-openai"
)

// Connect to LiteLLM proxy using OpenAI-compatible SDK
func NewClient(cfg Config) *openai.Client {
    config := openai.DefaultConfig(cfg.APIKey)
    config.BaseURL = cfg.BaseURL // LiteLLM proxy URL
    return openai.NewClientWithConfig(config)
}
```

---

## Quick Start

### 1. Initialize Project

```bash
mkdir myapp && cd myapp
go mod init github.com/yourname/myapp

# Install core dependencies
go get github.com/gin-gonic/gin
go get github.com/spf13/viper
go get github.com/sirupsen/logrus
go get gorm.io/gorm
```

### 2. Apply Tech Stack

| Layer | Recommendation |
|-------|----------------|
| HTTP Framework | Gin / Chi / Echo |
| Configuration | Viper |
| Logging | Logrus / Zap / Slog |
| Database ORM | GORM / sqlx / sqlc |
| Validation | go-playground/validator |
| Testing | testify / go test |

### Version Strategy

> **Always get latest. Never pin in templates.**

```bash
# Always fetch latest
go get -u github.com/gin-gonic/gin
go get -u ./...

# go.mod handles version locking
# go.sum ensures reproducible builds
```

### 3. Use Standard Structure

```
myapp/
├── cmd/
│   └── myapp/
│       └── main.go            # Entry point, dependency wiring
├── configs/
│   └── config.go              # Configuration struct + loader
├── internal/                  # Private application code
│   ├── handlers/              # HTTP handlers
│   ├── services/              # Business logic
│   ├── repositories/          # Data access
│   ├── models/                # Domain models
│   ├── middleware/            # HTTP middleware
│   └── router/                # Route definitions
├── pkg/                       # Public reusable packages
│   ├── errors/                # Error types
│   ├── logger/                # Logging setup
│   ├── response/              # Unified response format
│   └── database/              # Database connection
├── config.yaml                # Configuration file
├── Makefile                   # Build automation
├── Dockerfile
└── go.mod
```

---

## Architecture Layers

### cmd/ — Entry Point

Wire all dependencies here. No business logic.

```go
// cmd/myapp/main.go
func main() {
    // Load config
    cfg := configs.Load()

    // Initialize infrastructure
    db := database.New(cfg.Database)
    cache := cache.New(cfg.Redis)
    logger := logger.New(cfg.Log)

    // Initialize repositories
    userRepo := repositories.NewUserRepository(db)

    // Initialize services
    userService := services.NewUserService(userRepo)

    // Initialize handlers
    userHandler := handlers.NewUserHandler(userService)

    // Setup router
    r := router.Setup(cfg, userHandler)

    // Start server with graceful shutdown
    server.Run(r, cfg.Server)
}
```

### internal/ — Private Business Code

#### handlers/ — HTTP Layer

```go
// internal/handlers/user.go
type UserHandler struct {
    service services.UserService
}

func NewUserHandler(s services.UserService) *UserHandler {
    return &UserHandler{service: s}
}

func (h *UserHandler) Create(c *gin.Context) {
    var input CreateUserInput
    if err := c.ShouldBindJSON(&input); err != nil {
        response.Error(c, errors.ErrInvalidParams)
        return
    }

    user, err := h.service.Create(c.Request.Context(), input)
    if err != nil {
        response.Error(c, err)
        return
    }

    response.Success(c, user)
}
```

#### services/ — Business Logic

```go
// internal/services/user.go
type UserService interface {
    Create(ctx context.Context, input CreateUserInput) (*models.User, error)
    GetByID(ctx context.Context, id string) (*models.User, error)
}

type userService struct {
    repo repositories.UserRepository
}

func NewUserService(repo repositories.UserRepository) UserService {
    return &userService{repo: repo}
}

func (s *userService) Create(ctx context.Context, input CreateUserInput) (*models.User, error) {
    existing, _ := s.repo.FindByEmail(ctx, input.Email)
    if existing != nil {
        return nil, errors.ErrUserExists
    }

    user := &models.User{
        ID:    uuid.New().String(),
        Email: input.Email,
        Name:  input.Name,
    }

    return s.repo.Save(ctx, user)
}
```

#### repositories/ — Data Access

```go
// internal/repositories/user.go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*models.User, error)
    FindByEmail(ctx context.Context, email string) (*models.User, error)
    Save(ctx context.Context, user *models.User) (*models.User, error)
    Delete(ctx context.Context, id string) error
}

type userRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) UserRepository {
    return &userRepository{db: db}
}

func (r *userRepository) FindByID(ctx context.Context, id string) (*models.User, error) {
    var user models.User
    if err := r.db.WithContext(ctx).First(&user, "id = ?", id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, nil
        }
        return nil, err
    }
    return &user, nil
}
```

### pkg/ — Reusable Packages

#### errors/ — Error Handling

```go
// pkg/errors/errors.go
type AppError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
    Cause   error  `json:"-"`
}

func (e *AppError) Error() string { return e.Message }
func (e *AppError) Unwrap() error { return e.Cause }

func New(code int, message string) *AppError {
    return &AppError{Code: code, Message: message}
}

func Wrap(err error, code int, message string) *AppError {
    return &AppError{Code: code, Message: message, Cause: err}
}

// Predefined errors
var (
    ErrInternal      = New(500, "internal server error")
    ErrInvalidParams = New(400, "invalid parameters")
    ErrNotFound      = New(404, "resource not found")
    ErrUnauthorized  = New(401, "unauthorized")
    ErrUserExists    = New(409, "user already exists")
)
```

#### response/ — Unified Response

```go
// pkg/response/response.go
type Response struct {
    Code    int         `json:"code"`
    Message string      `json:"message"`
    Data    interface{} `json:"data,omitempty"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, Response{
        Code:    0,
        Message: "success",
        Data:    data,
    })
}

func Error(c *gin.Context, err error) {
    var appErr *errors.AppError
    if errors.As(err, &appErr) {
        c.JSON(appErr.Code/100, Response{
            Code:    appErr.Code,
            Message: appErr.Message,
        })
        return
    }
    c.JSON(http.StatusInternalServerError, Response{
        Code:    500,
        Message: "internal server error",
    })
}
```

---

## Configuration

### Viper + YAML + Environment Variables

```go
// configs/config.go
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
    Redis    RedisConfig    `mapstructure:"redis"`
    Log      LogConfig      `mapstructure:"log"`
    LLM      LLMConfig      `mapstructure:"llm"`
}

type LLMConfig struct {
    BaseURL      string `mapstructure:"base_url"`
    APIKey       string `mapstructure:"api_key"`
    DefaultModel string `mapstructure:"default_model"`
}

func Load() *Config {
    viper.SetConfigFile("config.yaml")
    viper.AutomaticEnv()
    viper.SetEnvPrefix("APP")
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    // Defaults
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("llm.base_url", "http://localhost:4000")
    viper.SetDefault("llm.default_model", "gpt-4o")

    viper.ReadInConfig()

    var cfg Config
    viper.Unmarshal(&cfg)
    return &cfg
}
```

---

## Graceful Shutdown

```go
// pkg/server/server.go
func Run(handler http.Handler, cfg ServerConfig) {
    srv := &http.Server{
        Addr:         fmt.Sprintf(":%d", cfg.Port),
        Handler:      handler,
        ReadTimeout:  cfg.ReadTimeout,
        WriteTimeout: cfg.WriteTimeout,
    }

    go func() {
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatalf("Server error: %v", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    srv.Shutdown(ctx)
}
```

---

## Makefile

```makefile
.PHONY: build run test lint clean

APP_NAME=myapp

build:
	go build -o bin/$(APP_NAME) ./cmd/$(APP_NAME)

run:
	go run ./cmd/$(APP_NAME)

dev:
	air

test:
	go test -v ./...

lint:
	golangci-lint run

clean:
	rm -rf bin/

tidy:
	go mod tidy

upgrade:
	go get -u ./...
	go mod tidy
```

---

## Checklist

```markdown
## Project Setup
- [ ] Go 1.21+ installed
- [ ] Standard directory structure (cmd/internal/pkg)
- [ ] go.mod initialized
- [ ] Makefile created

## Architecture
- [ ] Dependencies wired in main.go
- [ ] Handlers → Services → Repositories layers
- [ ] Interfaces defined at usage site
- [ ] No circular dependencies

## Infrastructure
- [ ] Configuration with Viper
- [ ] Structured logging
- [ ] Custom error types
- [ ] Unified response format
- [ ] Graceful shutdown

## Quality
- [ ] Tests for services
- [ ] golangci-lint configured
- [ ] go vet passes
- [ ] Race detection tested
```

---

## See Also

- [reference/architecture.md](reference/architecture.md) — Detailed architecture patterns
- [reference/tech-stack.md](reference/tech-stack.md) — Tech stack comparison
- [reference/patterns.md](reference/patterns.md) — Go design patterns
