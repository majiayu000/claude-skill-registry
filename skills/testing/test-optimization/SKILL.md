---
name: test-optimization
description: Advanced test optimization with cargo-nextest, property testing, and performance benchmarking. Use when optimizing test execution speed, implementing property-based tests, or analyzing test performance.
---

# Test Optimization for Episodic Memory

## cargo-nextest Integration

### Setup

```bash
# Install nextest
cargo install cargo-nextest --locked

# Run all tests with nextest
cargo nextest run

# Run specific test suite
cargo nextest run -p memory-core

# Run with CI profile
cargo nextest run --profile ci
```

### Configuration

Create `.config/nextest.toml`:

```toml
[profile.default]
retries = 0
fail-fast = true
slow-timeout = { period = "30s", terminate-after = 3 }

[profile.ci]
retries = 2
fail-fast = false
slow-timeout = { period = "60s", terminate-after = 5 }
test-threads = 4

[profile.quick]
# Fast feedback loop for development
fail-fast = true
slow-timeout = { period = "10s" }
test-threads = 8
```

## Property-Based Testing

### Episode ID Uniqueness Property

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_episode_id_uniqueness(
        task_descriptions in prop::collection::vec(any::<String>(), 1..100)
    ) {
        let rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(async {
            let memory = setup_memory().await;
            let mut ids = HashSet::new();

            for desc in task_descriptions {
                let id = memory.start_episode(
                    desc,
                    TaskContext::default(),
                    TaskType::CodeGeneration,
                ).await;

                // Property: all episode IDs must be unique
            prop_assert!(ids.insert(id), "Duplicate episode ID generated");
            }
        });
    }
}
```

### Reward Score Properties

```rust
proptest! {
    #[test]
    fn test_reward_score_bounds(
        efficiency in 0.0f64..1.0,
        quality in 0.0f64..1.0,
    ) {
        let score = calculate_reward_score(efficiency, quality);

        // Properties:
        // 1. Score is always non-negative
        prop_assert!(score >= 0.0);

        // 2. Perfect efficiency and quality yield high score
        if efficiency == 1.0 && quality == 1.0 {
            prop_assert!(score > 0.9);
        }

        // 3. Score is monotonic in efficiency
        let higher_eff_score = calculate_reward_score(
            (efficiency + 0.1).min(1.0),
            quality
        );
        prop_assert!(higher_eff_score >= score);
    }
}
```

## Test Selection Strategies

### Smart Test Selection by Changes

```bash
# Only test changed crates
CHANGED_CRATES=$(git diff --name-only HEAD~1 | \
    grep -E '^memory-.*/' | \
    cut -d/ -f1 | \
    sort -u)

for crate in $CHANGED_CRATES; do
    cargo nextest run -p $crate
done
```

### Tiered Testing Strategy

```bash
# Tier 1: Fast unit tests (< 1s)
cargo nextest run -E 'kind(lib) and not test(integration)'

# Tier 2: Integration tests
cargo nextest run -E 'kind(test)'

# Tier 3: Benchmarks (for validation)
cargo bench --no-run
```

## Performance Validation

### Criterion Benchmarks

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_episode_creation(c: &mut Criterion) {
    let rt = tokio::runtime::Runtime::new().unwrap();

    c.bench_function("episode_creation", |b| {
        b.to_async(&rt).iter(|| async {
            let memory = setup_memory().await;
            black_box(
                memory.start_episode(
                    "Benchmark task".to_string(),
                    TaskContext::default(),
                    TaskType::CodeGeneration,
                ).await
            )
        });
    });
}

criterion_group!(benches, bench_episode_creation);
criterion_main!(benches);
```

### Regression Detection

```bash
# Baseline
cargo bench --bench episode_ops -- --save-baseline main

# After changes
cargo bench --bench episode_ops -- --baseline main

# Fail if regression > 10%
cargo bench --bench episode_ops -- --baseline main --test
```

## Coverage Analysis

```bash
# Install tarpaulin
cargo install cargo-tarpaulin

# Generate coverage report
cargo tarpaulin --out Html --output-dir coverage

# Fail if coverage < 90%
cargo tarpaulin --fail-under 90
```

## Best Practices

1. **Use nextest profiles** - separate configs for dev/CI
2. **Implement property tests** - catch edge cases
3. **Monitor test duration** - identify slow tests
4. **Run benchmarks in CI** - detect performance regressions
5. **Track coverage trends** - maintain quality over time

## Proptest Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| `any::<T>()` | Random value of type T | `any::<String>()` |
| `prop::collection::vec()` | Collection of random values | `vec(any::<u32>(), 1..10)` |
| `1..N` | Range constraint | `1..100` |
| `prop::sample::subsequence()` | Random subset | `subsequence(vec, 5)` |

## Performance Targets

| Operation | Target (P95) | Actual |
|-----------|-------------|--------|
| Episode Creation | < 50ms | ~2.5 µs |
| Step Logging | < 20ms | ~1.1 µs |
| Episode Completion | < 500ms | ~3.8 µs |
| Pattern Extraction | < 1000ms | ~10.4 µs |
| Memory Retrieval | < 100ms | ~721 µs |
