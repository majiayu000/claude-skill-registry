---
name: rust-guide
description: |
  Rust guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Rust files (.rs), Cargo.toml, or when the user mentions Rust.
  Provides ownership conventions, error handling with Result/Option, testing standards,
  and unsafe code guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: rust
  extensions: ".rs"
---

# Rust Guide

> Applies to: Rust 2021 edition+, Systems Programming, CLIs, WebAssembly, APIs

## Core Principles

1. **Ownership Clarity**: Every value has one owner; borrowing is explicit and intentional
2. **Result Over Panic**: Return `Result<T, E>` for all fallible operations; `panic!` is a bug
3. **Zero-Cost Abstractions**: Use iterators, generics, and traits without runtime overhead
4. **Minimal Unsafe**: Default to `#[forbid(unsafe_code)]`; justify every `unsafe` block in writing
5. **Clippy Compliance**: All code passes `cargo clippy -- -D warnings` with zero exceptions

## Guardrails

### Edition & Toolchain

- Use Rust 2021 edition (`edition = "2021"` in Cargo.toml)
- Set `rust-version` (MSRV) in Cargo.toml for all published crates
- Use stable toolchain unless a nightly feature is explicitly justified
- Pin dependency versions with `~` for compatible updates in libraries
- Commit `Cargo.lock` for binaries; omit for libraries
- Run `cargo update` weekly for security patches

### Code Style

- Run `cargo fmt` before every commit (no exceptions)
- Run `cargo clippy -- -D warnings` before every commit
- Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- `snake_case` for functions, variables, modules, crate names
- `PascalCase` for types, traits, enums, type parameters
- `SCREAMING_SNAKE_CASE` for constants and statics
- Prefer exhaustive `match` over `if let` chains
- No `use super::*` in non-test modules (explicit imports only)
- Derive order: `Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize`

### Error Handling

- Return `Result<T, E>` for all operations that can fail
- Use `thiserror` for library error types, `anyhow` for application code
- Never use `String` as an error type (create enums or use `thiserror`)
- Use `?` operator for propagation; avoid manual `match` on `Result` when `?` suffices
- `unwrap()` is forbidden outside tests and examples
- `expect("reason")` is allowed only with a comment explaining the invariant
- Use `#[must_use]` on functions returning `Result` or important values

### Lifetimes

- Let the compiler infer lifetimes whenever possible (elision rules)
- Add explicit annotations only when the compiler requires them
- Prefer owned types in structs; use references only when zero-copy is measured to matter
- Use `Cow<'a, str>` when a function may or may not allocate
- Avoid `'static` bounds unless truly needed (e.g., thread spawning, lazy statics)

### Concurrency

- Use `tokio` as the async runtime (unless project requires `async-std`)
- All async operations must have timeouts via `tokio::time::timeout`
- Use `Arc<T>` for shared ownership across threads; never `Rc<T>` in async code
- Prefer `tokio::sync::Mutex` over `std::sync::Mutex` in async contexts
- Use channels (`mpsc`, `oneshot`, `broadcast`) over shared mutable state
- Spawn tasks with `tokio::spawn`; propagate errors via `JoinHandle`
- Every `select!` branch must handle cancellation

## Project Structure

### Binary Crate

```
myproject/
├── Cargo.toml
├── Cargo.lock
├── src/
│   ├── main.rs              # Entry point, minimal (parse args, call run)
│   ├── lib.rs               # Public API and module declarations
│   ├── config.rs            # Configuration loading
│   ├── error.rs             # Custom error types
│   ├── domain/
│   │   ├── mod.rs
│   │   └── user.rs
│   └── infra/
│       ├── mod.rs
│       ├── db.rs
│       └── http.rs
├── tests/                   # Integration tests
│   └── api_test.rs
├── benches/                 # Benchmarks (criterion)
│   └── throughput.rs
└── examples/
    └── basic_usage.rs
```

### Cargo Workspace

```
workspace/
├── Cargo.toml               # [workspace] members
├── crates/
│   ├── core/                # Domain logic (no I/O)
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── api/                 # HTTP layer
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   └── cli/                 # Binary entry point
│       ├── Cargo.toml
│       └── src/main.rs
└── tests/                   # Workspace-level integration tests
```

- `main.rs` should be thin: parse CLI args, build config, call `lib.rs` entry
- Put all business logic in `lib.rs` modules (testable without binary)
- Use workspaces for projects with 3+ crates
- `error.rs` at crate root defines the crate-level error enum
- No global mutable state; use dependency injection via function arguments or structs

## Error Handling Patterns

### Library Errors (thiserror)

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum StorageError {
    #[error("record {id} not found in {table}")]
    NotFound { table: &'static str, id: String },

    #[error("duplicate key: {0}")]
    Conflict(String),

    #[error(transparent)]
    Database(#[from] sqlx::Error),

    #[error(transparent)]
    Io(#[from] std::io::Error),
}
```

### Application Errors (anyhow)

```rust
use anyhow::{bail, Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let raw = std::fs::read_to_string(path)
        .with_context(|| format!("reading config from {path}"))?;

    let config: Config = toml::from_str(&raw)
        .context("parsing TOML config")?;

    if config.port == 0 {
        bail!("port must be non-zero");
    }

    Ok(config)
}
```

### Conversion With the ? Operator

```rust
// Define From impls via thiserror's #[from], then just use ?
fn create_user(db: &Pool, input: &NewUser) -> Result<User, AppError> {
    validate_email(&input.email)?;   // ValidationError -> AppError
    let user = db.insert(input)?;    // sqlx::Error -> AppError
    Ok(user)
}
```

## Testing

### Unit Tests (in-module)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_email_succeeds() {
        let result = Email::parse("user@example.com");
        assert!(result.is_ok());
    }

    #[test]
    fn parse_invalid_email_returns_error() {
        let err = Email::parse("not-an-email").unwrap_err();
        assert!(matches!(err, ValidationError::InvalidEmail(_)));
    }

    #[test]
    fn amount_cannot_be_negative() -> Result<(), Box<dyn std::error::Error>> {
        let result = Amount::new(-5);
        assert!(result.is_err());
        Ok(())
    }
}
```

### Integration Tests (tests/ directory)

```rust
// tests/api_test.rs
use myproject::app;

#[tokio::test]
async fn health_endpoint_returns_ok() {
    let app = app::build_test_app().await;
    let resp = app.get("/health").await;
    assert_eq!(resp.status(), 200);
}
```

### Doc Tests

```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// use mycrate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### Property-Based Testing (proptest)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn roundtrip_serialization(input in "[a-zA-Z0-9]{1,100}") {
        let encoded = encode(&input);
        let decoded = decode(&encoded)?;
        prop_assert_eq!(input, decoded);
    }
}
```

### Testing Standards

- Test names describe behavior: `fn rejected_order_cannot_be_shipped()`
- Unit tests live in `#[cfg(test)] mod tests` in the same file
- Integration tests go in `tests/` directory
- Use `#[should_panic(expected = "...")]` for panic-testing (rare)
- Use `assert!(matches!(...))` for enum variant assertions
- Coverage target: >80% for libraries, >60% for applications
- Use `cargo tarpaulin` or `cargo llvm-cov` for coverage
- Async tests use `#[tokio::test]`

## Tooling

### Essential Commands

```bash
cargo fmt                       # Format (non-negotiable)
cargo clippy -- -D warnings     # Lint with deny
cargo test                      # All tests
cargo test --all-features       # Test all feature combinations
cargo check                     # Fast type-check (no codegen)
cargo doc --open                # Generate and view docs
cargo audit                     # Check for vulnerable deps
cargo deny check                # License + advisory check
cargo bench                     # Run benchmarks (criterion)
```

### Cargo.toml Essentials

```toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"

[dependencies]
serde = { version = "1", features = ["derive"] }
thiserror = "2"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
tracing = "0.1"

[dev-dependencies]
proptest = "1"
tokio = { version = "1", features = ["test-util"] }

[profile.release]
lto = true
codegen-units = 1
strip = true

[lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "deny"
expect_used = "warn"
```

### Rustfmt Configuration

```toml
# rustfmt.toml
edition = "2021"
max_width = 100
use_field_init_shorthand = true
```

### MSRV Policy

- Set `rust-version` in Cargo.toml for every published crate
- Test MSRV in CI: `cargo +1.75.0 check`
- Bump MSRV only when a dependency or language feature requires it
- Document MSRV bumps in changelog

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Async server, builder, newtype, state machine patterns
- [references/pitfalls.md](references/pitfalls.md) -- Common ownership mistakes, lifetime traps, async gotchas
- [references/security.md](references/security.md) -- Unsafe auditing, dependency vetting, secret handling

## External References

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [The Async Book](https://rust-lang.github.io/async-book/)
- [Rustonomicon (Unsafe Rust)](https://doc.rust-lang.org/nomicon/)
- [Clippy Lint Reference](https://rust-lang.github.io/rust-clippy/)
- [Error Handling in Rust (blog)](https://blog.burntsushi.net/rust-error-handling/)
- [cargo-deny](https://embarkstudios.github.io/cargo-deny/)
