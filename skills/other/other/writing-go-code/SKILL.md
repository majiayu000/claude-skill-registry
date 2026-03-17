---
name: writing-go-code
description: Apply Go coding standards when writing or modifying Go code. Use when implementing functions, using dependency injection, handling errors idiomatically, or working with interfaces. For test conventions, use the `writing-go-tests` skill instead.
---

# Go Development Standards

Project-specific Go coding standards for this codebase.

## Companion Skills

- **`applying-effective-go`** — General Go idioms from the official Effective Go documentation (naming, control flow, error handling philosophy, concurrency patterns). Complementary to this skill.
- **`writing-go-tests`** — Test conventions, mock usage, assertions, naming. Always load when writing test files.

## Code Organization

```go
// 1. Struct definition
type MyService struct {
    logger Logger
    fs     FileSystem
}

// 2. Interface verification (immediately after struct)
var _ Service = (*MyService)(nil)

// 3. Constructor with dependency injection
func NewMyService(logger Logger, fs FileSystem) *MyService {
    return &MyService{logger: logger, fs: fs}
}
```

## Dependency Injection

Always inject dependencies via constructors. Never create dependencies internally.

```go
// Good: dependencies injected
func NewHandler(
    logger Logger,
    service Service,
    validator Validator,
) *Handler {
    return &Handler{
        logger:    logger,
        service:   service,
        validator: validator,
    }
}

// Bad: dependencies created internally
func NewHandler() *Handler {
    return &Handler{
        logger:    NewDefaultLogger(),  // Don't do this
        service:   NewService(),        // Don't do this
    }
}
```

## Mock Generation

Mocks use `mockery` with moq template. To regenerate all mocks:

```bash
mockery
```

Mock types are prefixed with `Moq` (e.g., `MoqLogger`, `MoqFileSystem`). For mock usage conventions in tests, see the `writing-go-tests` skill.

## Optional Types

Use `samber/mo` for safer nil handling:

```go
import "github.com/samber/mo"

type Config struct {
    Shell mo.Option[string]
}

if shell, ok := config.Shell.Get(); ok {
    // use shell
}
```

## Code Formatting

- Line length: 120 characters max.
- Vertically align function arguments when there are multiple arguments.
- Insert blank lines between logical sections of code.
- Do not separate error unwrapping from related code with a blank line; treat it as part of the same section.

```go
// Good: error handling is part of the same section
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}

// Next logical section starts after blank line
processResult(result)
```

## Documentation

End all type and function comments with a period, following Go conventions.

```go
// MyService handles business logic for the application.
type MyService struct {
    // ...
}

// Process executes the main workflow and returns the result.
func (s *MyService) Process(ctx context.Context) error {
    // ...
}
```

## Key Rules

- Use the Go standard library whenever possible. Only use third-party libraries when necessary.
- Pre-allocate slices/maps when size is known.
- Wrap OS operations in interfaces for mockability.
- Never edit mock files manually.
