---
name: vibe-debugging-journal
description: Records resolved bugs in a persistent journal — symptom, root cause, difficulty, fix, prevention. Organized by category for future reference.
user-invocable: true
---

# vibe-debugging-journal

Bugs come in patterns. Recording them prevents re-investigation.

## When to Use This Skill

- After resolving a non-trivial bug (took >10 minutes to find)
- After finding a bug that was hard to reproduce
- After debugging something where the root cause was surprising
- When you notice a bug pattern repeating

## When NOT to Use This Skill

- Trivial bugs (typos, missing imports)
- Bugs with immediately obvious causes
- Build/configuration issues (not really bugs)

## Steps

1. **Categorize** the bug:
   - Concurrency (race conditions, deadlocks, ordering)
   - State Management (stale state, missing updates, cache invalidation)
   - Type/Validation (type errors, missing validation, edge cases)
   - Integration (API mismatch, version incompatibility, protocol errors)
   - Environment (platform-specific, config, deployment)
   - UI/Rendering (layout, hooks, lifecycle)

2. **Record** in structured format:

```
### [Category]: [Short description]
**Date**: [date]
**Symptom**: [What was observed]
**Root Cause**: [The actual problem]
**Why Hard to Find**: [What made debugging difficult]
**Fix**: [What was changed]
**Prevention**: [How to prevent recurrence]
**Files**: [affected files]
```

3. **Save** to persistent storage:
   - Project: `docs/debugging-journal.md` or `DEBUGGING.md`
   - Memory: Claude auto-memory or MCP

4. **Cross-reference** — If this relates to an existing journal entry, link them

## Output Format

Present the entry for user confirmation, then save. Keep entries concise (5-10 lines each).
