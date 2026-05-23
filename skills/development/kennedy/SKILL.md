---
name: kennedy-mechanical-sympathy
description: Write Go code in the style of Bill Kennedy, author of Go in Action. Emphasizes mechanical sympathy, data-oriented design, and understanding how Go code executes. Use when writing performance-critical Go or when teaching Go fundamentals.
---

# Bill Kennedy Style Guide

## Overview

Bill Kennedy is the author of "Go in Action" and founder of Ardan Labs. His teaching emphasizes **mechanical sympathy**: understanding how software interacts with hardware. His "Ultimate Go" course is legendary for deep-dive explanations.

## Core Philosophy

> "Integrity, readability, and simplicity—in that order."

> "If you don't understand the data, you don't understand the problem."

> "Mechanical sympathy: understanding how the hardware and runtime work."

Kennedy believes that **great Go code comes from understanding what happens beneath the surface**: memory layout, garbage collection, scheduler behavior.

## Design Principles

1. **Data-Oriented Design**: Design around data transformations, not object hierarchies.

2. **Mechanical Sympathy**: Write code that works with the hardware, not against it.

3. **Value Semantics First**: Prefer values over pointers unless you have a reason.

4. **Integrity First**: Correctness beats performance, readability beats cleverness.

## When Writing Code

### Always

- Understand the memory layout of your data structures
- Know when copies happen and when references are used
- Consider CPU cache behavior for hot paths
- Profile before optimizing
- Use value semantics by default
- Understand escape analysis

### Never

- Optimize without profiling
- Use pointers just to "avoid copies" without measuring
- Create deep pointer chains (bad for cache)
- Ignore alignment and padding
- Assume you know what escapes to heap

### Prefer

- Contiguous data (slices) over pointer-heavy structures
- Value receivers for small, immutable types
- Stack allocation over heap when possible
- Struct of arrays over array of structs for hot loops
- Understanding over blind rules

## Code Patterns

### Data-Oriented Design

```go
// BAD: Object-oriented thinking, pointer-heavy
type Node struct {
    Value    int
    Children []*Node  // Pointers scattered in memory
}

// GOOD: Data-oriented, cache-friendly
type Tree struct {
    Values   []int    // Contiguous memory
    Children [][]int  // Indices into Values
}

// For hot loops, struct of arrays beats array of structs
// BAD: Array of structs (AoS)
type Particle struct {
    X, Y, Z  float64
    VX, VY, VZ float64
    Mass     float64
}
particles := make([]Particle, 1000)

// GOOD: Struct of arrays (SoA) - better cache utilization
type Particles struct {
    X, Y, Z    []float64
    VX, VY, VZ []float64
    Mass       []float64
}
p := Particles{
    X: make([]float64, 1000),
    Y: make([]float64, 1000),
    // ...
}

// When updating just positions:
for i := range p.X {
    p.X[i] += p.VX[i]  // Sequential memory access
    p.Y[i] += p.VY[i]
    p.Z[i] += p.VZ[i]
}
```

### Value vs Pointer Semantics

```go
// Value semantics: type is small, immutable logically
type Time struct {
    sec  int64
    nsec int32
}

func (t Time) Add(d Duration) Time {
    return Time{sec: t.sec + int64(d), nsec: t.nsec}
}

// Pointer semantics: type represents a resource or is large
type File struct {
    fd      int
    name    string
    // ...
}

func (f *File) Read(b []byte) (int, error) {
    // Modifies state, represents resource
}

// RULE: Pick one semantic and be consistent for a type
// If any method needs pointer, use pointer for all methods
```

### Understanding Escape Analysis

```go
// Stack allocation: fast, automatic cleanup
func sumLocal() int {
    numbers := [4]int{1, 2, 3, 4}  // Array on stack
    sum := 0
    for _, n := range numbers {
        sum += n
    }
    return sum  // numbers never escapes
}

// Heap allocation: slower, needs GC
func sumHeap() *int {
    sum := 0
    for i := 0; i < 4; i++ {
        sum += i
    }
    return &sum  // sum escapes to heap!
}

// Check with: go build -gcflags="-m"
// ./main.go:10:2: moved to heap: sum

// Slices and interfaces often cause escapes
func process(data []byte) {
    // If data is used after function returns
    // or passed to interface{}, it may escape
}
```

### Memory Layout Awareness

```go
// Struct padding wastes memory
// BAD: Poor layout (24 bytes with padding)
type BadLayout struct {
    a bool    // 1 byte + 7 padding
    b int64   // 8 bytes
    c bool    // 1 byte + 7 padding
}

// GOOD: Optimized layout (16 bytes)
type GoodLayout struct {
    b int64   // 8 bytes
    a bool    // 1 byte
    c bool    // 1 byte + 6 padding
}

// Check with: unsafe.Sizeof()
// Or use: go vet -fieldalignment
```

### Slice Internals

```go
// Slice header: (pointer, length, capacity)
// Understanding this prevents bugs

func modify(s []int) {
    s[0] = 999       // Modifies original!
    s = append(s, 4) // May or may not affect original
}

func main() {
    original := []int{1, 2, 3}
    modify(original)
    // original[0] is 999
    // but append may have created new backing array
}

// Safe pattern: return the slice
func appendSafe(s []int, v int) []int {
    return append(s, v)
}

original = appendSafe(original, 4)
```

### Benchmarking Properly

```go
func BenchmarkProcess(b *testing.B) {
    // Setup outside the loop
    data := generateTestData()
    
    b.ResetTimer()  // Don't count setup time
    
    for i := 0; i < b.N; i++ {
        result := Process(data)
        // Prevent compiler from optimizing away
        _ = result
    }
}

// Compare implementations
func BenchmarkProcessV1(b *testing.B) { ... }
func BenchmarkProcessV2(b *testing.B) { ... }

// Run with: go test -bench=. -benchmem
// BenchmarkProcessV1-8    1000000    1234 ns/op    256 B/op    3 allocs/op
// BenchmarkProcessV2-8    2000000     567 ns/op      0 B/op    0 allocs/op
```

### Goroutine Pool Pattern

```go
type Pool struct {
    work chan func()
    sem  chan struct{}
}

func NewPool(size int) *Pool {
    p := &Pool{
        work: make(chan func()),
        sem:  make(chan struct{}, size),
    }
    return p
}

func (p *Pool) Submit(task func()) {
    select {
    case p.work <- task:
        // Worker picked it up
    case p.sem <- struct{}{}:
        // Start new worker
        go p.worker(task)
    }
}

func (p *Pool) worker(task func()) {
    defer func() { <-p.sem }()
    
    for {
        task()
        task = <-p.work
    }
}
```

## Mental Model

Kennedy teaches by asking:

1. **What's the data?** Understand it before writing code.
2. **Where does it live?** Stack? Heap? How is it laid out?
3. **How does it flow?** What transformations happen?
4. **What's the cost?** Allocations, copies, cache misses?

## Kennedy's Priorities

1. **Integrity**: Code must be correct
2. **Readability**: Code must be maintainable
3. **Simplicity**: Don't over-engineer
4. **Performance**: After the above are satisfied

*In that order.*

