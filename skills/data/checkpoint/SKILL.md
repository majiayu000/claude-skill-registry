---
name: checkpoint
description: Save context state - auto-triggered every 5 tasks
allowed-tools: Read, Write, TaskList, Grep
model: sonnet
user-invocable: false
---

# Context Checkpoint

Save critical context before `/clear`. Enables 50-70% token savings.

## When to Checkpoint

- **Every 3 tasks** (aggressive - preserves tokens)
- Before switching feature areas
- After resolving complex bugs
- When response feels slow (context bloat sign)

## Checkpoint Format

Write to `.claude/checkpoint.md`:

```markdown
# Checkpoint: [TIMESTAMP]

## Sprint Status
[Sprint X: N/M complete]

## Completed This Session
- [Task]: [what was done]

## Key Learnings
- [Bug pattern]: [resolution]

## Next Priority
[Next task ID and title]

## Files Modified
- [file paths]
```

## After Saving

Tell user:
```
💾 Checkpoint saved.

Run /compact now to reclaim ~40% tokens (keeps context summary).
Use /clear only at major transitions (reclaims ~70% but wipes context).
```

## Auto-Restore

After `/clear`, read `.claude/checkpoint.md` and continue.

## What to Preserve

| Keep | Skip |
|------|------|
| Task progress | File contents |
| Learnings | Error traces |
| Next priority | Tool call logs |

## Token Savings

| Command | Savings | Use When |
|---------|---------|----------|
| `/compact` | ~40% | Default after checkpoint |
| `/clear` | ~70% | Major transitions, sprint end |

**Rule:** /compact after every checkpoint. /clear at major transitions.
