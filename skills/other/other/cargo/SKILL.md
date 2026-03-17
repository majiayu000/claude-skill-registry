---
name: cargo
description: Cargo Rust package manager and build system. Use for Rust crates.
---

# Cargo

Cargo is Rust's build system and package manager. It is famous for its reliability and developer experience.

## When to Use

- **Rust Projects**: Mandatory.
- **Formatting/Linting**: `cargo fmt`, `cargo clippy`.
- **Testing**: `cargo test` is built-in.

## Quick Start

```bash
cargo new my-project
cd my-project
cargo run
```

```toml
# Cargo.toml
[dependencies]
serde = "1.0"
```

## Core Concepts

### Crates

Packages. Published to crates.io.

### Cargo.lock

Ensures reproducible builds. Always commit for binaries, ignore for libraries.

### Workspaces

Manage multiple packages in one repo. `[workspace]` in root `Cargo.toml`.

## Best Practices (2025)

**Do**:

- **Use `cargo check`**: Faster than `build` for checking syntax during dev.
- **Use `clippy`**: Listen to the linter. It teaches you Rust.
- **Use `cargo-deny`**: Scan dependency tree for licenses and bans.

**Don't**:

- **Don't bloat**: Rust binaries can get huge. Use `cargo-bloat` to analyze size.

## References

- [The Cargo Book](https://doc.rust-lang.org/cargo/)
