---
name: rust-dev
description: This skill should be used when working with Rust code, reviewing Rust code, managing Rust dependencies, creating Rust projects, or fixing Rust compilation errors. It provides strict coding standards (especially FAIL FAST error handling), workspace architecture guidance, dependency management automation, and common Rust patterns.
---

# Rust Development

## Overview

This skill enables writing correct, idiomatic Rust code following strict standards and best practices. It enforces FAIL FAST error handling, manages dependencies properly, provides workspace templates, and offers solutions to common Rust patterns and pitfalls.

## When to Use This Skill

Activate this skill for:

- Adding or updating Rust dependencies
- Creating new Rust projects or workspaces
- Writing or modifying Rust code
- Fixing compilation errors, borrow checker issues, or lifetime problems
- Implementing error handling
- Setting up async/await patterns
- Configuring CLI applications
- Organizing tests and configuration
- Splitting large modules or reorganizing file structure

## Core Standards

**Critical principles to follow in ALL Rust code:**

1. **Edition 2024**: Always use `edition = "2024"` in Cargo.toml
2. **FAIL FAST Error Handling**: NEVER swallow errors - always propagate with `?` or explicit return
3. **Dependency Versioning**: Use `x.x` format (e.g., `serde = "1.0"`)
4. **Workspace Architecture**: Use workspace with single-responsibility crates
5. **Error Types**: thiserror (with backtrace) for libraries, anyhow for binaries/tests
6. **CLI-First Configuration**: Never bypass CLI argument parsing
7. **No env::set_var in Tests**: Pass config through function parameters
8. **Async Runtime**: Use tokio consistently

See `references/standards.md` for complete details on all standards.

## Dependency Management

### Adding Dependencies

When adding a dependency:

1. **Find the latest version** using the bundled script:
   ```bash
   python3 scripts/check_crate_version.py <crate-name>
   ```

2. **Use the x.x version format** from the script output:
   ```toml
   serde = "1.0"
   ```

3. **For workspace projects**, add to `[workspace.dependencies]` in root Cargo.toml:
   ```toml
   [workspace.dependencies]
   serde = { version = "1.0", features = ["derive"] }
   ```

4. **In member crates**, reference workspace dependencies:
   ```toml
   [dependencies]
   serde = { workspace = true }
   ```

### Common Dependencies

- **Error handling**: `thiserror = "1.0"` (libraries), `anyhow = "1.0"` (binaries/tests)
- **Async**: `tokio = { version = "1.40", features = ["full"] }`
- **Serialization**: `serde = { version = "1.0", features = ["derive"] }`
- **CLI**: `clap = { version = "4.5", features = ["derive"] }`
- **Derives**: `derive_more = { version = "1.0", features = ["full"] }`

## Creating New Projects

### Workspace Structure

Use the template in `assets/workspace-template/` as a starting point:

```
project/
├── Cargo.toml              # Workspace root, no code
├── project/                # Library crate (core logic)
│   ├── Cargo.toml          # Uses thiserror
│   └── src/lib.rs
└── project-cli/            # Binary crate (CLI interface)
    ├── Cargo.toml          # Uses anyhow + clap
    └── src/main.rs
```

**Steps to create a new workspace:**

1. Copy the template directory structure
2. Rename `project` and `project-cli` to match the actual project name
3. Update all package names in Cargo.toml files
4. Update the binary name in `project-cli/Cargo.toml`
5. Ensure all Cargo.toml files specify `edition = "2024"`

## Error Handling Workflow

**This is the MOST CRITICAL standard - violations are unacceptable.**

### Rule: FAIL FAST - Never Swallow Errors

**Why This Matters:**
- Silent failures corrupt data and leave systems in undefined states
- Half-completed operations are worse than crashes (harder to debug, data inconsistency)
- Errors cascade: one swallowed error causes 10 mysterious failures downstream
- Logging without propagating gives false confidence that errors are "handled"

**The Rule:** Every error MUST propagate up the call stack. The program halts on errors.

**✅ CORRECT - Always propagate errors:**

```rust
// Best: Use ? operator
operation()?;

// With context: Add context AND propagate
operation().context("failed during initialization")?;

// Log for observability AND propagate (both required!)
let result = operation().map_err(|e| {
    tracing::error!("Operation failed: {e}");
    e
})?;

// Explicit match when you need it
match operation() {
    Ok(val) => process(val),
    Err(e) => return Err(e.into()),
}
```

**❌ FORBIDDEN - These all swallow errors:**

```rust
if let Err(e) = operation() { log::error!("{e}"); }  // No return!
operation().unwrap_or_default();  // Silent fallback
operation().ok();  // Discards error
let _ = operation();  // Explicitly ignores
```

**Self-Check:** If you see `if let Err` or `match ... Err` without `return Err` or `?`, it's a bug.

**NOT "Error Handling":** Adding logging is NOT fixing/handling an error. The error must propagate.

### Choosing Error Types

**For library crates** (in src/lib.rs or modules) - use thiserror with backtrace:

```rust
use std::backtrace::Backtrace;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error, Backtrace),

    #[error("Parse error: {0}")]
    Parse(String, Backtrace),
}

pub type Result<T> = std::result::Result<T, MyError>;
```

**For binaries** (in main.rs):

```rust
use anyhow::{Context, Result};

#[tokio::main]
async fn main() -> Result<()> {
    let config = load_config()
        .context("Failed to load configuration")?;
    Ok(())
}
```

See `references/common-patterns.md` for more error handling examples.

## Common Patterns and Solutions

When encountering common Rust challenges, refer to `references/common-patterns.md` for solutions:

- **Lifetime issues**: Common struct lifetime patterns and elision rules
- **Async/await**: Tokio runtime setup, async traits (AFIT in Rust 1.75+)
- **Trait objects**: Dynamic dispatch, Box<dyn Trait>, Send + Sync
- **Configuration**: CLI-first patterns with clap
- **Testing**: Patterns that avoid env::set_var
- **Derives**: Common macro combinations
- **Newtypes**: Type safety patterns with derive_more
- **Builders**: Using derive_builder

**Search the reference file** for specific patterns when needed.

## CLI Application Pattern

All CLI applications should follow this pattern:

```rust
use anyhow::{Context, Result};
use clap::Parser;

#[derive(Parser, Debug)]
struct CliArgs {
    #[arg(long, env = "API_KEY")]
    api_key: String,
}

struct Config {
    api_key: String,
}

impl Config {
    fn from_cli_args(args: CliArgs) -> Self {
        Self { api_key: args.api_key }
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = CliArgs::parse();
    let config = Config::from_cli_args(args);
    run(config).await?
}
```

**Never** use Default trait that reads environment. **Always** use `from_cli_args()`.

## Testing Standards

**Critical rule**: NEVER use `std::env::set_var()` in tests.

**Correct pattern** - pass config through parameters:

```rust
pub struct Client {
    api_key: String,
}

impl Client {
    pub fn new(api_key: String) -> Self {
        Self { api_key }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_client() {
        // Pass test config directly
        let client = Client::new("test-key".to_string());
        assert_eq!(client.api_key, "test-key");
    }
}
```

## Code Quality Standards

Follow these principles:

- **Visibility**: Private (default) > pub(crate) > pub
- **Magic Numbers**: Use `const` or CLI args, never literals
- **Async Runtime**: Use tokio consistently
- **Breaking Changes**: OK for internal crates, preserve HTTP/WebSocket API compatibility

## Module Organization

**Keep files focused and manageable by splitting large modules.**

### When to Split Modules

Split a module into submodules when:

1. **File exceeds ~500 lines** and contains semantically distinct components
2. **Tests take 50% or more of the file** - extract to separate test module
3. **Multiple distinct responsibilities** exist that can be cleanly separated
4. **Re-exports can preserve the public API** without breaking existing code

### Test Module Extraction

When tests dominate a file (~50%+ of lines), move them to a separate file:

**Before** (single file `parser.rs`):
```rust
// 200 lines of implementation
pub fn parse(input: &str) -> Result<Ast> { ... }

#[cfg(test)]
mod tests {
    // 250 lines of tests - this should be extracted!
}
```

**After** - Sibling file approach (preferred):
```
src/
├── parser.rs           # Implementation only
└── parser_tests.rs     # Tests in sibling file
```

```rust
// parser.rs
pub fn parse(input: &str) -> Result<Ast> { ... }

#[cfg(test)]
#[path = "parser_tests.rs"]
mod tests;
```

Keep test file in same directory as source (e.g., `src/mymodule.rs` → `src/mymodule_tests.rs`).

**Alternative** - Submodule approach (when tests need subdirectory structure):
```
src/
├── parser.rs           # Implementation only
└── parser/
    └── tests.rs        # Tests in submodule
```

```rust
// parser.rs
#[cfg(test)]
#[path = "parser/tests.rs"]
mod tests;
```

### Splitting Implementation Modules

When splitting for semantic reasons:

```
// Before: large api.rs with 600+ lines
src/api.rs

// After: api/ directory with focused submodules
src/
└── api/
    ├── mod.rs          # Re-exports public items
    ├── client.rs       # Client implementation
    ├── endpoints.rs    # Endpoint definitions
    └── types.rs        # Request/response types
```

**Key rules for splitting:**

1. **Preserve visibility** - use `pub use` re-exports in `mod.rs` to maintain the same public API
2. **Keep related code together** - don't split tightly coupled code
3. **Use `pub(super)` or `pub(crate)`** when items need cross-module access but shouldn't be public

```rust
// api/mod.rs - re-export public interface
mod client;
mod endpoints;
mod types;

pub use client::ApiClient;
pub use endpoints::{get_user, create_order};
pub use types::{Request, Response};
```

### When NOT to Split

- **Under 300 lines** - usually not worth the overhead
- **Tightly coupled code** - splitting would require excessive `pub` visibility
- **Single responsibility** - file is focused even if long (e.g., a complex algorithm)
- **Artificial boundaries** - don't split if it forces unnatural separation between entities that belong together
- **Externalizing internals** - if splitting requires making private items `pub(crate)` or `pub` just for cross-module access, the coupling indicates they should stay together

## Resources

### scripts/

- `check_crate_version.py`: Query crates.io for latest dependency versions

### references/

- `standards.md`: Complete Rust project standards and rules
- `common-patterns.md`: Solutions to common Rust patterns and challenges

### assets/

- `workspace-template/`: Boilerplate workspace structure following all standards

## Workflow Summary

When working on Rust code:

1. **Check edition**: Ensure `edition = "2024"` in all Cargo.toml files
2. **Add dependencies**: Use `check_crate_version.py` to find latest versions, add with `x.x` format
3. **Handle errors**: ALWAYS propagate errors with `?`, NEVER swallow with logging or unwrap_or
4. **Use correct error types**: thiserror for libraries, anyhow for binaries
5. **Follow CLI-first config**: Never bypass CLI argument parsing
6. **Test without env pollution**: Pass config through parameters, never use env::set_var
7. **Reference patterns**: Check `common-patterns.md` for idiomatic solutions
8. **Use workspace template**: For new projects, start with the provided template
9. **Organize modules**: Split files >500 lines; extract tests to sibling `_tests.rs` files when they take 50%+ of file
