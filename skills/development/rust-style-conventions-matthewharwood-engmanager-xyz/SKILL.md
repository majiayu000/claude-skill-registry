---
name: rust-style-conventions
description: Foundational Rust style conventions that apply universally to all Rust code. Covers import organization, naming conventions, and code formatting standards. This skill is automatically applied to all Rust implementations and should be referenced by all other Rust skills.
always_apply: true
---

# Rust Style Conventions

*Universal Rust style conventions for consistent, readable production code*

## Applicability

**This skill applies automatically to ALL Rust code.** All other Rust skills (rust-core-patterns, axum-web-framework, rust-async-runtime, etc.) inherit these conventions.

## Import Style (MANDATORY)

All `use` imports MUST be at the top of files. Never use inline paths.

### The Rule

**Import types and functions at the top of the file, then use the imported names in code.**

### Incorrect (Inline Paths)

```rust
// WRONG: Inline paths scattered throughout code
fn main() {
    let url = std::env::var("DATABASE_URL")?;
    let duration = std::time::Duration::from_secs(5);
    let path = std::path::PathBuf::from("/tmp");
    let pending = std::future::pending::<()>();
}
```

### Correct (Top-Level Imports)

```rust
use std::env;
use std::future;
use std::path::PathBuf;
use std::time::Duration;

fn main() {
    let url = env::var("DATABASE_URL")?;
    let duration = Duration::from_secs(5);
    let path = PathBuf::from("/tmp");
    let pending = future::pending::<()>();
}
```

### Why This Matters

1. **Readability**: All dependencies visible at file top
2. **Refactoring**: Easier to track and update imports
3. **Conflict detection**: Namespace conflicts visible immediately
4. **IDE support**: Better autocomplete and navigation
5. **Consistency**: Matches Rust community conventions

### Use What You Import (CRITICAL)

**If a name is imported, USE the imported name. Never mix imported names with fully-qualified paths in the same file.**

```rust
// WRONG: Import exists but fully-qualified path used anyway
use std::env::var;

fn get_config() -> String {
    std::env::var("KEY").unwrap()  // BAD: ignores the import
}

// CORRECT: Use the imported name
use std::env::var;

fn get_config() -> String {
    var("KEY").unwrap()  // GOOD: uses the import
}
```

This applies to ALL imports — if you write `use X`, then use `X`, never the full path.

```rust
// WRONG: Mixed usage
use std::time::Duration;

let short = Duration::from_secs(1);      // Using import
let long = std::time::Duration::from_secs(60);  // Ignoring import - BAD

// CORRECT: Consistent usage
use std::time::Duration;

let short = Duration::from_secs(1);
let long = Duration::from_secs(60);
```

**Enforcement**: If you see a fully-qualified path in code, check the imports. If it's already imported, use the imported name.

### Import Organization

Group imports in this order with blank lines between groups:

```rust
// 1. Standard library
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

// 2. External crates (alphabetical)
use axum::{Router, routing::get};
use serde::{Deserialize, Serialize};
use tokio::sync::mpsc;

// 3. Workspace crates
use my_domain::User;
use my_utils::helpers;

// 4. Local modules
use crate::config::Config;
use crate::error::AppError;
```

### Partial Imports

Prefer importing the module rather than every function:

```rust
// Good: Import module, use qualified names
use std::env;
use std::fs;

let value = env::var("KEY")?;
let content = fs::read_to_string("file.txt")?;

// Also acceptable: Import specific frequently-used items
use std::time::Duration;
use std::sync::Arc;

let timeout = Duration::from_secs(30);
let shared = Arc::new(data);
```

### Nested Imports

Use nested imports for multiple items from the same module:

```rust
// Good: Grouped imports
use axum::{
    extract::{Path, Query, State},
    routing::{get, post},
    Router,
};

// Avoid: Many separate use statements
use axum::extract::Path;
use axum::extract::Query;
use axum::extract::State;
use axum::routing::get;
use axum::routing::post;
use axum::Router;
```

## Naming Conventions

Follow standard Rust naming conventions:

| Item | Convention | Example |
|------|------------|---------|
| Crates | snake_case | `my_crate` |
| Modules | snake_case | `user_service` |
| Types (struct, enum, trait) | PascalCase | `UserService` |
| Functions | snake_case | `get_user` |
| Methods | snake_case | `find_by_id` |
| Local variables | snake_case | `user_count` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_CONNECTIONS` |
| Statics | SCREAMING_SNAKE_CASE | `DEFAULT_TIMEOUT` |
| Type parameters | PascalCase, single letter preferred | `T`, `E`, `R` |
| Lifetimes | lowercase, short | `'a`, `'de` |

## Formatting Standards

### Use rustfmt

All code must pass `cargo fmt --check`. Use default rustfmt settings unless project specifies otherwise.

### Line Length

- Target 100 characters maximum
- Break long function signatures and chains

### Expression Breaking

```rust
// Break long chains
let result = collection
    .iter()
    .filter(|x| x.is_valid())
    .map(|x| x.process())
    .collect::<Vec<_>>();

// Break long function calls
let response = client
    .post(&url)
    .header("Authorization", token)
    .json(&payload)
    .send()
    .await?;
```

## Documentation

### Public API Documentation

All public items should have doc comments:

```rust
/// Creates a new user with the given email and name.
///
/// # Arguments
///
/// * `email` - The user's email address (must be valid format)
/// * `name` - The user's display name
///
/// # Errors
///
/// Returns `CreateUserError` if:
/// - Email is invalid or already exists
/// - Name is empty or too long
///
/// # Example
///
/// ```
/// let user = create_user("alice@example.com", "Alice")?;
/// ```
pub fn create_user(email: &str, name: &str) -> Result<User, CreateUserError> {
    // ...
}
```

### Module Documentation

Add module-level documentation:

```rust
//! User management module.
//!
//! This module provides functionality for creating, updating,
//! and deleting users in the system.

mod create;
mod delete;
mod update;
```

## Error Messages

Write clear, actionable error messages:

```rust
// Good: Specific and actionable
#[error("user not found with id {id}")]
NotFound { id: UserId },

#[error("email {email} is already registered")]
EmailExists { email: String },

// Bad: Vague and unhelpful
#[error("error occurred")]
GenericError,

#[error("invalid")]
Invalid,
```

## Best Practices Summary

1. **Imports at top**: Never use inline paths like `std::time::Duration`
2. **Use what you import**: If `use std::env::var;` exists, use `var()` not `std::env::var()`
3. **Organize imports**: Group by std, external, workspace, local
4. **Follow naming conventions**: PascalCase for types, snake_case for functions
5. **Run rustfmt**: All code must be formatted
6. **Document public APIs**: Use `///` doc comments
7. **Clear error messages**: Be specific and actionable

## Integration with Other Skills

This skill provides foundational conventions used by:

- **rust-core-patterns**: Type definitions follow naming conventions
- **axum-web-framework**: Handler functions follow import style
- **rust-async-runtime**: Tokio imports organized properly
- **rust-error-handling**: Error messages follow guidelines
- **rust-observability**: Tracing macros with proper imports
- **axum-service-architecture**: Module organization follows conventions
- **rust-testing-verification**: Test code follows same standards
- **rust-production-reliability**: All production code formatted
- **maud-syntax-fundamentals**: Template functions follow style
- **maud-axum-integration**: Integration code follows conventions
- **maud-components-patterns**: Component functions follow naming

## References

- **Rust API Guidelines**: https://rust-lang.github.io/api-guidelines/
- **rustfmt**: https://github.com/rust-lang/rustfmt
- **Clippy Lints**: https://rust-lang.github.io/rust-clippy/
