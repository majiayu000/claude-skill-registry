---
name: snapshot
description: Capture current session state without stopping
---

# Snapshot

Capture current session state for review without parking.

## Use Cases

- Session is getting long, want a checkpoint summary
- Want to share progress with someone
- Need to orient yourself on where you are

## Output Format

```
━━━ Session Snapshot ━━━
Focus: [Current focus/goal]

Progress:
✓ [Completed item]
✓ [Completed item]
○ [In progress item]
○ [Pending item]

Key decisions:
- [Decision 1]
- [Decision 2]

Files touched:
- path/to/file.ts (new)
- path/to/other.ts (modified)

Current thread: [What we're actively discussing/working on]
```

## Flags

### `--save`

Write the snapshot to the parking location as a checkpoint file.

Filename: `snapshot-[timestamp].md`

Format when saved:

```markdown
# Snapshot: [Focus]

**Captured:** [Date/time]
**Branch:** [branch-name]

## Progress
- [x] [Completed item]
- [x] [Completed item]
- [ ] [In progress item]
- [ ] [Pending item]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Files Touched
- path/to/file.ts (new)
- path/to/other.ts (modified)

## Current Thread
[What we're actively discussing/working on]
```

Report: "Snapshot saved to `[path]`"

## Difference from /park

| Aspect | /snapshot | /park |
|--------|-----------|-------|
| Intent | Review progress | Stop work for later |
| Output | Inline (default) | Always file |
| Resume prompt | No | Yes |
| Next steps | Current state | Future direction |
