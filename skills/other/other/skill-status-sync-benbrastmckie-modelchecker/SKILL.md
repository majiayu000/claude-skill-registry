---
name: skill-status-sync
description: Atomically update task status across TODO.md and state.json. Invoke when task status changes.
allowed-tools: Read, Write, Edit
context: fork
---

# Status Sync Skill

Atomic status updates across TODO.md and state.json.

## Trigger Conditions

This skill activates when:
- Task status needs to change
- Artifacts are added to a task
- Task metadata needs updating

## Two-Phase Commit Pattern

### Phase 1: Prepare

1. **Read Current State** (using jq/grep for efficiency)
   ```bash
   # Read task from state.json via jq (fast, ~12ms)
   task_data=$(jq -r --arg num "$task_number" \
     '.active_projects[] | select(.project_number == ($num | tonumber))' \
     .claude/specs/state.json)

   # Read next_project_number for create operations
   next_num=$(jq -r '.next_project_number' .claude/specs/state.json)

   # Find task section in TODO.md via grep
   task_line=$(grep -n "^### ${task_number}\." .claude/specs/TODO.md | cut -d: -f1)
   ```

2. **Validate Task Exists**
   - Check task_data is not empty (state.json)
   - Check task_line is found (TODO.md)
   - If not in both: Error

3. **Prepare Updates**
   - Calculate new status
   - Prepare jq update for state.json
   - Prepare Edit for TODO.md task entry
   - For create operations: also prepare frontmatter update
   - Validate both are consistent

### Phase 2: Commit

1. **Write state.json First**
   - Machine state is source of truth
   - Faster to query and validate

2. **Write TODO.md Second**
   - User-facing representation
   - May have formatting variations

3. **Verify Both Updated**
   - Re-read both files
   - Confirm changes applied

### Rollback (if needed)

If any write fails:
1. Log the failure
2. Attempt to restore original state
3. Return error with details

## Status Mapping

| Operation | Old Status | New Status | Sets Timestamp |
|-----------|------------|------------|----------------|
| Start research | not_started | researching | `started` (if null) |
| Complete research | researching | researched | `researched` |
| Start planning | researched | planning | - |
| Complete planning | planning | planned | `planned` |
| Start implement | planned | implementing | - |
| Complete implement | implementing | completed | `completed` |
| Block task | any | blocked | - |
| Abandon task | any | abandoned | - |

### Timestamp Fields
Lifecycle timestamps track when each phase completed:
- `started`: ISO date (YYYY-MM-DD) when work began
- `researched`: ISO date when research completed
- `planned`: ISO date when planning completed
- `completed`: ISO date when implementation completed

## Task Creation (Special Case)

When creating a new task, BOTH files require additional updates beyond task entries:

### state.json Updates
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.next_project_number = ($next_num | tonumber) + 1 |
   .active_projects = [{new_task_object}] + .active_projects' \
  .claude/specs/state.json > /tmp/state.json && \
  mv /tmp/state.json .claude/specs/state.json
```

### TODO.md Updates (TWO parts)
1. **Frontmatter**: Update `next_project_number` in YAML frontmatter
   ```bash
   # Use sed or Edit to update frontmatter
   sed -i 's/^next_project_number: [0-9]*/next_project_number: NEW_NUM/' \
     .claude/specs/TODO.md
   ```

2. **Task Entry**: Add entry under appropriate priority section

**CRITICAL**: `next_project_number` MUST match in both files after creation.

## Update Formats

### state.json Update
```json
{
  "project_number": N,
  "status": "new_status",
  "last_updated": "ISO_TIMESTAMP",
  "started": "YYYY-MM-DD",
  "researched": "YYYY-MM-DD",
  "planned": "YYYY-MM-DD",
  "completed": "YYYY-MM-DD",
  "artifacts": ["path1", "path2"]
}
```

### TODO.md Update
```markdown
### {N}. {Title}
- **Status**: [{NEW_STATUS}]
- **Started**: {YYYY-MM-DD}
- **Researched**: {YYYY-MM-DD}
- **Planned**: {YYYY-MM-DD}
- **Completed**: {YYYY-MM-DD}
- **{Artifact}**: [link](path)
```

## Timestamp Update Patterns

### Set Timestamp (state.json)
```bash
# Set a specific timestamp field
jq --arg ts "$(date +%Y-%m-%d)" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    "started": $ts,
    "last_updated": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }' .claude/specs/state.json > /tmp/state.json && \
  mv /tmp/state.json .claude/specs/state.json
```

### Set Timestamp (TODO.md)
Use Edit tool to add/update timestamp line in task entry:
```markdown
- **Started**: 2026-01-10
```

### Add Artifact (state.json)
```bash
# Add artifact to artifacts array
jq --arg path "$artifact_path" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    "artifacts": ((.artifacts // []) + [$path]),
    "last_updated": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }' .claude/specs/state.json > /tmp/state.json && \
  mv /tmp/state.json .claude/specs/state.json
```

## Task Counts Management

### Calculate task_counts
```bash
# Calculate counts from active_projects
active=$(jq '[.active_projects[] | select(.status != "completed" and .status != "abandoned")] | length' .claude/specs/state.json)
completed=$(jq '[.active_projects[] | select(.status == "completed")] | length' .claude/specs/state.json)
in_progress=$(jq '[.active_projects[] | select(.status == "implementing" or .status == "researching" or .status == "planning")] | length' .claude/specs/state.json)
```

### Update TODO.md Frontmatter task_counts
After calculating, update the frontmatter:
```yaml
task_counts:
  active: {active}
  completed: {completed}
  in_progress: {in_progress}
```

### When to Update task_counts
- After task creation (/task)
- After task completion (/implement)
- After task archival (/todo)

## Execution Flow

```
1. Receive update request:
   - task_number
   - new_status
   - artifacts (optional)
   - metadata (optional)

2. Phase 1 - Prepare:
   - Read both files
   - Validate task exists
   - Prepare updates

3. Phase 2 - Commit:
   - Write state.json
   - Write TODO.md
   - Verify success

4. Return result
```

## Return Format

```json
{
  "status": "completed|failed",
  "summary": "Updated task #N to [STATUS]",
  "task_number": N,
  "old_status": "previous",
  "new_status": "current",
  "files_updated": [
    ".claude/specs/state.json",
    ".claude/specs/TODO.md"
  ]
}
```

## Error Handling

### File Read Error
```json
{
  "status": "failed",
  "error": "Could not read state.json",
  "recovery": "Check file exists and permissions"
}
```

### Task Not Found
```json
{
  "status": "failed",
  "error": "Task #N not found",
  "recovery": "Verify task number, check if archived"
}
```

### Write Failure
```json
{
  "status": "failed",
  "error": "Failed to write TODO.md",
  "recovery": "Check permissions, state.json may be updated"
}
```

### Inconsistency Detected
```json
{
  "status": "failed",
  "error": "TODO.md and state.json inconsistent",
  "recovery": "Run /task --sync to reconcile"
}
```
