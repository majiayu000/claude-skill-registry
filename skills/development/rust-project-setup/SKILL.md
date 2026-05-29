---
name: rust-project-setup
description: >
  Guidance for scaffolding new Rust projects. Use when:
  (1) starting a new Rust project or workspace,
  (2) configuring Cargo.toml best practices,
  (3) setting up CI pipelines for Rust,
  (4) organizing a multi-crate workspace,
  (5) configuring clippy, rustfmt, and linting.
---

# Rust Project Setup

Step-by-step guidance for setting up new Rust projects with proper configuration, linting, and CI.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Cargo.toml configuration, profiles, dependencies | [references/cargo-config.md](references/cargo-config.md) |
| Workspace organization, member layout, shared deps | [references/workspace-layout.md](references/workspace-layout.md) |
| GitHub Actions CI, caching, MSRV checks | [references/ci-setup.md](references/ci-setup.md) |
| Feature flags, conditional compilation, build scripts | [references/features-conditional.md](references/features-conditional.md) |
| no_std development, embedded targets, cross-compilation | [references/no-std.md](references/no-std.md) |

## New Project Checklist

### 1. Create the Project

```shell
# Binary
cargo init my-app

# Library
cargo init --lib my-lib

# Workspace (create Cargo.toml manually)
mkdir my-workspace && cd my-workspace
```

### 2. Configure Cargo.toml

Set edition, rust-version (MSRV), and metadata:

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"
```

### 3. Set Up Linting

Add clippy and rustfmt configuration:

```toml
# Cargo.toml
[lints.clippy]
all = { level = "deny", priority = 10 }
pedantic = { level = "warn", priority = 3 }

[lints.rust]
future-incompatible = "warn"
nonstandard_style = "deny"
# unsafe_op_in_unsafe_fn is deny-by-default in edition 2024 — no need to set it
```

> **Edition 2024 lint defaults**: `unsafe_op_in_unsafe_fn` is deny by default. Unsafe operations inside `unsafe fn` require explicit `unsafe {}` blocks. The `gen` keyword is reserved — use `r#gen` if needed as an identifier.

```toml
# rustfmt.toml
edition = "2024"
reorder_imports = true
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

### 4. Configure Profiles

```toml
[profile.release]
lto = true
codegen-units = 1
strip = true
```

### 5. Set Up CI

Add GitHub Actions workflow for check, clippy, test, and fmt. See [references/ci-setup.md](references/ci-setup.md).

### 6. Cargo.lock Policy

- **Binaries**: Commit `Cargo.lock` (reproducible builds)
- **Libraries**: Do NOT commit `Cargo.lock` (consumers resolve their own versions)
- Add to `.gitignore` for libraries: `Cargo.lock`

### 7. Documentation Setup

For library crates, enable doc lints:

```rust
// src/lib.rs
#![deny(missing_docs)]
```

Prefer `#[expect(lint)]` over `#[allow(lint)]` for temporary suppressions — it warns when the suppression becomes unnecessary:

```rust
#[expect(dead_code, reason = "used in next PR")]
fn upcoming_feature() {}
```

## Workspace vs Single Crate

| Use | When |
|-----|------|
| Single crate | Small project, CLI tool, simple library |
| Workspace | Multiple related crates, shared dependencies, separate compile targets |

Workspaces reduce compile times by sharing dependencies and build artifacts across members.

## Project Structure

### Binary

```text
my-app/
  Cargo.toml
  rustfmt.toml
  src/
    main.rs
    lib.rs      # separate logic from entry point
  tests/
    integration_test.rs
```

### Library

```text
my-lib/
  Cargo.toml
  rustfmt.toml
  src/
    lib.rs
    module_a.rs
    module_b/
      mod.rs
      types.rs
  tests/
    api_test.rs
  examples/
    basic_usage.rs
```

### Workspace

```text
my-workspace/
  Cargo.toml          # [workspace] definition
  rustfmt.toml        # shared formatting
  crates/
    core/             # shared types and logic
    api/              # HTTP server
    cli/              # command-line interface
```

## Dependency Best Practices

- Pin exact versions for binaries: `serde = "=1.0.210"`
- Use version ranges for libraries: `serde = "1"`
- Group features explicitly: `tokio = { version = "1", features = ["rt-multi-thread", "macros"] }`
- Use `[dev-dependencies]` for test-only crates
- Review `cargo tree` for duplicate versions
- Run `cargo audit` for security vulnerabilities
- Replace `once_cell`/`lazy_static` with `std::sync::LazyLock` (stable since Rust 1.80)

## Edition 2024 Migration Notes

When migrating existing projects to edition 2024:

- `unsafe fn` bodies now require explicit `unsafe {}` blocks around unsafe operations
- `extern "C" {}` blocks must be written as `unsafe extern "C" {}`
- `#[no_mangle]` and `#[export_name]` require `#[unsafe(no_mangle)]` and `#[unsafe(export_name)]`
- `gen` is a reserved keyword — rename any `gen` identifiers to `r#gen` or choose a different name
- `-> impl Trait` captures all in-scope lifetimes by default; use `+ use<'a>` for precise control
- `!` (never type) falls back to `!` instead of `()` — review match arms and diverging expressions
- Temporaries in `if let` and tail expressions drop earlier — review code holding locks or guards in these positions

Run `cargo fix --edition` to auto-fix most mechanical changes.

## Setup completion gates

Use these as **objective pass conditions** after the checklist—not informal “looks done.”

1. **Manifest loads** — From the project or workspace root, run `cargo metadata --format-version 1`. **Pass:** exit code 0 and the output lists your crate(s) (package `name` matches what you expect).
2. **Lint and format** — Run `cargo clippy --all-targets` (add `-- -D warnings` if warnings must fail) and `cargo fmt --check`. **Pass:** both exit 0 before you treat CI as authoritative.
3. **CI present** — You committed the workflow you intend to run (see [references/ci-setup.md](references/ci-setup.md)). **Pass:** at least one pipeline run finishes green for check, clippy, tests, and fmt (or the subset you defined).
4. **Lockfile policy** — **Binary crate:** `Cargo.lock` is committed (`git ls-files Cargo.lock` prints `Cargo.lock`). **Library crate:** `Cargo.lock` is not tracked (empty `git ls-files Cargo.lock`, or file gitignored and never added). **Pass:** the index matches that policy with no surprise `Cargo.lock` changes.

## Related Skills

- `beagle-rust:rust-best-practices` — idiomatic patterns and edition 2024 coding guidance
- `beagle-rust:rust-code-review` — code review covering ownership, unsafe, and trait design
