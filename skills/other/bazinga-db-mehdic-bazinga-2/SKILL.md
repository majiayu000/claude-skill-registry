---
name: bazinga-db
description: DEPRECATED - Use domain-specific skills instead. Routes to bazinga-db-core, bazinga-db-workflow, bazinga-db-agents, or bazinga-db-context.
version: 2.0.0
allowed-tools: [Bash, Read]
---

# BAZINGA-DB (Deprecated Router)

**This skill is deprecated.** Use domain-specific skills instead:

| Domain | Skill | Use For |
|--------|-------|---------|
| Sessions & State | `bazinga-db-core` | Sessions, state snapshots, dashboard |
| Tasks & Plans | `bazinga-db-workflow` | Task groups, development plans, success criteria |
| Agent Tracking | `bazinga-db-agents` | Logs, reasoning, tokens, skill output, events |
| Context & Learning | `bazinga-db-context` | Context packages, error patterns, strategies |

## Command Routing Table

| Command | Target Skill |
|---------|--------------|
| `create-session`, `get-session`, `list-sessions` | `bazinga-db-core` |
| `update-session-status`, `save-state`, `get-state` | `bazinga-db-core` |
| `dashboard-snapshot`, `query`, `integrity-check` | `bazinga-db-core` |
| `recover-db`, `detect-paths` | `bazinga-db-core` |
| `create-task-group`, `update-task-group`, `get-task-groups` | `bazinga-db-workflow` |
| `save-development-plan`, `get-development-plan`, `update-plan-progress` | `bazinga-db-workflow` |
| `save-success-criteria`, `get-success-criteria`, `update-success-criterion` | `bazinga-db-workflow` |
| `log-interaction`, `stream-logs` | `bazinga-db-agents` |
| `save-reasoning`, `get-reasoning`, `reasoning-timeline` | `bazinga-db-agents` |
| `check-mandatory-phases` | `bazinga-db-agents` |
| `log-tokens`, `token-summary` | `bazinga-db-agents` |
| `save-skill-output`, `get-skill-output`, `get-skill-output-all` | `bazinga-db-agents` |
| `check-skill-evidence` | `bazinga-db-agents` |
| `save-event`, `get-events` | `bazinga-db-agents` |
| `save-context-package`, `get-context-packages`, `mark-context-consumed` | `bazinga-db-context` |
| `update-context-references` | `bazinga-db-context` |
| `save-consumption`, `get-consumption` | `bazinga-db-context` |
| `save-error-pattern`, `get-error-patterns` | `bazinga-db-context` |
| `update-error-confidence`, `cleanup-error-patterns` | `bazinga-db-context` |
| `save-strategy`, `get-strategies` | `bazinga-db-context` |
| `update-strategy-helpfulness`, `extract-strategies` | `bazinga-db-context` |

## Quick Reference

⚠️ **DO NOT use CLI directly.** Instead, invoke the domain-specific skill:

| Need | Invoke |
|------|--------|
| Session/state ops | `Skill(command: "bazinga-db-core")` |
| Task groups/plans | `Skill(command: "bazinga-db-workflow")` |
| Logging/reasoning | `Skill(command: "bazinga-db-agents")` |
| Context packages | `Skill(command: "bazinga-db-context")` |

**Reference docs (for skill authors only):**
- Schema: `.claude/skills/bazinga-db/references/schema.md`
- Examples: `.claude/skills/bazinga-db/references/command_examples.md`

## If You're Here By Mistake

1. Identify what you're trying to do
2. Invoke the correct domain skill:
   - Session ops? → `Skill(command: "bazinga-db-core")`
   - Task groups? → `Skill(command: "bazinga-db-workflow")`
   - Logging/reasoning? → `Skill(command: "bazinga-db-agents")`
   - Context packages? → `Skill(command: "bazinga-db-context")`

## Migration Notes

The original monolithic bazinga-db skill (v1.x, 887 lines) has been split into 4 domain-focused skills for better maintainability and to stay within file size limits.

**All scripts remain in this directory:**
- `scripts/bazinga_db.py` - Main CLI (unchanged)
- `scripts/init_db.py` - Database initialization
- `scripts/init_session.py` - Session creation helper

**All references remain in this directory:**
- `references/schema.md` - Full database schema
- `references/command_examples.md` - Detailed command examples

## Technical Notes

### Event Idempotency (v17+)

Events support idempotency keys via `idx_logs_idempotency` unique index:
- Index: `(session_id, event_subtype, group_id, idempotency_key)` WHERE `idempotency_key IS NOT NULL AND log_type = 'event'`
- Pattern: INSERT-first, catch IntegrityError, return existing row
- Recommended key format: `{session_id}|{group_id}|{event_type}|{iteration}`

### Group ID Validation (v18+)

Three explicit validators for group_id scope (See: research/domain-skill-migration-phase6-ultrathink.md):

| Validator | Allows 'global' | Use For |
|-----------|-----------------|---------|
| `validate_scope_global_or_group` | ✅ Yes | Events, reasoning, state (session-level) |
| `validate_scope_group_only` | ❌ No | Investigation state, consumption, strategies |
| `validate_task_group_id` | ❌ No (+ reserved) | Task group creation (rejects 'session', 'all', 'default') |

Reserved identifiers (cannot be used as task_group_id): `global`, `session`, `all`, `default`

### Legacy Data Diagnostic

```bash
# Scan for invalid group_ids (CI/CD)
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py diagnose-group-ids

# Auto-fix issues
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py diagnose-group-ids --fix
```
