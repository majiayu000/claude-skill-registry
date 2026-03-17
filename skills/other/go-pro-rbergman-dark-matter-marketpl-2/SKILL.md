---
name: go-pro
description: Expert Go developer specializing in idiomatic patterns, concurrency, error handling, and clean package design. This skill should be used PROACTIVELY when working on any Go code - implementing features, designing APIs, debugging issues, or reviewing code quality. Use unless a more specific subagent role applies.
---

# Go Pro

Senior-level Go expertise for production projects. Focuses on idiomatic patterns, simplicity, and Go's design philosophy.

## When Invoked

1. Review `go.mod` and `.golangci.yml` for project conventions
2. For build system setup, invoke the **just-pro** skill
3. Apply Go idioms and established project patterns

## Core Standards

**Non-Negotiable:**
- All exported identifiers have doc comments
- All errors checked and handled (no `_ = err`)
- NO `panic()` for recoverable errors
- golangci-lint passes with project configuration
- Table-driven tests for multiple cases

**Foundational Principles:**
- **Single Responsibility**: One package = one purpose, one function = one job
- **No God Objects**: Split large structs; if it has 10+ fields or methods, decompose
- **Dependency Injection**: Pass dependencies, don't create them internally
- **Small Interfaces**: 1-3 methods max; compose larger behaviors from small interfaces

---

## Project Setup (Go 1.25+)

### Version Management with mise

[mise](https://mise.jdx.dev) manages language runtimes per-project. Ensures all contributors use the same Go version—no "works on my machine" issues.

```bash
# Install mise (once)
curl https://mise.run | sh

# In project root
mise use go@1.25

# Creates .mise.toml — commit it
# Team members just run: mise install
```

### New Project Quick Start

```bash
# Initialize
go mod init github.com/org/project
go mod edit -go=1.25

# Add toolchain dependencies (tracked in go.mod)
go get -tool github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest
go get -tool golang.org/x/tools/cmd/goimports@latest

# Copy configs from this skill's references/ directory:
#   references/gitignore          → .gitignore
#   references/golangci-v2.yml    → .golangci.yml
# For build system, invoke just-pro skill

# Verify
just check   # Or: go tool golangci-lint run
```

### Developer Onboarding

```bash
git clone <repo> && cd <repo>
just setup         # Runs mise trust/install + go mod download
just check         # Verify everything works
```

Or manually:
```bash
mise trust && mise install  # Get pinned Go version
go mod download             # Get dependencies
```

**Why `go get -tool`?** Tools versioned in go.mod = reproducible builds, same versions for all devs, no separate installation needed.

---

## Build System

**Invoke the `just-pro` skill** for build system setup. It covers:
- Simple repos vs monorepos
- Hierarchical justfile modules
- Go-specific templates (`references/package-go.just`)

**Why just?** Consistent toolchain frontend between agents and humans. Instead of remembering `go tool golangci-lint run --fix`, use `just fix`.

---

## Quality Assurance

**Auto-Fix First** - Always try auto-fix before manual fixes:

```bash
just fix             # Or: go tool golangci-lint run --fix && go tool goimports -w .
```

**Verification:**
```bash
just check           # Or: go tool golangci-lint run && go test -race ./...
```

---

## Quick Reference

### Error Handling

| Pattern | Use |
|---------|-----|
| `return err` | Propagate unchanged (internal errors) |
| `fmt.Errorf("context: %w", err)` | Wrap with context (cross-boundary) |
| `errors.Is(err, target)` | Check specific error |
| `errors.As(err, &target)` | Extract typed error |

**Sentinel Errors** - Define package-level errors for expected conditions:
```go
var ErrNotFound = errors.New("not found")
var ErrInvalidInput = errors.New("invalid input")
```

### Generics

```go
// Constrained generics - prefer specific constraints
func Map[T, U any](items []T, fn func(T) U) []U {
    result := make([]U, len(items))
    for i, item := range items {
        result[i] = fn(item)
    }
    return result
}

// Type constraints - use interfaces
type Ordered interface {
    ~int | ~int64 | ~float64 | ~string
}

func Max[T Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// Avoid: overly generic signatures that lose type safety
// Prefer: concrete types until generics are clearly needed
```

### Structured Logging (slog)

```go
import "log/slog"

// Package-level logger with context
func NewService(logger *slog.Logger) *Service {
    return &Service{
        log: logger.With("component", "service"),
    }
}

// Structured logging with levels
s.log.Info("request processed",
    "method", r.Method,
    "path", r.URL.Path,
    "duration", time.Since(start),
)

s.log.Error("operation failed",
    "err", err,
    "user_id", userID,
)
```

### Iterators (Go 1.23+)

```go
import "iter"

// Return iterators for large collections
func (db *DB) Users() iter.Seq[User] {
    return func(yield func(User) bool) {
        rows, _ := db.Query("SELECT * FROM users")
        defer rows.Close()
        for rows.Next() {
            var u User
            rows.Scan(&u.ID, &u.Name)
            if !yield(u) {
                return
            }
        }
    }
}

// Consume with range
for user := range db.Users() {
    process(user)
}

// Seq2 for key-value pairs
func (m *Map[K, V]) All() iter.Seq2[K, V]
```

### Concurrency

| Pattern | Use |
|---------|-----|
| `sync.WaitGroup` | Wait for goroutines |
| `sync.Mutex` / `RWMutex` | Protect shared state |
| `context.Context` | Cancellation/timeouts |
| `errgroup.Group` | Concurrent with error collection |

```go
// Context-aware work
func DoWork(ctx context.Context, arg string) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    // ... work
}
```

### Testing

```go
// Table-driven tests with subtests
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Result
        wantErr bool
    }{
        {name: "valid", input: "foo", want: Result{Value: "foo"}},
        {name: "empty", input: "", wantErr: true},
        {name: "special", input: "a@b", want: Result{Value: "a@b"}},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Parse() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("Parse() = %v, want %v", got, tt.want)
            }
        })
    }
}

// Testify for complex assertions
import "github.com/stretchr/testify/assert"
import "github.com/stretchr/testify/require"

func TestService(t *testing.T) {
    require.NoError(t, err)           // Fail fast
    assert.Equal(t, expected, actual) // Continue on failure
    assert.Len(t, items, 3)
    assert.Contains(t, items, target)
}
```

### Pointer vs Value Receivers

```go
// Use pointer receivers when:
// - Method modifies the receiver
// - Receiver is large (avoid copy)
// - Consistency: if any method needs pointer, use pointer for all
func (s *Service) UpdateConfig(cfg Config) { s.cfg = cfg }

// Use value receivers when:
// - Receiver is small (int, string, small struct)
// - Method is read-only and receiver is immutable
func (p Point) Distance(other Point) float64 { ... }
```

### Package Organization

```
project/
├── cmd/appname/main.go   # Entry point
├── internal/             # Private packages
│   ├── api/              # Handlers
│   └── domain/           # Business logic
├── go.mod
├── .golangci.yml
└── justfile
```

**Rules:** One package = one purpose. Use `internal/` for implementation. Avoid `util`, `common`, `helpers` packages.

---

## DX Patterns

### Doctor Recipe with Version Validation

Doctor scripts should validate that toolchain versions meet requirements, not just check existence:

```just
# Validate toolchain versions meet requirements
doctor:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Checking toolchain..."

    # Validate Go version (requires 1.25+)
    GO_VERSION=$(go version | grep -oE 'go[0-9]+\.[0-9]+' | sed 's/go//')
    if [[ "$(printf '%s\n' "1.25" "$GO_VERSION" | sort -V | head -1)" != "1.25" ]]; then
        echo "FAIL: Go $GO_VERSION < 1.25 required"
        exit 1
    fi
    echo "✓ Go $GO_VERSION"

    # Add more version checks as needed
    echo "All checks passed"
```

### Port Conflict Detection

For services that bind ports, check availability before starting:

```just
# Check if required ports are available before starting
check-ports:
    #!/usr/bin/env bash
    for port in 8080 5432; do
        if lsof -i :$port >/dev/null 2>&1; then
            echo "FAIL: Port $port already in use"
            exit 1
        fi
    done
    echo "All ports available"
```

### First-Run Detection

Avoid redundant setup work with first-run detection:

```just
# Setup with first-run detection
setup:
    #!/usr/bin/env bash
    if [[ -f .setup-complete ]]; then
        echo "Already set up. Run 'just setup-force' to reinstall."
        exit 0
    fi
    mise trust && mise install
    go mod download
    touch .setup-complete
    echo "Setup complete"

setup-force:
    rm -f .setup-complete
    @just setup
```

---

## Anti-Patterns

- `panic()` for recoverable errors (use `return err`)
- Ignoring errors with `_`
- Exported package-level mutable variables
- Channels when mutex suffices
- Getter/setter methods (Go isn't Java)
- `init()` with side effects
- God structs with 10+ fields/methods
- `interface{}` or `any` when specific types work
- Premature generics (concrete types first)

---

## AI Agent Guidelines

**Before writing code:**
1. Read `go.mod` for module path and Go version
2. Check `.golangci.yml` for project-specific lint rules
3. Identify existing patterns in the codebase to follow

**When writing code:**
1. Handle all errors explicitly - never use `_ = err`
2. Add doc comments to exported identifiers immediately
3. Use existing project abstractions over creating new ones
4. Prefer concrete types; add generics only when pattern repeats 3+ times

**Before committing:**
1. Run `just check` (standard for projects using just)
2. Fallback: `go tool golangci-lint run --fix && go tool golangci-lint run`
3. Fallback: `go test -race ./...` to catch race conditions
