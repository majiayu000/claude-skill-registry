---
name: chicago-tdd-pattern
description: "Master Chicago TDD (state-based testing). Create tests that verify observable behavior with real collaborators. Use chicago-tdd-tools 1.4.0 AAA pattern. When writing tests, verifying implementation correctness, improving test quality, or analyzing test coverage. Covers: unit tests, integration tests, mutation testing, assertion analysis."
allowed_tools: "Read, Write, Bash(cargo make test:*), Bash(cargo make bench:*)"
---

# Chicago TDD Pattern Skill

## Core Philosophy

**Chicago TDD = State-based testing with real collaborators**

Verify observable behavior changes:
- Return values
- State mutations
- Side effects
- Actual system effects

**NOT** internal implementation, method calls, or mocks (except London TDD in tests).

## AAA Pattern (Arrange-Act-Assert)

```rust
#[test]
fn test_feature() {
    // ARRANGE: Set up real objects (no mocks)
    let manager = LockfileManager::new(temp_dir.path());

    // ACT: Call the public API being tested
    manager.upsert("pkg", "1.0.0", "sha256", "url").unwrap();

    // ASSERT: Verify observable state changed
    let entry = manager.get("pkg").unwrap().unwrap();
    assert_eq!(entry.version, "1.0.0");  // State changed ✓
}
```

## Test Organization

### Unit Tests (Fast, Focused)

Location: `src/module.rs` with `#[cfg(test)]` module

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cache_insertion() {
        // Arrange
        let mut cache = Cache::new();

        // Act
        cache.insert("key", "value");

        // Assert
        assert_eq!(cache.get("key"), Some("value"));
    }
}
```

**Focus**: Single responsibility, fast execution, deterministic results

### Integration Tests (End-to-End)

Location: `crates/*/tests/` directory

```rust
// tests/integration_test.rs
#[test]
fn test_full_pipeline() {
    let config = Config::load("test.toml").unwrap();
    let result = generate(&config).unwrap();

    assert!(result.contains("generated code"));
    assert!(Path::new("output.rs").exists());
}
```

**Focus**: Real filesystem, file I/O, full workflows

### E2E Tests (System-Level)

Location: `crates/ggen-e2e/tests/` with testcontainers

```rust
#[tokio::test]
async fn test_with_docker() {
    let container = RustContainer::default().start().await.unwrap();
    let output = container.exec("cargo make test").await.unwrap();

    assert!(output.contains("test result: ok"));
}
```

**Focus**: Real containers, actual system behavior, byte-for-byte validation

## Test Quality Metrics

### Mutation Score (Target: > 90%)

Tests should catch code mutations (changes):

```bash
cargo make test-audit mutations

# Mutation: Change == to !=
let x = 5;
if x == 5 { }  →  if x != 5 { }

# Good test catches this:
assert_eq!(result, 5);  // Would fail if == changed to !=
```

**Surviving mutations indicate weak tests** - add more assertions.

### Assertion Density (Target: > 1 per function)

Count assertions per function:

```rust
#[test]
fn test_parsing() {
    // Arrange
    let input = "key: value";

    // Act
    let result = parse(input).unwrap();

    // Assert: Multiple assertions per test ✓
    assert_eq!(result.key, "key");      // Assertion 1
    assert_eq!(result.value, "value");  // Assertion 2
    assert!(result.valid());             // Assertion 3
}
```

**Low assertion density** = incomplete testing.

### False Positives (Target: Zero)

Tests passing when implementation broken:

```rust
// ❌ BAD: Test passes even if add() is broken
#[test]
fn test_add() {
    let result = add(2, 3);
    // Missing assertion!
}

// ✓ GOOD: Test actually verifies behavior
#[test]
fn test_add() {
    let result = add(2, 3);
    assert_eq!(result, 5);  // Catches bugs ✓
}
```

## Exemptions: unwrap/expect in Tests

ALLOWED in test/benchmark code:

```rust
#[test]
fn test_something() {
    let obj = Object::new().unwrap();  // ✓ ALLOWED
    assert_eq!(obj.value(), 42);
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_error() {
        let result = parse("invalid");
        assert!(result.is_err());  // ✓ ALLOWED
    }
}

#[bench]
fn bench_iteration(b: &mut Bencher) {
    let data = setup().unwrap();  // ✓ ALLOWED in benches
    b.iter(|| process(&data))
}
```

**Rationale**: Tests should fail fast on setup errors. Don't hide test issues.

## Test Organization Best Practices

### 1. One Assertion Per Concept

```rust
// ✓ Good: Each assertion tests one thing
#[test]
fn test_user_creation() {
    let user = User::new("Alice", "alice@example.com").unwrap();
    assert_eq!(user.name, "Alice");         // Tests name
    assert_eq!(user.email, "alice@example.com");  // Tests email
    assert!(user.valid());                  // Tests validity
}

// ❌ Bad: Combined assertions hide failures
#[test]
fn test_user_creation() {
    let user = User::new("Alice", "alice@example.com").unwrap();
    assert!(user.name == "Alice" && user.email == "alice@example.com");
    // If either fails, both fail
}
```

### 2. Test One Error Path Per Test

```rust
// ✓ Good: Separate tests for each error
#[test]
fn test_parse_empty_input_error() {
    let result = parse("");
    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), Error::EmptyInput);
}

#[test]
fn test_parse_invalid_syntax_error() {
    let result = parse("invalid {syntax");
    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), Error::SyntaxError);
}

// ❌ Bad: Multiple error paths in one test
#[test]
fn test_parse_errors() {
    // This test does too much
}
```

### 3. Use Descriptive Test Names

```rust
// ✓ Good: Name tells you what is tested
#[test]
fn test_cache_returns_most_recent_value() { }

#[test]
fn test_cache_evicts_lru_on_full() { }

#[test]
fn test_cache_handles_concurrent_access() { }

// ❌ Bad: Unclear what's being tested
#[test]
fn test_cache_1() { }

#[test]
fn test_cache() { }
```

## Benchmarking with Criterion

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_generation(c: &mut Criterion) {
    c.bench_function("generate_small", |b| {
        b.iter(|| generate(black_box("small_input")))
    });

    c.bench_function("generate_large", |b| {
        b.iter(|| generate(black_box("large_input")))
    });
}

criterion_group!(benches, bench_generation);
criterion_main!(benches);
```

**Run benchmarks**:

```bash
cargo make bench              # Run all benchmarks
cargo make bench-compare      # Compare versions
```

## Property-Based Testing (proptest)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_parse_roundtrip(s in r#"[a-z]+""#) {
        let parsed = parse(&s).unwrap();
        let serialized = serialize(&parsed);
        prop_assert_eq!(s, serialized);
    }
}
```

**Advantage**: Tests many inputs automatically, catches edge cases.

## Test Frameworks Used

| Framework | Purpose | Use When |
|-----------|---------|----------|
| chicago-tdd-tools 1.4.0 | AAA pattern | Writing unit tests |
| proptest 1.8 | Property-based | Testing invariants |
| criterion 0.7 | Benchmarking | Performance tracking |
| testcontainers 0.25 | E2E with docker | Integration testing |
| assert_cmd 2.0 | CLI testing | Command validation |
| assert_fs 1.1 | Filesystem testing | File operations |
| mockall 0.13 | London TDD mocking | Test-only mocking |
| insta 1.43 | Snapshot testing | Golden files |

## Running Tests

```bash
# Quick unit tests only
cargo make test-unit        # ~10s

# All tests
cargo make test             # ~30s (120s escalation)

# Specific test
cargo test test_name        # Single test

# With output
cargo test -- --nocapture  # See println! output

# Benchmarks
cargo make bench            # All benchmarks
cargo bench bench_name      # Specific benchmark

# Mutation testing
cargo make test-audit mutations
```

## Success Criteria

✓ All tests pass
✓ Mutation score > 90%
✓ Assertion density > 1 per function
✓ No false positives
✓ Error paths tested
✓ Chicago TDD pattern used
✓ No flaky tests
✓ SLO timeouts met

## Key Principles

1. **Real Objects**: Use actual implementations, not mocks
2. **Observable State**: Test what you can see, not internals
3. **Comprehensive**: Test happy path, errors, edge cases
4. **Deterministic**: Same inputs = same results, always
5. **Fast**: Unit tests should run instantly
6. **Focused**: Each test has one purpose
7. **Mutation-Resistant**: Tests catch code changes

## Common Testing Mistakes

### ❌ Testing Internals

```rust
// WRONG: Testing internal detail
#[test]
fn test_cache_internal_structure() {
    let cache = Cache::new();
    assert_eq!(cache.data.capacity(), 100);  // Wrong!
}

// CORRECT: Test observable behavior
#[test]
fn test_cache_stores_and_retrieves() {
    let cache = Cache::new();
    cache.insert("key", "value");
    assert_eq!(cache.get("key"), Some("value"));
}
```

### ❌ Using Mocks

```rust
// WRONG: Mocks hide real behavior
#[test]
fn test_with_mock() {
    let mut mock = MockService::new();
    mock.expect_call().returning(|| 42);
    // Mock doesn't test real behavior!
}

// CORRECT: Use real objects
#[test]
fn test_with_real_service() {
    let service = RealService::new();
    let result = service.call();
    assert_eq!(result, 42);  // Tests real behavior ✓
}
```

### ❌ No Assertions

```rust
// WRONG: Test runs but doesn't verify
#[test]
fn test_something() {
    let result = do_something();  // Missing assertion!
}

// CORRECT: Assert expected behavior
#[test]
fn test_something() {
    let result = do_something();
    assert_eq!(result, expected);  // Verifies behavior ✓
}
```

## See Also

- `reference.md` - Detailed testing patterns
- `examples.md` - Real-world test examples
- Chicago TDD documentation
- criterion.rs benchmarking guide
