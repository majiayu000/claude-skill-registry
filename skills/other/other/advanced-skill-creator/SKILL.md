---
name: advanced-skill-creator
version: 1.0.0
description: Advanced patterns for creating complex, multi-step skills with error handling and state management.
metadata:
  openclaw:
    emoji: 🛠️
    category: development
---

# Advanced Skill Creator

Advanced patterns for creating complex, multi-step skills with error handling and state management.

## When to Use

- Multi-step workflows with dependencies
- Skills requiring state persistence
- Complex error handling scenarios
- Integration with external APIs

## Patterns

### State Machine Pattern

```yaml
# STATE.yaml
step: 2
status: in_progress
completed:
  - step_1_auth
remaining:
  - step_2_fetch
  - step_3_process
errors: []
```

### Error Recovery

```python
# Retry with backoff
for attempt in range(3):
    try:
        result = api.call()
        break
    except APIError as e:
        if attempt == 2:
            raise
        time.sleep(2 ** attempt)
```

## Best Practices

1. Define clear entry/exit points
2. Validate inputs before processing
3. Log all state transitions
4. Provide rollback on failure
