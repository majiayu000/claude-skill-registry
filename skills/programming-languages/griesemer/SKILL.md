---
name: griesemer-precise-go
description: Write Go code in the style of Robert Griesemer, co-creator of Go. Emphasizes clean syntax, precise semantics, and well-defined type system behavior. Use when designing APIs, type hierarchies, or code that requires precise specification.
---

# Robert Griesemer Style Guide

## Overview

Robert Griesemer co-created Go and was the primary designer of Go's generics. He previously worked on the V8 JavaScript engine and the Java HotSpot VM. His focus: precise semantics, clean syntax, and type system clarity.

## Core Philosophy

> "The language should help you think clearly."

> "Every feature adds complexity. Is the complexity worth it?"

Griesemer values **precision and clarity**. Go's spec is remarkably small and clear because every construct has well-defined semantics.

## Design Principles

1. **Precise Semantics**: Every language construct has exactly one meaning.

2. **Orthogonal Features**: Features should combine predictably.

3. **No Surprises**: Behavior should be obvious from reading the code.

4. **Spec-Driven**: If it's not in the spec, it's not guaranteed.

## When Writing Code

### Always

- Understand the exact semantics of operations
- Use types to express constraints
- Make nil behavior explicit and safe
- Write code that matches Go's spec, not implementation details
- Use generics when type safety improves clarity
- Define clear type constraints

### Never

- Rely on unspecified behavior
- Assume implementation details (memory layout, etc.)
- Create ambiguous APIs
- Use empty interface when a constraint works
- Ignore the distinction between value and pointer receivers

### Prefer

- Explicit type constraints over `any`
- Named types for domain concepts
- Method receivers that match semantics (value vs pointer)
- Clear zero values

## Code Patterns

### Generics Done Right (Go 1.18+)

```go
// BAD: Empty interface loses type safety
func Max(a, b interface{}) interface{} {
    // runtime type assertion needed
    switch v := a.(type) {
    case int:
        if v > b.(int) { return v }
        return b
    // ... repeat for every type
    }
    panic("unsupported type")
}

// GOOD: Type constraints preserve safety
type Ordered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
    ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
    ~float32 | ~float64 | ~string
}

func Max[T Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// Usage: type-safe, no assertions
result := Max(3, 5)        // int
result := Max(3.14, 2.71)  // float64
```

### Precise Type Constraints

```go
// Constraint: any type with these methods
type Stringer interface {
    String() string
}

// Constraint: underlying type is int
type Integer interface {
    ~int | ~int64
}

// Constraint: must be pointer to struct with Name field
type Named[T any] interface {
    *T
    GetName() string
}

// Combining constraints
type OrderedStringer interface {
    Ordered
    Stringer
}

// Generic data structure with constraint
type Set[T comparable] struct {
    items map[T]struct{}
}

func (s *Set[T]) Add(item T) {
    if s.items == nil {
        s.items = make(map[T]struct{})
    }
    s.items[item] = struct{}{}
}

func (s *Set[T]) Contains(item T) bool {
    _, ok := s.items[item]
    return ok
}
```

### Value vs Pointer Semantics

```go
// Value receiver: method doesn't modify, type is small
type Point struct {
    X, Y float64
}

func (p Point) Distance(q Point) float64 {
    dx := p.X - q.X
    dy := p.Y - q.Y
    return math.Sqrt(dx*dx + dy*dy)
}

// Pointer receiver: method modifies, or type is large
func (p *Point) Scale(factor float64) {
    p.X *= factor
    p.Y *= factor
}

// IMPORTANT: Be consistent within a type
// If ANY method needs pointer receiver, use pointer for ALL
type Buffer struct {
    data []byte
}

func (b *Buffer) Write(p []byte) (int, error) {
    b.data = append(b.data, p...)
    return len(p), nil
}

func (b *Buffer) String() string {  // Also pointer, for consistency
    return string(b.data)
}
```

### Safe Nil Handling

```go
// Make nil receiver safe
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) {
    if s == nil {
        panic("nil stack")  // Or return error
    }
    s.items = append(s.items, item)
}

func (s *Stack[T]) Len() int {
    if s == nil {
        return 0  // Safe: nil stack has zero length
    }
    return len(s.items)
}

// Named types for clarity
type UserID int64
type OrderID int64

// Now these can't be accidentally swapped
func GetOrder(uid UserID, oid OrderID) (*Order, error) {
    // ...
}
```

### Precise Interface Design

```go
// Small, precise interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// Compose precisely
type ReadCloser interface {
    Reader
    Closer
}

type WriteCloser interface {
    Writer
    Closer
}

type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

// Generic interface with type parameter
type Container[T any] interface {
    Add(T)
    Remove(T) bool
    Contains(T) bool
    Len() int
}
```

## Mental Model

Griesemer designs by asking:

1. **What does the spec say?** Not the implementation—the specification.
2. **Is this unambiguous?** Can two people read this differently?
3. **What are the edge cases?** nil, zero values, overflow?
4. **Is the type constraint minimal?** Don't over-constrain.

## Spec-Level Thinking

| Feature | Spec Guarantee |
|---------|----------------|
| Map iteration | Random order |
| Goroutine scheduling | Unspecified |
| Struct layout | Unspecified |
| String indexing | Bytes, not runes |
| Interface nil | nil interface ≠ interface holding nil |

Write code that works regardless of implementation details.

