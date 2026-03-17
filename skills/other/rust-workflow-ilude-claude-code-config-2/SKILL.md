---
name: rust-workflow
description: Rust project workflow guidelines. Activate when working with Rust files (.rs), Cargo.toml, Cargo.lock, or Rust-specific tooling.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Rust Projects Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | Clippy | `cargo clippy` |
| Format | rustfmt | `cargo fmt` |
| Type check | built-in | `cargo check` |
| Build | cargo | `cargo build` |
| Test | cargo | `cargo test` |
| Security | cargo-audit | `cargo audit` |
| Coverage | cargo-tarpaulin | `cargo tarpaulin` |
| Docs | rustdoc | `cargo doc` |

## Workflow Commands

### Development Cycle
```bash
# Check before commit
cargo fmt --check && cargo clippy -- -D warnings && cargo test

# Full validation
cargo fmt && cargo clippy --fix --allow-dirty && cargo test && cargo doc --no-deps
```

### Release Builds
```bash
cargo build --release
cargo test --release
```

---

## Trait Requirements

### Public Types
All public types MUST implement:
- `Debug` - Required for error messages and debugging
- `Clone` - Required unless the type explicitly manages unique resources

Public types SHOULD implement:
- `PartialEq` - When equality comparison is meaningful
- `Eq` - When `PartialEq` is reflexive (most cases)
- `Hash` - When the type may be used as a key
- `Default` - When a sensible default exists

### Common Derive Patterns
```rust
// Minimal public struct
#[derive(Debug, Clone)]
pub struct Config { /* ... */ }

// Value type (data container)
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct UserId(String);

// With default
#[derive(Debug, Clone, Default, PartialEq)]
pub struct Settings { /* ... */ }

// Serializable types
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct ApiResponse { /* ... */ }
```

### Display Trait
Types representing user-facing values SHOULD implement `Display`:
```rust
use std::fmt;

impl fmt::Display for UserId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}
```

---

## Cargo.lock Rules

### Binaries and Applications
- MUST commit `Cargo.lock` to version control
- Ensures reproducible builds across environments
- Add to `.gitignore` exceptions if using a global ignore

### Libraries
- MAY ignore `Cargo.lock` (add to `.gitignore`)
- Downstream consumers use their own lockfile
- RECOMMENDED to commit for CI reproducibility, but not required

### Workspaces
- MUST commit the root `Cargo.lock`
- All workspace members share the same lockfile

---

## Error Handling

### Libraries: Use `thiserror`
```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum LibraryError {
    #[error("invalid configuration: {0}")]
    InvalidConfig(String),

    #[error("resource not found: {resource}")]
    NotFound { resource: String },

    #[error(transparent)]
    Io(#[from] std::io::Error),
}
```

### Applications: Use `anyhow`
```rust
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let config = load_config()
        .context("failed to load configuration")?;

    run_app(config)?;
    Ok(())
}
```

### Error Handling Rules
- MUST NOT use `.unwrap()` in library code (except tests)
- MUST NOT use `.expect()` without a meaningful message
- SHOULD use `?` operator for propagation
- SHOULD add context with `.context()` or `.with_context()`
- MAY use `.unwrap()` in `main()` for unrecoverable errors

### Result Type Aliases
Libraries SHOULD define a Result alias:
```rust
pub type Result<T> = std::result::Result<T, LibraryError>;
```

---

## Memory Safety

### Ownership Rules
- Each value has exactly one owner
- When the owner goes out of scope, the value is dropped
- Ownership can be transferred (moved) or borrowed

### Borrowing Rules
- Multiple immutable borrows (`&T`) allowed simultaneously
- Only one mutable borrow (`&mut T`) at a time
- Cannot mix mutable and immutable borrows

### Lifetime Annotations
```rust
// Explicit lifetime when returning borrowed data
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct containing references
struct Parser<'a> {
    input: &'a str,
}
```

### Common Patterns
```rust
// Clone to avoid borrow issues (acceptable for small types)
let owned = borrowed.to_string();

// Use Cow for flexible ownership
use std::borrow::Cow;
fn process(input: Cow<'_, str>) -> String { /* ... */ }

// Arc/Rc for shared ownership
use std::sync::Arc;
let shared = Arc::new(data);
```

### Memory Safety Rules
- MUST NOT use raw pointers outside `unsafe` blocks
- SHOULD prefer `&[T]` over raw pointers for slices
- SHOULD use `Box<T>` for heap allocation
- SHOULD use `Arc<T>` or `Rc<T>` for shared ownership

---

## Module Organization

### File Structure
```
src/
├── lib.rs          # Library root (pub mod declarations)
├── main.rs         # Binary entry point (optional)
├── config.rs       # Single-file module
├── handlers/       # Multi-file module
│   ├── mod.rs      # Module root (pub mod + re-exports)
│   ├── auth.rs     # Submodule
│   └── api.rs      # Submodule
└── utils/
    ├── mod.rs
    └── helpers.rs
```

### mod.rs Patterns
```rust
// src/handlers/mod.rs
mod auth;
mod api;

// Re-export public items
pub use auth::AuthHandler;
pub use api::{ApiClient, ApiError};

// Keep private implementation details
use auth::internal_helper;
```

### Visibility Rules
- MUST use `pub` only for intentional public API
- SHOULD use `pub(crate)` for crate-internal items
- SHOULD use `pub(super)` for parent-module access
- MAY use `pub(in path)` for fine-grained control

### Prelude Pattern (Optional)
```rust
// src/prelude.rs
pub use crate::config::Config;
pub use crate::error::{Error, Result};
pub use crate::traits::*;
```

---

## Testing

### Unit Tests
Unit tests MUST be in the same file as the code being tested:
```rust
// src/calculator.rs
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, -1), -2);
    }
}
```

### Integration Tests
Integration tests MUST be in the `tests/` directory:
```
tests/
├── common/
│   └── mod.rs      # Shared test utilities
├── api_tests.rs    # Integration test file
└── cli_tests.rs    # Another test file
```

### Test Patterns
```rust
// Use test fixtures
#[test]
fn test_with_fixture() {
    let fixture = TestFixture::new();
    // test code
}

// Test error conditions
#[test]
fn test_invalid_input() {
    let result = parse("");
    assert!(result.is_err());
}

// Use should_panic for expected panics
#[test]
#[should_panic(expected = "index out of bounds")]
fn test_panic_condition() {
    let v = vec![1, 2, 3];
    let _ = v[10];
}
```

### Test Configuration
```rust
// Run expensive tests only with --ignored
#[test]
#[ignore]
fn expensive_test() { /* ... */ }

// Async tests (with tokio)
#[tokio::test]
async fn async_test() { /* ... */ }
```

### Testing Rules
- MUST have unit tests for public functions
- SHOULD have integration tests for public API
- SHOULD use `#[ignore]` for slow tests
- MUST NOT have tests that depend on execution order

---

## Documentation

### Item Documentation (///)
```rust
/// Calculates the factorial of a number.
///
/// # Arguments
///
/// * `n` - The number to calculate factorial for
///
/// # Returns
///
/// The factorial of `n`, or `None` if overflow occurs.
///
/// # Examples
///
/// ```
/// use mylib::factorial;
/// assert_eq!(factorial(5), Some(120));
/// ```
///
/// # Panics
///
/// This function does not panic.
pub fn factorial(n: u64) -> Option<u64> {
    // implementation
}
```

### Module Documentation (//!)
```rust
//! # Authentication Module
//!
//! This module provides authentication and authorization
//! functionality for the application.
//!
//! ## Features
//!
//! - JWT token validation
//! - Role-based access control
//! - Session management

mod jwt;
mod roles;
```

### Documentation Rules
- MUST document all public items
- MUST include `# Examples` for non-trivial functions
- SHOULD include `# Panics` if the function can panic
- SHOULD include `# Errors` for functions returning `Result`
- SHOULD include `# Safety` for unsafe functions
- MAY use `#[doc(hidden)]` for public-but-internal items

### Doc Tests
Examples in documentation are compiled and run as tests:
```rust
/// ```
/// # use mylib::Config;  // Hidden setup line
/// let config = Config::default();
/// assert!(config.is_valid());
/// ```
```

---

## Unsafe Code

### Minimization Rules
- MUST minimize use of `unsafe` blocks
- MUST encapsulate `unsafe` in safe abstractions
- MUST NOT use `unsafe` for convenience/performance without justification

### Documentation Requirements
```rust
/// Reads a value from the given pointer.
///
/// # Safety
///
/// The caller MUST ensure:
/// - `ptr` is valid and properly aligned
/// - `ptr` points to initialized memory
/// - No other references to this memory exist
pub unsafe fn read_ptr<T>(ptr: *const T) -> T {
    // SAFETY: Caller guarantees pointer validity per function contract
    unsafe { std::ptr::read(ptr) }
}
```

### Safe Abstractions
```rust
pub struct SafeBuffer {
    ptr: *mut u8,
    len: usize,
}

impl SafeBuffer {
    pub fn new(size: usize) -> Self {
        let ptr = unsafe {
            // SAFETY: size > 0 checked, layout is valid
            std::alloc::alloc(std::alloc::Layout::array::<u8>(size).unwrap())
        };
        Self { ptr, len: size }
    }

    // Safe public API
    pub fn get(&self, index: usize) -> Option<u8> {
        if index < self.len {
            // SAFETY: bounds checked above
            Some(unsafe { *self.ptr.add(index) })
        } else {
            None
        }
    }
}
```

### Unsafe Code Rules
- MUST add `// SAFETY:` comment before every `unsafe` block
- MUST document safety requirements in function docs
- SHOULD use `#[deny(unsafe_op_in_unsafe_fn)]`
- SHOULD audit unsafe code regularly

---

## Common Patterns

### Builder Pattern
```rust
#[derive(Debug, Clone, Default)]
pub struct RequestBuilder {
    url: String,
    headers: Vec<(String, String)>,
    timeout: Option<u64>,
}

impl RequestBuilder {
    pub fn new(url: impl Into<String>) -> Self {
        Self { url: url.into(), ..Default::default() }
    }

    pub fn header(mut self, key: &str, value: &str) -> Self {
        self.headers.push((key.to_string(), value.to_string()));
        self
    }

    pub fn timeout(mut self, seconds: u64) -> Self {
        self.timeout = Some(seconds);
        self
    }

    pub fn build(self) -> Request {
        Request { /* ... */ }
    }
}
```

### Newtype Pattern
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Email(String);

impl Email {
    pub fn new(value: &str) -> Result<Self, ValidationError> {
        if value.contains('@') {
            Ok(Self(value.to_string()))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

### Type State Pattern
```rust
pub struct Connection<State> {
    inner: TcpStream,
    _state: std::marker::PhantomData<State>,
}

pub struct Disconnected;
pub struct Connected;

impl Connection<Disconnected> {
    pub fn connect(addr: &str) -> Result<Connection<Connected>, Error> {
        let stream = TcpStream::connect(addr)?;
        Ok(Connection { inner: stream, _state: std::marker::PhantomData })
    }
}

impl Connection<Connected> {
    pub fn send(&mut self, data: &[u8]) -> Result<(), Error> { /* ... */ }
}
```

---

## Clippy Configuration

### Recommended Lints
Add to `Cargo.toml` or `clippy.toml`:
```toml
# Cargo.toml
[lints.clippy]
pedantic = "warn"
nursery = "warn"
unwrap_used = "deny"
expect_used = "warn"
```

### Allowing Specific Lints
```rust
#[allow(clippy::too_many_arguments)]
fn complex_function(/* many args */) { /* ... */ }
```

### CI Configuration
```bash
cargo clippy -- -D warnings -D clippy::unwrap_used
```
