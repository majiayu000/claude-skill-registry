---
name: stroustrup-cpp-style
description: Write C++ code in the style of Bjarne Stroustrup, creator of C++. Emphasizes type safety, resource management via RAII, zero-overhead abstractions, and direct hardware mapping. Use when designing C++ systems, APIs, or when clarity and efficiency must coexist.
---

# Bjarne Stroustrup Style Guide

## Overview

Bjarne Stroustrup created C++ in 1979 at Bell Labs, evolving it from "C with Classes" into the multi-paradigm language used in systems from browsers to databases to operating systems. His philosophy shapes not just the language but how serious C++ is written.

## Core Philosophy

> "C++ is designed to allow you to express ideas directly in code. If you can think of it, you should be able to express it in C++."

> "Leave no room for a lower-level language below C++ (except assembler)."

> "What you don't use, you don't pay for. What you do use, you couldn't hand-code any better."

## Design Principles

1. **Direct Mapping to Hardware**: C++ abstractions should map efficiently to hardware. No hidden costs, no magic.

2. **Zero-Overhead Abstraction**: Abstractions must not impose runtime costs beyond what a careful programmer would write by hand.

3. **Type Safety as Foundation**: The type system is your ally. Use it to catch errors at compile time, not runtime.

4. **Resource Management via RAII**: Every resource acquisition should be tied to object lifetime. No manual cleanup.

5. **Express Intent Clearly**: Code should say what it means. Prefer declarative over clever.

## When Writing Code

### Always

- Use RAII for all resource management (memory, files, locks, connections)
- Prefer compile-time checking to runtime checking
- Use the type system to make illegal states unrepresentable
- Initialize variables at point of declaration
- Prefer `const` by default—mutability should be the exception
- Use standard library algorithms over hand-written loops
- Design classes with clear invariants

### Never

- Use raw `new`/`delete` in application code (use smart pointers, containers)
- Leave resources unmanaged (no naked pointers to owned memory)
- Use C-style casts (use `static_cast`, `dynamic_cast`, etc.)
- Ignore compiler warnings—they're often errors waiting to happen
- Write "clever" code that sacrifices clarity for brevity
- Use macros where `constexpr`, templates, or `inline` suffice

### Prefer

- `std::unique_ptr` over `std::shared_ptr` unless sharing is truly needed
- `std::string_view` over `const std::string&` for read-only string parameters
- `std::span` over pointer+size pairs
- Structured bindings for multiple return values
- Range-based for loops over index-based iteration
- `constexpr` over runtime computation when possible
- Concepts over SFINAE for template constraints (C++20+)

## Code Patterns

### Resource Management (RAII)

```cpp
// BAD: Manual resource management
void process_file_bad(const char* filename) {
    FILE* f = fopen(filename, "r");
    if (!f) return;
    // ... what if exception thrown here?
    fclose(f);  // Easy to forget, impossible with exceptions
}

// GOOD: RAII via standard library
void process_file_good(const std::filesystem::path& filename) {
    std::ifstream file(filename);
    if (!file) return;
    // File automatically closed when 'file' goes out of scope
    // Exception-safe by construction
}
```

### Type-Safe Interfaces

```cpp
// BAD: Primitive obsession
void set_timeout(int milliseconds);
void set_timeout(int seconds);  // Which is it?

// GOOD: Strong types express intent
class Milliseconds {
    int value_;
public:
    explicit Milliseconds(int v) : value_(v) {}
    int count() const { return value_; }
};

void set_timeout(Milliseconds timeout);
// Usage: set_timeout(Milliseconds{500});  // Clear and type-safe
```

### Const Correctness

```cpp
class Buffer {
    std::vector<std::byte> data_;
public:
    // Const method: promises not to modify state
    std::span<const std::byte> view() const { return data_; }
    
    // Non-const: may modify
    std::span<std::byte> data() { return data_; }
    
    // Return by value for computed results (enables move semantics)
    std::vector<std::byte> compressed() const;
};
```

## Mental Model

Stroustrup thinks of C++ as a tool for **direct expression of ideas** with **predictable performance**. When writing code:

1. **Model the domain**: What are the key abstractions? What invariants must hold?
2. **Leverage the type system**: Make incorrect usage a compile error
3. **Consider resource lifetime**: Who owns what? When is it released?
4. **Measure, don't assume**: Profile before optimizing

## Evolution

Stroustrup's thinking has evolved with the language:
- **C++11**: "Modern C++" begins—move semantics, smart pointers, lambdas
- **C++17**: Structured bindings, `std::optional`, `std::variant`
- **C++20**: Concepts finally arrive, coroutines, ranges
- **C++23+**: Continued refinement toward safety and expressiveness

## Additional Resources

- For detailed philosophy, see [philosophy.md](philosophy.md)
- For references (books, talks), see [references.md](references.md)
