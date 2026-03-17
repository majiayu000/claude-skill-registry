---
name: swc
description: SWC Rust-based JS/TS compiler. Use for fast compilation.
---

# SWC

SWC (Speedy Web Compiler) is a Rust-based extensible platform. It is the compiler inside **Next.js** and **Deno**.

## When to Use

- **Compilation**: Replacing Babel.
- **Minification**: Faster and often smaller than Terser.
- **Jest**: `@swc/jest` speeds up tests by 10x.

## Core Concepts

### Transforms

Supports standard transforms (React JSX, TypeScript, legacy decorators).

### Plugins (Wasm)

SWC plugins are written in Rust (Wasm), making them fast but harder to write than Babel plugins.

## Best Practices (2025)

**Do**:

- **Use `swc-loader`**: In Webpack configs.
- **Use `.swcrc`**: JSON configuration file (similar to `.babelrc`).

**Don't**:

- **Don't stick with Babel**: Unless you need a very niche Babel plugin that doesn't exist in SWC yet.

## References

- [SWC Documentation](https://swc.rs/)
