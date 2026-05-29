---
name: find-current-phase
description: Find the active phase directory based on status. Use when you need to locate which phase to work on.
user-invocable: false
---

# Current Phase Status

## How to Check

Run this command to see all phases and their status:

```bash
if [ -d .ushabti/phases ] && [ "$(ls -A .ushabti/phases 2>/dev/null)" ]; then
  for dir in .ushabti/phases/*/; do
    name=$(basename "$dir")
    phase_status=$(grep "^  status:" "$dir/progress.yaml" 2>/dev/null | awk '{print $2}')
    echo "$name: $phase_status"
  done
else
  echo "No phases exist yet"
fi
```

## Status Reference

| Status | Agent | Meaning |
|--------|-------|---------|
| `planned` | Builder | Ready to start implementation |
| `building` | Builder | Implementation in progress or fixes requested |
| `review` | Overseer | Ready for review |
| `complete` | — | Phase is green, no work needed |

## Agent Guidance

**Builder**: Work on phases with `status: building` or `status: planned`. If multiple exist, work on the lowest-numbered one first.

**Overseer**: Review phases with `status: review`. If none exist, no phase is ready for review.
