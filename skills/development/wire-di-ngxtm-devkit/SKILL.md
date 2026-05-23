---
name: Wire Dependency Injection
description: Compile-time dependency injection from Google.
metadata:
  labels: [golang, wire, di, dependency-injection]
  triggers:
    files: ['**/wire.go', '**/wire_gen.go']
    keywords: [wire, Build, NewSet, Bind, Injector]
---

# Wire DI Standards

## Basic Setup

```go
// wire.go
//go:build wireinject
// +build wireinject

package main

import "github.com/google/wire"

func InitializeApp() (*App, error) {
    wire.Build(
        NewDatabase,
        NewUserRepository,
        NewUserService,
        NewApp,
    )
    return nil, nil
}
```

```bash
# Generate wire_gen.go
wire ./...
```

## Providers

```go
// Providers are constructors
func NewDatabase(cfg *Config) (*sql.DB, error) {
    return sql.Open("postgres", cfg.DatabaseURL)
}

func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}

func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}

func NewApp(svc *UserService) *App {
    return &App{userService: svc}
}
```

## Provider Sets

```go
// Group related providers
var DatabaseSet = wire.NewSet(
    NewDatabase,
    NewUserRepository,
    NewPostRepository,
)

var ServiceSet = wire.NewSet(
    NewUserService,
    NewPostService,
)

// Use sets in injector
func InitializeApp(cfg *Config) (*App, error) {
    wire.Build(
        DatabaseSet,
        ServiceSet,
        NewApp,
    )
    return nil, nil
}
```

## Interface Binding

```go
type UserRepository interface {
    FindByID(id int) (*User, error)
}

type userRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) *userRepository {
    return &userRepository{db: db}
}

// Bind implementation to interface
var RepositorySet = wire.NewSet(
    NewUserRepository,
    wire.Bind(new(UserRepository), new(*userRepository)),
)
```

## Struct Providers

```go
type Config struct {
    DatabaseURL string
    Port        int
}

// Provide struct fields
var ConfigSet = wire.NewSet(
    wire.Struct(new(Config), "*"), // All fields
    // or
    wire.Struct(new(Config), "DatabaseURL", "Port"), // Specific fields
)

// Field providers must exist
func InitializeApp(dbURL string, port int) (*App, error) {
    wire.Build(
        ConfigSet,
        // ...
    )
    return nil, nil
}
```

## Value Providers

```go
func InitializeApp() (*App, error) {
    wire.Build(
        wire.Value(&Config{
            DatabaseURL: "postgres://...",
            Port:        8080,
        }),
        NewDatabase,
        NewApp,
    )
    return nil, nil
}

// Or interface value
wire.InterfaceValue(new(io.Writer), os.Stdout)
```

## Cleanup Functions

```go
func NewDatabase(cfg *Config) (*sql.DB, func(), error) {
    db, err := sql.Open("postgres", cfg.DatabaseURL)
    if err != nil {
        return nil, nil, err
    }

    cleanup := func() {
        db.Close()
    }

    return db, cleanup, nil
}

// Injector returns cleanup
func InitializeApp(cfg *Config) (*App, func(), error) {
    wire.Build(
        NewDatabase,
        NewApp,
    )
    return nil, nil, nil
}

// Usage
app, cleanup, err := InitializeApp(cfg)
if err != nil {
    log.Fatal(err)
}
defer cleanup()
```

## Multiple Injectors

```go
// wire.go
//go:build wireinject

package main

import "github.com/google/wire"

// For HTTP server
func InitializeHTTPServer(cfg *Config) (*HTTPServer, func(), error) {
    wire.Build(
        DatabaseSet,
        HTTPSet,
    )
    return nil, nil, nil
}

// For CLI
func InitializeCLI(cfg *Config) (*CLI, error) {
    wire.Build(
        DatabaseSet,
        CLISet,
    )
    return nil, nil
}
```

## Testing

```go
// Mock for testing
type mockUserRepository struct{}

func (m *mockUserRepository) FindByID(id int) (*User, error) {
    return &User{ID: id, Name: "Test"}, nil
}

// Test injector
func InitializeTestApp() (*App, error) {
    wire.Build(
        wire.Value(&mockUserRepository{}),
        wire.Bind(new(UserRepository), new(*mockUserRepository)),
        NewUserService,
        NewApp,
    )
    return nil, nil
}
```

## Best Practices

1. **Provider sets**: Group related providers
2. **Interfaces**: Use `wire.Bind` for testability
3. **Cleanup**: Return cleanup functions for resources
4. **Build tags**: Use `wireinject` build tag
5. **Regenerate**: Run `wire ./...` after changes
