---
name: episodic-memory-testing
description: Domain-specific testing patterns for episodic memory operations. Use when testing episode lifecycle, pattern extraction, reward scoring, or memory retrieval.
---

# Episodic Memory Testing Patterns

Specialized testing patterns for the episodic memory system.

## Episode Lifecycle Testing

### Complete Flow

```rust
#[tokio::test]
async fn test_complete_episode_lifecycle() {
    let memory = setup_memory().await;

    // 1. Start episode
    let id = memory.start_episode("Test task", ctx, TaskType::CodeGen).await;
    assert!(!id.is_empty());

    // 2. Log steps
    memory.log_execution_step(id.clone(), step1).await;
    memory.log_execution_step(id.clone(), step2).await;

    // 3. Complete episode
    memory.complete_episode(id.clone(), TaskOutcome::Success, None).await?;

    // 4. Verify
    let episode = memory.get_episode(&id).await?;
    assert_eq!(episode.outcome, TaskOutcome::Success);
    assert_eq!(episode.steps.len(), 2);
}
```

### ID Uniqueness

```rust
#[tokio::test]
async fn test_episode_ids_unique() {
    let ids: HashSet<String> = (0..100)
        .map(|i| memory.start_episode(format!("Task {}", i), ctx, type_).await)
        .collect();
    assert_eq!(ids.len(), 100);
}
```

## Pattern Extraction Testing

```rust
#[tokio::test]
async fn test_pattern_extraction() {
    let patterns = memory.extract_patterns(episode_id).await?;
    assert!(!patterns.is_empty());
    for pattern in &patterns {
        assert!(!pattern.name.is_empty());
        assert!(pattern.frequency > 0.0);
    }
}
```

## Reward Scoring Testing

```rust
#[tokio::test]
async fn test_reward_score_bounds() {
    let perfect = calculate_reward_score(1.0, 1.0);
    assert!(perfect >= 0.9);

    let zero_efficiency = calculate_reward_score(0.0, 1.0);
    assert!(zero_efficiency < perfect);
}
```

## Memory Retrieval Testing

```rust
#[tokio::test]
async fn test_retrieval_by_context() {
    let rust_memories = memory.retrieve_context("rust", Some(10)).await?;
    assert!(rust_memories.len() >= 1);
    assert!(rust_memories.iter().all(|m| m.context.language == "rust"));
}
```

## Best Practices

- Use setup functions for memory initialization
- Clean up after tests
- Test edge cases (empty episodes, failed operations)
- Verify state transitions
- Mock embedding providers for speed
