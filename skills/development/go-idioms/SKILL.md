---
name: go-idioms
description: |
  Idiomatic Go patterns for errors, interfaces, concurrency, and packages. Use when:
  - Writing or reviewing Go code
  - Designing interfaces or package structure
  - Implementing concurrency patterns
  - Handling errors and context propagation
  - Structuring Go projects
  Keywords: Go, golang, error wrapping, interface design, goroutine, channel,
  context, package design, dependency injection, race condition
---

# Go Idioms

Boring, explicit, race-safe Go. Accept interfaces, return structs.

## Error Handling

**Always wrap with context at package boundaries:**
```go
// Use %w to preserve error chain
return fmt.Errorf("fetching user %s: %w", userID, err)

// Check wrapped errors
if errors.Is(err, sql.ErrNoRows) { ... }

var paymentErr *PaymentError
if errors.As(err, &paymentErr) { ... }
```

Never: `%v` (loses type), raw errors from exported functions, generic context.

## Interface Design

**Define interfaces in consuming package, not provider:**
```go
// notification/sender.go (consumer defines interface)
type EmailSender interface {
    Send(ctx context.Context, to, subject, body string) error
}

// email/client.go (provider implements)
type Client struct { ... }
func (c *Client) Send(ctx context.Context, to, subject, body string) error { ... }
```

**Small interfaces (1-3 methods). Compose larger from smaller:**
```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface { Reader; Writer }
```

**Compile-time verification:**
```go
var _ EmailSender = (*Client)(nil)
```

## Concurrency

**Always propagate context:**
```go
func FetchData(ctx context.Context) ([]byte, error) {
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    case result := <-dataChan:
        return result, nil
    }
}
```

**Bounded concurrency (semaphore):**
```go
sem := make(chan struct{}, 10)
for _, item := range items {
    sem <- struct{}{}
    go func(item Item) {
        defer func() { <-sem }()
        process(item)
    }(item)
}
```

**Race safety:** Always run `go test -race ./...`

## Package Design

```
internal/
  user/          # Domain: single purpose
    user.go
    service.go
    repository.go
  order/         # Another domain
  app/           # Dependency wiring
cmd/
  api/           # Entry points
```

**Rules:**
- Single purpose per package
- No generic names (utils, helpers, common)
- No circular dependencies
- Export only what's necessary

## Dependency Injection

```go
// Constructor accepts interfaces
func NewUserService(repo UserRepository, mailer EmailSender) *UserService {
    return &UserService{repo: repo, mailer: mailer}
}

// Wire in app/ package
func NewApp() *App {
    repo := postgres.NewUserRepo(db)
    mailer := sendgrid.NewClient(apiKey)
    userSvc := user.NewUserService(repo, mailer)
    return &App{UserService: userSvc}
}
```

## Anti-Patterns

- Goroutines without cancellation path (leaks)
- Monolithic interfaces (10+ methods)
- Framework-like inheritance patterns
- Reflection when explicit types work
- Global singletons for dependencies
- Generic everything (overuse of generics)
- `interface{}` / `any` without justification

## Embrace Boring

- Explicit error handling at each step
- Standard library first (`map`, `[]T`, `sort.Slice`)
- Table-driven tests
- Struct composition, not inheritance
- Clear, verbose code over clever code
