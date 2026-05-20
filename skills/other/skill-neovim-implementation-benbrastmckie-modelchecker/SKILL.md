---
name: skill-neovim-implementation
description: Implement Neovim configuration changes from plans. Invoke for neovim implementation tasks.
allowed-tools: Task, Bash, Edit, Read, Write
---

# Neovim Implementation Skill

Thin wrapper that delegates Neovim implementation to `neovim-implementation-agent` subagent.

**IMPORTANT**: This skill implements the skill-internal postflight pattern. After the subagent returns,
this skill handles all postflight operations (status update, artifact linking, git commit) before returning.

## Context References

Reference (do not load eagerly):
- Path: `.claude/context/core/formats/return-metadata-file.md` - Metadata file schema
- Path: `.claude/context/core/patterns/postflight-control.md` - Marker file protocol
- Path: `.claude/context/core/patterns/jq-escaping-workarounds.md` - jq escaping patterns

## Trigger Conditions

This skill activates when:
- Task language is "neovim"
- Implementation plan exists for the task
- Neovim configuration changes need to be applied

---

## Execution Flow

### Stage 1: Input Validation

Validate required inputs:
- `task_number` - Must be provided and exist in state.json
- `plan_path` - Implementation plan must exist

```bash
# Lookup task
task_data=$(jq -r --argjson num "$task_number" \
  '.active_projects[] | select(.project_number == $num)' \
  specs/state.json)

# Validate exists
if [ -z "$task_data" ]; then
  return error "Task $task_number not found"
fi

# Extract fields
language=$(echo "$task_data" | jq -r '.language // "neovim"')
status=$(echo "$task_data" | jq -r '.status')
project_name=$(echo "$task_data" | jq -r '.project_name')

# Find plan file (use padded directory number)
padded_num=$(printf "%03d" "$task_number")
plan_path="specs/${padded_num}_${project_name}/plans/implementation-001.md"
if [ ! -f "$plan_path" ]; then
  return error "Plan not found: $plan_path"
fi
```

---

### Stage 2: Preflight Status Update

Update task status to "implementing" BEFORE invoking subagent.

**Update state.json**:
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg status "implementing" \
   --arg sid "$session_id" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    status: $status,
    last_updated: $ts,
    session_id: $sid
  }' specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
```

**Update TODO.md**: Use Edit tool to change status marker to `[IMPLEMENTING]`.

**Update plan file** (if exists): Update the Status field in plan metadata:
```bash
# Find latest plan file
plan_file=$(ls -1 "specs/${padded_num}_${project_name}/plans/implementation-"*.md 2>/dev/null | sort -V | tail -1)
if [ -n "$plan_file" ] && [ -f "$plan_file" ]; then
    # Try bullet pattern first, then non-bullet pattern
    sed -i 's/^\- \*\*Status\*\*: \[.*\]$/- **Status**: [IMPLEMENTING]/' "$plan_file"
    sed -i 's/^\*\*Status\*\*: \[.*\]$/**Status**: [IMPLEMENTING]/' "$plan_file"
fi
```

---

### Stage 3: Create Postflight Marker

```bash
mkdir -p "specs/${padded_num}_${project_name}"

cat > "specs/${padded_num}_${project_name}/.postflight-pending" << EOF
{
  "session_id": "${session_id}",
  "skill": "skill-neovim-implementation",
  "task_number": ${task_number},
  "operation": "implement",
  "reason": "Postflight pending: status update, artifact linking, git commit",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

---

### Stage 4: Prepare Delegation Context

```json
{
  "session_id": "sess_{timestamp}_{random}",
  "delegation_depth": 1,
  "delegation_path": ["orchestrator", "implement", "skill-neovim-implementation"],
  "timeout": 3600,
  "task_context": {
    "task_number": N,
    "task_name": "{project_name}",
    "description": "{description}",
    "language": "neovim"
  },
  "plan_path": "specs/{NNN}_{SLUG}/plans/implementation-001.md",
  "metadata_file_path": "specs/{NNN}_{SLUG}/.return-meta.json"
}
```

---

### Stage 5: Invoke Subagent

**CRITICAL**: You MUST use the **Task** tool to spawn the subagent.

```
Tool: Task (NOT Skill)
Parameters:
  - subagent_type: "neovim-implementation-agent"
  - prompt: [Include task_context, delegation_context, plan_path, metadata_file_path]
  - description: "Execute Neovim implementation for task {N}"
```

The subagent will:
- Read and parse implementation plan
- Execute phases sequentially
- Create/modify Neovim config files
- Verify changes with nvim --headless
- Create implementation summary
- Write metadata file
- Return brief text summary

---

### Stage 5a: Validate Subagent Return Format

**IMPORTANT**: Check if subagent accidentally returned JSON to console (v1 pattern) instead of writing to file (v2 pattern).

If the subagent's text return parses as valid JSON, log a warning:

```bash
# Check if subagent return looks like JSON (starts with { and is valid JSON)
subagent_return="$SUBAGENT_TEXT_RETURN"
if echo "$subagent_return" | grep -q '^{' && echo "$subagent_return" | jq empty 2>/dev/null; then
    echo "WARNING: Subagent returned JSON to console instead of writing metadata file."
    echo "This indicates the agent may have outdated instructions (v1 pattern instead of v2)."
    echo "The skill will continue by reading the metadata file, but this should be fixed."
fi
```

This validation:
- Does NOT fail the operation (continues to read metadata file)
- Logs a warning for debugging
- Indicates the subagent instructions need updating
- Allows graceful handling of mixed v1/v2 agents

---

### Stage 6: Parse Subagent Return

```bash
metadata_file="specs/${padded_num}_${project_name}/.return-meta.json"

if [ -f "$metadata_file" ] && jq empty "$metadata_file" 2>/dev/null; then
    status=$(jq -r '.status' "$metadata_file")
    phases_completed=$(jq -r '.metadata.phases_completed // 0' "$metadata_file")
    phases_total=$(jq -r '.metadata.phases_total // 0' "$metadata_file")

    # Extract completion_data fields (if present)
    completion_summary=$(jq -r '.completion_data.completion_summary // ""' "$metadata_file")
    roadmap_items=$(jq -c '.completion_data.roadmap_items // []' "$metadata_file")
else
    status="failed"
fi
```

---

### Stage 7: Update Task Status (Postflight)

If status is "implemented", update state.json and TODO.md.

**Update state.json**:
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg status "completed" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    status: $status,
    last_updated: $ts,
    completed: $ts
  }' specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json

# Add completion_summary (always required for completed tasks)
if [ -n "$completion_summary" ]; then
    jq --arg summary "$completion_summary" \
      '(.active_projects[] | select(.project_number == '$task_number')).completion_summary = $summary' \
      specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
fi

# Add roadmap_items (if present and non-empty)
if [ "$roadmap_items" != "[]" ] && [ -n "$roadmap_items" ]; then
    jq --argjson items "$roadmap_items" \
      '(.active_projects[] | select(.project_number == '$task_number')).roadmap_items = $items' \
      specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
fi
```

**Update TODO.md**: Use Edit tool to change status marker to `[COMPLETED]`.

**Update plan file** (if exists): Update the Status field to `[COMPLETED]` with verification:
```bash
plan_file=$(ls -1 "specs/${padded_num}_${project_name}/plans/implementation-"*.md 2>/dev/null | sort -V | tail -1)
if [ -n "$plan_file" ] && [ -f "$plan_file" ]; then
    # Try bullet pattern first, then non-bullet pattern
    sed -i 's/^\- \*\*Status\*\*: \[.*\]$/- **Status**: [COMPLETED]/' "$plan_file"
    sed -i 's/^\*\*Status\*\*: \[.*\]$/**Status**: [COMPLETED]/' "$plan_file"
    # Verify update
    if grep -qE '^\*\*Status\*\*: \[COMPLETED\]|^\- \*\*Status\*\*: \[COMPLETED\]' "$plan_file"; then
        echo "Plan file status updated to [COMPLETED]"
    else
        echo "WARNING: Could not verify plan file status update"
    fi
else
    echo "INFO: No plan file found to update (file: $plan_file)"
fi
```

**If status is "partial"**:

Keep status as "implementing" but update resume point:
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --argjson phase "$phases_completed" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    last_updated: $ts,
    resume_phase: ($phase + 1)
  }' specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
```

TODO.md stays as `[IMPLEMENTING]`.

**Update plan file** (if exists): Update the Status field to `[PARTIAL]` with verification:
```bash
plan_file=$(ls -1 "specs/${padded_num}_${project_name}/plans/implementation-"*.md 2>/dev/null | sort -V | tail -1)
if [ -n "$plan_file" ] && [ -f "$plan_file" ]; then
    # Try bullet pattern first, then non-bullet pattern
    sed -i 's/^\- \*\*Status\*\*: \[.*\]$/- **Status**: [PARTIAL]/' "$plan_file"
    sed -i 's/^\*\*Status\*\*: \[.*\]$/**Status**: [PARTIAL]/' "$plan_file"
    # Verify update
    if grep -qE '^\*\*Status\*\*: \[PARTIAL\]|^\- \*\*Status\*\*: \[PARTIAL\]' "$plan_file"; then
        echo "Plan file status updated to [PARTIAL]"
    else
        echo "WARNING: Could not verify plan file status update"
    fi
else
    echo "INFO: No plan file found to update (directory: specs/${padded_num}_${project_name}/plans/)"
fi
```

**On failed**: Keep status as "implementing" for retry. Do not update plan file (leave as `[IMPLEMENTING]` for retry).

---

### Stage 8: Link Artifacts

Add implementation artifacts to state.json.

---

### Stage 9: Git Commit

```bash
git add -A
git commit -m "task ${task_number}: complete implementation

Session: ${session_id}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

### Stage 10: Cleanup

```bash
rm -f "specs/${padded_num}_${project_name}/.postflight-pending"
rm -f "specs/${padded_num}_${project_name}/.return-meta.json"
```

---

### Stage 11: Return Brief Summary

```
Implementation completed for task {N}:
- Executed {phases_completed}/{phases_total} phases
- Created/modified Neovim config files
- Verified startup and module loading
- Created summary at specs/{NNN}_{SLUG}/summaries/implementation-summary-{DATE}.md
- Status updated to [COMPLETED]
- Changes committed
```

---

## Error Handling

### Plan Not Found
Return error if implementation plan doesn't exist.

### Verification Failure
If nvim --headless fails:
1. Keep status as "implementing"
2. Mark phase as [PARTIAL]
3. Report verification error

### Git Commit Failure
Non-blocking: Log failure but continue.

---

## Return Format

Brief text summary (NOT JSON).
