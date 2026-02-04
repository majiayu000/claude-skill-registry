---
name: get-phase-status
description: Check the current status of a phase. Use when you need to understand where a phase is in the workflow.
user-invocable: false
---

# Phase Status

## How to Check Status

Run this command to see all phases with their status and step counts:

```bash
if [ -d .ushabti/phases ] && [ "$(ls -A .ushabti/phases 2>/dev/null)" ]; then
  for dir in .ushabti/phases/*/; do
    name=$(basename "$dir")
    status=$(grep "^  status:" "$dir/progress.yaml" 2>/dev/null | awk '{print $2}')
    impl=$(grep -c "implemented: true" "$dir/progress.yaml" 2>/dev/null || echo 0)
    total=$(grep -c "implemented:" "$dir/progress.yaml" 2>/dev/null || echo 0)
    echo "$name: $status ($impl/$total steps)"
  done
else
  echo "No phases exist yet"
fi
```

## Status Values

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `planned` | Phase created, not started | Builder begins implementation |
| `building` | Implementation in progress | Builder continues or addresses fixes |
| `review` | Implementation complete | Overseer reviews |
| `complete` | Phase is green | Scribe plans next phase |

## Status Transitions

```
planned → building    (Builder starts)
building → review     (Builder finishes all steps)
review → building     (Overseer requests fixes)
review → complete     (Overseer approves)
```
