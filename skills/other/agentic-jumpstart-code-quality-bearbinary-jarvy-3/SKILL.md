---
name: "agentic-jumpstart-code-quality"
description: "Code quality guidelines for Jarvy CLI - Rust formatting, Clippy linting, error handling patterns, documentation standards, and Conventional Commits."
---

# Code Quality Guidelines

This skill defines code quality standards for the Jarvy CLI project.

## Build and Validation Commands

Run these before every commit:

```bash
cargo fmt --all                                # Format code
cargo clippy --all-features -- -D warnings     # Lint (must pass)
cargo check --verbose                          # Type check
cargo test --verbose -- --show-output          # Run tests
```

## Rust Style Guidelines

### Edition and Idioms

- Use Rust 2024 edition idioms
- Prefer stdlib over new crates
- Use derive macros (clap, serde, thiserror)

### Naming Conventions

```rust
// Functions and variables: snake_case
fn install_package(package_name: &str) -> Result<(), InstallError>

// Types and traits: PascalCase
struct ToolConfig { }
enum InstallError { }

// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRY_ATTEMPTS: u32 = 3;

// Modules: snake_case
mod package_manager;
```

### Platform-Specific Code

```rust
#[cfg(target_os = "macos")]
fn install_macos() -> Result<(), InstallError> { }

#[cfg(target_os = "linux")]
fn install_linux() -> Result<(), InstallError> { }

#[cfg(target_os = "windows")]
fn install_windows() -> Result<(), InstallError> { }
```

### Lazy Statics

Use `OnceLock` for lazy initialization:

```rust
use std::sync::OnceLock;
use std::sync::RwLock;

static REGISTRY: OnceLock<RwLock<HashMap<String, HandlerFn>>> = OnceLock::new();

fn get_registry() -> &'static RwLock<HashMap<String, HandlerFn>> {
    REGISTRY.get_or_init(|| RwLock::new(HashMap::new()))
}
```

## Clippy Compliance

Code must pass `cargo clippy --all-features -- -D warnings`.

### Common Fixes

```rust
// Use if-let for single pattern
if let Ok(v) = result {
    process(v);
}

// Use ? operator
let value = operation()?;

// Use is_empty()
if items.is_empty() { }

// Avoid needless borrows
function(&string)  // not &string.clone()
```

## Error Handling

### thiserror Pattern

```rust
#[derive(thiserror::Error, Debug)]
pub enum InstallError {
    #[error("unsupported platform")]
    Unsupported,

    #[error("prerequisite missing: {0}")]
    Prereq(&'static str),

    #[error("command failed: {cmd} (code: {code:?})\n{stderr}")]
    CommandFailed { cmd: String, code: Option<i32>, stderr: String },

    #[error(transparent)]
    Io(#[from] std::io::Error),
}
```

### Error Propagation

```rust
pub fn ensure(min_hint: &str) -> Result<(), InstallError> {
    let config = load_config()?;
    if !is_installed(&config)? {
        install()?;
    }
    Ok(())
}
```

### Exit Codes

```rust
pub const SUCCESS: i32 = 0;
pub const CONFIG_ERROR: i32 = 2;
pub const PREREQ_MISSING: i32 = 3;
pub const PERMISSION_REQUIRED: i32 = 5;
```

## Testing Standards

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_version() {
        let result = parse_version("2.40");
        assert!(result.is_ok());
    }
}
```

### Test Environment Variables

- `JARVY_TEST_MODE=1` - Disable interactive prompts
- `JARVY_FAST_TEST` - Skip external commands

## Documentation Standards

### Module Documentation

```rust
//! Tool registry for managing package installer handlers.
//!
//! This module provides a global registry that maps tool names
//! to their installation handler functions.
```

### Function Documentation

```rust
/// Ensures a tool is installed at the specified minimum version.
///
/// # Arguments
///
/// * `min_hint` - Minimum version string (e.g., "2.40")
///
/// # Returns
///
/// Returns `Ok(())` if installed or successfully installed.
pub fn ensure(min_hint: &str) -> Result<(), InstallError> { }
```

## Commit Message Format

Use Conventional Commits:

```
<type>(<scope>): <description>

[optional body]
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `chore:` - Maintenance
- `refactor:` - Code restructuring
- `test:` - Tests

### Examples

```
feat(tools): add Node.js version manager support

fix(config): handle missing jarvy.toml gracefully

docs: update README with installation instructions

chore(deps): update clap to 4.5

refactor(registry): simplify handler lookup

test(cli): add integration tests for setup
```

### Scope Guidelines

- `tools` - Tool implementations
- `config` - Configuration parsing
- `cli` - Command-line interface
- `registry` - Tool registry
- `telemetry` - Analytics
- `deps` - Dependencies

## Pre-Commit Checklist

1. [ ] `cargo fmt --all` - formatted
2. [ ] `cargo clippy --all-features -- -D warnings` - no warnings
3. [ ] `cargo check --verbose` - compiles
4. [ ] `cargo test --verbose -- --show-output` - tests pass
5. [ ] Commit message follows Conventional Commits
6. [ ] New public APIs documented
7. [ ] Platform-specific code uses `#[cfg]`
