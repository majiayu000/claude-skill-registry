---
name: rust-async-testing
description: Comprehensive async/tokio testing patterns for episodic memory operations. Use when writing tests for async functions, time-based operations, concurrent tasks, or tokio runtime management.
---

# Rust Async Testing Patterns

This skill provides best practices for testing async Rust code with Tokio in the episodic memory system.

## Core Patterns

### 1. Basic Async Test Setup

```rust
use tokio::test;

#[tokio::test]
async fn test_episode_creation() {
    let memory = SelfLearningMemory::new(Default::default()).await?;
    let episode_id = memory.start_episode(
        "Test task".to_string(),
        TaskContext::default(),
        TaskType::CodeGeneration,
    ).await;
    assert!(!episode_id.is_empty());
}
```

### 2. Time-Based Testing with Paused Time

For operations involving `tokio::time::sleep` or timeouts:

```rust
#[tokio::test(start_paused = true)]
async fn test_pattern_extraction_timeout() {
    let memory = setup_memory().await;

    // Time advances only when awaited
    let start = tokio::time::Instant::now();
    tokio::time::sleep(Duration::from_secs(5)).await;

    // Actual elapsed time is near-zero
    assert!(start.elapsed().as_millis() < 100);
}
```

### 3. Concurrent Operation Testing

```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_concurrent_episode_operations() {
    let memory = Arc::new(setup_memory().await);

    let handles: Vec<_> = (0..10)
        .map(|i| {
            let memory = memory.clone();
            tokio::spawn(async move {
                memory.start_episode(
                    format!("Task {}", i),
                    TaskContext::default(),
                    TaskType::CodeGeneration,
                ).await
            })
        })
        .collect();

    let results = futures::future::join_all(handles).await;
    assert_eq!(results.len(), 10);
}
```

### 4. Storage Backend Mocking

```rust
#[tokio::test]
async fn test_episode_with_mock_storage() {
    let mock_turso = MockTursoStorage::new();
    let mock_redb = MockRedbCache::new();

    mock_turso.expect_create_episode()
        .times(1)
        .returning(|_| Ok(()));

    let memory = SelfLearningMemory::with_storage(
        mock_turso,
        mock_redb,
    ).await?;

    memory.start_episode(/* ... */).await;
}
```

### 5. Timeout Testing

```rust
#[tokio::test]
async fn test_operation_timeout() {
    let result = tokio::time::timeout(
        Duration::from_secs(2),
        slow_operation()
    ).await;

    assert!(result.is_err(), "Operation should timeout");
}
```

## Memory-Specific Patterns

### Episode Lifecycle Testing

```rust
#[tokio::test]
async fn test_complete_episode_lifecycle() {
    let memory = setup_memory().await;

    // 1. Start episode
    let episode_id = memory.start_episode(/* ... */).await;

    // 2. Log execution steps
    memory.log_execution_step(/* ... */).await;

    // 3. Complete episode
    memory.complete_episode(
        episode_id,
        TaskOutcome::Success,
        None,
    ).await?;

    // 4. Verify storage
    let episode = memory.get_episode(&episode_id).await?;
    assert_eq!(episode.outcome, TaskOutcome::Success);
}
```

### Pattern Extraction Testing

```rust
#[tokio::test]
async fn test_async_pattern_extraction() {
    let memory = setup_memory().await;
    let episode_id = create_test_episode(&memory).await;

    // Pattern extraction runs asynchronously
    memory.extract_patterns(episode_id).await?;

    // Wait for async workers to complete
    tokio::time::sleep(Duration::from_millis(100)).await;

    let patterns = memory.get_patterns_for_episode(&episode_id).await?;
    assert!(!patterns.is_empty());
}
```

## Best Practices

1. **Use `#[tokio::test]` instead of `tokio::test::block_on`** - cleaner syntax
2. **Enable `start_paused = true` for time-dependent tests** - faster execution
3. **Use `flavor = "multi_thread"` for concurrency tests** - realistic scenarios
4. **Always clean up test data** - prevent test pollution
5. **Mock external dependencies** - faster, more reliable tests
6. **Test error paths** - async error handling is critical

## Common Pitfalls

- **Don't use blocking operations in async tests**
```rust
// BAD
std::thread::sleep(Duration::from_secs(1));

// GOOD
tokio::time::sleep(Duration::from_secs(1)).await;
```

- **Don't forget to await futures**
```rust
// BAD - creates future but doesn't run it
memory.start_episode(/* ... */);

// GOOD
memory.start_episode(/* ... */).await;
```

- **Don't use single-threaded runtime for concurrency tests**
```rust
// BAD - uses single-threaded runtime
#[tokio::test]
async fn test_concurrent_ops() { /* ... */ }

// GOOD
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_concurrent_ops() { /* ... */ }
```

## Resources

- View `resources/tokio-patterns.md` for advanced patterns
- View `resources/concurrent-ops.md` for parallel execution strategies
- View `resources/mock-storage.md` for storage mocking patterns
