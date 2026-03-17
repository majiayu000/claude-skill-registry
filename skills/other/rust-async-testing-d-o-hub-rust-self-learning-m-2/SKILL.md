---
name: rust-async-testing
description: Comprehensive async/tokio testing patterns for episodic memory operations. Use when writing tests for async functions, time-based operations, concurrent tasks, or tokio runtime management.
---

# Rust Async Testing Patterns

Best practices for testing async Rust code with Tokio.

## Core Patterns

### Basic Async Test

```rust
#[tokio::test]
async fn test_episode_creation() {
    let memory = SelfLearningMemory::new(Default::default()).await?;
    let id = memory.start_episode("Test", ctx, TaskType::CodeGen).await;
    assert!(!id.is_empty());
}
```

### Time-Based Testing

```rust
#[tokio::test(start_paused = true)]
async fn test_timeout_behavior() {
    // Time advances only when awaited
    let start = tokio::time::Instant::now();
    tokio::time::sleep(Duration::from_secs(5)).await;
    assert!(start.elapsed().as_millis() < 100);
}
```

### Concurrent Operations

```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_concurrent_episodes() {
    let memory = Arc::new(setup_memory().await);

    let handles: Vec<_> = (0..10).map(|i| {
        let mem = memory.clone();
        tokio::spawn(async move {
            mem.start_episode(format!("Task {}", i), ctx, type_).await
        })
    }).collect();

    let results = futures::future::join_all(handles).await;
    assert_eq!(results.len(), 10);
}
```

### Timeout Testing

```rust
#[tokio::test]
async fn test_operation_timeout() {
    let result = tokio::time::timeout(
        Duration::from_secs(2),
        slow_operation()
    ).await;
    assert!(result.is_err());
}
```

## Best Practices

1. Use `#[tokio::test]` instead of `block_on`
2. Enable `start_paused = true` for time tests
3. Use `multi_thread` for concurrency tests
4. Mock external dependencies
5. Test error paths

## Common Pitfalls

| Bad | Good |
|-----|------|
| `std::thread::sleep()` | `tokio::time::sleep().await` |
| `memory.start_episode()` | `memory.start_episode().await` |
| Single-threaded for concurrency | `multi_thread` runtime |

## Memory-Specific Pattern

```rust
#[tokio::test]
async fn test_complete_lifecycle() {
    let memory = setup_memory().await;

    // Start → Log Steps → Complete → Verify
    let id = memory.start_episode("test", ctx, type_).await;
    memory.log_execution_step(id.clone(), step).await;
    memory.complete_episode(id.clone(), outcome, None).await?;

    let episode = memory.get_episode(&id).await?;
    assert_eq!(episode.outcome, outcome);
}
