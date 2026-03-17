---
name: go-data-structures
description: Go data structures including allocation with new vs make, arrays, slices, maps, printing with fmt, and constants with iota. Use when working with Go's built-in data structures, memory allocation, or formatted output.
---

# Go Data Structures

> **Source**: Effective Go

This skill covers Go's built-in data structures and allocation primitives.

---

## Allocation: new vs make

Go has two allocation primitives: `new` and `make`. They do different things.

### new

`new(T)` allocates zeroed storage for a new item of type `T` and returns `*T`:

```go
p := new(SyncedBuffer)  // type *SyncedBuffer, zeroed
var v SyncedBuffer      // type  SyncedBuffer, zeroed
```

**Zero-value design**: Design data structures so the zero value is useful without
further initialization. Examples: `bytes.Buffer`, `sync.Mutex`.

```go
type SyncedBuffer struct {
    lock    sync.Mutex
    buffer  bytes.Buffer
}
// Ready to use immediately upon allocation
```

### make

`make(T, args)` creates slices, maps, and channels only. It returns an
**initialized** (not zeroed) value of type `T` (not `*T`):

```go
make([]int, 10, 100)  // slice: length 10, capacity 100
make(map[string]int)  // map: ready to use
make(chan int)        // channel: ready to use
```

### The Difference

```go
var p *[]int = new([]int)       // *p == nil; rarely useful
var v  []int = make([]int, 100) // v is a usable slice of 100 ints

// Idiomatic:
v := make([]int, 100)
```

**Rule**: `make` applies only to maps, slices, and channels and does not return
a pointer.

---

## Composite Literals

Create and initialize structs, arrays, slices, and maps in one expression:

```go
// Struct with positional fields
f := File{fd, name, nil, 0}

// Struct with named fields (order doesn't matter, missing = zero)
f := &File{fd: fd, name: name}

// Zero value
f := &File{}  // equivalent to new(File)

// Arrays, slices, maps
a := [...]string{Enone: "no error", Eio: "Eio", Einval: "invalid"}
s := []string{Enone: "no error", Eio: "Eio", Einval: "invalid"}
m := map[int]string{Enone: "no error", Eio: "Eio", Einval: "invalid"}
```

**Note**: It's safe to return the address of a local variable in Go—the storage
survives after the function returns.

---

## Arrays

Arrays are values in Go (unlike C):

- Assigning one array to another copies all elements
- Passing an array to a function passes a copy, not a pointer
- The size is part of the type: `[10]int` and `[20]int` are distinct

```go
func Sum(a *[3]float64) (sum float64) {
    for _, v := range *a {
        sum += v
    }
    return
}

array := [...]float64{7.0, 8.5, 9.1}
x := Sum(&array)  // Pass pointer for efficiency
```

**Recommendation**: Use slices instead of arrays in most cases.

---

## Slices

Slices wrap arrays to provide a flexible, powerful interface to sequences.

### Slice Basics

Slices hold references to an underlying array. Assigning one slice to another
makes both refer to the same array:

```go
func (f *File) Read(buf []byte) (n int, err error)

// Read into first 32 bytes of larger buffer
n, err := f.Read(buf[0:32])
```

### Length and Capacity

- `len(s)`: current length
- `cap(s)`: maximum length (from start of slice to end of underlying array)

### The append Function

```go
func append(slice []T, elements ...T) []T
```

**Always assign the result**—the underlying array may change:

```go
x := []int{1, 2, 3}
x = append(x, 4, 5, 6)

// Append a slice to a slice
y := []int{4, 5, 6}
x = append(x, y...)  // Note the ...
```

### Two-Dimensional Slices

**Method 1**: Independent inner slices (can grow/shrink independently):

```go
picture := make([][]uint8, YSize)
for i := range picture {
    picture[i] = make([]uint8, XSize)
}
```

**Method 2**: Single allocation (more efficient for fixed sizes):

```go
picture := make([][]uint8, YSize)
pixels := make([]uint8, XSize*YSize)
for i := range picture {
    picture[i], pixels = pixels[:XSize], pixels[XSize:]
}
```

For detailed slice internals, see [references/SLICES.md](references/SLICES.md).

### Declaring Empty Slices

> **Normative**: This is required per Go Wiki CodeReviewComments.

When declaring an empty slice, prefer:

```go
var t []string
```

over:

```go
t := []string{}
```

The former declares a **nil slice**, while the latter is **non-nil but zero-length**.
They are functionally equivalent—their `len` and `cap` are both zero—but the nil
slice is the preferred style.

**Exception for JSON encoding:** A nil slice encodes to `null`, while an empty
slice `[]string{}` encodes to `[]`. Use non-nil when you need a JSON array:

```go
// nil slice → JSON null
var tags []string
json.Marshal(tags)  // "null"

// empty slice → JSON array
tags := []string{}
json.Marshal(tags)  // "[]"
```

**Interface design:** When designing interfaces, avoid making a distinction
between a nil slice and a non-nil zero-length slice, as this can lead to subtle
programming errors.

---

## Maps

Maps associate keys with values. Keys must support equality (`==`).

### Creating and Using Maps

```go
var timeZone = map[string]int{
    "UTC":  0*60*60,
    "EST": -5*60*60,
    "CST": -6*60*60,
}

offset := timeZone["EST"]  // -18000
```

### Testing for Presence

An absent key returns the zero value. Use the "comma ok" idiom to distinguish:

```go
seconds, ok := timeZone[tz]
if !ok {
    log.Println("unknown time zone:", tz)
}

// Or combined:
if seconds, ok := timeZone[tz]; ok {
    return seconds
}
```

### Deleting Entries

```go
delete(timeZone, "PDT")  // Safe even if key doesn't exist
```

### Implementing a Set

Use `map[T]bool`:

```go
attended := map[string]bool{"Ann": true, "Joe": true}

if attended[person] {  // false if not in map
    fmt.Println(person, "was at the meeting")
}
```

---

## Printing

The `fmt` package provides rich formatted printing.

### Basic Functions

| Function | Output |
|----------|--------|
| `Printf` | Formatted to stdout |
| `Sprintf` | Returns formatted string |
| `Fprintf` | Formatted to io.Writer |
| `Print/Println` | Default format |

```go
fmt.Printf("Hello %d\n", 23)
fmt.Println("Hello", 23)
s := fmt.Sprintf("Hello %d", 23)
```

### The %v Format

`%v` prints any value with a reasonable default:

```go
fmt.Printf("%v\n", timeZone)
// map[CST:-21600 EST:-18000 MST:-25200 PST:-28800 UTC:0]
```

For structs:
- `%v`: values only
- `%+v`: with field names
- `%#v`: full Go syntax

```go
type T struct {
    a int
    b float64
    c string
}
t := &T{7, -2.35, "abc\tdef"}

fmt.Printf("%v\n", t)   // &{7 -2.35 abc   def}
fmt.Printf("%+v\n", t)  // &{a:7 b:-2.35 c:abc     def}
fmt.Printf("%#v\n", t)  // &main.T{a:7, b:-2.35, c:"abc\tdef"}
```

### Other Useful Formats

| Format | Purpose |
|--------|---------|
| `%T` | Type of value |
| `%q` | Quoted string |
| `%x` | Hex (strings, bytes, ints) |

### The Stringer Interface

Define `String() string` to control default formatting:

```go
func (t *T) String() string {
    return fmt.Sprintf("%d/%g/%q", t.a, t.b, t.c)
}
```

**Warning**: Don't call `Sprintf` with `%s` on the receiver—infinite recursion:

```go
// Bad: infinite recursion
func (m MyString) String() string {
    return fmt.Sprintf("MyString=%s", m)
}

// Good: convert to basic type
func (m MyString) String() string {
    return fmt.Sprintf("MyString=%s", string(m))
}
```

---

## Constants and iota

Constants are created at compile time and can only be numbers, characters,
strings, or booleans.

### iota Enumerator

`iota` creates enumerated constants:

```go
type ByteSize float64

const (
    _           = iota // ignore first value (0)
    KB ByteSize = 1 << (10 * iota)
    MB
    GB
    TB
    PB
    EB
)
```

Combine with `String()` for automatic formatting:

```go
func (b ByteSize) String() string {
    switch {
    case b >= EB:
        return fmt.Sprintf("%.2fEB", b/EB)
    case b >= PB:
        return fmt.Sprintf("%.2fPB", b/PB)
    // ... etc
    }
    return fmt.Sprintf("%.2fB", b)
}
```

---

## Copying

> **Advisory**: This is a best practice recommendation from Go Wiki CodeReviewComments.

To avoid unexpected aliasing, be careful when copying a struct from another
package. For example, `bytes.Buffer` contains a `[]byte` slice. If you copy a
`Buffer`, the slice in the copy may alias the array in the original, causing
subsequent method calls to have surprising effects.

```go
// Dangerous: copying a bytes.Buffer
var buf1 bytes.Buffer
buf1.WriteString("hello")

buf2 := buf1  // buf2's internal slice may alias buf1's array!
buf2.WriteString(" world")  // May affect buf1 unexpectedly
```

**General rule:** Do not copy a value of type `T` if its methods are associated
with the pointer type `*T`.

This applies to many types in the standard library and third-party packages:
- `bytes.Buffer`
- `sync.Mutex`, `sync.WaitGroup`, `sync.Cond`
- Types containing the above

```go
// Bad: copying a mutex
var mu sync.Mutex
mu2 := mu  // Copying a mutex is almost always a bug

// Good: use pointers or embed carefully
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

// Pass by pointer, not by value
func increment(sc *SafeCounter) {
    sc.mu.Lock()
    sc.count++
    sc.mu.Unlock()
}
```

---

## Quick Reference

| Topic | Key Point |
|-------|-----------|
| `new(T)` | Returns `*T`, zeroed |
| `make(T)` | Slices, maps, channels only; returns `T`, initialized |
| Arrays | Values, not references; size is part of type |
| Slices | Reference underlying array; use `append` |
| Maps | Key must support `==`; use comma-ok for presence |
| Copying | Don't copy `T` if methods are on `*T`; beware aliasing |
| `%v` | Default format for any value |
| `%+v` | Struct with field names |
| `%#v` | Full Go syntax |
| `iota` | Enumerated constants |

## See Also

- **go-style-core** - Core Go style principles
- **go-control-flow** - Control structures including range
- **go-interfaces** - Interface patterns and embedding
- **go-concurrency** - Channels and goroutines
