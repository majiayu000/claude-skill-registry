---
name: cargo-ecosystem
description: Master Cargo, testing, and Rust development tools
sasmp_version: "1.3.0"
bonded_agent: rust-tooling-agent
bond_type: PRIMARY_BOND
version: "1.0.0"
---

# Cargo & Ecosystem Skill

Master Rust's build system, package manager, and development tools.

## Quick Start

### Essential Commands

```bash
# Project management
cargo new my_project          # Create binary project
cargo new my_lib --lib        # Create library project
cargo init                    # Initialize in existing dir

# Build & Run
cargo build                   # Debug build
cargo build --release         # Optimized build
cargo run                     # Build and run
cargo run --release           # Optimized run

# Testing
cargo test                    # Run all tests
cargo test test_name          # Run specific test
cargo test -- --nocapture     # Show output

# Quality
cargo fmt                     # Format code
cargo clippy                  # Lint code
cargo doc --open              # Generate docs
```

### Cargo.toml Configuration

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
authors = ["You <you@example.com>"]
description = "A sample application"
license = "MIT"
repository = "https://github.com/you/my-app"

[dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "1.0"

[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
proptest = "1.0"

[profile.release]
lto = true
codegen-units = 1
opt-level = 3

[[bin]]
name = "my-app"
path = "src/main.rs"

[[bench]]
name = "my_benchmark"
harness = false
```

## Testing

### Unit Tests

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn test_panic() {
        // Expected to panic
    }

    #[test]
    #[ignore]
    fn slow_test() {
        // Run with: cargo test -- --ignored
    }
}
```

### Integration Tests

```rust
// tests/integration_test.rs
use my_crate::public_function;

#[test]
fn test_public_api() {
    assert!(public_function().is_ok());
}
```

### Benchmarks

```rust
// benches/my_benchmark.rs
use criterion::{criterion_group, criterion_main, Criterion};

fn benchmark(c: &mut Criterion) {
    c.bench_function("my_function", |b| {
        b.iter(|| my_function())
    });
}

criterion_group!(benches, benchmark);
criterion_main!(benches);
```

## Development Tools

### Code Quality

```bash
# Install components
rustup component add rustfmt clippy

# Format
cargo fmt
cargo fmt -- --check  # CI check

# Lint
cargo clippy
cargo clippy -- -D warnings  # Strict mode
cargo clippy --fix           # Auto-fix
```

### Recommended Tools

```bash
# Install useful tools
cargo install cargo-watch     # Auto-rebuild
cargo install cargo-edit      # cargo add/rm
cargo install cargo-nextest   # Fast parallel tests
cargo install cargo-audit     # Security check
cargo install cargo-bloat     # Binary size analysis
```

### rustfmt.toml

```toml
edition = "2021"
max_width = 100
use_small_heuristics = "Max"
tab_spaces = 4
```

### .cargo/config.toml

```toml
[alias]
t = "test"
c = "clippy"
b = "build --release"

[build]
rustflags = ["-D", "warnings"]
```

## Workspaces

```toml
# Root Cargo.toml
[workspace]
members = [
    "core",
    "cli",
    "server",
]

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

## Resources

- [Cargo Book](https://doc.rust-lang.org/cargo/)
- [Rustfmt Config](https://rust-lang.github.io/rustfmt/)
- [Clippy Lints](https://rust-lang.github.io/rust-clippy/)
