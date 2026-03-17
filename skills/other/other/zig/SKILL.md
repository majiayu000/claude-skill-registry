---
name: zig
description: Zig systems programming with manual memory and no hidden control flow. Use for .zig files.
---

# Zig

Zig is a modern system language competing with C/Rust. v0.13 (2025) stabilizes the stdlib and build system. It is famous for its **C toolchain** capabilities (`zig cc`).

## When to Use

- **Systems Programming**: OS kernels, game engines, embedded.
- **Cross-Compilation**: The best cross-compiler toolchain in existence.
- **Drop-in C Replacement**: Can compile .c files directly.

## Core Concepts

### Comptime

Run code at compile time. `comptime { ... }`.

### Allocators

Memory management is explicit. You pass an `Allocator` to functions.

### Defer

`defer allocator.free(bytes)` ensures cleanup.

## Best Practices (2025)

**Do**:

- **Use `zig cc`**: To compile C/C++ projects easier than Make/CMake.
- **Handle Errors**: Zig uses error unions `!T`.
- **Use `GeneralPurposeAllocator`**: Included debug features for leaks.

**Don't**:

- **Don't expect stability**: Only use if you can tolerate breaking changes until v1.0.

## References

- [Zig Documentation](https://ziglang.org/)
