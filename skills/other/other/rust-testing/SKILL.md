---
name: rust-testing
description: Write and run Rust tests using cargo test with unit tests, integration tests, doc tests, and property-based testing. Use when writing Rust tests or setting up test infrastructure.
---

# Rust Testing Skill

## When to Activate

Activate this skill when:
- Writing Rust unit tests
- Creating integration tests
- Working with doc tests
- Setting up property-based testing
- Running benchmarks

## Quick Commands

```bash
# Run all tests
cargo test

# With output
cargo test -- --nocapture

# Run specific test
cargo test test_user_create

# Run tests in module
cargo test auth::

# Run ignored tests
cargo test -- --ignored

# Doc tests only
cargo test --doc

# Integration tests only
cargo test --test integration
```

## Unit Tests (Same File)

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, -1), -2);
    }
}
```

## Test Attributes

```rust
#[test]
fn regular_test() { }

#[test]
#[ignore]
fn slow_test() { }  // Skip unless --ignored

#[test]
#[should_panic]
fn test_panic() {
    panic!("This should panic");
}

#[test]
#[should_panic(expected = "specific message")]
fn test_panic_message() {
    panic!("specific message here");
}

#[test]
fn test_with_result() -> Result<(), String> {
    let result = some_operation()?;
    assert_eq!(result, expected);
    Ok(())
}
```

## Assertions

```rust
// Basic
assert_eq!(1 + 1, 2);
assert_ne!(1 + 1, 3);
assert!(true);

// With messages
assert_eq!(result, expected, "values should match: got {}", result);

// Pattern matching
assert!(matches!(value, Pattern::Variant(_)));

// Option/Result
assert!(some_option.is_some());
assert!(some_result.is_ok());
```

## Integration Tests

```rust
// tests/api_integration.rs
use my_crate::{Config, Server};

#[test]
fn test_server_startup() {
    let config = Config::default();
    let server = Server::new(config);
    assert!(server.start().is_ok());
}
```

## Directory Structure

```
project/
├── Cargo.toml
├── src/
│   ├── lib.rs          # Unit tests in #[cfg(test)]
│   └── user.rs         # Module with inline tests
└── tests/              # Integration tests
    ├── common/
    │   └── mod.rs      # Shared utilities
    └── api_test.rs
```

## Mocking with Traits

```rust
pub trait UserRepository {
    fn find_by_id(&self, id: u64) -> Option<User>;
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    struct MockUserRepo {
        users: HashMap<u64, User>,
    }

    impl UserRepository for MockUserRepo {
        fn find_by_id(&self, id: u64) -> Option<User> {
            self.users.get(&id).cloned()
        }
    }

    #[test]
    fn test_user_service() {
        let mut users = HashMap::new();
        users.insert(1, User { id: 1, email: "test@example.com".into() });
        let repo = MockUserRepo { users };

        let service = UserService::new(Box::new(repo));
        let user = service.get_user(1).unwrap();
        assert_eq!(user.email, "test@example.com");
    }
}
```

## Async Testing (tokio)

```rust
#[tokio::test]
async fn test_async_operation() {
    let result = fetch_data().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_with_timeout() {
    let result = tokio::time::timeout(
        Duration::from_secs(5),
        slow_operation()
    ).await;
    assert!(result.is_ok());
}
```

## Doc Tests

```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// use my_crate::add;
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Property-Based Testing (proptest)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_add_commutative(a: i32, b: i32) {
        prop_assert_eq!(add(a, b), add(b, a));
    }
}
```

## Coverage

```bash
# Using cargo-tarpaulin
cargo install cargo-tarpaulin
cargo tarpaulin --out Html

# Using cargo-llvm-cov
cargo install cargo-llvm-cov
cargo llvm-cov --html
```

## Related Resources

See `AgentUsage/testing_rust.md` for complete documentation including:
- Benchmarking with criterion
- Setup/teardown patterns
- Mockall crate usage
- CI configuration
