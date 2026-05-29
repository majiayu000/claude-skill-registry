---
name: crash-recovery
description: Invoke CRASH_RECOVERY_SPECIALIST for session recovery after crashes or context loss. Creates checkpoints, reconstructs state, and generates handoff notes for seamless recovery.
model_tier: haiku
parallel_hints:
  can_parallel_with: [historian, medcom, devcom]
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 20
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "uncommitted work"
    reason: "Data loss risk - immediate recovery needed"
  - keyword: ["crash", "context loss", "termination"]
    reason: "Session continuity threatened"
---

# Crash Recovery Skill

Session continuity and post-crash state reconstruction specialist. Ensures seamless recovery after IDE crashes, context resets, or unexpected terminations.

## When This Skill Activates

- After crashes or unexpected terminations
- Context loss or session reset
- Before risky operations (proactive checkpoint)
- When resuming work after long break
- Recovering in-progress tasks
- Reconstructing session timeline

## Purpose

CRASH_RECOVERY_SPECIALIST ensures session continuity by:
- Creating periodic checkpoints before risky operations
- Reconstructing session state from git and scratchpad artifacts
- Generating handoff notes for seamless recovery
- Implementing "Prior You / Current You" protocol

**Key Insight:** Future you depends on current you leaving breadcrumbs.

## Reports To

- **SYNTHESIZER** (Special Staff - Session Continuity)
- May coordinate with HISTORIAN for session documentation
- Provides recovery instructions to ORCHESTRATOR

## Agent Identity

Loads: `/home/user/Autonomous-Assignment-Program-Manager/.claude/Agents/CRASH_RECOVERY_SPECIALIST.md`

## Key Workflows

### Workflow 1: Checkpoint Creation

```
INPUT: Current task state before risky operation
OUTPUT: Checkpoint file in .claude/Scratchpad/

1. Snapshot git state (branch, status, recent commits)
2. Capture scratchpad state
3. Document in-progress tasks
4. Create recovery breadcrumbs
5. Save to checkpoint file

Use before: git operations, large refactors, system updates
```

### Workflow 2: Post-Crash Reconstruction

```
INPUT: Available artifacts (git status, scratchpad files)
OUTPUT: Session state reconstruction

1. Parse git status for uncommitted work
2. Read scratchpad files for context
3. Identify in-progress tasks from history
4. Reconstruct session timeline
5. Cross-reference multiple sources
6. Generate handoff notes
```

### Workflow 3: Handoff Note Generation

```
INPUT: Recovered state
OUTPUT: Resume notes for next session

1. Summarize recovered state
2. List incomplete tasks
3. Provide recommended first action
4. Flag uncertainties
5. Document what couldn't be determined
```

## "Prior You / Current You" Protocol

Incremental work habits that enable recovery:

1. **Commit incrementally** (~30 min intervals)
2. **Write to disk, not just memory**
3. **Leave breadcrumbs in scratchpad**
4. **Document decisions and context**

This protocol makes recovery possible even without explicit checkpoints.

## Output Formats

### Checkpoint File

```markdown
# Recovery Checkpoint: [timestamp]

## Session State
- Branch: [name]
- Last Commit: [hash] [message]
- Uncommitted: [list files]

## Current Task
[What's being worked on]

## Progress
- Completed: [list]
- In Progress: [item]
- Not Started: [list]

## Recent Decisions
[Key choices and rationale]

## Resume Point
[Where to start when recovering]
```

### Recovery Handoff

```markdown
# Session Recovery: [timestamp]

## Recommended First Action
[Single clear next step]

## Recovered State
- Branch: [name]
- In-progress work: [description]
- Last completed: [task]

## Timeline Reconstruction
[What happened in session]

## Uncertainties
[What couldn't be determined]

## Full Context
[Detailed reconstruction]
```

## Integration with Other Skills

### With historian
**Coordination:** Recovery findings may inform session narratives
```
1. CRASH_RECOVERY_SPECIALIST reconstructs session
2. If session was significant, findings passed to HISTORIAN
3. HISTORIAN creates narrative documentation
```

### With session-end
**Coordination:** Crash recovery complements normal session handoff
```
Normal flow: session-end creates structured handoff
Crash flow: crash-recovery reconstructs what session-end would have captured
```

## Aliases

- `/recover` - Quick recovery invocation
- `/restore` - Explicit state restoration

## Usage Examples

### Example 1: Create Checkpoint Before Risky Operation
```
Use the crash-recovery skill to create a checkpoint before attempting
a complex git rebase.

## Current State
- Branch: feature/swap-improvements
- Task: Rebasing 15 commits to clean up history
- Progress: All tests passing, ready to rebase
- Recent decisions: Decided to squash related commits

## Output
Save checkpoint to .claude/Scratchpad/checkpoint_[timestamp].md
```

### Example 2: Recover After Crash
```
Use the crash-recovery skill to recover session state after crash.

## Available Artifacts
- Git branch: feature/resilience-dashboard
- Git status:
  On branch feature/resilience-dashboard
  Changes not staged for commit:
    modified: backend/app/resilience/dashboard.py
    modified: frontend/components/Dashboard.tsx
  Untracked files:
    backend/tests/test_dashboard.py

- Scratchpad files:
  .claude/Scratchpad/ORCHESTRATOR_ADVISOR_NOTES.md
  .claude/Scratchpad/TODO.md

- Last known task: Implementing resilience dashboard endpoints

## Request
1. Reconstruct session timeline
2. Identify in-progress tasks
3. Generate handoff notes
4. Recommend first action to resume work
```

### Example 3: Routine Recovery at Session Start
```
Use the crash-recovery skill to review what was happening last session.

Context: Starting new session, want to understand where we left off.

Available:
- Git log (last 10 commits)
- Scratchpad files list
- Current branch: main

Return: Brief summary of last session's work and recommended first step.
```

## Common Failure Modes

| Failure Mode | Symptom | Recovery |
|--------------|---------|----------|
| **Incomplete Checkpoints** | Missing key context | Cross-reference multiple artifact sources; ask user |
| **Stale Scratchpad** | Scratchpad reflects old state | Use git commits as ground truth; flag discrepancies |
| **Uncommitted Work Loss** | Work vanished after crash | Check IDE autosave, temp files, .git/ objects |
| **Context Ambiguity** | Multiple interpretations | Present options to user; avoid assumptions |
| **Handoff Overwhelm** | Too detailed, can't find resume point | Lead with "Recommended First Action" |

## Quality Checklist

Before completing recovery:

- [ ] Git state captured (branch, status, commits)
- [ ] Scratchpad files reviewed
- [ ] In-progress tasks identified
- [ ] Timeline reconstructed
- [ ] Uncertainties flagged
- [ ] Recommended first action provided
- [ ] Handoff notes clear and actionable
- [ ] Cross-referenced multiple sources

## Recovery Artifact Locations

### Always Check These Files

- `.claude/Scratchpad/ORCHESTRATOR_ADVISOR_NOTES.md` - Session history
- `.claude/Scratchpad/*.md` - Session artifacts
- `CHANGELOG.md` - Recent committed changes
- Git log (last 10 commits) - Timeline reconstruction
- Git status - Uncommitted work

### Checkpoint Storage

Checkpoints saved to: `.claude/Scratchpad/checkpoint_[timestamp].md`

## Context Isolation Awareness

When delegating to CRASH_RECOVERY_SPECIALIST:

**For Checkpoint Creation:**
- Current task description
- In-progress work status
- Recent decisions made
- Risky operation about to be performed

**For Post-Crash Recovery:**
- Git branch and full status output
- List of scratchpad files available
- Last known task (if available)
- Approximate time of crash

**Recovery scope:**
- What needs to be recovered
- Who will resume the work
- Urgency level

## Success Metrics

- Recovery completes < 10 minutes
- 95%+ in-progress tasks identified
- Zero data loss from uncommitted work
- Handoff enables seamless resume

## Best Practices

### Before Risky Operations

Always create checkpoint before:
- Major git operations (rebase, merge, reset)
- Large refactoring
- Database migrations
- System configuration changes
- Complex multi-step procedures

### Continuous Recovery Preparation

Implement "Prior You / Current You" protocol:
- Commit every 30 minutes with descriptive messages
- Update scratchpad with decisions
- Write notes explaining "why" not just "what"
- Keep TODO list current

### After Crash

1. Don't panic
2. Run crash-recovery skill immediately
3. Review recovered state carefully
4. Verify git status matches expectations
5. Check for uncommitted work before continuing
6. Document what was lost (if anything)

## References

- Session history: `.claude/Scratchpad/ORCHESTRATOR_ADVISOR_NOTES.md`
- Recent changes: `CHANGELOG.md`
- Checkpoint location: `.claude/Scratchpad/checkpoint_*.md`
- Recovery patterns: `.claude/dontreadme/synthesis/PATTERNS.md`

---

*"Future you depends on current you leaving breadcrumbs."*
