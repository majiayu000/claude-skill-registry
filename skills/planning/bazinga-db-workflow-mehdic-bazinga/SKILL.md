---
name: bazinga-db-workflow
description: Task groups and development planning. Use when managing task groups, development plans, or success criteria.
version: 2.0.0
allowed-tools: [Bash, Read]
---

# BAZINGA-DB Workflow Skill

You are the bazinga-db-workflow skill. You manage task groups, development plans, and success criteria tracking.

## When to Invoke This Skill

**Invoke when:**
- Creating or updating task groups
- Saving or retrieving development plans
- Managing success criteria
- Tracking plan progress

**Do NOT invoke when:**
- Managing sessions or state → Use `bazinga-db-core`
- Logging interactions or reasoning → Use `bazinga-db-agents`
- Managing context packages → Use `bazinga-db-context`

## Script Location

**Path:** `.claude/skills/bazinga-db/scripts/bazinga_db.py`

All commands use this script with `--quiet` flag:
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet <command> [args...]
```

## Commands

### create-task-group

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet create-task-group \
  "<group_id>" "<session_id>" "<description>" \
  [--specializations '<json_array>'] [--item_count N] [--initial_tier "<tier>"] \
  [--component-path "<path>"] [--complexity N] [--security_sensitive 0|1]
```

**Parameters:**
- `group_id`: Short identifier (e.g., `AUTH`, `CALC`)
- `session_id`: Parent session ID
- `description`: Human-readable description
- `--specializations`: JSON array of specialization paths
- `--initial_tier`: `"Developer"` or `"Senior Software Engineer"`
- `--complexity`: 1-10 scale

**Returns:** Created task group object.

### update-task-group

**CRITICAL: Argument order is `<group_id> <session_id>` (NOT session first)**

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-task-group \
  "<group_id>" "<session_id>" [--status "<status>"] [--assigned_to "<agent_id>"] \
  [--specializations '<json_array>'] [--item_count N] [--initial_tier "<tier>"] \
  [--component-path "<path>"] [--qa_attempts N] [--tl_review_attempts N] \
  [--security_sensitive 0|1] [--complexity N] \
  [--review_iteration N] [--no_progress_count N] [--blocking_issues_count N]
```

**Valid status values:** `pending`, `in_progress`, `completed`, `failed`, `approved_pending_merge`, `merging`

**Review iteration fields (v16):**
- `review_iteration`: Current iteration in TL→Dev feedback loop (starts at 1)
- `no_progress_count`: Consecutive iterations with 0 issues fixed (escalation at 2)
- `blocking_issues_count`: Current unresolved CRITICAL/HIGH issues

**Example:**
```bash
python3 .../bazinga_db.py --quiet update-task-group "CALC" "bazinga_xxx" --status "in_progress"
```

### get-task-groups

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-task-groups \
  "<session_id>" [status]
```

**Returns:** Array of task groups for the session, optionally filtered by status.

### save-development-plan

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-development-plan \
  "<session_id>" '<json_plan>'
```

Saves PM's development plan with phases, estimates, and dependencies.

**Example:**
```bash
python3 .../bazinga_db.py --quiet save-development-plan "bazinga_xxx" \
  '{"phases": [{"name": "Core", "tasks": [...]}], "estimated_groups": 3}'
```

### get-development-plan

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-development-plan "<session_id>"
```

**Returns:** Latest development plan for the session.

### update-plan-progress

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-plan-progress \
  "<session_id>" "<phase_name>" "<status>" [progress_percent]
```

Updates phase status within the development plan.

**Valid status values:** `pending`, `in_progress`, `completed`, `blocked`

### save-success-criteria

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-success-criteria \
  "<session_id>" '<json_criteria_array>'
```

**Format:**
```json
[
  {"criterion": "All tests pass", "status": "pending", "priority": 1},
  {"criterion": "Code review approved", "status": "pending", "priority": 2}
]
```

### get-success-criteria

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-success-criteria "<session_id>"
```

**Returns:** Array of success criteria with current status.

### update-success-criterion

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-success-criterion \
  "<session_id>" "<criterion_text>" "<status>" [notes]
```

**Valid status values:** `pending`, `met`, `failed`, `blocked`

## Output Format

Return ONLY raw JSON output. No formatting, markdown, or commentary.

## Error Handling

- Missing task group: Returns `{"error": "Task group not found: <id>"}`
- Invalid status: Returns `{"error": "Invalid status: <status>"}`
- Argument order error: Check `<group_id>` comes before `<session_id>`

## References

- Full schema: `.claude/skills/bazinga-db/references/schema.md`
- All commands: `.claude/skills/bazinga-db/references/command_examples.md`
- CLI help: `python3 .../bazinga_db.py help`
