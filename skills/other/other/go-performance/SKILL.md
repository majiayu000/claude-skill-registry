---
name: go-performance
description: Go performance patterns including efficient string handling, type conversions, and container capacity hints. Use when optimizing Go code or writing performance-critical sections.
---

# Go Performance Patterns

> **Source**: Uber Go Style Guide

Performance-specific guidelines apply only to the **hot path**. Don't prematurely optimize—focus these patterns where they matter most.

---

## Prefer strconv over fmt

When converting primitives to/from strings, `strconv` is faster than `fmt`.

> **Source**: Uber Go Style Guide

**Bad:**

```go
for i := 0; i < b.N; i++ {
    s := fmt.Sprint(rand.Int())
}
```

**Good:**

```go
for i := 0; i < b.N; i++ {
    s := strconv.Itoa(rand.Int())
}
```

**Benchmark comparison:**

| Approach | Speed | Allocations |
|----------|-------|-------------|
| `fmt.Sprint` | 143 ns/op | 2 allocs/op |
| `strconv.Itoa` | 64.2 ns/op | 1 allocs/op |

---

## Avoid Repeated String-to-Byte Conversions

Do not create byte slices from a fixed string repeatedly. Instead, perform the conversion once and capture the result.

> **Source**: Uber Go Style Guide

**Bad:**

```go
for i := 0; i < b.N; i++ {
    w.Write([]byte("Hello world"))
}
```

**Good:**

```go
data := []byte("Hello world")
for i := 0; i < b.N; i++ {
    w.Write(data)
}
```

**Benchmark comparison:**

| Approach | Speed |
|----------|-------|
| Repeated conversion | 22.2 ns/op |
| Single conversion | 3.25 ns/op |

The good version is **~7x faster** because it avoids allocating a new byte slice on each iteration.

---

## Prefer Specifying Container Capacity

Specify container capacity where possible to allocate memory up front. This minimizes subsequent allocations from copying and resizing as elements are added.

> **Source**: Uber Go Style Guide

### Map Capacity Hints

Provide capacity hints when initializing maps with `make()`.

```go
make(map[T1]T2, hint)
```

**Note**: Unlike slices, map capacity hints do not guarantee complete preemptive allocation—they approximate the number of hashmap buckets required.

**Bad:**

```go
files, _ := os.ReadDir("./files")

m := make(map[string]os.DirEntry)
for _, f := range files {
    m[f.Name()] = f
}
// Map resizes dynamically, causing multiple allocations
```

**Good:**

```go
files, _ := os.ReadDir("./files")

m := make(map[string]os.DirEntry, len(files))
for _, f := range files {
    m[f.Name()] = f
}
// Map is right-sized at initialization, fewer allocations
```

### Slice Capacity

Provide capacity hints when initializing slices with `make()`, particularly when appending.

```go
make([]T, length, capacity)
```

Unlike maps, slice capacity is **not a hint**—the compiler allocates exactly that much memory. Subsequent `append()` operations incur zero allocations until capacity is reached.

**Bad:**

```go
for n := 0; n < b.N; n++ {
    data := make([]int, 0)
    for k := 0; k < size; k++ {
        data = append(data, k)
    }
}
```

**Good:**

```go
for n := 0; n < b.N; n++ {
    data := make([]int, 0, size)
    for k := 0; k < size; k++ {
        data = append(data, k)
    }
}
```

**Benchmark comparison:**

| Approach | Time (100M iterations) |
|----------|------------------------|
| No capacity | 2.48s |
| With capacity | 0.21s |

The good version is **~12x faster** due to zero reallocations during append.

---

## Pass Values

> **Source**: Go Wiki CodeReviewComments (Advisory)

Don't pass pointers as function arguments just to save a few bytes. If a function refers to its argument `x` only as `*x` throughout, then the argument shouldn't be a pointer.

**Common instances where values should be passed directly:**

- Pointer to a string (`*string`) — strings are already small fixed-size headers
- Pointer to an interface value (`*io.Reader`) — interfaces are fixed-size (type + data pointers)

**Bad:**

```go
func process(s *string) {
	fmt.Println(*s)  // only dereferences, never modifies
}
```

**Good:**

```go
func process(s string) {
	fmt.Println(s)
}
```

**Exceptions:**
- Large structs where copying is expensive
- Small structs that might grow in the future

---

## Quick Reference

| Pattern | Bad | Good | Improvement |
|---------|-----|------|-------------|
| Int to string | `fmt.Sprint(n)` | `strconv.Itoa(n)` | ~2x faster |
| Repeated `[]byte` | `[]byte("str")` in loop | Convert once outside | ~7x faster |
| Map initialization | `make(map[K]V)` | `make(map[K]V, size)` | Fewer allocs |
| Slice initialization | `make([]T, 0)` | `make([]T, 0, cap)` | ~12x faster |
| Small fixed-size args | `*string`, `*io.Reader` | `string`, `io.Reader` | No indirection |

---

## See Also

- For core style principles: `go-style-core`
- For naming conventions: `go-naming`
