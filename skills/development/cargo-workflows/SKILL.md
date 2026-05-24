---
name: cargo-workflows
description: >
  Manage Rust projects effectively with Cargo workspaces, features, and tooling.
  Use when the user sets up Cargo workspaces, configures feature flags, writes
  build.rs scripts, prepares crates for publishing, or uses cargo clippy, cargo
  fmt, and other Cargo development tools.
---

# Cargo Workflows

Manage Rust projects with Cargo workspaces, feature flags, build scripts,
and development tooling for productive, well-structured Rust development.

## When to Use
- Organizing a multi-crate Rust project
- Adding optional functionality with feature flags
- Running code generation or native compilation with build.rs
- Preparing a crate for crates.io publication
- Setting up CI-friendly lint and format checks

## Core Patterns

### Pattern 1: Cargo Workspaces

Organize related crates in a single repository with shared dependencies and a
unified build.

```toml
# Root Cargo.toml
[workspace]
resolver = "2"
members = [
    "crates/core",
    "crates/api",
    "crates/cli",
]

# Share dependency versions across workspace members
[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
tracing = "0.1"

# Shared package metadata
[workspace.package]
edition = "2021"
rust-version = "1.75"
license = "MIT"
repository = "https://github.com/user/project"
```

```toml
# crates/core/Cargo.toml
[package]
name = "myproject-core"
version = "0.1.0"
edition.workspace = true
license.workspace = true

[dependencies]
serde.workspace = true        # uses workspace version
anyhow.workspace = true
```

```
project/
  Cargo.toml                  # workspace root
  Cargo.lock                  # single lock file for reproducibility
  crates/
    core/
      Cargo.toml
      src/lib.rs
    api/
      Cargo.toml
      src/lib.rs
    cli/
      Cargo.toml
      src/main.rs
```

### Pattern 2: Feature Flags

Enable optional functionality without forcing dependencies on all users.

```toml
# Cargo.toml
[features]
default = ["json"]                   # enabled unless user opts out
json = ["dep:serde_json"]            # optional dependency
postgres = ["dep:sqlx", "sqlx/postgres"]
full = ["json", "postgres"]          # convenience feature combining others

[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = { version = "1", optional = true }
sqlx = { version = "0.7", optional = true, features = ["runtime-tokio"] }
```

```rust
// Conditional compilation based on features
pub fn serialize<T: serde::Serialize>(value: &T) -> Result<Vec<u8>, Error> {
    #[cfg(feature = "json")]
    {
        return serde_json::to_vec(value).map_err(Error::Serialization);
    }

    #[cfg(not(feature = "json"))]
    {
        // Fallback to a simpler format
        todo!("non-JSON serialization")
    }
}

// Feature-gated modules
#[cfg(feature = "postgres")]
pub mod postgres;

// Feature-gated trait implementations
#[cfg(feature = "json")]
impl FromStr for Config {
    type Err = serde_json::Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        serde_json::from_str(s)
    }
}
```

Usage: `cargo build --features "json,postgres"` or `cargo build --all-features`.

### Pattern 3: Build Scripts (build.rs)

Run custom logic before compilation: code generation, native library linking,
environment detection.

```rust
// build.rs
fn main() {
    // Tell Cargo to re-run if these change
    println!("cargo::rerun-if-changed=proto/");
    println!("cargo::rerun-if-env-changed=DATABASE_URL");

    // Set a cfg flag based on environment
    if std::env::var("CI").is_ok() {
        println!("cargo::rustc-cfg=ci_build");
    }

    // Expose build-time info as environment variables
    let git_hash = std::process::Command::new("git")
        .args(["rev-parse", "--short", "HEAD"])
        .output()
        .ok()
        .and_then(|o| String::from_utf8(o.stdout).ok())
        .unwrap_or_else(|| "unknown".to_string());

    println!("cargo::rustc-env=GIT_HASH={}", git_hash.trim());

    // Link native libraries
    println!("cargo::rustc-link-lib=sqlite3");
}
```

```rust
// In your code, access build-time values
const GIT_HASH: &str = env!("GIT_HASH");

fn version_info() -> String {
    format!("v{} ({})", env!("CARGO_PKG_VERSION"), GIT_HASH)
}
```

### Pattern 4: Publishing to crates.io

Prepare a crate for publication with proper metadata and checks.

```toml
[package]
name = "my-library"
version = "0.2.0"
edition = "2021"
description = "A concise description of what this crate does"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/my-library"
documentation = "https://docs.rs/my-library"
readme = "README.md"
keywords = ["keyword1", "keyword2"]      # max 5
categories = ["development-tools"]
exclude = ["tests/fixtures/*", ".github/"]
rust-version = "1.75"                    # MSRV
```

```bash
# Pre-publish checklist
cargo fmt --check                   # formatting
cargo clippy -- -D warnings         # lints as errors
cargo test                          # all tests pass
cargo doc --no-deps                 # docs build
cargo package --list                # review included files
cargo publish --dry-run             # verify packaging

# Publish
cargo publish
```

### Pattern 5: Clippy and Fmt Configuration

Configure linting and formatting for consistent code quality.

```toml
# Cargo.toml -- workspace-level clippy config
[workspace.lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
nursery = { level = "warn", priority = -1 }
# Allow specific lints you disagree with
module_name_repetitions = "allow"
must_use_candidate = "allow"
missing_errors_doc = "allow"

[workspace.lints.rust]
unsafe_code = "forbid"
missing_debug_implementations = "warn"
```

```toml
# crates/core/Cargo.toml
[lints]
workspace = true   # inherit workspace lint config
```

```toml
# rustfmt.toml
edition = "2021"
max_width = 100
use_field_init_shorthand = true
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

```bash
# CI commands
cargo fmt --all -- --check          # check formatting
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
```

## Anti-Patterns

- **Massive single-crate projects** -- Split into workspace members when crate
  compile time becomes a bottleneck. Each member compiles independently.

- **Features that change behavior rather than add it** -- Features should be
  additive. A crate with feature A enabled should be a superset of the crate
  without it. Do not use features to toggle between alternative implementations.
  ```toml
  # BAD: mutually exclusive features
  [features]
  backend_a = []
  backend_b = []

  # GOOD: additive features
  [features]
  postgres = ["dep:sqlx"]
  caching = ["dep:redis"]
  ```

- **Skipping `cargo clippy` in CI** -- Clippy catches real bugs. Run it with
  `-D warnings` to treat lints as errors in CI.

- **Not pinning workspace dependency versions** -- Use `Cargo.lock` for applications
  (commit it to git). For libraries, let `Cargo.lock` be gitignored but use
  workspace dependencies for consistency.

- **Overly broad `build.rs` re-run triggers** -- Use `cargo::rerun-if-changed`
  and `cargo::rerun-if-env-changed` to avoid unnecessary rebuilds.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `cargo build --workspace` | Build all workspace members |
| `cargo test --workspace` | Test all workspace members |
| `cargo clippy --workspace` | Lint all workspace members |
| `cargo fmt --all` | Format all workspace members |
| `cargo build --features "x,y"` | Build with specific features |
| `cargo build --all-features` | Build with every feature enabled |
| `cargo build --no-default-features` | Build without default features |
| `cargo publish --dry-run` | Verify packaging without publishing |
| `cargo doc --open` | Build and open documentation |
| `cargo tree` | Show dependency tree |
| `cargo udeps` | Find unused dependencies |
| `cargo deny check` | Audit licenses and advisories |
