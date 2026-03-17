---
name: cargo
description: Rust package manager (36 subcommands).
metadata:
  trit: 0
---

# cargo

Rust package manager (36 subcommands).

## Build

```bash
cargo build --release
cargo check
cargo test
cargo run
cargo bench
```

## Package

```bash
cargo new myproject
cargo init
cargo add serde
cargo remove tokio
```

## Dependencies

```bash
cargo tree
cargo update
cargo fetch
```

## Publish

```bash
cargo publish
cargo search regex
cargo install ripgrep
```

## Workspace

```toml
# Cargo.toml
[workspace]
members = ["crates/*"]

[dependencies]
serde = { version = "1.0", features = ["derive"] }
```

## Fix

```bash
cargo fix --edition
cargo clippy --fix
cargo fmt
```
