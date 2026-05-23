---
name: start
description: Session startup with context recovery. USE WHEN starting session, after /clear, or recovering from autocompact.
---

# /start - Session Startup & Context Recovery

Gather project context and recover from handoffs automatically.

## Data Source Priority

**1. Pre-loaded (preferred)**: Check for "Pre-loaded Session Status" in the SessionStart hook output (appears in system-reminder tags at conversation start with `additionalContext`). If found, parse the JSON code block and use this data directly—no MCP call needed.

**2. MCP fallback**: If no pre-loaded data exists, call `get_session_status` with appropriate level.

Look for a section like this in the startup system-reminders:
```
# Pre-loaded Session Status

The following session context was gathered at startup...

```json
{
  "level": "standard",
  "integrations": {...},
  "recovery": {...},
  "project": {...},
  "beads_triage": {...}
}
```

The pre-loaded data has the same structure as the MCP response—format and display it the same way.

## Quick Start (MCP Fallback)

```typescript
// Fresh session - full context
get_session_status({ level: "full" })

// Context recovery mid-session
get_session_status()  // defaults to minimal

// Restore specific handoff
get_session_status({ handoff: "h7k2m" })
```

## Output Levels

| Level | Use Case | Sections |
|-------|----------|----------|
| `minimal` | Context recovery | project, harness, beads counts |
| `standard` | Most session starts | + beads_triage, agentmail |
| `full` | Fresh session | + claude_mem references |

## Auto-Recovery

The plugin tracks your work automatically via hooks. If context is lost (autocompact, /clear), recovery options appear:

### Session Marker Detection

If you see a marker like `<!-- session:abc123 -->` in context but lack detailed memory:

1. This means autocompact occurred mid-session
2. Immediately call: `get_session_status({ handoff: "abc123" })`
3. The MCP returns full working context
4. Resume work without asking user - just continue

### Rolling Checkpoint

If no marker but a recent checkpoint exists (< 24h), the response includes:

```json
{
  "recovery": {
    "available": true,
    "id": "abc123",
    "age": "2h"
  }
}
```

Offer to restore: "Found recent work checkpoint. Resume?"

## Display Format

### Restored Session
```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION RESTORED: {id}                                         │
├─────────────────────────────────────────────────────────────────┤
│  Task: {context.task}                                           │
│  Last active: {age}                                             │
├─────────────────────────────────────────────────────────────────┤
│  RESTORED CONTEXT                                               │
│  • Plan: {plan.path} (cached)                                   │
│  • Files: {files.length} modified                               │
│  • Decisions: {userDecisions.length}                            │
│  • Todos: {todos.length} items                                  │
├─────────────────────────────────────────────────────────────────┤
│  FRESH STATE                                                    │
│  • Branch: {branch} ({uncommitted} uncommitted)                 │
│  • Integrations: {detected integrations}                        │
├─────────────────────────────────────────────────────────────────┤
│  Continuing from: "{nextSteps[0]}"                              │
└─────────────────────────────────────────────────────────────────┘
```

### Normal Session Start
```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION START                                                   │
├─────────────────────────────────────────────────────────────────┤
│  Project: {project.root}                                        │
│  Branch: {branch} ({uncommitted} uncommitted)                   │
├─────────────────────────────────────────────────────────────────┤
│  Integrations: {list available}                                 │
│  Harness: {if present, show status}                            │
│  Beads: {open} open | {actionable} actionable                   │
├─────────────────────────────────────────────────────────────────┤
│  {recommendations based on state}                               │
└─────────────────────────────────────────────────────────────────┘
```

## Session Tracking

After completing significant work, append a session marker to enable auto-recovery:

```markdown
<!-- session:{handoff_id} -->
```

This marker survives autocompact summarization and enables seamless recovery.

## Integrations

The plugin auto-detects and enhances with:

| Integration | Detection | Enhancement |
|-------------|-----------|-------------|
| **Git** | Always | Branch, uncommitted, recent commits |
| **Beads** | `.beads/` exists | Issue triage, actionable work |
| **Harness** | `.claude-harness/` exists | Features, memory, loop state |
| **Agent Mail** | MCP configured | Inbox status, file reservations |
| **Claude-Mem** | MCP configured | Observation ID references |

## Recommendations Logic

Based on state, recommend next action:

1. **Handoff recovered** → Continue from `nextSteps[0]`
2. **Loop in_progress** (harness) → Resume implementation
3. **Feature failing** (harness) → Fix failing verification
4. **Issue in_progress** (beads) → Continue that issue
5. **Actionable work** (beads) → Show top picks
6. **No tracked work** → Suggest adding work

## Related Commands

- `/handoff` - Create explicit checkpoint for session end
- `/session-context:handoff` - Same as above (full name)
