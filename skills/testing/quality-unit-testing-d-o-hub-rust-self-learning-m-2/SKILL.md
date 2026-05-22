---
name: quality-unit-testing
description: Write high-quality Rust unit tests following best practices. Use when writing new tests, reviewing test code, or improving test quality. Emphasizes clear naming, AAA pattern, isolation, and deployment confidence.
---

# Quality Unit Testing for Rust

Write tests that catch real bugs and provide deployment confidence.

## Core Principles

**Quality over coverage**: Tests should catch real bugs, not just boost percentages.

## Quick Reference

### Naming: `test_<function>_<scenario>_<expected>`

```rust
#[test]
fn test_process_payment_insufficient_funds_returns_error()

#[tokio::test]
async fn test_withdraw_valid_amount_decreases_balance()
```

### AAA Pattern (Arrange-Act-Assert)

```rust
#[test]
fn test_account_withdraw_decreases_balance() {
    // Arrange
    let mut account = Account::new(100);

    // Act
    let result = account.withdraw(30);

    // Assert
    assert!(result.is_ok());
    assert_eq!(account.balance(), 70);
}
```

### Isolation

✓ Mock: APIs, databases, file systems, external services
✗ Don't mock: Value types, pure functions, code under test

### Single Responsibility

Each test verifies ONE behavior with ONE reason to fail.

## Rust-Specific Patterns

```rust
// Async tests
#[tokio::test]
async fn test_async_operation() { /* ... */ }

// Result-based tests
#[test]
fn test_operation() -> anyhow::Result<()> { /* ... */ }

// Test builders
let episode = TestEpisodeBuilder::new()
    .with_task("Test task")
    .completed(true)
    .build();

// RAII cleanup
struct TestDb(TempDir);
impl Drop for TestDb { fn drop(&mut self) { /* auto cleanup */ } }
```

## Success Metrics

✓ Deploy without manual testing
✓ Test failures pinpoint exact problems
✓ Refactoring doesn't break unrelated tests
✓ Tests run in milliseconds

## Workflow

**Creating Tests**:
1. Understand the code behavior
2. Identify risks
3. Write failing test first (red-green-refactor)
4. Apply AAA pattern
5. Isolate dependencies
6. Verify speed (milliseconds)

**Reviewing Tests**:
1. Run analysis script
2. Check naming conventions
3. Ensure isolation
4. Confirm single responsibility
