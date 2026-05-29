---
name: episode-start
description: Start a new learning episode in the self-learning memory system with proper context. Use this skill when beginning a new task that should be tracked for learning from execution patterns.
---

# Episode Start

Start a new learning episode in the self-learning memory system.

## Purpose
Create a new episode record with proper context for the memory backend to learn from execution patterns.

## Steps

1. **Understand the task**: Parse the task description and identify:
   - Task type (implementation, debugging, refactoring, testing)
   - Domain (storage, patterns, retrieval, testing, etc.)
   - Language context (Rust/Tokio/async patterns)

2. **Prepare TaskContext**: Ensure you have:
   - `language`: "rust"
   - `domain`: One of [storage, patterns, retrieval, embedding, testing, ci]
   - `tags`: Array of relevant tags (e.g., ["turso", "async", "tokio"])

3. **Create episode**: Call `SelfLearningMemory::start_episode(task_description, context)`
   - Task description should be clear and concise (1-2 sentences)
   - Include relevant context from the user's request

4. **Store episode_id**: Keep the episode ID for logging subsequent steps

5. **Initialize step logging**: Prepare to log execution steps with:
   - Tool used
   - Action taken
   - Latency/tokens (if applicable)
   - Success status
   - Observations

## Storage Requirements
- Persist to Turso (durable storage)
- Cache in redb (fast access)
- Store context as JSON blob

## Example

```rust
let context = TaskContext {
    language: "rust".to_string(),
    domain: "storage".to_string(),
    tags: vec!["turso".to_string(), "async".to_string()],
};

let episode_id = memory
    .start_episode(
        "Implement async batch pattern updates",
        context
    )
    .await?;
```

## Notes
- Always validate that both Turso and redb connections are healthy
- Use anyhow::Result for error handling
- Log any initialization failures with context
