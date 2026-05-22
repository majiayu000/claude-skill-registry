---
name: rust-testing-verification
description: Comprehensive testing strategies for Rust including property-based testing with proptest, fuzz testing with cargo-fuzz, benchmark testing with Criterion, contract testing for traits, and Miri for undefined behavior detection. Use when writing tests, ensuring code correctness, detecting edge cases, or measuring performance.
---

# Rust Testing & Verification

*Production testing strategies for correctness and performance validation*

## Version Context
- **proptest**: 1.x
- **Criterion**: 0.5.x
- **cargo-fuzz**: 0.11.x
- **cargo-miri**: Latest nightly

## When to Use This Skill

- Writing comprehensive test suites
- Finding edge cases automatically
- Verifying trait implementations
- Benchmarking performance
- Detecting undefined behavior
- Ensuring code correctness

## Property-Based Testing

### Basic Property Tests

```rust
use proptest::prelude::*;

proptest! {
    /// Property: Serialization round-trip preserves data
    #[test]
    fn user_serialization_roundtrip(user in any::<User>()) {
        let serialized = serde_json::to_string(&user)?;
        let deserialized: User = serde_json::from_str(&serialized)?;
        prop_assert_eq!(user, deserialized);
    }

    /// Property: Email validation accepts valid emails
    #[test]
    fn email_validation_accepts_valid_emails(
        email in r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    ) {
        let result = Email::parse(&email);
        prop_assert!(result.is_ok());
    }

    /// Property: Vec operations maintain size invariants
    #[test]
    fn vec_push_increases_len(
        mut vec in prop::collection::vec(any::<i32>(), 0..100),
        value in any::<i32>()
    ) {
        let original_len = vec.len();
        vec.push(value);
        prop_assert_eq!(vec.len(), original_len + 1);
    }
}
```

### Advanced Property Tests

```rust
proptest! {
    /// Property: Account balance invariants
    #[test]
    fn account_balance_invariants(
        initial_balance in 0u64..1_000_000,
        transactions in prop::collection::vec(
            prop::oneof![
                (1u64..10_000).prop_map(Transaction::Deposit),
                (1u64..10_000).prop_map(Transaction::Withdrawal),
            ],
            1..100
        )
    ) {
        let mut account = Account::new(initial_balance);
        let mut expected_balance = initial_balance;

        for transaction in transactions {
            match transaction {
                Transaction::Deposit(amount) => {
                    account.deposit(amount)?;
                    expected_balance += amount;
                }
                Transaction::Withdrawal(amount) => {
                    if account.balance() >= amount {
                        account.withdraw(amount)?;
                        expected_balance -= amount;
                    }
                }
            }

            // Invariant: balance must always be non-negative
            prop_assert!(account.balance() >= 0);
            prop_assert_eq!(account.balance(), expected_balance);
        }
    }

    /// Property: Sorted vector stays sorted after insertion
    #[test]
    fn sorted_insert_maintains_order(
        mut sorted_vec in prop::collection::vec(any::<i32>(), 0..100)
            .prop_map(|mut v| { v.sort(); v }),
        value in any::<i32>()
    ) {
        sorted_vec.insert(
            sorted_vec.binary_search(&value).unwrap_or_else(|i| i),
            value
        );

        // Verify still sorted
        for i in 1..sorted_vec.len() {
            prop_assert!(sorted_vec[i - 1] <= sorted_vec[i]);
        }
    }
}
```

### Custom Generators

```rust
use proptest::strategy::{Strategy, BoxedStrategy};

/// Custom strategy for generating valid users
fn arb_user() -> BoxedStrategy<User> {
    (
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        r"[A-Z][a-z]+ [A-Z][a-z]+",
        13u8..=120u8,
    )
        .prop_map(|(email, name, age)| {
            User {
                id: UserId::new(),
                email,
                name,
                age,
                created_at: chrono::Utc::now(),
            }
        })
        .boxed()
}

proptest! {
    #[test]
    fn test_with_valid_users(user in arb_user()) {
        // Test only runs with valid user data
        prop_assert!(user.age >= 13 && user.age <= 120);
        prop_assert!(user.email.contains('@'));
    }
}
```

## Fuzz Testing

### Basic Fuzz Target

```rust
// fuzz/fuzz_targets/parse_input.rs
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    // Should never panic on arbitrary input
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = parse_user_input(s);
    }
});
```

### Structured Fuzzing

```rust
// fuzz/fuzz_targets/api_request.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use arbitrary::Arbitrary;

#[derive(Debug, Arbitrary)]
struct FuzzApiRequest {
    method: String,
    path: String,
    headers: Vec<(String, String)>,
    body: Vec<u8>,
}

fuzz_target!(|req: FuzzApiRequest| {
    // Test API handler doesn't panic on arbitrary inputs
    let _ = handle_request(
        req.method,
        req.path,
        req.headers,
        req.body,
    );
});
```

### Regression Tests from Fuzzing

```rust
#[cfg(test)]
mod fuzz_regression_tests {
    use super::*;

    /// Edge cases discovered by fuzzing
    #[test]
    fn test_known_edge_cases() {
        let edge_cases = vec![
            "",                    // Empty input
            "\0",                  // Null byte
            "🦀",                  // Unicode
            &"x".repeat(10_000),   // Large input
            "\n\r\t",              // Whitespace
            "{{{{",                // Unbalanced braces
        ];

        for case in edge_cases {
            // Should handle gracefully without panicking
            let result = parse_user_input(case);
            assert!(result.is_ok() || result.is_err());
        }
    }
}
```

## Benchmark Testing

### Basic Criterion Benchmarks

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};

fn benchmark_user_operations(c: &mut Criterion) {
    let mut group = c.benchmark_group("user_operations");

    // Benchmark with different input sizes
    for size in [10, 100, 1000, 10000].iter() {
        group.bench_with_input(
            BenchmarkId::new("lookup", size),
            size,
            |b, &size| {
                let users = generate_test_users(size);
                b.iter(|| {
                    let id = &users[rand::random::<usize>() % users.len()].id;
                    black_box(lookup_user(black_box(id)))
                })
            },
        );
    }

    group.finish();
}

criterion_group!(benches, benchmark_user_operations);
criterion_main!(benches);
```

### Advanced Benchmarking

```rust
use criterion::{Criterion, BenchmarkId, Throughput};
use std::time::Duration;

fn benchmark_serialization(c: &mut Criterion) {
    let mut group = c.benchmark_group("serialization");

    // Configure statistical parameters
    group.sample_size(100);
    group.measurement_time(Duration::from_secs(10));
    group.confidence_level(0.95);

    for size in [10, 100, 1000].iter() {
        let data = generate_data(*size);

        // Set throughput for bytes per second calculation
        group.throughput(Throughput::Bytes(data.len() as u64));

        group.bench_with_input(
            BenchmarkId::new("json", size),
            &data,
            |b, data| {
                b.iter(|| {
                    let serialized = serde_json::to_string(black_box(data)).unwrap();
                    black_box(serialized)
                })
            },
        );

        group.bench_with_input(
            BenchmarkId::new("bincode", size),
            &data,
            |b, data| {
                b.iter(|| {
                    let serialized = bincode::serialize(black_box(data)).unwrap();
                    black_box(serialized)
                })
            },
        );
    }

    group.finish();
}
```

### Allocation Benchmarking

```rust
#[cfg(test)]
mod allocation_tests {
    use super::*;

    #[test]
    fn test_zero_allocation_path() {
        let allocations_before = allocation_counter::current();

        // Critical path that should not allocate
        let result = process_request_zero_alloc(&input);

        let allocations_after = allocation_counter::current();
        let total_allocations = allocations_after - allocations_before;

        assert_eq!(
            total_allocations, 0,
            "Critical path allocated {} bytes",
            total_allocations
        );
    }
}
```

## Contract Testing

### Trait Contract Tests

```rust
use async_trait::async_trait;

#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn get_user(&self, id: UserId) -> Result<User, RepositoryError>;
    async fn save_user(&self, user: &User) -> Result<(), RepositoryError>;
}

/// Contract tests that all implementations must satisfy
#[cfg(test)]
pub mod contract_tests {
    use super::*;

    pub async fn test_user_repository_contract<R: UserRepository>(repo: R) {
        // Test: Save and retrieve should be consistent
        let user = User::new("test@example.com".to_string(), "Test User".to_string());

        repo.save_user(&user).await.unwrap();
        let retrieved = repo.get_user(user.id).await.unwrap();

        assert_eq!(user.id, retrieved.id);
        assert_eq!(user.email, retrieved.email);
        assert_eq!(user.name, retrieved.name);
    }

    pub async fn test_user_repository_not_found<R: UserRepository>(repo: R) {
        // Test: Getting non-existent user should return error
        let non_existent_id = UserId::new();
        let result = repo.get_user(non_existent_id).await;

        assert!(matches!(result, Err(RepositoryError::NotFound)));
    }
}

/// Apply contract tests to concrete implementation
#[tokio::test]
async fn postgres_repository_satisfies_contract() {
    let repo = PostgresUserRepository::new(get_test_db().await);
    contract_tests::test_user_repository_contract(repo.clone()).await;
    contract_tests::test_user_repository_not_found(repo).await;
}

#[tokio::test]
async fn in_memory_repository_satisfies_contract() {
    let repo = InMemoryUserRepository::new();
    contract_tests::test_user_repository_contract(repo.clone()).await;
    contract_tests::test_user_repository_not_found(repo).await;
}
```

## Miri for Undefined Behavior Detection

### Using Miri

```bash
# Install Miri
rustup +nightly component add miri

# Run tests with Miri
cargo +nightly miri test

# Run specific test
cargo +nightly miri test test_concurrent_access
```

### Miri-Compatible Tests

```rust
#[cfg(test)]
mod miri_tests {
    use super::*;

    #[test]
    fn test_safe_concurrent_access() {
        use std::sync::Arc;
        use std::thread;

        let counter = Arc::new(AtomicCounter::new());
        let mut handles = vec![];

        for _ in 0..10 {
            let counter_clone = counter.clone();
            handles.push(thread::spawn(move || {
                for _ in 0..100 {
                    counter_clone.increment();
                }
            }));
        }

        for handle in handles {
            handle.join().unwrap();
        }

        assert_eq!(counter.get(), 1000);
    }
}
```

## Table-Driven Tests

### Data-Driven Test Cases

```rust
#[cfg(test)]
mod table_driven_tests {
    use super::*;

    #[test]
    fn test_email_validation() {
        let test_cases = vec![
            ("test@example.com", true),
            ("user+tag@domain.co.uk", true),
            ("invalid.email", false),
            ("@example.com", false),
            ("user@", false),
            ("", false),
        ];

        for (input, expected_valid) in test_cases {
            let result = Email::parse(input);
            assert_eq!(
                result.is_ok(),
                expected_valid,
                "Email validation failed for: {}",
                input
            );
        }
    }

    #[test]
    fn test_status_code_mapping() {
        let test_cases = vec![
            (ApiError::ValidationError(_), StatusCode::BAD_REQUEST),
            (ApiError::Unauthorized, StatusCode::UNAUTHORIZED),
            (ApiError::Forbidden, StatusCode::FORBIDDEN),
            (ApiError::NotFound, StatusCode::NOT_FOUND),
            (ApiError::InternalError, StatusCode::INTERNAL_SERVER_ERROR),
        ];

        for (error, expected_status) in test_cases {
            let status = error.status_code();
            assert_eq!(
                status, expected_status,
                "Status code mismatch for error: {:?}",
                error
            );
        }
    }
}
```

## Best Practices

1. **Use property tests** for invariant checking
2. **Fuzz parsers** and deserializers extensively
3. **Benchmark hot paths** with Criterion
4. **Write contract tests** for trait implementations
5. **Run Miri** on unsafe code and concurrent code
6. **Table-driven tests** for comprehensive coverage
7. **Regression tests** for bugs found in production
8. **Integration tests** with real dependencies (testcontainers)

## Common Dependencies

```toml
[dev-dependencies]
proptest = "1"
criterion = { version = "0.5", features = ["html_reports"] }
testcontainers = "0.23"

[dependencies]
# For fuzz testing
arbitrary = { version = "1", optional = true, features = ["derive"] }

[features]
fuzzing = ["arbitrary"]
```

## CI Integration

```yaml
# Run all test suites in CI
- name: Unit tests
  run: cargo test --workspace

- name: Property tests
  run: cargo test --workspace -- --ignored proptest

- name: Miri (UB detection)
  run: |
    rustup component add miri
    cargo miri test

- name: Benchmarks (smoke test)
  run: cargo bench --no-run

- name: Fuzz (smoke test)
  run: |
    cargo install cargo-fuzz
    timeout 60s cargo fuzz run parse_input || true
```
