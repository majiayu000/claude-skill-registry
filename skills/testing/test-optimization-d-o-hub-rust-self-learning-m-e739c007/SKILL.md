---
name: test-optimization
description: Advanced test optimization with cargo-nextest, property testing, and performance benchmarking. Use when optimizing test execution speed, implementing property-based tests, or analyzing test performance.
---

# Test Optimization

Advanced test optimization with cargo-nextest, property testing, and benchmarking.

## cargo-nextest Integration

```bash
# Install
cargo install cargo-nextest --locked

# Run all tests
cargo nextest run

# CI profile (with retries)
cargo nextest run --profile ci
```

### Configuration (.config/nextest.toml)

```toml
[profile.default]
slow-timeout = { period = "30s", terminate-after = 3 }

[profile.ci]
retries = 2
fail-fast = false
test-threads = 4
```

## Property-Based Testing (proptest)

```rust
proptest! {
    #[test]
    fn test_episode_id_uniqueness(
        tasks in prop::collection::vec(any::<String>(), 1..100)
    ) {
        let rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(async {
            let memory = setup_memory().await;
            let mut ids = HashSet::new();
            for desc in tasks {
                let id = memory.start_episode(desc, ctx, type_).await;
                prop_assert!(ids.insert(id));
            }
        });
    }
}
```

## Performance Targets

| Operation | Target | Actual |
|-----------|--------|--------|
| Episode Creation | < 50ms | ~2.5 µs |
| Step Logging | < 20ms | ~1.1 µs |
| Pattern Extraction | < 1000ms | ~10.4 µs |
| Memory Retrieval | < 100ms | ~721 µs |

## Best Practices

- Use nextest profiles for dev/CI separation
- Implement property tests for edge cases
- Monitor test duration
- Track coverage trends
