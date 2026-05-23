---
name: esbuild
description: esbuild extremely fast bundler. Use for fast builds.
---

# esbuild

esbuild changed the industry by proving that build tools could be 100x faster if written in Go/Rust. It is not just a bundler but a transpiler.

## When to Use

- **Pre-bundling**: Used by Vite to bundle dependencies.
- **Lambda Bundling**: Creating small, single-file bundles for AWS Lambda.
- **Speed**: When Webpack takes 5 mins, esbuild takes 200ms.

## Core Concepts

### Go

Written in Go, compiled to native code. No JS overhead.

### API

Simple, minimal API. `esbuild.build({ ... })`.

### Plugins

Allows intercepting imports, but limited compared to Rollup/Webpack (by design).

## Best Practices (2025)

**Do**:

- **Use for TS Transpilation**: It strips types instantly.
- **Target `esnext`**: Let it output modern code for modern browsers.

**Don't**:

- **Don't expect Type Checking**: esbuild strips types; it does not check them. Run `tsc --noEmit` separately.

## References

- [esbuild Documentation](https://esbuild.github.io/)
