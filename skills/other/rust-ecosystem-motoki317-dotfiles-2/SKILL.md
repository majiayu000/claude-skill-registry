---
name: Rust Ecosystem
description: This skill should be used when working with Rust projects, "Cargo.toml", "rustc", "cargo build/test/run", "clippy", "rustfmt", or Rust language patterns. Provides comprehensive Rust ecosystem patterns and best practices.
---

# Rust Ecosystem

## Core Concepts

- **Ownership**: Each value has one owner; when owner goes out of scope, value is dropped
- **Borrowing**: `&T` allows multiple immutable borrows; `&mut T` allows exactly one; cannot mix
- **Result/Option**: `Result<T, E>` for recoverable errors, `Option<T>` for optional values; use `?` for propagation
- **Traits**: Define behavior with traits; use `derive` for common implementations

## Borrowing Rules

- `&T` - multiple simultaneous immutable borrows allowed
- `&mut T` - exactly one mutable borrow allowed
- Cannot have `&mut T` while `&T` exists

## Error Handling

```rust
// Custom error with thiserror
#[derive(Debug, thiserror::Error)]
enum MyError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Parse error: {msg}")]
    Parse { msg: String },
}

// Propagate with ?
fn read_config() -> Result<Config, MyError> {
    let content = std::fs::read_to_string("config.toml")?;
    Ok(parse(content)?)
}
```

## Common Traits

- `Clone` - explicit `.clone()`; `Copy` - implicit bitwise copy
- `Debug` - `{:?}` formatting; `Display` - `{}` formatting
- `Default` - default value construction
- `PartialEq/Eq`, `PartialOrd/Ord` - comparison
- `From/Into` - type conversions
- `Hash` - for HashMap/HashSet keys

## Project Structure

```
Cargo.toml
src/
  lib.rs        # Library crate root
  main.rs       # Binary crate root
  bin/          # Additional binaries
tests/          # Integration tests
benches/        # Benchmarks
examples/       # Example code
```

## Cargo.toml

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.83"

[dependencies]
serde = { version = "1.0", features = ["derive"] }

[lints.clippy]
pedantic = "warn"
unwrap_used = "deny"

[profile.release]
lto = true
codegen-units = 1
strip = true
```

## Workspace

```toml
[workspace]
resolver = "2"
members = ["crate-a", "crate-b"]

[workspace.dependencies]
serde = "1.0"
tokio = { version = "1", features = ["full"] }
```

Member crates inherit with `serde.workspace = true`.

## Anti-Patterns

- **unwrap() in library code**: Use `?` or proper error handling
- **Clone abuse**: Prefer borrowing when possible
- **String for everything**: Use enums, newtypes for domain modeling
- **Arc<Mutex<T>> overuse**: Consider channels or ownership patterns first

## Tools

- `cargo check` - Fast syntax/type check
- `cargo clippy -- -D warnings` - Linter
- `cargo fmt` - Formatter
- `cargo nextest run` - Better test runner
- `cargo audit` - Security vulnerability scanning
- `cargo tree` - Dependency tree

## rustfmt.toml

```toml
edition = "2021"
max_width = 100
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

## Context7 Reference

- Rust Book: `/rust-lang/book`
- Cargo: `/rust-lang/cargo.git`
- Clippy: `/rust-lang/rust-clippy`
