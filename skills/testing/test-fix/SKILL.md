---
name: test-fix
description: Systematic approach to diagnosing and fixing failing tests in Rust projects. Use when tests fail and you need to diagnose root causes, fix async/await issues, handle race conditions, or resolve database connection problems.
---

# Test Fix

Systematic approach to diagnosing and fixing failing tests.

## Purpose
Quickly identify, diagnose, and resolve test failures in the Rust codebase.

## Process

### Step 1: Identify Failing Tests
```bash
# Run tests to see failures
cargo test --all

# Or run specific test suite
cargo test --test integration_memory
```

**Capture**:
- Test name
- Failure message
- Stack trace
- Module/file location

### Step 2: Reproduce Locally
```bash
# Run the specific failing test with output
cargo test test_name -- --exact --nocapture

# With debug logging
RUST_LOG=debug cargo test test_name -- --exact --nocapture

# Force single-threaded for race conditions
cargo test test_name -- --exact --nocapture --test-threads=1
```

### Step 3: Diagnose Root Cause

#### Common Failure Patterns

**Pattern 1: Async/Await Issues**
```
error: future cannot be sent between threads safely
```
**Diagnosis**: Missing `.await` or non-Send type across await
**Fix**:
- Add missing `.await`
- Use `Arc<Mutex<T>>` instead of `Rc<RefCell<T>>`
- Ensure all types are `Send + Sync`

**Pattern 2: Database Errors**
```
error: connection refused / timeout
```
**Diagnosis**: Database not available or wrong credentials
**Fix**:
- Check environment variables
- Use test database instance
- Verify connection string

**Pattern 3: Race Conditions**
```
assertion failed: expected X but got Y (intermittent)
```
**Diagnosis**: Concurrent access without proper synchronization
**Fix**:
- Add proper locking (`Mutex`, `RwLock`)
- Use sequential test execution
- Add synchronization barriers

**Pattern 4: Type Errors**
```
error: expected `Result<X>`, found `Result<Y>`
```
**Diagnosis**: Type mismatch after refactoring
**Fix**:
- Update function signatures
- Add type conversions
- Fix error type propagation

**Pattern 5: Lifetime Issues**
```
error: borrowed value does not live long enough
```
**Diagnosis**: Reference outlives owner
**Fix**:
- Clone data when needed
- Adjust lifetime parameters
- Use `Arc` for shared ownership

### Step 4: Implement Fix

#### Example: Fix Missing Await
```rust
// BEFORE (failing)
#[tokio::test]
async fn test_episode_creation() {
    let id = memory.start_episode("test", ctx); // Missing .await
    assert!(!id.is_empty());
}

// AFTER (fixed)
#[tokio::test]
async fn test_episode_creation() {
    let id = memory.start_episode("test", ctx).await.unwrap();
    assert!(!id.is_empty());
}
```

#### Example: Fix Race Condition
```rust
// BEFORE (flaky)
#[tokio::test]
async fn test_concurrent_writes() {
    let memory = create_test_memory().await;

    tokio::join!(
        memory.write_pattern(pattern1),
        memory.write_pattern(pattern2),
    );

    let count = memory.get_pattern_count().await;
    assert_eq!(count, 2); // Sometimes fails!
}

// AFTER (fixed)
#[tokio::test]
async fn test_concurrent_writes() {
    let memory = create_test_memory().await;

    // Use proper synchronization
    memory.write_pattern(pattern1).await.unwrap();
    memory.write_pattern(pattern2).await.unwrap();

    let count = memory.get_pattern_count().await;
    assert_eq!(count, 2); // Reliable
}
```

#### Example: Fix Database Connection
```rust
// BEFORE (failing)
#[tokio::test]
async fn test_turso_connection() {
    let client = TursoClient::new("hardcoded_url", "token").await;
    // Fails in CI
}

// AFTER (fixed)
#[tokio::test]
async fn test_turso_connection() {
    use std::env;

    let url = env::var("TEST_TURSO_URL")
        .unwrap_or_else(|_| "file:test.db".to_string());
    let token = env::var("TEST_TURSO_TOKEN")
        .unwrap_or_else(|_| "test_token".to_string());

    let client = TursoClient::new(&url, &token).await;
    assert!(client.is_ok());
}
```

### Step 5: Verify Fix
```bash
# Run the fixed test multiple times
for i in {1..10}; do
    cargo test test_name -- --exact || break
done

# Run full test suite
cargo test --all

# Run with different thread counts
cargo test --all -- --test-threads=1
cargo test --all -- --test-threads=4
```

### Step 6: Regression Prevention

Add tests for the bug if not covered:
```rust
#[tokio::test]
async fn test_regression_issue_123() {
    // Test for the specific bug that was fixed
    let memory = create_test_memory().await;

    // Reproduce the bug scenario
    let result = memory.problematic_operation().await;

    // Ensure it doesn't happen again
    assert!(result.is_ok());
}
```

## Systematic Debugging Checklist

- [ ] Run failing test in isolation
- [ ] Check test environment (env vars, file paths)
- [ ] Review recent changes (git diff)
- [ ] Check for missing `.await` on async calls
- [ ] Verify database connections are valid
- [ ] Look for race conditions (run with --test-threads=1)
- [ ] Check type compatibility after refactoring
- [ ] Review error propagation (? operator, unwrap)
- [ ] Verify test cleanup (no leftover state)
- [ ] Check for platform-specific issues

## Tools

### 1. Cargo Test with Filters
```bash
# Run only tests matching pattern
cargo test storage

# Exclude tests
cargo test -- --skip integration
```

### 2. Logging
```bash
# Debug level
RUST_LOG=debug cargo test

# Trace level (very verbose)
RUST_LOG=trace cargo test

# Specific module
RUST_LOG=memory_core=debug cargo test
```

### 3. Backtrace
```bash
# Full backtrace on panic
RUST_BACKTRACE=full cargo test
```

### 4. Valgrind (memory issues)
```bash
# Check for memory leaks
cargo build --tests
valgrind --leak-check=full ./target/debug/deps/test_binary
```

## Batch Fixing Multiple Tests

When multiple tests fail for the same reason:

```bash
# List all failing tests
cargo test 2>&1 | grep "test.*FAILED"

# Fix common issue (e.g., missing await)
# Use sed or manual editing

# Verify all fixed
cargo test --all
```

## Documentation

After fixing, update:
1. **Test comment**: Explain what the test verifies
2. **Code comment**: Note why the fix was needed
3. **Commit message**: Reference issue/test name
4. **CHANGELOG**: If user-facing impact

## Example Commit Message

```
[tests] fix async/await in episode_creation test

- Added missing .await on start_episode call
- Test was panicking with "cannot call async fn without await"
- Added proper error handling with unwrap
- Verified fix runs 10x without failure

Fixes: test_episode_creation
```

## Performance Testing After Fix

```bash
# Ensure fix doesn't slow down tests
time cargo test --all

# Compare before/after
# Before: 2.3s
# After: 2.4s (acceptable)
```

## When to Skip vs Fix

### Skip (temporarily) if:
- Test requires external service that's down
- Platform-specific issue being investigated
- Known upstream bug

```rust
#[tokio::test]
#[ignore = "Requires external Turso instance"]
async fn test_production_sync() {
    // ...
}
```

### Fix immediately if:
- Logic error in code
- Incorrect assertion
- Missing error handling
- Race condition

## Escalation

If unable to fix after reasonable effort:
1. Document findings in issue
2. Add `#[ignore]` with reason
3. Create detailed bug report
4. Request help from goap-agent
