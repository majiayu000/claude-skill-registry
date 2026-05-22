---
name: cpp-pro
description: C++20 specialist with expertise in modern C++ features, performance optimization, and system programming
---

# C++ Professional

## Purpose

Provides expert C++20 programming capabilities specializing in modern C++ features (concepts, modules, ranges, coroutines), performance optimization, and system-level programming. Excels at building high-performance applications, embedded systems, game engines, and low-level system software with memory safety and optimal resource utilization.

## When to Use

- Building high-performance applications requiring C++ speed (game engines, simulations)
- Implementing system-level software (device drivers, operating systems, embedded systems)
- Optimizing performance-critical code (SIMD, cache optimization, lock-free programming)
- Migrating legacy C++ codebases to modern C++20 standards
- Building cross-platform C++ libraries and SDKs
- Implementing template metaprogramming and compile-time optimizations
- Working with modern C++20 features (concepts, modules, ranges, coroutines)

## Quick Start

**Invoke this skill when:**
- Building high-performance C++ applications (games, simulations, trading)
- System-level programming (device drivers, embedded systems, OS)
- Performance optimization (SIMD, cache, lock-free)
- Modern C++20 features (concepts, modules, ranges, coroutines)
- Template metaprogramming and compile-time computation
- Cross-platform library development

**Do NOT invoke when:**
- Web development → Use frontend-developer or backend-developer
- Scripting tasks → Use python-pro or javascript-pro
- Simple utilities without performance needs → Use appropriate language
- Mobile development → Use swift-expert or kotlin-specialist

## Core Capabilities

### C++20 Modern Features
- **Concepts**: Type constraints and template requirements
- **Modules**: Replacing header files with importable modules
- **Ranges**: Lazy evaluation algorithms and views
- **Coroutines**: Asynchronous programming with co_await
- **Spaceship Operator**: Three-way comparison <=> 
- **Designated Initializers**: Struct member initialization by name
- **std::format**: Type-safe string formatting
- **std::span**: Safe array views without ownership
- **std::jthread**: Thread with automatic join capability

### Performance Optimization
- **Template Metaprogramming**: Compile-time computation
- **SIMD Programming**: Vector instructions for parallel processing
- **Memory Management**: Smart pointers, allocators, memory pools
- **Cache-Aware Algorithms**: Data-oriented design patterns
- **Lock-Free Programming**: Atomic operations and memory ordering
- **Compiler Optimizations**: Profile-guided optimization, link-time optimization

### System Programming
- **Low-Level I/O**: File descriptors, sockets, epoll/kqueue
- **Memory Mapping**: Shared memory, memory-mapped files
- **Process Management**: Fork, exec, signal handling
- **System Calls**: POSIX/Linux system interface
- **Embedded Systems**: Bare-metal programming, real-time constraints

## Decision Framework

### C++ Feature Selection

```
C++20 Feature Decision
├─ Type constraints needed
│   └─ Use concepts instead of SFINAE
│       • Clearer error messages
│       • More readable templates
│
├─ Header file management
│   └─ Use modules for new projects
│       • Faster compilation
│       • Better encapsulation
│
├─ Data transformations
│   └─ Use ranges for lazy evaluation
│       • Composable algorithms
│       • Memory efficient
│
├─ Async operations
│   └─ Use coroutines for I/O-bound work
│       • Efficient state machines
│       • Readable async code
│
└─ Error handling
    ├─ Recoverable errors → std::expected
    ├─ Exceptional cases → exceptions
    └─ Low-level code → return codes
```

### Performance Optimization Matrix

| Bottleneck | Solution | Complexity |
|------------|----------|------------|
| CPU-bound computation | SIMD, parallelism | High |
| Memory allocation | Memory pools, allocators | Medium |
| Cache misses | Data-oriented design | High |
| Lock contention | Lock-free structures | Very High |
| Compilation time | Modules, precompiled headers | Low |

## Best Practices

### Modern C++ Development
- **Prefer Composition to Inheritance**: Use value semantics and composition
- **const Correctness**: Mark member functions const when possible
- **noexcept When Appropriate**: Mark functions that won't throw
- **Explicit is Better**: Use explicit constructors and conversion operators
- **RAII Everywhere**: Wrap all resources in RAII objects

### Performance Optimization
- **Profile Before Optimizing**: Use perf, VTune, or Tracy
- **Rule of Zero**: Define destructors, copy, and move only if needed
- **Move Semantics**: Return by value, rely on move semantics
- **Inline Judiciously**: Let compiler decide; focus on cache-friendly data
- **Measure Cache Efficiency**: Cache misses are often more expensive

### Template Metaprogramming
- **Concepts Over SFINAE**: Use concepts for clearer template constraints
- **constexpr When Possible**: Move computation to compile time
- **Type Traits**: Use std::type_traits for compile-time introspection
- **Variadic Templates**: Use parameter packs for flexible functions

### Concurrency and Parallelism
- **Avoid Premature Locking**: Consider lock-free for high-contention
- **Understand Memory Ordering**: Use std::memory_order explicitly
- **Future/Promise Patterns**: Use std::future for async results
- **Coroutines for I/O**: Use C++20 coroutines for async I/O
- **Thread Pools**: Prefer pools over spawning threads

### System-Level Programming
- **Zero-Cost Abstractions**: High-level code that compiles efficiently
- **Handle Errors Explicitly**: Use std::expected without exceptions
- **Resource Management**: Apply RAII consistently
- **Platform Abstraction**: Isolate platform-specific code
- **Testing Strategy**: Use unit tests, fuzzing, property-based testing

## Anti-Patterns

### Memory Management
- **Raw new/delete**: Use smart pointers instead
- **Manual Resource Management**: Apply RAII
- **Dangling Pointers**: Use ownership semantics

### Performance
- **Premature Optimization**: Profile first
- **Virtual Call Overhead**: Use CRTP when performance critical
- **Unnecessary Copies**: Use move semantics and references

### Code Organization
- **Header-Only Everything**: Use modules or proper compilation units
- **Macro Abuse**: Use constexpr, templates, inline functions
- **Global State**: Use dependency injection

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
