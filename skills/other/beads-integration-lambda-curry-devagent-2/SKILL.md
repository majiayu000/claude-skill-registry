---
name: beads-integration
description: "Use Beads CLI (`bd`) commands to manage tasks, status, and progress tracking for Ralph's autonomous execution. Use when: (1) Querying ready tasks with `bd ready`, (2) Updating task status (open → in_progress → closed), (3) Adding progress comments to tasks, (4) Managing task details (priority, design, notes, labels), (5) Handling task dependencies. This skill enables Ralph to use Beads' native memory and state management."
---

# Beads Integration

Use Beads CLI (`bd`) commands for task management, status tracking, and progress comments.

## Prerequisites

- Beads CLI (`bd`) installed and available in PATH
- Beads database initialized (`.beads/beads.db`)
- **Recommended for setup workflows:** Prefer direct mode to avoid daemon staleness during ID creation and dependency wiring:
  ```bash
  export BD_NO_DAEMON=1
  ```

## Core Commands

### Query Ready Tasks

**Get next available task:**

```bash
bd ready --json
```

**Scope ready work to an epic (recommended for Ralph):**

```bash
bd ready --parent <EPIC_ID> --limit 200 --json
```

**Get ready tasks for specific project:**

```bash
bd ready --project <project-name> --json
```

- `bd ready --json` returns an array of tasks that are in `open` status and have all dependencies met.
- `bd ready` defaults to `--limit 10`, so increase the limit for epics to avoid hiding ready tasks.
- Use `--parent <EPIC_ID>` when you need only tasks for a specific epic; this avoids missing tasks due to global sorting/limits.
- Use `jq -r '.[0]?.id // empty'` for first task.
- Guard against empty output.

### Update Task Status

**Mark task in progress:**

```bash
bd update <task-id> --status in_progress
```

**Mark task closed (completed):**

```bash
bd update <task-id> --status closed
```

**Reset task to open (if failed or abandoned):**

```bash
bd update <task-id> --status open
```

**Block a task:**

```bash
bd update <task-id> --status blocked
```

**Note:** `ready` is NOT a valid settable status. Use `open`.

### Manage Task Details

**Set Priority:**

```bash
bd update <task-id> --priority P0  # Critical
bd update <task-id> --priority P1  # High
bd update <task-id> --priority P2  # Medium (Default)
bd update <task-id> --priority P3  # Low
```

**Add Design & Architecture Notes:**

```bash
bd update <task-id> --design "Use Factory Pattern for widget creation. See design doc at docs/widgets.md"
```

**Add General Notes:**

```bash
bd update <task-id> --notes "Requires update to API schema first."
```

**Set Estimate (Minutes):**

```bash
bd update <task-id> --estimate 60  # 1 hour
```

**Manage Labels:**

```bash
bd update <task-id> --add-label "frontend" --add-label "ui"
bd update <task-id> --remove-label "bug"
```

Alternative label commands (equivalent in most workflows):
```bash
bd label list <task-id>
bd label add <task-id> "frontend"
bd label remove <task-id> "bug"
```

### Add Progress Comments

**List latest comments (required before starting work):**

```bash
bd comments <task-id> --json
```

**Add comment to task:**

```bash
bd comments add <task-id> "<comment-text>"
```

**Safe multiline/markdown (recommended when using backticks or code blocks):**

```bash
cat <<'EOF' > /tmp/bd-comment.md
## Progress Update

- \`bd ready --parent <EPIC_ID>\`
- Added tests and updated docs
EOF

bd comments add <task-id> -f /tmp/bd-comment.md
rm /tmp/bd-comment.md
```

**Comment Format:**

- Use markdown formatting.
- Include timestamps and reasoning.
- Link to files changed or external references.

**Example:**

```bash
bd comments add bd-a3f8.1 "## Progress Update

- ✅ Completed function implementation
- ✅ Added unit tests
- 📝 Updated documentation"
```

### Import Tasks from JSON Payload

**Create Task:**

```bash
bd create --title "<title>" --description "<desc>" --priority P2 --labels "engineering" --json
# Note: bd create does NOT support --status flag. Set status after creation:
# bd update <task-id> --status open
```

**Import with Dependencies:**

```bash
bd create --title "<child>" --parent <parent-id> --deps <dep-id> --json
# Note: bd create does NOT support --status flag. Set status after creation:
# bd update <task-id> --status open
# Also note: Use --deps (not --depends-on) for dependencies
```

## Hierarchical Task IDs

Beads supports hierarchical task IDs (e.g., `project-abc.1`, `project-abc.1.1`):

- Parent relationship is **automatically inferred** from the ID structure
- Do NOT use `--parent` flag when creating tasks with hierarchical IDs
- Example: `bd create --id project-abc.1 --title "Task"` automatically sets parent to `project-abc`

**Common mistake:**
```bash
# ❌ WRONG - will error: "cannot specify both --id and --parent flags"
bd create --id project-abc.1 --parent project-abc --title "Task"

# ✅ CORRECT
bd create --id project-abc.1 --title "Task"
```

## Handling Multiline Content

For descriptions or notes with newlines:

1. Write content to temporary file
2. Use `--body-file` flag instead of `--description` or `--notes`
3. Clean up temp file after creation

**Example:**
```bash
echo "Line 1\nLine 2" > /tmp/desc.txt
bd create --title "Task" --body-file /tmp/desc.txt
rm /tmp/desc.txt
```

**Why use `--body-file`?**
- Inline `--description` with newlines can cause parsing errors
- `--body-file` handles multiline content reliably
- Always use `--body-file` for descriptions containing newlines

## Using --force Flag

The `--force` flag is required when:

- Creating tasks with explicit IDs that match the database prefix
- Overriding prefix validation warnings

**When to use:**
```bash
# When creating task with explicit ID matching database prefix
bd create --id project-abc.1 --title "Task" --force

# When prefix validation requires override
bd create --id project-abc.1 --title "Task" --force --json
```

**When NOT to use:**
- Don't use `--force` to bypass dependency checks
- Don't use `--force` if you're unsure about prefix compatibility
- Always verify prefix matches database before using `--force`

**Prefix Detection:**
```bash
# First, try to get prefix from database configuration (most reliable)
DB_PREFIX=$(bd config get issue_prefix 2>/dev/null | tr -d '\n' | grep -v "Error\|not found" || echo "")

# Fallback: try to get prefix from existing tasks
if [ -z "$DB_PREFIX" ] || [ "$DB_PREFIX" = "" ]; then
  DB_PREFIX=$(bd list --json 2>/dev/null | jq -r '.[0].id' | cut -d'-' -f1-2)
fi

# Final fallback: use directory name (matches bd init default behavior)
if [ -z "$DB_PREFIX" ] || [ "$DB_PREFIX" = "null" ] || [ "$DB_PREFIX" = "" ]; then
  DB_PREFIX=$(basename "$(pwd)")
  # Last resort: default to "bd" only if directory name is invalid
  if [ -z "$DB_PREFIX" ] || [ "$DB_PREFIX" = "." ] || [ "$DB_PREFIX" = ".." ]; then
    DB_PREFIX="bd"
  fi
fi
```

**Important:** `bd init` stores the prefix in database configuration (`issue_prefix`). Always query the configured prefix first using `bd config get issue_prefix` to avoid mismatches between what `bd init` set and what we detect from tasks.

## Workflow Patterns

### Autonomous Execution Loop

1. **Select Next Task:** `bd ready --parent <EPIC_ID> --limit 200 --json`
2. **Mark In Progress:** `bd update <task-id> --status in_progress`
3. **Read Details:** `bd show <task-id> --json` (Check `description`, `design`, `notes`, `acceptance_criteria`)
4. **Implement:** Write code, run tests.
5. **Log Progress:** `bd comments add <task-id> "..."`
6. **Mark Complete:** `bd update <task-id> --status closed`

### Dependency Management

**Check Dependencies:**

```bash
bd show <task-id> --json
```

Check `depends_on` array. Tasks with incomplete dependencies will not appear in `bd ready`.

## Error Handling

- **Invalid Status:** Do not use `ready` as a status. Use `open`.
- **Task Not Found:** Check ID.
- **Locked DB:** If DB is locked, wait and retry.

## Best Practices

### Task Creation & Naming

**Core Principle: Atomicity**

- Create focused, single-purpose tasks with clear, actionable titles
- Each task should be small enough for fast agent processing
- Break large tasks into smaller, atomic beads

**Title Guidelines:**
✅ **Good Task Titles:**

- "Add user authentication endpoint"
- "Fix memory leak in WebSocket handler"
- "Create database migration for user schema"
- "Update TypeScript interface for HealthResponse"
- "Remove CPU metrics from healthcheck UI"

❌ **Poor Task Titles:**

- "Fix stuff"
- "Update code"
- "Make it better"
- "Handle edge cases"
- "Do the thing"

**Title Format Rules:**

1. Start with action verb (imperative mood): "Add", "Fix", "Create", "Update", "Refactor", "Document"
2. Be specific: Include what and where (e.g., "Add pagination to user list endpoint")
3. Keep concise: Aim for 50-70 characters
4. Use consistent terminology: Align with codebase vocabulary

### Rich Metadata

**Always populate these fields when enriching tasks:**

1. **Description (`--description`)**:
   - Clear objective explaining what the task accomplishes
   - Link to planning documents when available (include specific path)
   - Example: "Update `/api/health` to return only relevant metrics for Vercel serverless architecture. See plan document: `.devagent/workspace/tasks/active/2026-01-10_healthcheck-improvements/plan/2026-01-10_healthcheck-plan.md` for full context."
2. **Design (`--design`)**:
   - Architecture and design decisions
   - Technical considerations and constraints
   - Patterns to follow or avoid
   - Example: "Vercel serverless functions are stateless and ephemeral. Focus on metrics that persist: database connectivity, environment info, deployment status. Avoid collecting metrics that don't persist across invocations."
3. **Notes (`--notes`)**:
   - Context, constraints, or prerequisites
   - References to related work or documentation (always include specific paths)
   - Implementation hints or warnings
   - Example: "Interface changes affect api.health.ts, health.tsx, and app.health.tsx. Plan document: `.devagent/workspace/tasks/active/2026-01-10_healthcheck-improvements/plan/2026-01-10_healthcheck-plan.md`. See plan document for interface requirements."
4. **Acceptance Criteria (`--acceptance`)**:
  - Measurable, verifiable outcomes
  - Specific conditions for task completion
  - Format: Semicolon-separated list of criteria
  - Example: "CPU metrics removed from interface; Memory metrics removed from interface; Interface only contains relevant serverless metrics"

### Priority Guidelines

- **P0 (Critical)**: Blocking work or high-impact items that unblock other tasks
- **P1 (High)**: Important features or fixes with significant impact
- **P2 (Medium)**: Default priority for most tasks
- **P3 (Low)**: Nice-to-have improvements, non-critical work

**Default to P2 unless the task is clearly blocking or high-impact.**

### Task Enrichment Workflow

When enriching existing tasks (e.g., from setup-loop):

1. **Extract from plan document**: Use plan's "Objective", "Acceptance Criteria", architecture notes, and context
2. **Populate description**: Convert objective to clear description
3. **Add design notes**: Extract architecture considerations, technical constraints, patterns
4. **Add general notes**: Include context, file references, related work, quality gates
5. **Set acceptance criteria**: Convert acceptance criteria list to semicolon-separated format

**Example enrichment:**

```bash
bd update task-id \
  --description "Update API endpoint to return simplified health metrics for serverless architecture. See plan document: `.devagent/workspace/tasks/active/2026-01-10_healthcheck-improvements/plan/2026-01-10_healthcheck-plan.md` for full context." \
  --design "Vercel serverless functions are stateless. Focus on: database connectivity, environment info, deployment status. Avoid CPU/memory/uptime metrics." \
  --notes "Endpoint: /api/health. Plan document: `.devagent/workspace/tasks/active/2026-01-10_healthcheck-improvements/plan/2026-01-10_healthcheck-plan.md`. Maintain backward compatibility for 'status' field." \
  --acceptance "CPU metrics removed; Memory metrics removed; Database connectivity included; Deployment info included when available"
```

### Traceability

- **Comment on tasks**: Add progress comments with every commit or significant step
- **Link to commits**: Reference commit SHAs in comments for traceability
- **Document decisions**: Use design field to capture architectural decisions during implementation
- **Update notes**: Add implementation discoveries or constraints to notes field

### JSON Output

Always use `--json` flag for programmatic interaction with Beads CLI to ensure consistent parsing.
