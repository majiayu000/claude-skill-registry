---
name: go-interfaces
description: Go interfaces, type assertions, type switches, and embedding from Effective Go. Covers implicit interface satisfaction, comma-ok idiom, generality through interface returns, interface and struct embedding for composition. Use when defining or implementing interfaces, using type assertions/switches, or composing types through embedding.
---

# Go Interfaces and Composition

Go's interfaces enable flexible, decoupled designs through implicit satisfaction
and composition. This skill covers interface fundamentals, type inspection, and
Go's approach to composition over inheritance.

> **Source**: [Effective Go](https://go.dev/doc/effective_go)

---

## Interface Basics

Interfaces in Go specify behavior: if something can do *this*, it can be used
*here*. Types implement interfaces implicitly—no `implements` keyword needed.

```go
// io.Writer interface - any type with this method satisfies it
type Writer interface {
    Write(p []byte) (n int, err error)
}
```

A type satisfies an interface by implementing its methods:

```go
type ByteSlice []byte

// ByteSlice now implements io.Writer
func (p *ByteSlice) Write(data []byte) (n int, err error) {
    *p = append(*p, data...)
    return len(data), nil
}

// Can be used anywhere io.Writer is expected
var w io.Writer = &ByteSlice{}
fmt.Fprintf(w, "Hello, %s", "World")
```

### Multiple Interface Implementation

A type can implement multiple interfaces simultaneously:

```go
type Sequence []int

// Implements sort.Interface
func (s Sequence) Len() int           { return len(s) }
func (s Sequence) Less(i, j int) bool { return s[i] < s[j] }
func (s Sequence) Swap(i, j int)      { s[i], s[j] = s[j], s[i] }

// Implements fmt.Stringer
func (s Sequence) String() string {
    sort.Sort(s)
    return fmt.Sprint([]int(s))
}
```

### Interface Naming

By convention, one-method interfaces use the method name plus `-er` suffix:
`Reader`, `Writer`, `Formatter`, `Stringer`.

---

## Type Assertions

A type assertion extracts the concrete value from an interface.

### Basic Syntax

```go
value.(typeName)
```

The result has the static type `typeName`. The type must be either:
- The concrete type held by the interface, or
- Another interface type the value can be converted to

```go
var w io.Writer = os.Stdout
f := w.(*os.File)  // Extract *os.File from io.Writer
```

### Comma-Ok Idiom

Without checking, a failed assertion causes a runtime panic. Use the comma-ok
idiom to test safely:

```go
str, ok := value.(string)
if ok {
    fmt.Printf("string value is: %q\n", str)
} else {
    fmt.Printf("value is not a string\n")
}
```

If the assertion fails, `str` is the zero value (empty string) and `ok` is
false.

### Checking Interface Implementation

To check if a value implements an interface without using the result:

```go
if _, ok := val.(json.Marshaler); ok {
    fmt.Printf("value %v implements json.Marshaler\n", val)
}
```

---

## Type Switch

A type switch discovers the dynamic type of an interface variable using the
`.(type)` syntax:

```go
var t interface{}
t = functionOfSomeType()

switch t := t.(type) {
default:
    fmt.Printf("unexpected type %T\n", t)
case bool:
    fmt.Printf("boolean %t\n", t)             // t has type bool
case int:
    fmt.Printf("integer %d\n", t)             // t has type int
case *bool:
    fmt.Printf("pointer to boolean %t\n", *t) // t has type *bool
case *int:
    fmt.Printf("pointer to integer %d\n", *t) // t has type *int
}
```

### Idiomatic Reuse of Variable Name

It's idiomatic to reuse the name in the switch expression. This declares a new
variable with the same name but the correct type in each case branch.

### Mixing Concrete and Interface Types

Type switches can match both concrete types and interface types:

```go
type Stringer interface {
    String() string
}

var value interface{}
switch str := value.(type) {
case string:
    return str                // str is string
case Stringer:
    return str.String()       // str is Stringer
}
```

---

## Generality

If a type exists only to implement an interface with no exported methods beyond
that interface, don't export the type—return the interface from constructors.

### Hide Implementation, Expose Interface

```go
// Good: Constructor returns interface type
func NewHash() hash.Hash32 {
    return &myHash{}  // unexported type
}

// The implementation is hidden; callers only see hash.Hash32
```

### Real-World Example: crypto/cipher

The `crypto/cipher` package demonstrates this pattern:

```go
type Block interface {
    BlockSize() int
    Encrypt(dst, src []byte)
    Decrypt(dst, src []byte)
}

type Stream interface {
    XORKeyStream(dst, src []byte)
}

// Returns Stream interface, hiding implementation details
func NewCTR(block Block, iv []byte) Stream
```

**Benefits**:
- Implementation can change without affecting callers
- Substituting algorithms requires only changing the constructor call
- Documentation lives on the interface, not repeated on each implementation

---

## Interface Embedding

Combine interfaces by embedding them:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// ReadWriter combines Reader and Writer
type ReadWriter interface {
    Reader
    Writer
}
```

A `ReadWriter` can do what a `Reader` does *and* what a `Writer` does—it's a
union of the embedded interfaces.

**Rule**: Only interfaces can be embedded within interfaces.

---

## Struct Embedding

Go uses embedding for composition instead of inheritance. Embedding promotes
methods from the inner type to the outer type.

### Basic Struct Embedding

```go
// bufio.ReadWriter embeds Reader and Writer
type ReadWriter struct {
    *Reader  // *bufio.Reader
    *Writer  // *bufio.Writer
}
```

Without embedding, you'd need forwarding methods:

```go
// Without embedding - tedious boilerplate
type ReadWriter struct {
    reader *Reader
    writer *Writer
}

func (rw *ReadWriter) Read(p []byte) (n int, err error) {
    return rw.reader.Read(p)
}
```

With embedding, methods are promoted automatically. `bufio.ReadWriter` satisfies
`io.Reader`, `io.Writer`, and `io.ReadWriter` without explicit forwarding.

### Embedding for Convenience

Mix embedded and named fields:

```go
type Job struct {
    Command string
    *log.Logger
}

// Job now has Print, Printf, Println methods
job.Println("starting now...")
```

### Accessing Embedded Fields

The type name (without package qualifier) serves as the field name:

```go
// Access the embedded Logger directly
job.Logger.SetPrefix("Job: ")
```

### Method Overriding

Define a method on the outer type to override the embedded method:

```go
func (job *Job) Printf(format string, args ...interface{}) {
    job.Logger.Printf("%q: %s", job.Command, fmt.Sprintf(format, args...))
}
```

### Embedding vs Subclassing

**Key difference**: When an embedded method is invoked, the receiver is the
*inner* type, not the outer one. The embedded type doesn't know it's embedded.

```go
type ReadWriter struct {
    *Reader
    *Writer
}

// When rw.Read() is called, the receiver is the Reader, not ReadWriter
```

### Name Conflict Resolution

1. **Outer fields/methods hide inner ones**: A field `X` on the outer type hides
   any `X` in embedded types
2. **Same level conflicts are errors**: Embedding two types with the same method
   name at the same level causes an error (unless never accessed)

---

## Interface Satisfaction Checks

Most interface conversions are checked at compile time. But sometimes you need
to verify implementation explicitly.

### Compile-Time Interface Check

Use a blank identifier assignment to verify a type implements an interface:

```go
// Verify *RawMessage implements json.Marshaler at compile time
var _ json.Marshaler = (*RawMessage)(nil)
```

This causes a compile error if `*RawMessage` doesn't implement `json.Marshaler`.

### When to Use This Pattern

Use compile-time checks when:
- There are no static conversions that would verify the interface automatically
- The type must satisfy an interface for correct behavior (e.g., custom JSON
  marshaling)
- Interface changes should break compilation, not silently degrade

```go
// In your package
type MyType struct { /* ... */ }

func (m *MyType) MarshalJSON() ([]byte, error) { /* ... */ }

// Compile-time check - fails if MarshalJSON signature is wrong
var _ json.Marshaler = (*MyType)(nil)
```

**Don't** add these checks for every interface implementation—only when there's
no other static conversion that would catch the error.

---

## Receiver Type

> **Advisory**: Go Wiki CodeReviewComments

Choosing whether to use a value or pointer receiver on methods can be difficult.
**If in doubt, use a pointer**, but there are times when a value receiver makes
sense.

### When to Use Pointer Receiver

- **Method mutates receiver**: The receiver must be a pointer
- **Receiver contains sync.Mutex or similar**: Must be a pointer to avoid copying
- **Large struct or array**: A pointer receiver is more efficient. If passing all
  elements as arguments feels too large, it's too large for a value receiver
- **Concurrent or called methods might mutate**: If changes must be visible in
  the original receiver, it must be a pointer
- **Elements are pointers to something mutating**: Prefer pointer receiver to
  make the intention clearer

### When to Use Value Receiver

- **Small unchanging structs or basic types**: Value receiver for efficiency
- **Map, func, or chan**: Don't use a pointer to them
- **Slice without reslicing/reallocating**: Don't use a pointer if the method
  doesn't reslice or reallocate the slice
- **Small value types with no mutable fields**: Types like `time.Time` with no
  mutable fields and no pointers work well as value receivers
- **Simple basic types**: `int`, `string`, etc.

```go
// Value receiver: small, immutable type
type Point struct {
    X, Y float64
}

func (p Point) Distance(q Point) float64 {
    return math.Hypot(q.X-p.X, q.Y-p.Y)
}

// Pointer receiver: method mutates receiver
func (p *Point) ScaleBy(factor float64) {
    p.X *= factor
    p.Y *= factor
}

// Pointer receiver: contains sync.Mutex
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    c.count++
    c.mu.Unlock()
}
```

### Consistency Rule

**Don't mix receiver types**. Choose either pointers or struct types for all
available methods on a type. If any method needs a pointer receiver, use pointer
receivers for all methods.

```go
// Good: Consistent pointer receivers
type Buffer struct {
    data []byte
}

func (b *Buffer) Write(p []byte) (int, error) { /* ... */ }
func (b *Buffer) Read(p []byte) (int, error)  { /* ... */ }
func (b *Buffer) Len() int                     { return len(b.data) }

// Bad: Mixed receiver types
func (b Buffer) Len() int                      { return len(b.data) }  // inconsistent
```

---

## Quick Reference

| Concept | Pattern | Notes |
|---------|---------|-------|
| Implicit implementation | Just implement the methods | No `implements` keyword |
| Type assertion | `v := x.(Type)` | Panics if wrong type |
| Safe type assertion | `v, ok := x.(Type)` | Returns zero value + false |
| Type switch | `switch v := x.(type)` | Variable has correct type per case |
| Interface embedding | `type RW interface { Reader; Writer }` | Union of methods |
| Struct embedding | `type S struct { *T }` | Promotes T's methods |
| Access embedded field | `s.T` or `s.T.Method()` | Type name is field name |
| Interface check | `var _ I = (*T)(nil)` | Compile-time verification |
| Generality | Return interface from constructor | Hide implementation |

---

## See Also

- **go-style-core**: Core Go style principles and formatting
- **go-naming**: Interface naming conventions (Reader, Writer, etc.)
- **go-error-handling**: Error interface and custom error types
- **go-functional-options**: Using interfaces for flexible APIs
- **go-defensive**: Defensive programming patterns
