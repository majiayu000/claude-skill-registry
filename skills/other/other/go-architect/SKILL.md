---
name: go-architect
description: Go application architecture with net/http 1.22+ routing, project structure patterns, graceful shutdown, and dependency injection. Use when building Go web servers, designing project layout, or structuring application dependencies.
---

# Lead Go Architect

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Flat vs modular project layout, migration signals | [references/project-structure.md](references/project-structure.md) |
| Graceful shutdown with signal handling | [references/graceful-shutdown.md](references/graceful-shutdown.md) |
| Dependency injection patterns, testing seams | [references/dependency-injection.md](references/dependency-injection.md) |

## Core Principles

1. **Standard library first** -- Use `net/http` and the Go 1.22+ enhanced `ServeMux` for routing. Only reach for a framework (chi, echo, gin) when you have a concrete need the stdlib cannot satisfy (e.g., complex middleware chains, regex routes).
2. **Dependency injection over globals** -- Pass databases, loggers, and services through struct fields and constructors, never package-level `var`.
3. **Explicit over magic** -- No `init()` side effects, no framework auto-wiring. `main.go` is the composition root where everything is assembled visibly.
4. **Small interfaces, big structs** -- Define interfaces at the consumer, keep them narrow (1-3 methods). Concrete types carry the implementation.

## Go 1.22+ Enhanced Routing

Go 1.22 upgraded `http.ServeMux` with method-based routing and path parameters, eliminating the most common reason for third-party routers.

### Method-Based Routing and Path Parameters

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /api/users", s.handleListUsers)
mux.HandleFunc("GET /api/users/{id}", s.handleGetUser)
mux.HandleFunc("POST /api/users", s.handleCreateUser)
mux.HandleFunc("DELETE /api/users/{id}", s.handleDeleteUser)
```

### Extracting Path Parameters

```go
func (s *Server) handleGetUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    if id == "" {
        http.Error(w, "missing id", http.StatusBadRequest)
        return
    }

    user, err := s.users.GetUser(r.Context(), id)
    if err != nil {
        s.logger.Error("getting user", "err", err, "id", id)
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}
```

### Wildcard and Exact Match

```go
// Exact match on trailing slash -- serves /api/files/ only
mux.HandleFunc("GET /api/files/", s.handleListFiles)

// Wildcard to end of path -- /api/files/path/to/doc.txt
mux.HandleFunc("GET /api/files/{path...}", s.handleGetFile)
```

### Routing Precedence

The new `ServeMux` uses most-specific-wins precedence:

- `GET /api/users/{id}` is more specific than `GET /api/users/`
- `GET /api/users/me` is more specific than `GET /api/users/{id}`
- Method routes take precedence over method-less routes

## Server Struct Pattern

The Server struct is the central dependency container for your application. It holds all shared dependencies and implements `http.Handler`.

```go
type Server struct {
    db     *sql.DB
    logger *slog.Logger
    router *http.ServeMux
}

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
    s.router.HandleFunc("GET /healthz", s.handleHealth)
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    s.router.ServeHTTP(w, r)
}
```

### Middleware Wrapping

Apply middleware at the `http.Server` level or per-route:

```go
// Wrap entire server
httpServer := &http.Server{
    Addr:    ":8080",
    Handler: requestLogger(s),
}

// Or per-route
s.router.Handle("GET /api/admin/", adminOnly(http.HandlerFunc(s.handleAdmin)))
```

### Middleware Signature

```go
func requestLogger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        slog.Info("request", "method", r.Method, "path", r.URL.Path, "dur", time.Since(start))
    })
}
```

## Project Structure

Choose based on project size:

- **Flat structure** -- single package, all files in root. Best for CLIs, small services, < ~10 handlers. See [references/project-structure.md](references/project-structure.md).
- **Modular/domain-driven** -- `cmd/`, `internal/` with domain packages. For larger apps with multiple bounded contexts. See [references/project-structure.md](references/project-structure.md).

Start flat. Migrate when you see the signs described in the reference.

## Graceful Shutdown

Every production Go server needs graceful shutdown. The pattern uses `signal.NotifyContext` to listen for OS signals and `http.Server.Shutdown` to drain connections.

```go
ctx, cancel := signal.NotifyContext(ctx, os.Interrupt, syscall.SIGTERM)
defer cancel()

// ... start server in goroutine ...

<-ctx.Done()

shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
defer shutdownCancel()
httpServer.Shutdown(shutdownCtx)
```

Full pattern with cleanup ordering in [references/graceful-shutdown.md](references/graceful-shutdown.md).

## When to Load References

Load **project-structure.md** when:
- Scaffolding a new Go project
- Discussing package layout or directory organization
- The project is growing and needs restructuring

Load **graceful-shutdown.md** when:
- Setting up a production HTTP server
- Implementing signal handling or clean shutdown
- Discussing deployment or container readiness

Load **dependency-injection.md** when:
- Designing how services, stores, and handlers connect
- Making code testable with interfaces
- Reviewing constructor functions or wiring logic

## Anti-Patterns

### Global database variables

```go
// BAD -- untestable, hidden dependency
var db *sql.DB

func handleGetUser(w http.ResponseWriter, r *http.Request) {
    db.QueryRow(...)
}
```

Pass `db` through a Server or Service struct instead.

### Framework-first thinking

Do not start with `gin.Default()` or `echo.New()`. Start with `http.NewServeMux()`. Only introduce a framework if you hit a real limitation of the stdlib that justifies the dependency.

### God packages

A single `handlers` package with 50 files is not organization. Group by domain (`user`, `order`, `billing`), not by technical layer.

### Using init() for setup

```go
// BAD -- invisible side effects, untestable
func init() {
    db, _ = sql.Open("postgres", os.Getenv("DATABASE_URL"))
}
```

All initialization belongs in `main()` or a `run()` function so it can be tested and errors can be handled.

### Reading config in business logic

```go
// BAD -- couples handler to environment
func (s *Server) handleSendEmail(w http.ResponseWriter, r *http.Request) {
    apiKey := os.Getenv("SENDGRID_API_KEY") // don't do this
}
```

Inject configuration values or clients through constructors.
