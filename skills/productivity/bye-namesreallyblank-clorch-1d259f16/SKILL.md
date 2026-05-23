---
name: bye
description: Save session state (continue working or exit safely)
invokes:
  - session-saver
---

# Save Session

When the user invokes `/bye` or "save session", you should:

## Step 1: Save Session

**Spawn the `session-saver` agent** to create:
1. YAML handoff at `thoughts/shared/handoffs/{date}_{topic}.yaml`
2. Quick state files in `.claude/memory/`

This is the unified save mechanism - one source of truth for all hooks.

## Step 2: Confirm with User

After saving, show:

```
✓ Session saved to: thoughts/shared/handoffs/{date}_{topic}.yaml

Summary:
- Goal: [what you were working on]
- Done: [key accomplishments]
- Next: [first action item]

You can:
- Continue working (session state is checkpointed)
- Safely exit (use `/resume` next time to pick up where you left off)
```

## Usage

- `/bye` - full save with summary
- `/bye quick` - minimal save (goal/now/done/next only)
- "save session" - same as `/bye`

## Quick Mode

If `/bye quick`, tell session-saver to create minimal handoff:
```yaml
goal: [1-line summary]
outcome: IN_PROGRESS
now: [immediate next action]
done_this_session:
  - [1-2 key items]
next:
  - priority: P0
    task: [most important next step]
```

## Migration Note

This replaces the old dual-system where `/create_handoff` wrote Markdown and `session-saver` wrote separate state files. Now everything goes through session-saver for consistency.
