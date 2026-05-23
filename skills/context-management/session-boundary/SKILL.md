# Session Boundary Skill

Detect and handle session boundaries for multi-context autopilot workflows.

## Purpose

Manage smooth transitions across context windows by:
1. Detecting when context is about to be compacted
2. Generating comprehensive handoff documents
3. Restoring state after context restoration
4. Tracking session metrics for workflow optimization

## When to Invoke

- Automatically via SessionStart hook (startup, resume, compact triggers)
- Automatically via PreCompact hook (before context compaction)
- Automatically via Stop hook (session end)
- Manually via `/context next` or `/context status`
- During `/feature continue` or `/epic continue`

## Core Concepts

### Write-Through State Pattern

**Critical**: Never keep state only in conversation memory. Always persist immediately.

```yaml
# Good: Write to state.yaml immediately
session:
  id: "session-20251204-143000"
  started_at: "2025-12-04T14:30:00Z"
  phase_at_start: "implement"
  decisions_made: ["Redis for token blacklist"]

# Bad: Keeping state only in conversation
# "I decided to use Redis..." (lost on compaction)
```

### Session Lifecycle

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ SessionStart │───▶│   Working    │───▶│     Stop     │
│   (restore)  │    │   (track)    │    │ (checkpoint) │
└──────────────┘    └──────────────┘    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  PreCompact  │
                    │  (handoff)   │
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ SessionStart │
                    │  (restore)   │
                    └──────────────┘
```

### Hook Integration

| Hook | Trigger | Purpose |
|------|---------|---------|
| SessionStart | startup, resume, compact | Restore workflow context |
| PreCompact | auto, manual | Generate handoff before context loss |
| Stop | session end | Checkpoint current state |

## Session Manager Commands

```bash
# Start new session (with optional autopilot)
bash .spec-flow/scripts/bash/session-manager.sh start --autopilot

# View current status
bash .spec-flow/scripts/bash/session-manager.sh status

# Record important decision
bash .spec-flow/scripts/bash/session-manager.sh decision "Using Redis for caching"

# Generate handoff manually
bash .spec-flow/scripts/bash/session-manager.sh handoff

# End session with summary
bash .spec-flow/scripts/bash/session-manager.sh end --summary "Completed auth implementation"

# Control autopilot mode
bash .spec-flow/scripts/bash/session-manager.sh autopilot on|off|status

# View session history
bash .spec-flow/scripts/bash/session-manager.sh history
```

## State Schema (session block)

Added to state.yaml (schema v2.2.0):

```yaml
session:
  id: "session-20251204-143000"
  started_at: "2025-12-04T14:30:00Z"
  ended_at: null
  last_activity: "2025-12-04T16:45:00Z"
  phase_at_start: "implement"
  tasks_at_start: 12
  tasks_completed_this_session: 4
  decisions_made:
    - "Redis for token blacklist"
    - "JWT expiry 15min"
  handoffs:
    - id: "handoff-20251204-163000"
      at: "2025-12-04T16:30:00Z"
  last_handoff_id: "handoff-20251204-163000"
  last_handoff_at: "2025-12-04T16:30:00Z"
  autopilot_enabled: false
  duration_seconds: null
  summary: null
```

## Handoff Document Structure

Located at: `{workflow_dir}/sessions/handoff-{timestamp}.md`

```markdown
# Session Handoff: {slug}

> Generated: {timestamp}
> Trigger: {context compaction | manual | session end}
> Phase: {current_phase}
> Status: {current_status}

## Quick Resume

```bash
/{workflow_type} continue
```

## Current State

| Metric | Value |
|--------|-------|
| Workflow Type | feature/epic |
| Slug | {slug} |
| Current Phase | {phase} |
| Phase Status | {status} |
| Tasks Progress | {completed} / {total} |

## Next Task

{next_uncompleted_task}

## Recent Decisions

{list_of_recent_decisions}

## Key Artifacts

- State: `state.yaml`
- Tasks: `tasks.md`
- Notes: `NOTES.md`
...

## Context for Next Session

1. Read state.yaml for complete workflow state
2. Check tasks.md for task completion status
3. Review NOTES.md for recent decisions and blockers
4. Use `/context next` for detailed next steps
```

## Integration Points

### /feature continue and /epic continue

Both commands now:
1. Display session status before resuming
2. Check for and display handoff documents
3. Start a new session for tracking

### /context Command

- `/context status` - Shows session and workflow status
- `/context next` - Generates handoff document
- `/context add` - Records item to backlog

### NOTES.md Session Markers

Session boundaries are recorded in NOTES.md:

```markdown
---

## Session Boundary: 2025-12-04T16:30:00Z

*Context compaction occurred. Handoff saved to: sessions/handoff-20251204-163000.md*
```

## Autopilot Mode

When `autopilot_enabled: true`:

1. Stop hook can return `{"decision": "block"}` to continue execution
2. Workflow continues through context compaction automatically
3. Session boundaries are transparent to the workflow
4. Only blocks on actual failures (CI, tests, deployment)

Enable via:
```bash
bash .spec-flow/scripts/bash/session-manager.sh autopilot on
```

Or during session start:
```bash
bash .spec-flow/scripts/bash/session-manager.sh start --autopilot
```

## Metrics Tracked

- Session duration
- Tasks completed per session
- Decisions made per session
- Handoffs generated
- Phase transitions within session

Used for:
- Workflow optimization
- Velocity analysis
- Context usage patterns
