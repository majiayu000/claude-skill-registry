---
name: testing
description: Testing and debugging workflows for Kagenti development
---

# Testing Skills

Skills for testing, debugging, and TDD workflows.

## Available Skills

| Skill | Description |
|-------|-------------|
| `testing:kubectl-debugging` | Common kubectl debugging commands |

## Debugging Workflow

```
Test Failure → Live Debugging → Kubectl Commands → Fix → Verify
```

1. **Start**: Run failing test with verbose output
2. **Diagnose**: Check pod status, logs, configuration
3. **Fix**: Make targeted changes
4. **Verify**: Re-run specific test

## Quick Commands

```bash
# Check pods
kubectl get pods -n kagenti-system

# Get logs
kubectl logs -n kagenti-system deployment/<name>

# Check events
kubectl get events -n kagenti-system --sort-by='.lastTimestamp'
```

## Related Skills

- `k8s:health`
- `k8s:pods`
