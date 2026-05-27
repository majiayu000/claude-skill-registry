---
name: build-compile
description: Build Rust code with proper error handling and optimization for development, testing, and production. Use when compiling the self-learning memory project or troubleshooting build errors.
---

# Build and Compile

Build Rust code with proper error handling and optimization.

## Build Commands

| Build Type | Command | Purpose |
|------------|---------|---------|
| Development | `cargo build` | Fast compile, debug symbols |
| Release | `cargo build --release` | Optimized for production |
| Check | `cargo check` | Fast type check only |

## Build Profiles

```toml
[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
lto = "fat"
codegen-units = 1
strip = true
```

## Common Errors

### Type Errors
```
error[E0308]: mismatched types
```
**Fix**: Ensure return types match

### Lifetime Errors
```
error[E0597]: value does not live long enough
```
**Fix**: Clone data or return owned type

### Trait Bound Errors
```
error[E0277]: trait bound `X: Send` not satisfied
```
**Fix**: Use Send-safe types (Arc<Mutex<T>>)

### Async Errors
```
error: await only allowed in async functions
```
**Fix**: Make function async

## Speed Up Builds

```bash
# Incremental
export CARGO_INCREMENTAL=1

# Clean rebuild
cargo clean && cargo build --all

# Parallel jobs
cargo build -j 8
```

## Optimization Tips

- LTO: `lto = "fat"` in release
- Codegen units: `codegen-units = 1`
- Profile: `cargo build --timings`
