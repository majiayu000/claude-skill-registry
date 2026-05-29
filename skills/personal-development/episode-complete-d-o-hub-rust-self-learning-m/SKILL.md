---
name: episode-complete
description: Complete and score a learning episode to extract patterns and update heuristics. Use when finalizing a task to enable pattern extraction and future learning.
---

# Episode Complete

Complete and score a learning episode to extract patterns and update heuristics.

## Purpose
Finalize an episode with outcome scoring, reflection generation, and pattern extraction for future retrieval.

## Steps

1. **Gather outcome data**:
   - Final verdict (success, partial_success, failure)
   - Total time spent
   - Total tokens used (if applicable)
   - Key artifacts produced
   - Errors encountered

2. **Create TaskOutcome**:
   ```rust
   let outcome = TaskOutcome {
       verdict: Verdict::Success,
       time_ms: total_time,
       tokens: total_tokens,
       artifacts: vec![/* paths to created/modified files */],
       errors: vec![/* any errors encountered */],
   };
   ```

3. **Call complete_episode**:
   ```rust
   memory.complete_episode(episode_id, outcome).await?;
   ```

4. **System processes**:
   - Computes RewardScore based on:
     - Success/failure
     - Time efficiency
     - Code quality
   - Generates Reflection:
     - What worked well
     - What could be improved
     - Key learnings
   - Extracts Patterns:
     - Tool sequences
     - Decision points
     - Common pitfalls

5. **Update storage**:
   - Store in Turso (permanent record)
   - Update redb cache
   - Index by task_type and timestamp
   - Update related patterns and heuristics

6. **Validation**:
   - Verify episode was scored
   - Check patterns were extracted
   - Ensure heuristics were updated

## Pattern Types Extracted

- **ToolSequence**: Common tool usage patterns
- **DecisionPoint**: Key decision moments and outcomes
- **ErrorPattern**: Common errors and resolutions
- **PerformancePattern**: Optimization opportunities

## Scoring Rubric

- **Success**: Task completed, tests pass, meets requirements
- **Partial Success**: Task mostly complete, minor issues
- **Failure**: Task incomplete, major issues, tests failing

## Example

```rust
let outcome = TaskOutcome {
    verdict: Verdict::Success,
    time_ms: 45000,
    tokens: 12000,
    artifacts: vec![
        "src/storage/batch.rs".to_string(),
        "tests/integration/batch_test.rs".to_string(),
    ],
    errors: vec![],
};

memory.complete_episode(episode_id, outcome).await?;
```

## Post-Completion

- Patterns are now available for future retrieval
- Heuristics updated for similar tasks
- Episode stored for long-term learning
- Embeddings computed (if service configured)
