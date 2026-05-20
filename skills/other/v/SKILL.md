---
name: v
description: V simple systems programming language. Use for .v files.
---

# V (Vlang)

V (2024 updates) focuses on **compilation speed** (1 million LOC/s) and safety (Autofree). It aims to be a modern C replacement with Go-like simplicity.

## When to Use

- **Fast Compilation**: Iteration speed of an interpreted language.
- **Graphics**: `v ui` module provides a cross-platform UI toolkit.
- **No Dependencies**: V is a single binary executable.

## Core Concepts

### Autofree

Compiler inserts `free()` calls automatically (experimental/improving).

### C Interop

`C.printf()`. Direct calling of C functions.

### Option/Result

`fn foo() ?int`. Error handling with `or { ... }`.

## Best Practices (2025)

**Do**:

- **Use `v fmt`**: Built-in formatter.
- **Use `v install`**: Built-in package manager.
- **Cross-compile**: V makes outputting C for other platforms easy.

**Don't**:

- **Don't use globals**: V discourages mutable global state.

## References

- [V Lang](https://vlang.io/)
