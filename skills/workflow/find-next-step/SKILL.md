---
name: find-next-step
description: Find the next unimplemented step in a phase. Use when determining what to work on next.
user-invocable: false
---

# Next Step

## How to Find Next Step

Run this command to see active phases and their next unimplemented step:

```bash
if [ -d .ushabti/phases ] && [ "$(ls -A .ushabti/phases 2>/dev/null)" ]; then
  for dir in .ushabti/phases/*/; do
    status=$(grep "^  status:" "$dir/progress.yaml" 2>/dev/null | awk '{print $2}')
    if [ "$status" = "building" ] || [ "$status" = "planned" ]; then
      name=$(basename "$dir")
      next=$(awk '/- id:/{id=$3} /implemented: false/{print id; exit}' "$dir/progress.yaml" 2>/dev/null)
      impl=$(grep -c "implemented: true" "$dir/progress.yaml" 2>/dev/null || echo 0)
      total=$(grep -c "implemented:" "$dir/progress.yaml" 2>/dev/null || echo 0)
      if [ -n "$next" ]; then
        echo "$name: next step is $next ($impl/$total done)"
      else
        echo "$name: all steps implemented - ready for review"
      fi
    fi
  done
else
  echo "No active phases"
fi
```

## How Steps Are Tracked

In `progress.yaml`, each step has:
- `id`: Step identifier (S001, S002, ...)
- `implemented`: false until Builder completes it
- `reviewed`: false until Overseer verifies it

## Workflow

1. Find the current phase (use find-current-phase)
2. Read `progress.yaml` to find first step with `implemented: false`
3. Read that step's details in `steps.md`
4. Implement the step
5. Update `progress.yaml`: set `implemented: true`, add notes, list touched files
6. Repeat until all steps are implemented

## When All Steps Are Done

If no steps have `implemented: false`, the phase is ready for review. Set `phase.status: review` in progress.yaml and hand off to Overseer.
