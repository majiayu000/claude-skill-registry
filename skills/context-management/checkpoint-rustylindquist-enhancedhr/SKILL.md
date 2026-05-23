---
name: checkpoint
description: Save mid-session state for recovery without clearing context. Use after major milestones, before risky operations, or periodically during long sessions.
allowed-tools: Read, Write
---

# Checkpoint

Save session state at key points to enable recovery without losing progress. Unlike /compact (clears context), checkpoint preserves everything.

## When to Use

- After completing significant work
- Before attempting something risky
- Every 30-45 minutes in long sessions
- Before spawning multiple parallel agents
- When user takes a break

## Checkpoint Types

| Type | Trigger | Depth |
|------|---------|-------|
| **Milestone** | Major work completed | Full |
| **Periodic** | Time-based (30-45 min) | Standard |
| **Pre-risk** | About to try uncertain operation | Full + rollback plan |
| **Quick** | User stepping away | Minimal |

## What Gets Saved

- Current objective and task in progress
- Position in workflow (which steps complete)
- Files changed and decisions made
- Active agents and pending results
- Docs loaded and key facts established

## Process

1. Determine checkpoint type (milestone/periodic/pre-risk/quick)
2. Write to `.context/checkpoints/checkpoint-[timestamp].md`
3. Update `.context/checkpoints/INDEX.md`
4. Confirm to user and continue work

## Output Location

`.context/checkpoints/checkpoint-[timestamp].md`

## Quick Checkpoint

For rapid saves:
```markdown
# Quick Checkpoint - [timestamp]
**Task**: [current]
**Position**: [where]
**Next**: [next action]
**Files**: [changed]
```

## Comparison

| Skill | When | Context | Purpose |
|-------|------|---------|---------|
| /checkpoint | Mid-session | Preserved | Recovery point |
| /compact | Context saturated | Cleared | Continue working |
| /handoff | Session ending | N/A | Pass to next session |

## Related

- Full checkpoint template: See [reference/full-template.md](reference/full-template.md)
- Pre-risk template: See [reference/pre-risk-template.md](reference/pre-risk-template.md)
- Recovery instructions: See [reference/recovery.md](reference/recovery.md)
- To resume: `/session-start --checkpoint [timestamp]`
