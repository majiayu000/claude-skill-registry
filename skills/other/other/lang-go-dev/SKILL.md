---
name: lang-go-dev
description: Foundational Go patterns covering types, interfaces, goroutines, channels, and common idioms. Use when writing Go code, understanding Go's concurrency model, or needing guidance on which specialized Go skill to use. This is the entry point for Go development.
---

# Go Fundamentals

Foundational Go patterns and core language features. This skill serves as both a reference for common patterns and an index to specialized Go skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       Go Skill Hierarchy                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────────┐                          │
│                    │   lang-go-dev   │ ◄── You are here         │
│                    │  (foundation)   │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ concurrency │    │   testing   │    │   modules   │         │
│  │  patterns   │    │  patterns   │    │  packages   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Basic types and zero values
- Structs, interfaces, and embedding
- Slices, maps, and iteration
- Error handling patterns
- Goroutines and channels basics
- Common idioms and conventions

**This skill does NOT cover (see specialized skills):**
- Advanced concurrency patterns → `go-concurrency-patterns`
- Module management and versioning → future skill
- Testing strategies → future skill
- Performance optimization → future skill

---

## Quick Reference

| Task | Syntax |
|------|--------|
| Variable declaration | `var x int` or `x := 0` |
| Constant | `const Pi = 3.14` |
| Function | `func name(x int) int { return x }` |
| Multiple return | `func f() (int, error)` |
| Struct | `type User struct { Name string }` |
| Interface | `type Reader interface { Read() }` |
| Slice | `[]int{1, 2, 3}` |
| Map | `map[string]int{"a": 1}` |
| Goroutine | `go func() { ... }()` |
| Channel | `ch := make(chan int)` |
| Defer | `defer file.Close()` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Complex concurrency (worker pools, fan-out) | `go-concurrency-patterns` |
| Module versioning, go.mod management | future: `lang-go-modules-dev` |
| Testing strategies, mocking | future: `lang-go-testing-dev` |
| HTTP servers, middleware | future: `lang-go-http-dev` |

---

## Types and Variables

### Basic Types

```go
// Boolean
var active bool = true

// Numeric types
var i int = 42           // Platform-dependent size
var i64 int64 = 42       // Explicit 64-bit
var f float64 = 3.14     // Default float type
var c complex128 = 1+2i  // Complex numbers

// String (immutable UTF-8)
var s string = "hello"

// Byte and rune
var b byte = 'A'         // Alias for uint8
var r rune = '世'        // Alias for int32 (Unicode code point)
```

### Zero Values

Every type has a zero value - no uninitialized variables in Go:

| Type | Zero Value |
|------|------------|
| `bool` | `false` |
| `int`, `float64` | `0` |
| `string` | `""` (empty string) |
| `pointer`, `slice`, `map`, `chan`, `func` | `nil` |
| `struct` | All fields zero-valued |

### Variable Declaration

```go
// Explicit type
var name string = "Alice"

// Type inference
var name = "Alice"

// Short declaration (inside functions only)
name := "Alice"

// Multiple variables
var x, y int = 1, 2
a, b := 1, "hello"

// Block declaration
var (
    name   string = "Alice"
    age    int    = 30
    active bool   = true
)
```

### Constants

```go
// Typed constant
const Pi float64 = 3.14159

// Untyped constant (more flexible)
const MaxSize = 1024

// Constant block with iota
const (
    Sunday = iota  // 0
    Monday         // 1
    Tuesday        // 2
)

// Iota patterns
const (
    _  = iota             // Skip 0
    KB = 1 << (10 * iota) // 1024
    MB                    // 1048576
    GB                    // 1073741824
)
```

---

## Functions

### Basic Functions

```go
// Simple function
func greet(name string) string {
    return "Hello, " + name
}

// Multiple parameters of same type
func add(x, y int) int {
    return x + y
}

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Named return values
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return // Naked return
}
```

### Variadic Functions

```go
// Accept any number of arguments
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

// Usage
sum(1, 2, 3)
sum([]int{1, 2, 3}...) // Spread slice
```

### Function Values and Closures

```go
// Functions are first-class values
var fn func(int) int
fn = func(x int) int { return x * 2 }

// Closure (captures outer variable)
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

c := counter()
c() // 1
c() // 2
```

### Defer

```go
// Deferred calls execute in LIFO order when function returns
func process(filename string) error {
    f, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer f.Close() // Guaranteed to run

    // Process file...
    return nil
}

// Arguments evaluated immediately, call deferred
func demo() {
    for i := 0; i < 3; i++ {
        defer fmt.Println(i) // Prints 2, 1, 0
    }
}
```

---

## Structs

### Definition and Instantiation

```go
// Define struct type
type User struct {
    ID        int
    Name      string
    Email     string
    CreatedAt time.Time
}

// Create instances
u1 := User{ID: 1, Name: "Alice", Email: "alice@example.com"}
u2 := User{1, "Alice", "alice@example.com", time.Now()} // Positional (fragile)
u3 := User{Name: "Bob"} // Other fields get zero values

// Pointer to struct
u4 := &User{Name: "Charlie"}

// Anonymous struct (one-off use)
point := struct {
    X, Y int
}{10, 20}
```

### Methods

```go
// Value receiver (copy)
func (u User) FullName() string {
    return u.Name
}

// Pointer receiver (can modify, avoids copy)
func (u *User) UpdateEmail(email string) {
    u.Email = email
}

// Usage
user := User{Name: "Alice"}
user.UpdateEmail("new@example.com") // Automatic &user
```

### When to Use Pointer vs Value Receiver

| Use Pointer Receiver | Use Value Receiver |
|---------------------|-------------------|
| Method modifies the receiver | Method only reads |
| Struct is large | Struct is small |
| Consistency with other methods | Immutability desired |

### Embedding (Composition)

```go
type Person struct {
    Name string
    Age  int
}

func (p Person) Greet() string {
    return "Hello, " + p.Name
}

type Employee struct {
    Person              // Embedded (not named)
    EmployeeID string
    Department string
}

// Employee "inherits" Person's fields and methods
emp := Employee{
    Person:     Person{Name: "Alice", Age: 30},
    EmployeeID: "E001",
    Department: "Engineering",
}

emp.Name        // Promoted field
emp.Greet()     // Promoted method
emp.Person.Name // Explicit access
```

---

## Interfaces

### Definition and Implementation

```go
// Define interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose interfaces
type ReadWriter interface {
    Reader
    Writer
}

// Implement implicitly (no "implements" keyword)
type FileReader struct {
    data []byte
    pos  int
}

func (f *FileReader) Read(p []byte) (int, error) {
    n := copy(p, f.data[f.pos:])
    f.pos += n
    return n, nil
}

// FileReader now implements Reader
```

### Empty Interface

```go
// interface{} accepts any type (like any in TS)
func printAnything(v interface{}) {
    fmt.Println(v)
}

// Go 1.18+: 'any' is alias for interface{}
func printAnything(v any) {
    fmt.Println(v)
}
```

### Type Assertions

```go
// Assert specific type
var i interface{} = "hello"

s := i.(string)        // Panics if wrong type
s, ok := i.(string)    // Safe: ok is false if wrong type

if s, ok := i.(string); ok {
    fmt.Println(s)
}
```

### Type Switch

```go
func describe(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("Integer: %d\n", v)
    case string:
        fmt.Printf("String: %s\n", v)
    case bool:
        fmt.Printf("Boolean: %t\n", v)
    default:
        fmt.Printf("Unknown type: %T\n", v)
    }
}
```

### Common Interfaces

| Interface | Methods | Use |
|-----------|---------|-----|
| `io.Reader` | `Read([]byte) (int, error)` | Read data |
| `io.Writer` | `Write([]byte) (int, error)` | Write data |
| `io.Closer` | `Close() error` | Clean up resources |
| `fmt.Stringer` | `String() string` | Custom string representation |
| `error` | `Error() string` | Error type |

---

## Collections

### Arrays

```go
// Fixed size, rarely used directly
var arr [5]int              // Zero-valued
arr := [5]int{1, 2, 3, 4, 5}
arr := [...]int{1, 2, 3}    // Size inferred (3)

// Arrays are values, not references
arr2 := arr // Full copy
```

### Slices

```go
// Dynamic, reference type (view into array)
var s []int                 // nil slice
s := []int{1, 2, 3}         // Literal
s := make([]int, 5)         // Length 5, capacity 5
s := make([]int, 0, 10)     // Length 0, capacity 10

// Slice operations
len(s)                      // Length
cap(s)                      // Capacity
s[1:3]                      // Sub-slice [1, 3)
s[:3]                       // [0, 3)
s[1:]                       // [1, len)

// Append (may reallocate)
s = append(s, 4)            // Single element
s = append(s, 4, 5, 6)      // Multiple elements
s = append(s, other...)     // Another slice

// Copy
dst := make([]int, len(src))
copy(dst, src)
```

### Slice Gotchas

```go
// Slices share underlying array
original := []int{1, 2, 3, 4, 5}
slice := original[1:3] // [2, 3]
slice[0] = 99          // Modifies original!

// Safe copy
safeCopy := make([]int, len(original[1:3]))
copy(safeCopy, original[1:3])
```

### Maps

```go
// Create maps
var m map[string]int        // nil map (read ok, write panics)
m := map[string]int{}       // Empty map
m := make(map[string]int)   // Empty map
m := map[string]int{        // With values
    "alice": 30,
    "bob":   25,
}

// Operations
m["key"] = 42               // Set
val := m["key"]             // Get (zero value if missing)
val, ok := m["key"]         // Check existence
delete(m, "key")            // Delete
len(m)                      // Size

// Iterate (order is random!)
for key, value := range m {
    fmt.Println(key, value)
}
```

### Iteration

```go
// Range over slice
for i, v := range slice {
    fmt.Println(i, v)
}

// Index only
for i := range slice {
    fmt.Println(i)
}

// Value only
for _, v := range slice {
    fmt.Println(v)
}

// Range over map
for k, v := range m {
    fmt.Println(k, v)
}

// Range over string (runes)
for i, r := range "hello" {
    fmt.Printf("%d: %c\n", i, r)
}

// Range over channel
for msg := range ch {
    fmt.Println(msg)
}
```

---

## Error Handling

### The error Interface

```go
// error is a built-in interface
type error interface {
    Error() string
}

// Create errors
err := errors.New("something went wrong")
err := fmt.Errorf("failed to process %s: %w", name, originalErr)
```

### Error Handling Pattern

```go
// Check errors immediately
result, err := doSomething()
if err != nil {
    return err // Or handle appropriately
}
// Use result...

// Multiple operations
f, err := os.Open(filename)
if err != nil {
    return fmt.Errorf("open file: %w", err)
}
defer f.Close()

data, err := io.ReadAll(f)
if err != nil {
    return fmt.Errorf("read file: %w", err)
}
```

### Custom Errors

```go
// Simple custom error
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Usage
return ValidationError{Field: "email", Message: "invalid format"}
```

### Error Wrapping (Go 1.13+)

```go
// Wrap error with context
if err != nil {
    return fmt.Errorf("failed to connect: %w", err)
}

// Check error type
if errors.Is(err, os.ErrNotExist) {
    // Handle file not found
}

// Extract wrapped error
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println("Path:", pathErr.Path)
}
```

### Panic and Recover

```go
// Panic for unrecoverable errors (avoid in library code)
func mustParse(s string) int {
    n, err := strconv.Atoi(s)
    if err != nil {
        panic(err)
    }
    return n
}

// Recover from panic
func safeCall(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic: %v", r)
        }
    }()
    fn()
    return nil
}
```

---

## Concurrency Basics

### Goroutines

```go
// Start goroutine
go doWork()

// Anonymous goroutine
go func() {
    fmt.Println("In goroutine")
}()

// With arguments (captured by value)
for i := 0; i < 5; i++ {
    go func(n int) {
        fmt.Println(n)
    }(i)
}
```

### Channels

```go
// Create channel
ch := make(chan int)        // Unbuffered
ch := make(chan int, 10)    // Buffered (capacity 10)

// Send and receive
ch <- 42        // Send (blocks if full/unbuffered)
val := <-ch     // Receive (blocks if empty)

// Close channel
close(ch)

// Check if closed
val, ok := <-ch
if !ok {
    fmt.Println("Channel closed")
}

// Range over channel (until closed)
for val := range ch {
    fmt.Println(val)
}
```

### Channel Directions

```go
// Send-only channel
func producer(ch chan<- int) {
    ch <- 42
}

// Receive-only channel
func consumer(ch <-chan int) {
    val := <-ch
}
```

### Select

```go
// Wait on multiple channels
select {
case msg := <-ch1:
    fmt.Println("From ch1:", msg)
case msg := <-ch2:
    fmt.Println("From ch2:", msg)
case ch3 <- 42:
    fmt.Println("Sent to ch3")
default:
    fmt.Println("No communication ready")
}

// Timeout pattern
select {
case result := <-ch:
    fmt.Println(result)
case <-time.After(time.Second):
    fmt.Println("Timeout")
}
```

### WaitGroup

```go
import "sync"

var wg sync.WaitGroup

for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(n int) {
        defer wg.Done()
        fmt.Println(n)
    }(i)
}

wg.Wait() // Block until all done
```

### Mutex

```go
import "sync"

type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}

// RWMutex for read-heavy workloads
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) string {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.data[key]
}
```

---

## Common Patterns

### Options Pattern (Functional Options)

```go
type Server struct {
    host    string
    port    int
    timeout time.Duration
}

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) {
        s.port = port
    }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(host string, opts ...Option) *Server {
    s := &Server{
        host:    host,
        port:    8080,           // Default
        timeout: time.Minute,    // Default
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
server := NewServer("localhost",
    WithPort(9000),
    WithTimeout(30*time.Second),
)
```

### Constructor Pattern

```go
type User struct {
    id   int
    name string
}

// Constructor function (New prefix convention)
func NewUser(id int, name string) *User {
    return &User{
        id:   id,
        name: name,
    }
}

// MustX for constructors that can fail
func MustCompile(pattern string) *regexp.Regexp {
    re, err := regexp.Compile(pattern)
    if err != nil {
        panic(err)
    }
    return re
}
```

### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Context for Cancellation

```go
import "context"

func doWork(ctx context.Context) error {
    select {
    case <-time.After(time.Hour):
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

// Usage with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

if err := doWork(ctx); err != nil {
    log.Println("Work cancelled:", err)
}

// Usage with cancellation
ctx, cancel := context.WithCancel(context.Background())
go func() {
    time.Sleep(time.Second)
    cancel() // Signal cancellation
}()
```

---

## Go Conventions

### Naming

| Type | Convention | Example |
|------|------------|---------|
| Exported (public) | PascalCase | `UserService` |
| Unexported (private) | camelCase | `userCache` |
| Acronyms | All caps | `HTTPClient`, `xmlParser` |
| Interfaces | -er suffix | `Reader`, `Stringer` |
| Getters | No Get prefix | `Name()` not `GetName()` |
| Package names | lowercase, single word | `http`, `strconv` |

### Code Organization

```go
// Standard file structure
package main

import (
    "fmt"           // Standard library
    "net/http"

    "github.com/pkg/errors"  // Third-party

    "myproject/internal/user"  // Internal packages
)

// Constants
const MaxRetries = 3

// Package-level variables (minimize these)
var defaultClient = &http.Client{}

// Types
type Server struct { ... }

// Functions
func NewServer() *Server { ... }

// Methods
func (s *Server) Start() error { ... }
```

### Error Strings

```go
// Lowercase, no punctuation
errors.New("connection refused")  // Good
errors.New("Connection refused.") // Bad

// With context
fmt.Errorf("open %s: %w", filename, err)
```

---

## Troubleshooting

### "declared and not used"

```go
// Go requires all variables to be used
x := 5  // Error if x is never used

// Use blank identifier to ignore
x, _ := someFuncReturningTwo()
```

### "cannot use X as type Y"

```go
// Types must match exactly
var x int64 = 5
var y int = x    // Error: int64 != int

// Explicit conversion required
var y int = int(x)
```

### "nil pointer dereference"

```go
// Check for nil before dereferencing
var u *User
fmt.Println(u.Name)  // Panic!

if u != nil {
    fmt.Println(u.Name)
}
```

### "all goroutines are asleep - deadlock!"

```go
// Common cause: unbuffered channel with no receiver
ch := make(chan int)
ch <- 1  // Blocks forever, no receiver

// Fix: use buffered channel or ensure receiver exists
ch := make(chan int, 1)
ch <- 1  // OK
```

### "race condition detected"

```go
// Run with race detector
// go run -race main.go

// Fix: use sync primitives
var mu sync.Mutex
mu.Lock()
shared++
mu.Unlock()
```

---

## Module System

Go uses a module system for dependency management and package organization.

### Package Basics

```go
// Every .go file starts with package declaration
package main    // Executable (has main function)
package user    // Library package

// Package names should be:
// - lowercase, single word
// - match the directory name
// - not generic (utils, common, misc)
```

### Import Paths

```go
import (
    // Standard library
    "fmt"
    "net/http"
    "encoding/json"

    // Third-party packages
    "github.com/gorilla/mux"
    "github.com/pkg/errors"

    // Internal packages
    "myproject/internal/config"
    "myproject/pkg/utils"
)

// Aliased imports
import (
    "fmt"
    myfmt "myproject/fmt"  // Avoid name collision
)

// Blank import (side effects only)
import _ "github.com/lib/pq"  // Register database driver

// Dot import (avoid in production)
import . "fmt"  // Allows Println() instead of fmt.Println()
```

### Visibility

```go
// Uppercase = exported (public)
// Lowercase = unexported (private)

package user

type User struct {       // Exported
    Name  string        // Exported
    email string        // Unexported (package-private)
}

func NewUser() *User {   // Exported
    return &User{}
}

func validate() bool {   // Unexported
    return true
}
```

### Project Structure

```
myproject/
├── go.mod              # Module definition
├── go.sum              # Dependency checksums
├── main.go             # Entry point (package main)
├── cmd/                # Multiple executables
│   ├── server/
│   │   └── main.go
│   └── cli/
│       └── main.go
├── pkg/                # Public library code
│   └── utils/
│       └── strings.go
├── internal/           # Private packages (enforced by Go)
│   └── database/
│       └── conn.go
└── api/                # API definitions (proto, OpenAPI)
```

### Internal Packages

```go
// Packages under 'internal/' are only importable by code
// within the parent of 'internal/'

// myproject/internal/database/conn.go
// Can be imported by: myproject/...
// Cannot be imported by: other projects

// This is enforced by the Go compiler
```

---

## Serialization

Go uses struct tags for serialization configuration.

### JSON Basics

```go
import "encoding/json"

type User struct {
    Name  string `json:"name"`
    Email string `json:"email"`
    Age   int    `json:"age"`
}

// Serialize (Marshal)
user := User{Name: "Alice", Email: "alice@example.com", Age: 30}
data, err := json.Marshal(user)
// {"name":"Alice","email":"alice@example.com","age":30}

// Pretty print
data, err := json.MarshalIndent(user, "", "  ")

// Deserialize (Unmarshal)
var user User
err := json.Unmarshal([]byte(jsonStr), &user)

// Stream encoding/decoding
encoder := json.NewEncoder(writer)
encoder.Encode(user)

decoder := json.NewDecoder(reader)
decoder.Decode(&user)
```

### Struct Tags

```go
type Config struct {
    // Rename field
    Name string `json:"name"`

    // Omit if empty/zero value
    Email string `json:"email,omitempty"`

    // Ignore field (never serialize)
    Password string `json:"-"`

    // String encoding for numbers
    Count int `json:"count,string"`

    // Multiple tags
    CreatedAt time.Time `json:"created_at" db:"created_at"`
}
```

### Optional Fields

```go
type User struct {
    Name  string  `json:"name"`
    Email *string `json:"email,omitempty"` // Pointer = nullable
    Age   int     `json:"age,omitempty"`   // Omit if 0
}

// Check for null
if user.Email != nil {
    fmt.Println(*user.Email)
}
```

### Custom Marshal/Unmarshal

```go
type Status int

const (
    StatusPending Status = iota
    StatusActive
    StatusDone
)

func (s Status) MarshalJSON() ([]byte, error) {
    var str string
    switch s {
    case StatusPending:
        str = "pending"
    case StatusActive:
        str = "active"
    case StatusDone:
        str = "done"
    default:
        return nil, fmt.Errorf("unknown status: %d", s)
    }
    return json.Marshal(str)
}

func (s *Status) UnmarshalJSON(data []byte) error {
    var str string
    if err := json.Unmarshal(data, &str); err != nil {
        return err
    }
    switch str {
    case "pending":
        *s = StatusPending
    case "active":
        *s = StatusActive
    case "done":
        *s = StatusDone
    default:
        return fmt.Errorf("unknown status: %s", str)
    }
    return nil
}
```

### Validation

```go
// Using go-playground/validator
import "github.com/go-playground/validator/v10"

type User struct {
    Name  string `json:"name" validate:"required,min=1,max=100"`
    Email string `json:"email" validate:"required,email"`
    Age   int    `json:"age" validate:"gte=0,lte=150"`
}

var validate = validator.New()

func (u *User) Validate() error {
    return validate.Struct(u)
}

// Usage
if err := user.Validate(); err != nil {
    // Handle validation errors
    for _, err := range err.(validator.ValidationErrors) {
        fmt.Printf("%s: %s\n", err.Field(), err.Tag())
    }
}
```

### Other Formats

```go
// YAML: gopkg.in/yaml.v3
import "gopkg.in/yaml.v3"
data, err := yaml.Marshal(config)
err = yaml.Unmarshal(data, &config)

// TOML: github.com/BurntSushi/toml
import "github.com/BurntSushi/toml"
_, err := toml.DecodeFile("config.toml", &config)

// XML: encoding/xml (standard library)
import "encoding/xml"
data, err := xml.Marshal(config)
```

**See also:** `patterns-serialization-dev` for cross-language serialization patterns

---

## Build and Dependencies

Go uses Go Modules for dependency management.

### go.mod

```go
// go mod init myproject
module github.com/user/myproject

go 1.21

require (
    github.com/gorilla/mux v1.8.0
    github.com/pkg/errors v0.9.1
)

require (
    // Indirect dependencies (automatically managed)
    github.com/some/transitive v1.0.0 // indirect
)

// Replace directive (local development)
replace github.com/original/pkg => ../local/pkg

// Exclude problematic versions
exclude github.com/broken/pkg v1.0.0
```

### Dependency Commands

| Command | Purpose |
|---------|---------|
| `go mod init <module>` | Initialize new module |
| `go mod tidy` | Add missing, remove unused deps |
| `go mod download` | Download dependencies |
| `go mod verify` | Verify dependency checksums |
| `go mod why <pkg>` | Explain why package is needed |
| `go mod graph` | Print dependency graph |
| `go mod vendor` | Copy deps to vendor/ |

### Adding Dependencies

```bash
# Add dependency (latest version)
go get github.com/gorilla/mux

# Add specific version
go get github.com/gorilla/mux@v1.8.0

# Add latest of major version
go get github.com/gorilla/mux@v1

# Add from branch
go get github.com/gorilla/mux@main

# Update dependency
go get -u github.com/gorilla/mux

# Update all dependencies
go get -u ./...

# Remove dependency
go mod tidy  # After removing imports
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `go build` | Compile package |
| `go build -o app` | Compile with output name |
| `go build ./...` | Build all packages |
| `go install` | Compile and install |
| `go run main.go` | Compile and run |
| `go clean` | Remove build artifacts |

### Build Flags

```bash
# Cross-compilation
GOOS=linux GOARCH=amd64 go build -o app-linux

# Static binary (no CGO)
CGO_ENABLED=0 go build -o app

# Strip debug info (smaller binary)
go build -ldflags="-s -w" -o app

# Inject version info
go build -ldflags="-X main.Version=1.0.0" -o app

# Race detector
go build -race -o app

# Embed version
var Version = "dev"  // Set by -ldflags
```

### Workspaces (Go 1.18+)

```bash
# For multi-module development
go work init ./module1 ./module2

# go.work file
go 1.21

use (
    ./module1
    ./module2
)
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `GOPATH` | Workspace path (legacy) |
| `GOBIN` | Binary install location |
| `GOPROXY` | Module proxy URL |
| `GOPRIVATE` | Private module patterns |
| `GONOPROXY` | Skip proxy for patterns |
| `GONOSUMDB` | Skip checksum DB |

```bash
# Private repos
go env -w GOPRIVATE=github.com/mycompany/*

# Use default proxy with fallback
go env -w GOPROXY=https://proxy.golang.org,direct
```

---

## Testing

Go has built-in testing support with the `testing` package.

### Basic Tests

```go
// user_test.go (must end with _test.go)
package user

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

func TestAddNegative(t *testing.T) {
    result := Add(-1, 1)
    if result != 0 {
        t.Errorf("Add(-1, 1) = %d; want 0", result)
    }
}
```

### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 1, 2, 3},
        {"negative numbers", -1, -2, -3},
        {"zero", 0, 0, 0},
        {"mixed", -1, 1, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Test Helpers

```go
// Helper function
func setupTestDatabase(t *testing.T) *Database {
    t.Helper()  // Marks as helper (better error locations)
    db, err := NewTestDatabase()
    if err != nil {
        t.Fatalf("setup failed: %v", err)
    }
    t.Cleanup(func() {  // Cleanup after test
        db.Close()
    })
    return db
}

func TestUser(t *testing.T) {
    db := setupTestDatabase(t)
    // Test using db...
}
```

### Subtests and Parallel

```go
func TestUser(t *testing.T) {
    // Subtests
    t.Run("Create", func(t *testing.T) {
        t.Parallel()  // Run in parallel
        // Test create...
    })

    t.Run("Update", func(t *testing.T) {
        t.Parallel()
        // Test update...
    })
}
```

### Running Tests

```bash
# Run all tests
go test ./...

# Run specific package
go test ./pkg/user

# Run specific test
go test -run TestAdd ./...

# Run with verbose output
go test -v ./...

# Run with coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Run with race detector
go test -race ./...

# Run benchmarks
go test -bench=. ./...

# Timeout
go test -timeout 30s ./...

# Skip long tests
go test -short ./...
```

### Benchmarks

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(1, 2)
    }
}

func BenchmarkAddParallel(b *testing.B) {
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            Add(1, 2)
        }
    })
}

// With setup
func BenchmarkProcess(b *testing.B) {
    data := setupLargeData()
    b.ResetTimer()  // Don't count setup time

    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

### Mocking with Interfaces

```go
// Define interface for dependencies
type UserStore interface {
    GetUser(id int) (*User, error)
    SaveUser(user *User) error
}

// Real implementation
type PostgresStore struct { ... }

// Mock implementation
type MockStore struct {
    users map[int]*User
}

func (m *MockStore) GetUser(id int) (*User, error) {
    user, ok := m.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return user, nil
}

// Test with mock
func TestService(t *testing.T) {
    mock := &MockStore{
        users: map[int]*User{
            1: {ID: 1, Name: "Alice"},
        },
    }

    service := NewUserService(mock)
    user, err := service.GetUser(1)
    // Assert...
}
```

### Example Tests

```go
// Example tests appear in documentation
func ExampleAdd() {
    sum := Add(2, 3)
    fmt.Println(sum)
    // Output: 5
}

func ExampleUser_FullName() {
    u := User{FirstName: "Alice", LastName: "Smith"}
    fmt.Println(u.FullName())
    // Output: Alice Smith
}
```

### TestMain

```go
func TestMain(m *testing.M) {
    // Setup before all tests
    setup()

    // Run tests
    code := m.Run()

    // Cleanup after all tests
    teardown()

    os.Exit(code)
}
```

---

## Metaprogramming

Go has limited metaprogramming capabilities compared to languages with macros. The primary approach is code generation.

### Code Generation

```go
//go:generate stringer -type=Status

type Status int

const (
    StatusPending Status = iota
    StatusActive
    StatusDone
)

// Run: go generate ./...
// Generates: status_string.go with String() method
```

### Common Generators

| Tool | Purpose |
|------|---------|
| `stringer` | Generate String() for enums |
| `mockgen` | Generate mock implementations |
| `protoc` | Generate from Protocol Buffers |
| `go-bindata` | Embed files in binary |
| `sqlc` | Generate from SQL |
| `ent` | Generate ORM code |

### Build Tags

```go
// +build linux
// +build !windows

package mypackage

// This file only compiles on Linux, not on Windows
```

```go
//go:build linux && amd64

package mypackage

// Go 1.17+ syntax
```

### Reflection (Runtime)

```go
import "reflect"

func PrintFields(v interface{}) {
    t := reflect.TypeOf(v)
    val := reflect.ValueOf(v)

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        value := val.Field(i)
        tag := field.Tag.Get("json")

        fmt.Printf("%s (%s): %v [json:%s]\n",
            field.Name, field.Type, value.Interface(), tag)
    }
}

// Use reflection sparingly - it's slow and unsafe
```

**See also:** `patterns-metaprogramming-dev` for cross-language comparison

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Goroutines, channels, select patterns
- `patterns-serialization-dev` - JSON, struct tags, validation
- `patterns-metaprogramming-dev` - Code generation, build tags

---

## References

- [Go Documentation](https://go.dev/doc/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go by Example](https://gobyexample.com/)
- Specialized skills: `go-concurrency-patterns` (external)
