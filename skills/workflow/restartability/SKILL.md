---
name: restartability
description: STATUS.md format and guidance for tracking progress and resuming work after interruptions.
---

# Restartability

**Always maintain STATUS.md** to enable picking up work after interruptions.

## STATUS.md Format

```markdown
# Status: [PROJECT NAME]
**Updated**: [timestamp] | **Tasks**: X/Y complete

## Tasks
| Task | Status | Wave | Notes |
|------|--------|------|-------|
| Feature A | Done | E | PR merged |
| Feature B | Active | D | Writing tests |
| Bug fix C | Blocked | B | Need input |

## Artifacts
| File | Status |
|------|--------|
| spec.md | Done |
| architecture.md | Draft |
| test-plan.md | Missing |

## Session Log
- Completed: [what]
- In progress: [what]
- Blocked: [what + why]
```

## When to Update STATUS.md

- **Start of session:** Read STATUS.md first
- **After completing a wave:** Update task status and artifacts
- **When blocked:** Document what's blocking and why
- **Before ending session:** Update with current state

## Resuming from Interruption

1. Read STATUS.md first
2. Skip completed work
3. Resume from last good state
4. Update frequently as you work

## Status Icons

| Icon | Meaning |
|------|---------|
| Done | Task complete |
| Active | Currently working |
| Blocked | Waiting on something |
| Missing | Artifact not yet created |
| Draft | Work in progress |
