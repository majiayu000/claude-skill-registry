---
name: lang-go-library-dev
description: Go-specific library/package development patterns. Use when creating Go libraries, designing public APIs with Go idioms, configuring go.mod, managing module versioning, publishing packages, or writing package documentation. Extends meta-library-dev with Go tooling and ecosystem practices.
---

# Go Library Development

Go-specific patterns for library/package development. This skill extends `meta-library-dev` with Go tooling, module management, and ecosystem practices.

## This Skill Extends

- `meta-library-dev` - Foundational library patterns (API design, versioning, testing strategies)

For general concepts like semantic versioning, module organization principles, and testing pyramids, see the meta-skill first.

## This Skill Adds

- **Go tooling**: go.mod, module versioning, workspaces, package documentation
- **Go idioms**: Interface design, error handling, API patterns, zero values
- **Go ecosystem**: pkg.go.dev, module proxies, major version strategies

## This Skill Does NOT Cover

- General library patterns - see `meta-library-dev`
- Basic Go syntax - see `lang-go-dev`
- CLI development - see `lang-go-cli-dev`
- Web services - see `lang-go-http-dev`

---

## Quick Reference

| Task | Command/Pattern |
|------|-----------------|
| New module | `go mod init github.com/user/repo` |
| Add dependency | `go get package@version` |
| Update dependencies | `go get -u ./...` |
| Tidy dependencies | `go mod tidy` |
| Run tests | `go test ./...` |
| Run tests with coverage | `go test -cover ./...` |
| Generate docs | `go doc -all` |
| Format code | `go fmt ./...` |
| Vet code | `go vet ./...` |
| Build | `go build ./...` |

---

## Module Structure

### go.mod Configuration

```go
module github.com/username/mylibrary

go 1.21  // Minimum Go version

require (
    github.com/pkg/errors v0.9.1
    golang.org/x/sync v0.5.0
)

require (
    // Indirect dependencies
    golang.org/x/sys v0.15.0 // indirect
)
```

### Best Practices

**Use semantic import versioning for v2+:**
```go
// v0 or v1
module github.com/user/lib

// v2+
module github.com/user/lib/v2
```

**Specify minimum Go version:**
```go
// Enables use of features from that version
go 1.21
```

**Organize indirect dependencies:**
```bash
# Let Go manage indirect deps automatically
go mod tidy
```

---

## Package Organization

### Standard Library Structure

```
mylibrary/
├── go.mod
├── go.sum
├── README.md
├── LICENSE
├── doc.go              # Package-level documentation
├── library.go          # Main public API
├── types.go            # Public types
├── options.go          # Configuration/options
├── errors.go           # Error types
├── internal/           # Internal implementation
│   └── helper.go
├── testdata/           # Test fixtures
│   └── sample.json
└── example_test.go     # Example tests for godoc
```

### Package Naming

**Good package names:**
- Short, lowercase, single word: `http`, `json`, `xml`
- No underscores or mixedCaps: `ioutil` not `io_util`
- Descriptive: `encoding/json` not `encoding/j`

**Avoid:**
```go
// Bad: Generic names
package util
package common
package helpers

// Good: Specific names
package httputil
package stringutil
package mathutil
```

### Internal Packages

```
mylibrary/
├── library.go          # Public API
└── internal/           # Cannot be imported by external packages
    ├── parser.go
    └── validator.go
```

**Use internal/ to prevent external dependencies on implementation details.**

---

## Public API Design

### Interface Design

**Keep interfaces small:**
```go
// Good: Single method interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

// Good: Composed from small interfaces
type ReadWriter interface {
    Reader
    Writer
}

// Avoid: Large interfaces
type DataStore interface {
    Read() error
    Write() error
    Delete() error
    Update() error
    // ... 10 more methods
}
```

**Accept interfaces, return concrete types:**
```go
// Good: Accept interface (flexible)
func Process(r io.Reader) (*Result, error)

// Good: Return concrete type (clear contract)
func NewClient(url string) *Client

// Avoid: Returning interface unnecessarily
func NewClient(url string) ClientInterface
```

**Define interfaces at point of use:**
```go
// Good: Define interface where you use it
package consumer

type DataFetcher interface {
    FetchData(id string) ([]byte, error)
}

func ProcessData(fetcher DataFetcher) error {
    // Use fetcher
}

// Not: Define interface in provider package
```

### Functional Options Pattern

**Preferred pattern for optional configuration:**
```go
type Client struct {
    baseURL    string
    timeout    time.Duration
    maxRetries int
}

type Option func(*Client)

func WithTimeout(d time.Duration) Option {
    return func(c *Client) {
        c.timeout = d
    }
}

func WithMaxRetries(n int) Option {
    return func(c *Client) {
        c.maxRetries = n
    }
}

func NewClient(baseURL string, opts ...Option) *Client {
    c := &Client{
        baseURL:    baseURL,
        timeout:    30 * time.Second,  // defaults
        maxRetries: 3,
    }
    for _, opt := range opts {
        opt(c)
    }
    return c
}

// Usage
client := NewClient("https://api.example.com",
    WithTimeout(10*time.Second),
    WithMaxRetries(5),
)
```

### Constructor Patterns

**New prefix for constructors:**
```go
// Returns pointer (can fail, stateful)
func NewClient(url string) (*Client, error) {
    if url == "" {
        return nil, errors.New("url required")
    }
    return &Client{url: url}, nil
}

// Must prefix for constructors that panic
func MustCompile(pattern string) *Regexp {
    re, err := Compile(pattern)
    if err != nil {
        panic(err)
    }
    return re
}
```

### Error Design

**Create specific error types:**
```go
// Error type
type ValidationError struct {
    Field string
    Err   error
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %v", e.Field, e.Err)
}

func (e *ValidationError) Unwrap() error {
    return e.Err
}

// Sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Check with errors.Is
if errors.Is(err, ErrNotFound) {
    // Handle not found
}

// Check type with errors.As
var validErr *ValidationError
if errors.As(err, &validErr) {
    fmt.Println("Field:", validErr.Field)
}
```

**Error wrapping:**
```go
// Wrap errors with context
if err != nil {
    return fmt.Errorf("failed to connect to %s: %w", url, err)
}

// Allows callers to unwrap
originalErr := errors.Unwrap(err)
```

### Zero Values

**Design types to have useful zero values:**
```go
// Good: Zero value is useful
type Buffer struct {
    buf []byte
}

var b Buffer
b.Write([]byte("hello"))  // Works without initialization

// Good: Document when zero value is not useful
type Client struct {
    baseURL string  // Must be set
}

func NewClient(baseURL string) *Client {
    return &Client{baseURL: baseURL}
}
```

---

## Testing Patterns

### Table-Driven Tests

**Standard Go testing pattern:**
```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Result
        wantErr bool
    }{
        {
            name:  "valid input",
            input: "key=value",
            want:  Result{Key: "key", Value: "value"},
        },
        {
            name:    "empty input",
            input:   "",
            wantErr: true,
        },
        {
            name:  "multiple pairs",
            input: "a=1,b=2",
            want:  Result{Pairs: map[string]string{"a": "1", "b": "2"}},
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Parse() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !tt.wantErr && !reflect.DeepEqual(got, tt.want) {
                t.Errorf("Parse() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Subtests

**Organize tests hierarchically:**
```go
func TestClient(t *testing.T) {
    t.Run("GET", func(t *testing.T) {
        t.Run("success", func(t *testing.T) {
            // Test successful GET
        })
        t.Run("not found", func(t *testing.T) {
            // Test 404
        })
    })

    t.Run("POST", func(t *testing.T) {
        t.Run("success", func(t *testing.T) {
            // Test successful POST
        })
    })
}
```

### Test Helpers

**Use t.Helper() to improve error messages:**
```go
func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func assertEqual(t *testing.T, got, want interface{}) {
    t.Helper()
    if !reflect.DeepEqual(got, want) {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

### Example Tests

**Generate documentation with runnable examples:**
```go
// Example tests appear in godoc
func ExampleParse() {
    result, _ := Parse("key=value")
    fmt.Println(result.Key)
    // Output: key
}

func ExampleParse_multiple() {
    result, _ := Parse("a=1,b=2")
    fmt.Println(len(result.Pairs))
    // Output: 2
}

func ExampleClient_Get() {
    client := NewClient("https://api.example.com")
    data, _ := client.Get("/endpoint")
    fmt.Printf("Got %d bytes\n", len(data))
    // Output: Got 42 bytes
}
```

### Test Coverage

```bash
# Run tests with coverage
go test -cover ./...

# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# View coverage by function
go tool cover -func=coverage.out
```

---

## Documentation with godoc

### Package Documentation

**doc.go pattern:**
```go
// Package mylibrary provides utilities for parsing configuration files.
//
// This package supports JSON, YAML, and TOML formats with automatic
// format detection based on file extension.
//
// Basic usage:
//
//	config, err := mylibrary.Load("config.yaml")
//	if err != nil {
//		log.Fatal(err)
//	}
//
// The package provides three main types:
//
//   - Config: The main configuration structure
//   - Parser: Interface for custom parsers
//   - Validator: Interface for custom validation
//
// For more examples, see the examples/ directory.
package mylibrary
```

### Type and Function Documentation

**Standard documentation format:**
```go
// Client represents an HTTP client for the API.
// It is safe for concurrent use by multiple goroutines.
type Client struct {
    baseURL string
    client  *http.Client
}

// NewClient creates a new API client with the given base URL.
// It returns an error if the URL is invalid.
//
// Example:
//
//	client, err := NewClient("https://api.example.com")
//	if err != nil {
//		log.Fatal(err)
//	}
func NewClient(baseURL string) (*Client, error) {
    // Implementation
}

// Get performs a GET request to the specified path.
// The path should not include the base URL.
//
// Get returns the response body as bytes. If the request fails
// or returns a non-2xx status code, an error is returned.
func (c *Client) Get(path string) ([]byte, error) {
    // Implementation
}
```

### Documentation Best Practices

| Practice | Example |
|----------|---------|
| Start with type/function name | `// Client represents...` not `// This is...` |
| Use complete sentences | `// NewClient creates a new client.` |
| Document parameters | `// path should be relative to base URL` |
| Document return values | `// Returns nil if not found` |
| Include examples | Code blocks in comments |
| Mark deprecated items | `// Deprecated: Use NewClient instead.` |

---

## Versioning and Releases

### Semantic Versioning

**Go modules use semantic versioning:**

- `v0.x.x` - Initial development, no stability guarantees
- `v1.x.x` - Stable API, backward compatible changes only
- `v2.x.x+` - Breaking changes require new major version

### Major Version Strategy

**v2+ requires module path change:**

```go
// v1
module github.com/user/lib

// v2 - add /v2 suffix
module github.com/user/lib/v2
```

**In code:**
```go
// Import v2
import "github.com/user/lib/v2"

// Both v1 and v2 can coexist
import (
    libv1 "github.com/user/lib"
    libv2 "github.com/user/lib/v2"
)
```

### Tagging Releases

```bash
# Tag v1 release
git tag v1.0.0
git push origin v1.0.0

# Tag v2 release (after creating /v2 module path)
git tag v2.0.0
git push origin v2.0.0

# Pre-release
git tag v1.1.0-beta.1
git push origin v1.1.0-beta.1
```

### Retract Versions

**Retract broken versions in go.mod:**
```go
module github.com/user/lib

go 1.21

retract (
    v1.0.0 // Published accidentally
    v1.0.1 // Critical bug, use v1.0.2+
    [v1.5.0, v1.7.0] // Range retraction
)
```

---

## Publishing and Distribution

### Making Your Module Discoverable

**Requirements for pkg.go.dev:**

1. **Public repository** on GitHub, GitLab, or Bitbucket
2. **Valid go.mod** with module path matching repo
3. **Version tags** using semantic versioning
4. **LICENSE file** (required)
5. **Documentation** in godoc format

**Trigger indexing:**
```bash
# pkg.go.dev automatically indexes on first request
curl https://pkg.go.dev/github.com/user/lib@v1.0.0
```

### LICENSE

**Common licenses for Go libraries:**
- MIT - Permissive, simple
- Apache 2.0 - Permissive, patent grant
- BSD 3-Clause - Permissive, attribution required

**Include LICENSE file in repository root.**

### README Best Practices

**Include in README.md:**

```markdown
# My Library

Brief description of what the library does.

## Installation

```bash
go get github.com/user/lib
```

## Quick Start

```go
package main

import "github.com/user/lib"

func main() {
    // Example usage
}
```

## Documentation

Full documentation available at [pkg.go.dev](https://pkg.go.dev/github.com/user/lib).

## License

MIT License - see [LICENSE](LICENSE) file.
```

### Go Module Proxy

**By default, Go uses proxy.golang.org:**

```bash
# Verify module is available
go list -m -versions github.com/user/lib

# Force direct access (bypass proxy)
GOPRIVATE=github.com/user/* go get github.com/user/lib
```

---

## API Compatibility

### Backward Compatibility Rules

**Within major version v1:**

**OK (minor/patch):**
- Add new functions, types, methods
- Add new fields to structs (if not used in comparisons)
- Add new error types
- Make unexported symbols exported

**NOT OK (requires v2):**
- Remove or rename exported symbols
- Change function signatures
- Change error types returned
- Remove struct fields
- Change exported variable types

### Deprecation Pattern

```go
// Deprecated: Use NewClient instead.
// OldClient will be removed in v2.
func OldClient(url string) *Client {
    return NewClient(url)
}

// NewClient creates a new API client.
func NewClient(url string) *Client {
    // Implementation
}
```

---

## Common Patterns

### Config Struct with Defaults

```go
type Config struct {
    Timeout    time.Duration
    MaxRetries int
    Debug      bool
}

// DefaultConfig returns a Config with sensible defaults.
func DefaultConfig() *Config {
    return &Config{
        Timeout:    30 * time.Second,
        MaxRetries: 3,
        Debug:      false,
    }
}

// Usage
config := DefaultConfig()
config.Debug = true
```

### Graceful Initialization

```go
type Manager struct {
    once sync.Once
    db   *sql.DB
}

func (m *Manager) init() {
    m.once.Do(func() {
        m.db, _ = sql.Open("postgres", "connection_string")
    })
}

func (m *Manager) Query(q string) (*Result, error) {
    m.init()  // Lazy initialization
    return m.db.Query(q)
}
```

### Context for Cancellation

```go
// Accept context as first parameter
func (c *Client) Fetch(ctx context.Context, url string) (*Response, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    resp, err := c.client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    // Process response
    return parseResponse(resp)
}

// Usage with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

response, err := client.Fetch(ctx, "https://api.example.com")
```

---

## Anti-Patterns

### 1. init() Functions

```go
// Avoid: Non-deterministic initialization
func init() {
    db = connectDatabase()  // What if this fails?
}

// Prefer: Explicit initialization
func New() (*Client, error) {
    db, err := connectDatabase()
    if err != nil {
        return nil, err
    }
    return &Client{db: db}, nil
}
```

### 2. Global State

```go
// Avoid: Global variables
var defaultClient *Client

func Get(url string) (*Response, error) {
    return defaultClient.Get(url)
}

// Prefer: Explicit dependencies
type Client struct { }

func (c *Client) Get(url string) (*Response, error) {
    // Implementation
}
```

### 3. Interface Pollution

```go
// Avoid: Interfaces for every type
type UserRepository interface {
    Save(u User) error
}

type userRepository struct {}

// Prefer: Concrete types unless abstraction needed
type UserRepository struct {}

func (r *UserRepository) Save(u User) error {
    // Implementation
}
```

### 4. Returning Pointers to Slices/Maps

```go
// Avoid: Unnecessary pointer
func GetUsers() *[]User {
    users := []User{ /* ... */ }
    return &users
}

// Prefer: Return slice directly (already a reference type)
func GetUsers() []User {
    return []User{ /* ... */ }
}
```

---

## Troubleshooting

### Module Path Issues

**Problem:** `go get` fails with "module not found"

**Solutions:**
1. Ensure module path matches repository URL
2. Check that repository is public
3. Verify version tag exists: `git tag v1.0.0`
4. Wait for pkg.go.dev to index (can take a few minutes)

### Import Cycle

**Problem:** "import cycle not allowed"

**Solutions:**
1. Extract shared code to a separate package
2. Use interfaces to break dependency
3. Restructure package organization

```go
// Before: Cycle between user and auth packages
package user
import "myapp/auth"

package auth
import "myapp/user"

// After: Extract common types to separate package
package types
type User struct { }

package user
import "myapp/types"

package auth
import "myapp/types"
```

### Breaking API Changes

**Problem:** Need to make breaking change in v1

**Solutions:**
1. Add new function, deprecate old
2. Create v2 module with /v2 suffix
3. Use options pattern for extensibility

```go
// Instead of changing signature
func Process(data string) error

// Add new function
func ProcessWithOptions(data string, opts Options) error
```

---

## References

- `meta-library-dev` - Foundational library patterns
- `lang-go-dev` - Basic Go syntax and patterns
- [Go Modules Reference](https://go.dev/ref/mod)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go API Guidelines](https://go.dev/wiki/CodeReviewComments)
- [pkg.go.dev](https://pkg.go.dev) - Package documentation
