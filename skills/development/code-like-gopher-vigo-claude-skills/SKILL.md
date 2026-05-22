---
name: code-like-gopher
description: Provides Go programming expertise, including language syntax, idiomatic patterns, concurrency, and standard library usage. Use when generating, analyzing, refactoring, or reviewing Go code.
---

## When to Use

Use this skill when:

- Writing, reviewing, or refactoring Go code
- Setting up Go project structure and tooling
- Debugging concurrency issues
- Configuring linters and formatters
- Writing idiomatic Go code

## Prerequisites Check

Before starting any Go work:

```bash
# Check Go version
go version

# Check go.mod version requirement
grep '^go ' go.mod 2>/dev/null | awk '{print $2}'

# Check if golangci-lint is available
command -v golangci-lint
```

---

## Instructions

### General Coding Approach

- All naming and comments must be in **English**
- Always check the Go version in `go.mod` and use appropriate language features
- Starting with **Go 1.22+**, the loop variable capture issue is fixed
- Starting with **Go 1.23+**, range-over-integers is available:

```go
// Go 1.23+ only
for i := range 10 {
    fmt.Println(i)
}

// Go 1.22+ - loop variable capture is safe
for i := range items {
    go func() {
        fmt.Println(i) // safe, no need for tt := tt
    }()
}
```

---

### Formatting and Linting

**golangci-lint** is the standard tool for Go code quality. 

```bash
# Install if missing
brew install golangci-lint      # macOS
# or
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

Check for existing config files:

- `.golangci.yml` / `.golangci.yaml`
- `.golangci.toml` / `.golangci.json`

If config version is not `"2"`, migrate:

```bash
golangci-lint migrate
```

#### Minimal `.golangci.yml` Config

```yaml
version: "2"

run:
  timeout: 5m
  tests: false

linters:
  enable:
    - errcheck
    - govet
    - ineffassign
    - staticcheck
    - unused
    - misspell
    - unconvert
    - unparam
    - gosec
    - prealloc
    - revive
    - wrapcheck
  settings:
    govet:
      enable:
        - assign
        - appends
        - bools
        - defers
        - shadow
        - unmarshal
        - waitgroup
        - lostcancel
        - slog
        - unreachable
    errcheck:
      check-type-assertions: true
      exclude-functions:
        - fmt.Fprintln
        - fmt.Fprintf
    wrapcheck:
      ignore-package-globs:
        - encoding/*
        - github.com/pkg/*
    revive:
      enable-all-rules: true
      rules:
        - name: package-comments
          disabled: true
        - name: cognitive-complexity
          disabled: true
        - name: cyclomatic
          disabled: true
        - name: function-length
          disabled: true
        - name: line-length-limit
          arguments: [120]
        - name: add-constant
          arguments:
            - max-lit-count: "3"
              allow-strs: '""'
              allow-ints: "0,1,2,10,64"

formatters:
  enable:
    - gofmt
    - gofumpt
    - goimports
    - golines
  settings:
    golines:
      max-len: 120
```

#### Usage

```bash
golangci-lint run ./...
golangci-lint fmt ./...
```

All the details of the configuration file can be found here:

https://github.com/golangci/golangci-lint/blob/HEAD/.golangci.reference.yml

- `gofmt` is your friend, use for formatting the `*.go` files
- `goimports` helps you to sort and find required package imports

---

### Naming Conventions

#### Variables

Name variables by **what they hold**, not their type:

```go
// ❌ Bad
var userString string
var countInt int
var usersMap map[string]*User
var usersList []User

// ✅ Good
var username string
var count int
var users map[string]*User
var users []User
```

**Short variable conventions:**

- `i`, `j`, `k` - loop indices
- `n` - counter, total, quantity
- `k`, `v` - map key/value
- `a`, `b` - same-type comparisons
- `s` - string values
- `err` - errors
- `ctx` - context

**Collections** always use plural names:

```go
// ❌ Bad
var userString string
var countInt int
var usersMap     map[string]*User
var companiesMap map[string]*Company
var productsMap  map[string]*Product
var usersList    []User

// ✅ Good
var username string
var count int

var users     map[string]*User
var users     []User

var companies map[string]*Company
var companies []Company
var products  []Product
```


#### Functions vs Methods

**Functions** - name by the result they return:

```go
// ❌ Bad - describes operation
func Add(a, b int) int {}

// ✅ Good - describes result
func Sum(a, b int) int {}
```

**Methods** - name by the action they perform:

```go
type User struct {
    email string
}

// Getter - no "Get" prefix
func (u User) Email() string {
    return u.email
}

// Setter - "Set" prefix
func (u *User) SetEmail(email string) {
    u.email = email
}
```

#### Packages

- Lowercase, single-word names
- No underscores or mixedCaps
- Package name = base directory name
- Avoid `util`, `common`, `misc`, `helpers`, `tools`, `models`, `api`, `types`
  or `interfaces`.

```go
// ❌ Bad
package string_utils
func NewStringSet(...string) map[string]bool {}

// ✅ Good
package stringset
func New(...string) Set {}
```

**Constructor naming:**

```go
// When package exports one main type, use New()
q := list.New()      // returns *list.List
r := ring.New(10)    // returns *ring.Ring
```

Rules:

- Don’t use the `import .` notation, which can simplify tests that must run 
  outside the package they are testing, but should otherwise be avoided.
- Package names may be abbreviated when the abbreviation is familiar to the 
  programmer. stdlib includes:
  
  ```
  strconv (string conversion)
  syscall (system call)
  fmt (formatted I/O)
  ```

- **Avoid repetition**. The HTTP server provided by the `http` package is 
  called `Server`, not **HTTPServer**. Client code refers to this type 
  as `http.Server`, so there is no ambiguity.
- Simplify function names. When a function in package `pkg` returns a value 
  of `type pkg.Pkg` (or `*pkg.Pkg`), the function name can often omit the 
  type name without confusion:
  
  ```go
  start := time.Now()                                  // start is a time.Time
  t, err := time.Parse(time.Kitchen, "6:06PM")         // t is a time.Time
  ctx = context.WithTimeout(ctx, 10*time.Millisecond)  // ctx is a context.Context
  ip, ok := userip.FromContext(ctx)                    // ip is a net.IP
  ```

#### Structs

- Go doesn’t provide automatic support for **getters** and **setters**. You can
  provide getters and setters by your self, it's neither idiomatic nor 
  necessary to put **Get** into the getter's name. If you have a field called 
  `owner` (lower case, unexported), the getter method should be called `Owner` 
  (upper case, exported), **not GetOwner**. The use of upper-case names for 
  export provides the hook to discriminate the field from the method. 
  A setter function, if needed, will likely be called `SetOwner`. 
  Both names read well in practice:
  
  ```go
  owner := obj.Owner()
  if owner != user {
      obj.SetOwner(user)
  }
  ```

#### Interfaces

One-method interfaces use **-er** suffix:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Stringer interface {
    String() string
}

// Combined interfaces
type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}
```

---

### Error Handling

**Always wrap errors with context:**

```go
// ❌ Bad - loses context
if err != nil {
    return err
}

// ✅ Good - stdlib way (Go 1.13+)
if err != nil {
    return fmt.Errorf("authenticate user %s: %w", userID, err)
}
```

**Use `errors.Is` and `errors.As` for error checking:**

```go
// Check error type
if errors.Is(err, os.ErrNotExist) {
    // handle not found
}

// Extract error type
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println(pathErr.Path)
}
```

**Custom error types:**

```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Sentinel errors with context
func GetUser(id string) (*User, error) {
    if user == nil {
        return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
    }
    return user, nil
}
```

---

### Functional Options Pattern

Use instead of config structs:

```go
type Server struct {
    port   string
    logger *slog.Logger
}

type Option func(*Server) error

func WithPort(port string) Option {
    return func(s *Server) error {
        if port == "" {
            return errors.New("port cannot be empty")
        }
        s.port = port
        return nil
    }
}

func WithLogger(l *slog.Logger) Option {
    return func(s *Server) error {
        if l == nil {
            return errors.New("logger cannot be nil")
        }
        s.logger = l
        return nil
    }
}

func New(opts ...Option) (*Server, error) {
    s := &Server{
        port: "8080", // default
    }
    
    for _, opt := range opts {
        if err := opt(s); err != nil {
            return nil, fmt.Errorf("apply option: %w", err)
        }
    }
    
    return s, nil
}

// Usage
server, err := New(
    WithPort("3000"),
    WithLogger(slog.Default()),
)
```

---

### Concurrency

#### Golden Rule

> **Only the sender closes the channel, never the receiver.**

The sender knows when work is finished; the receiver does not.

```go
func produce(ch chan<- int) {
    defer close(ch) // sender closes
    for i := range 10 {
        ch <- i
    }
}

func consume(ch <-chan int) {
    for v := range ch { // receiver just reads
        fmt.Println(v)
    }
}
```

#### Buffered Channels

Prefer buffered channel with capacity 1 for signals:

```go
// Signal/done channel
done := make(chan struct{}, 1)

// Error propagation
errCh := make(chan error, 1)
```

#### Concurrent-Safe Maps

Use `sync.Map` for concurrent access:

```go
var cache sync.Map

// Store
cache.Store("key", value)

// Load
if v, ok := cache.Load("key"); ok {
    // use v
}

// LoadOrStore
actual, loaded := cache.LoadOrStore("key", newValue)
```

---

### Best Practices

1. **Zero values** - Make them useful (like `bytes.Buffer`, `sync.Mutex`)
2. **Context** - Always first parameter, never in struct fields
3. **Avoid naked returns** - Use explicit returns
4. **Use `any`** instead of `interface{}`
5. **Generics** - Last resort, prefer interfaces
6. **Struct field alignment** - Order by size (8, 4, 2, 1 bytes)
7. **Pointer vs value receivers** - Be consistent per type

```go
// ❌ Bad - context in struct
type Service struct {
    ctx context.Context
}

// ✅ Good - context as first param
func (s *Service) Do(ctx context.Context, id string) error {}
```

**Compile-time interface checks:**

```go
var _ io.Reader = (*MyReader)(nil)
var _ http.Handler = (*MyHandler)(nil)
```

---

### Testing

#### Naming

```go
// ❌ Bad - describes input
func TestTitleIllegalChar(t *testing.T) {}

// ✅ Good - describes behavior
func TestTitleEscapesSpecialCharacters(t *testing.T) {}
```

#### Table-Driven Tests

```go
func TestSum(t *testing.T) {
    t.Parallel()
    
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -1, -2},
        {"zero", 0, 0, 0},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Go 1.22+ safe
            
            got := Sum(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Sum(%d, %d) = %d; want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

---

### Pre-Commit Hooks

```bash
brew install pre-commit
pre-commit install
```

Minimal `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/TekWizely/pre-commit-golang
    rev: v1.0.0-rc.1
    hooks:
      - id: golangci-lint-mod
      - id: go-mod-tidy
      - id: go-test-mod
```

---

### Commit Messages

Format:

```
[claude]: <verb> <description in lowercase>

- Detail 1
- Detail 2

Fixes #123

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

Example:

```
[claude]: add user authentication middleware

- Implement JWT validation
- Add rate limiting per user
- Handle token refresh

Fixes #42

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Check Go version | `go version` |
| Run linter | `golangci-lint run ./...` |
| Format code | `golangci-lint fmt ./...` |
| Run tests | `go test -race ./...` |
| Tidy modules | `go mod tidy` |
| Build | `go build ./...` |

---

## Resources

- [Go Language Spec](https://go.dev/ref/spec)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [golangci-lint Reference](https://github.com/golangci/golangci-lint/blob/HEAD/.golangci.reference.yml)
