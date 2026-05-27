---
description: Dispatch queue pattern for tracking pending tasks across sessions. Use when managing task continuity, understanding pending work, or implementing the /continue workflow.
---

# Dispatch Queue Pattern

The dispatch queue (`.studio/dispatch-queue.md`) tracks pending tasks for session continuity.

## File Format

```markdown
# Dispatch Queue

## Pending Tasks (Priority Order)

### 1. [Task Name]
- **Agent:** [fully-qualified agent name]
- **Context:** [what needs to be done and why]
- **Blocked by:** [dependencies, or "None"]
- **Added:** [when queued]

## Completed This Session
- [x] [Task] → [result/artifact]

## Notes
[Context for next session]
```

## When to Update

**Add tasks:**
- After identifying work during implementation
- When completion-auditor finds gaps
- When project-health-monitor identifies issues
- When user requests deferred work

**Remove/Complete:**
- When task dispatched and completed
- When task becomes irrelevant
- When blocked indefinitely

## Priority Ordering

1. Blockers first (tasks that block other work)
2. Critical path (required for playable game)
3. Quick wins (fast, unblock progress)
4. Polish (nice-to-have)

## Task Format

**Agent:** Use fully-qualified names: `zx-procgen:asset-generator`

**Context:** Include enough to resume: what exists, what's needed, file paths

**Blocked by:** `None`, `#2`, `[dependency]`, or `User decision needed`

## Integration

- `/ai-game-studio:continue` reads and dispatches from queue
- `next-step-suggester` checks queue first
- `request-dispatcher` updates queue before stopping
- `completion-auditor` adds remediation tasks

## Empty Queue

```markdown
# Dispatch Queue

## Pending Tasks (Priority Order)
No pending tasks.

## Notes
Run project-health-monitor to identify potential work.
```
