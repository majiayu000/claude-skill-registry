---
name: context-handoff
description: Creates context handoff documents for session continuity. Use when ending sessions, switching tasks, or handing off work.
---

# Context Handoff

Capture everything needed to resume work with zero context loss.

## Template

```markdown
# Context Handoff: [Task Name]

**Status:** in-progress | blocked | paused
**Created:** [date]

## What We're Building
[One paragraph: goal, success criteria]

## Current State
### Completed
- [x] [Task] — [file/commit]
### In Progress
- [ ] [Task] — [how far, what remains]
### Not Started
- [ ] [Task]

## Key Files
| File | Role | Status |
|------|------|--------|

## Decisions Made
| Decision | Rationale |
|----------|-----------|

## Blockers / Open Questions
- [Blocker/question with context]

## What to Do Next
1. [Specific action with details]
2. [Specific action with details]

## Gotchas
- [Non-obvious things that will trip you up]
```

## Rules

- Use absolute paths (no relative paths)
- Include exact test/build commands (copy-pasteable)
- Capture WHY for decisions, not just WHAT
- Write as if reader knows nothing about recent work
- Update as last action before stopping
