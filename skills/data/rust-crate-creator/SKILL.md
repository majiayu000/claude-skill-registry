---
name: rust-crate-creator
description: Create new Rust crates in this Cargo workspace following established
  patterns for dependency management, testing, documentation, and project structure.
  Use when adding new workspace members, creating
---

---
name: rust-crate-creator
description: Create new Rust crates in this Cargo workspace following established patterns for dependency management, testing, documentation, and project structure. Use when adding new workspace members, creating modules, or structuring code. Keywords: cargo, crate, workspace, module, new crate, add crate, dependency, Rust project
---

# Rust Crate Creator

Creates new Rust crates in the workspace following established project conventions for dependency management, testing, documentation, and modular architecture.

## Instructions

When creating a new crate, follow this structured approach:

### 1. Analyze Workspace Structure

**Workspace root patterns:**
- All dependencies must be pinned in `Cargo.toml:[workspace.dependencies]`
- Workspace members live under `crates/`
- Use `resolver = "2"` for workspace-level dependency resolution
- Generate artifacts belong in `target/` (never commit)

**Current workspace dependencies to reference:**
```toml
[workspace.dependencies]
# Internal crates (always use path references)
common = { path = "crates/common" }
expr = { path = "crates/expr" }
types = { path = "crates/types" }

# External dependencies (pin versions here)
proptest = "1.9.0"
pretty_assertions = "1"
serde = { version = "1.0.228", features = ["derive"] }
serde_json = "1.0.145"
sqlparser = "0.43"
tempfile = "3.23.0"
thiserror = "1.0.69"
ahash = "0.8.12"
hashbrown = { version = "0.14.5", features = ["serde"] }
uuid = { version = "1.18.1", features = ["serde", "v4"] }
bincode = { version = "2.0.1", features = ["serde"] }
bytes = "1.10.1"
```

### 2. Create Crate Structure

**Directory layout:**
```
crates/<crate-name>/
├── Cargo.toml
├── CLAUDE.md
├── AGENTS.md
├── src/
│   ├── lib.rs
│   └── tests.rs (or mod tests in lib.rs)
└── tests/ (optional integration tests)
```

**Cargo.toml template:**
```toml
[package]
name = "crate-name"
version = "0.1.0"
edition = "2024"  # or "2021" if needed

[dependencies]
# Reference workspace deps with { workspace = true }
common = { workspace = true }
types = { workspace = true }
serde = { workspace = true }
thiserror = { workspace = true }

[dev-dependencies]
# Test dependencies also from workspace
tempfile = { workspace = true }
proptest = { workspace = true }
pretty_assertions = { workspace = true }
```

**Critical rules:**
- NEVER specify versions in member crates—always use `{ workspace = true }`
- Even path-only dependencies (`common`, `expr`, `types`) must use workspace references
- Add new dependencies to root `[workspace.dependencies]` first, then reference them

### 3. Generate CLAUDE.md (Crate Guidelines)

**Template structure:**
```markdown
# [Crate Name] Guidelines

## Role Within The Workspace
- Purpose and responsibility of this crate
- How it integrates with other workspace members
- Key contracts and APIs it provides

## Integration Contracts
- **Parser** – How parser interacts with this crate
- **Types** – Type dependencies and shared structures
- **Common** – Error handling and shared utilities
- **Storage/Catalog/Expr** – Domain-specific integrations

## Module Layout & Extension Points
- Key source files and their responsibilities
- How to add new features or extend existing ones
- Important patterns to follow

## Build, Test, and Development Commands
- `cargo check -p [crate-name]` — fast validation
- `cargo test -p [crate-name]` — run crate tests
- `cargo fmt` / `cargo fmt -- --check` — formatting
- `cargo clippy -p [crate-name] --all-targets` — linting
- `scripts/coverage.sh -- --package [crate-name]` — coverage

## Coding Style & Naming Conventions
- Follow rustfmt defaults (4-space indent, trailing commas)
- Modules: snake_case (`mod storage_backend`)
- Types/traits: UpperCamelCase (`SqlValue`)
- Constants: SCREAMING_SNAKE_CASE
- Workspace dependency pattern: `{ workspace = true }`

## Testing Guidelines
- Co-locate unit tests using `mod tests`
- Use `tempfile::tempdir()` for filesystem tests
- Property tests with `proptest` (name as `prop_*`)
- Integration tests in `tests/` directory
- Run tests before commits

## Commit & Pull Request Guidelines
- Imperative mood commits
- PRs include: motivation, changes, validation commands, affected crates
- Mention downstream impacts
```

### 4. Generate AGENTS.md (Implementation Guardrails)

**Template structure:**
```markdown
# [Crate Name] - agents.md

> Implementation guardrails for the `[crate-name]` crate so future agents can extend it without breaking workspace conventions.

## Purpose

- Core responsibility and domain
- Key abstractions provided
- Integration points with other crates

## Architecture checkpoints

1. **Key pattern 1** - Description and constraints
2. **Key pattern 2** - Description and constraints
3. **Key pattern 3** - Description and constraints

## Workspace coordination

- Dependencies must be declared via `{ workspace = true }`
- Shared domain types come from `common`/`types`
- Tests rely on `tempfile` for temporary directories
- All errors use `common::DbResult` and `DbError` variants

## Extending the crate

- How to add new features safely
- Patterns to maintain consistency
- Integration points to coordinate with other crates

By following these constraints we keep the [crate-name] layer aligned with the rest of the SQL database workspace.
```

### 5. Add Rust Documentation Comments

**Module-level docs (in lib.rs):**
```rust
//! Brief description of the crate's purpose.
//!
//! # Examples
//!
//! ```
//! // Show basic usage
//! ```
//!
//! # Architecture
//!
//! Explain key design decisions or patterns.
```

**Type/function docs:**
```rust
/// Brief description of what this does.
///
/// # Examples
///
/// ```
/// let example: TypeName = ...;
/// // Show usage
/// ```
///
/// # Errors
///
/// Returns `DbError::...` when conditions occur.
pub struct TypeName { ... }

/// Identifier for a column within a table schema.
/// Examples:
/// - `let id_col: ColumnId = 1; // maps to "id"`
/// - `let name_col: ColumnId = 2; // maps to "name"`
pub type ColumnId = u64;
```

### 6. Set Up Testing Patterns

**Unit tests (co-located):**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn descriptive_test_name() {
        // Arrange

        // Act

        // Assert
    }
}
```

**Using tempfile for filesystem tests:**
```rust
use tempfile::tempdir;

#[test]
fn test_with_temp_directory() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("test.file");

    // Use path for testing

    // dir automatically cleaned up on drop
}
```

**Property-based tests:**
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn prop_roundtrip_preserves_value(input: Vec<u8>) {
        let encoded = encode(&input);
        let decoded = decode(&encoded).unwrap();
        prop_assert_eq!(input, decoded);
    }
}
```

### 7. Update Workspace Configuration

**Add to root Cargo.toml members:**
```toml
[workspace]
members = [
    # ... existing members
    "crates/new-crate-name",
]
```

**Add internal dependency to workspace:**
```toml
[workspace.dependencies]
new-crate-name = { path = "crates/new-crate-name" }
```

### 8. Code Coverage Setup

The project uses `cargo-llvm-cov` for coverage:

**Run coverage for specific crate:**
```bash
scripts/coverage.sh -- --package crate-name
```

**Coverage generates:**
- HTML report: `target/llvm-cov/html/index.html`
- LCOV format: `target/llvm-cov/lcov.info`

### 9. Common Patterns

**Error handling:**
```rust
use common::{DbError, DbResult};

pub fn operation() -> DbResult<T> {
    // ... implementation
    Err(DbError::CrateName(format!("descriptive error")))
}
```

**Serialization with bincode:**
```rust
use bincode::config::{self, Config};
use bincode::serde::{decode_from_slice, encode_to_vec};

fn bincode_config() -> impl Config {
    config::legacy()
}

// Encoding
let bytes = encode_to_vec(data, bincode_config())?;

// Decoding
let (decoded, read) = decode_from_slice(&bytes, bincode_config())?;
```

**Module organization:**
```rust
// src/lib.rs
pub mod submodule;

pub use submodule::PublicType;

// src/submodule.rs
use common::{DbError, DbResult};

pub struct PublicType { ... }

#[cfg(test)]
mod tests { ... }
```

## Common Pitfalls and Solutions

### Test Module Configuration

**Problem:** Tests fail to compile with "unresolved import" errors for dev-dependencies.

**Solution:** Always add `#[cfg(test)]` attribute to test modules:
```rust
#[cfg(test)]
mod tests;
```

This ensures test-only imports (like `tempfile`) are only compiled during test runs.

### File I/O and Clippy Warnings

**Problem:** Clippy warns about "file opened with `create`, but `truncate` behavior not defined".

**Solution:** Explicitly specify truncate behavior when using `create(true)`:
```rust
// For append-only files (don't truncate existing content)
OpenOptions::new()
    .read(true)
    .write(true)
    .create(true)
    .truncate(false)  // Keep existing content
    .open(&path)?;

// For overwriting files
OpenOptions::new()
    .write(true)
    .create(true)
    .truncate(true)   // Overwrite existing content
    .open(&path)?;
```

### Page Allocation and File Extension

**Problem:** Sequential ID allocation fails because the file doesn't actually extend until data is written.

**Solution:** Write the page to disk immediately after allocation to reserve the space:
```rust
fn allocate_page(&mut self, table: TableId) -> DbResult<PageId> {
    let pid = PageId(file_len / PAGE_SIZE);
    let page = Page::new(pid.0);

    // Write immediately to extend the file
    self.write_page(table, &page)?;

    // Then add to cache
    self.cache.push((table, pid), page);
    Ok(pid)
}
```

### Coverage Script Usage

**Problem:** Running `scripts/coverage.sh -- --package crate-name` fails with "Unrecognized option: 'package'".

**Solution:** Use `cargo llvm-cov` directly for single-crate coverage:
```bash
# Correct approach
cargo llvm-cov --package crate-name --html

# View summary
cargo llvm-cov --package crate-name --summary-only
```

The workspace `scripts/coverage.sh` is designed for full workspace coverage, not filtered runs.

### Import Organization

**Problem:** Rustfmt reorders imports in unexpected ways.

**Solution:** Follow rustfmt's preference:
- External crates first (alphabetically)
- Then standard library imports
- Import items alphabetically within each use statement
```rust
use common::{DbError, DbResult, PageId, TableId};
use hashbrown::HashMap;
use lru::LruCache;
use std::{
    fs::OpenOptions,
    io::{Read, Seek, SeekFrom, Write},
    num::NonZeroUsize,
    path::PathBuf,
};
use storage::{PAGE_SIZE, Page};  // Items sorted alphabetically
```

### Function Coverage Targets

**Problem:** Coverage shows low function coverage (e.g., 50%) even when tests seem comprehensive.

**Solution:** Test error paths and edge cases explicitly:
- Test functions that return `Result<T>` with both success and error cases
- Test private helper functions indirectly through public API
- Add tests for all public trait implementations
- Test panic conditions with `#[should_panic]`
- Target 90%+ line coverage and 85%+ function coverage

Example:
```rust
#[test]
fn test_error_path() {
    let result = operation_that_can_fail();
    assert!(matches!(result, Err(DbError::Storage(_))));
}

#[test]
#[should_panic(expected = "descriptive message")]
fn test_panic_condition() {
    function_that_panics();
}
```

## Validation Checklist

Before completing crate creation:

- [ ] `Cargo.toml` uses `{ workspace = true }` for all dependencies
- [ ] Added to workspace members in root `Cargo.toml`
- [ ] `CLAUDE.md` documents integration contracts
- [ ] `AGENTS.md` captures architecture guardrails
- [ ] Module-level doc comments (`//!`) in `lib.rs`
- [ ] Type/function doc comments (`///`) with examples
- [ ] Unit tests use `mod tests` pattern
- [ ] Filesystem tests use `tempfile::tempdir()`
- [ ] Error types use `common::DbError` variants
- [ ] `cargo check -p crate-name` passes
- [ ] `cargo test -p crate-name` passes
- [ ] `cargo fmt -- --check` passes
- [ ] `cargo clippy -p crate-name --all-targets` passes
- [ ] `cargo llvm-cov --package crate-name --summary-only` shows 85%+ function coverage
- [ ] `cargo llvm-cov --package crate-name --summary-only` shows 90%+ line coverage
- [ ] Error paths and edge cases are explicitly tested

## Output Format

When creating a new crate, generate files in this order:

1. **Show workspace analysis** - List existing crates and dependencies
2. **Create directory structure** - Use Write tool for `Cargo.toml`, `CLAUDE.md`, `AGENTS.md`
3. **Generate src/lib.rs** - With proper doc comments
4. **Add tests** - Either in-module or separate `tests.rs`
5. **Update workspace** - Modify root `Cargo.toml`
6. **Run validation** - Execute check/test/fmt/clippy
7. **Summary** - List created files and next steps

## Example Usage

User: "Create a new crate for query planning"