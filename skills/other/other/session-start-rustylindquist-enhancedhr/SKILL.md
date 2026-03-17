---
name: session-start
description: Resumes work from a previous session using handoff notes, checkpoints, or compact state. Use at the beginning of a new session to restore context and continuity.
allowed-tools: Read, Glob
---

# Session Start

Restore context from previous session. Prevents "starting from scratch" problem.

## When to Use

- Beginning new session after handoff
- Resuming after break
- Recovering from crash/timeout
- User says "continue where we left off"

## Recovery Priority

1. **Handoff** → `.context/handoff.md` (complete session summary)
2. **Checkpoint** → `.context/checkpoints/checkpoint-*.md` (point-in-time)
3. **Compact State** → `.context/compact-state.md` (post-compaction)
4. **Agent Registry** → `.context/agents/active.yaml` (coordination)

## Process

1. **Locate Sources**: Check .context/ for handoff, checkpoints, compact-state
2. **Load Primary**: Read handoff or specified checkpoint
3. **Verify State**: Confirm files match expected state
4. **Load Docs**: Based on task, run `/doc-discovery` or spawn @doc-agent
5. **Refresh Instructions**: Safety rules, orchestration mode, tools
6. **Report Ready**: Show context restored, ready to continue

## Output

```markdown
## Session Started

### Recovered From
**Source**: [handoff/checkpoint/compact-state]

### Context Restored
- **Objective**: [goal]
- **Task**: [current]
- **Position**: [where in workflow]

### Verification
- [x] State matches expected
- [x] Environment ready
- [x] Instructions refreshed

### Next Action
[specific next step]
```

## Quick Start (No Handoff)

```markdown
## Fresh Session

No previous state found.

### Available
- CLAUDE.md loaded
- Core instructions active
- Tools available

### To Begin
Describe what you'd like to work on.
```

## Related

- Checkpoint recovery: See [reference/checkpoint-recovery.md](reference/checkpoint-recovery.md)
- State mismatch handling: See [reference/state-mismatch.md](reference/state-mismatch.md)
- Consumes output from: `/handoff`, `/checkpoint`, `/compact`
