---
name: episode-log-steps
description: Log execution steps during episode execution for detailed tracking and learning. Use when recording tool usage, decision points, errors, or milestones during task execution.
---

# Episode Log Steps

Log execution steps during episode execution for detailed tracking and learning.

## Purpose
Record individual execution steps to build a complete picture of task execution for pattern learning.

## When to Log Steps

1. **Tool usage**: Each time a significant tool is used
2. **Decision points**: When making architectural or implementation choices
3. **Error handling**: When encountering and resolving errors
4. **Milestones**: Key progress points (test passing, module complete)

## Step Structure

```rust
pub struct ExecutionStep {
    pub tool: String,           // Tool/action used
    pub action: String,         // Description of action
    pub latency_ms: u64,        // Time taken
    pub tokens: Option<u32>,    // Tokens used (if applicable)
    pub success: bool,          // Whether step succeeded
    pub observation: String,    // Outcome/observations
}
```

## Logging Guidelines

### 1. Batch When Appropriate
- Don't log every tiny operation
- Batch related steps when many occur quickly
- Log significant operations individually

### 2. Include Context
- Tool: cargo, rustfmt, clippy, git, etc.
- Action: Specific command or operation
- Observation: Result, output summary, or error

### 3. Track Performance
- Record latency for slow operations
- Note token usage for LLM calls
- Mark success/failure clearly

## Examples

### Build Step
```rust
let step = ExecutionStep {
    tool: "cargo".to_string(),
    action: "build --all".to_string(),
    latency_ms: 12500,
    tokens: None,
    success: true,
    observation: "Build successful, 0 warnings".to_string(),
};
memory.log_step(episode_id, step).await?;
```

### Test Step
```rust
let step = ExecutionStep {
    tool: "cargo".to_string(),
    action: "test --test integration_test".to_string(),
    latency_ms: 3200,
    tokens: None,
    success: false,
    observation: "2 tests failed: test_batch_insert, test_concurrent_writes".to_string(),
};
memory.log_step(episode_id, step).await?;
```

### Code Generation Step
```rust
let step = ExecutionStep {
    tool: "claude".to_string(),
    action: "generate async batch implementation".to_string(),
    latency_ms: 4500,
    tokens: Some(2800),
    success: true,
    observation: "Generated batch.rs with async Tokio patterns".to_string(),
};
memory.log_step(episode_id, step).await?;
```

### Error Resolution Step
```rust
let step = ExecutionStep {
    tool: "clippy".to_string(),
    action: "check --all".to_string(),
    latency_ms: 1500,
    tokens: None,
    success: true,
    observation: "Fixed 3 warnings: unused imports, unnecessary clone".to_string(),
};
memory.log_step(episode_id, step).await?;
```

## Batching Strategy

When multiple related steps occur in a burst (e.g., fixing multiple test failures):

```rust
let step = ExecutionStep {
    tool: "cargo".to_string(),
    action: "fix 5 test failures in batch_test.rs".to_string(),
    latency_ms: 18000,
    tokens: Some(3500),
    success: true,
    observation: "Fixed: test_batch_insert (await missing), test_concurrent (lock order), test_timeout (semaphore added)".to_string(),
};
memory.log_step(episode_id, step).await?;
```

## Notes

- Steps are stored as JSON array in episode record
- Use clear, actionable observations
- Include error messages when relevant
- Keep observation strings concise but informative
