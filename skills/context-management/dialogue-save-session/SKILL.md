---
name: dialogue-save-session
description: Save session context for continuity across sessions. Creates a per-user session memo capturing active focus, recent work, and open questions. Triggers on "save session", "end session", "session memo", "remember context".
---

# Skill: Save Session

Saves session context to a per-user session memo file for continuity across Claude sessions. This implements the TMS externalisation operation.

## When to Use

- At the end of a work session to preserve context
- Before switching to a different task or project
- When you want the next session to have context about current work

## How It Works

Session memos are stored per-user at `.dialogue/session-memo-{username}.yaml`. This supports multi-user workflows where each developer has their own session state that doesn't conflict with others.

At session start, the Dialogue Framework hook reads your session memo and includes key context in the system message.

## Schema

```yaml
# Session memo for {username}
username: "pidster"
last_session: "2026-01-16T18:30:00Z"
active_focus: "FW-017: Merge-Friendly Artifact Structure"
recent_tasks:
  - "FW-017"  # Tasks worked on
recent_decisions:
  - "DEC-20260116-180240"  # Decisions made
open_questions:
  - "How should session memos handle task completion?"
notes: |
  Optional freeform notes about session context.
```

## To Save Session Context

Gather the following information and write to `.dialogue/session-memo-{username}.yaml`:

1. **Determine username**: Use `$USER` environment variable
2. **Identify active focus**: Current task or primary activity
3. **List recent work**: Task IDs worked on, decisions made
4. **Note open questions**: Unresolved questions or blockers
5. **Write file**: Create/update `.dialogue/session-memo-{username}.yaml`

### Example

```bash
# Determine username
USERNAME="${USER:-$(whoami)}"

# Write session memo
cat > .dialogue/session-memo-${USERNAME}.yaml << 'EOF'
username: "pidster"
last_session: "2026-01-16T18:30:00Z"
active_focus: "FW-017: Merge-Friendly Artifact Structure"
recent_tasks:
  - "FW-017"
recent_decisions:
  - "DEC-20260116-180240"
open_questions:
  - "How should session memos handle multi-session context?"
notes: |
  Completed per-file migration. Next: test with new session.
EOF
```

## Multi-User Workflow

Each user has their own session memo file:
- `session-memo-pidster.yaml`
- `session-memo-alice.yaml`
- `session-memo-bob.yaml`

This avoids merge conflicts in distributed VCS workflows - session state is personal context, not shared state.

## Relationship to Other Skills

| Skill | Purpose |
|-------|---------|
| `dialogue-manage-tasks` | Track shared task state |
| `dialogue-log-decision` | Record shared decisions |
| `dialogue-save-session` | Preserve personal session context |

Session memos reference tasks and decisions but contain personal context about what *you* were working on, not the shared project state.
