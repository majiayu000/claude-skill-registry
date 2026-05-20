---
name: skill-planner
description: Create phased implementation plans from research findings. Invoke when a task needs an implementation plan.
allowed-tools: Task, Bash, Edit, Read, Write
# Original context (now loaded by subagent):
#   - .claude/context/core/formats/plan-format.md
#   - .claude/context/core/workflows/task-breakdown.md
# Original tools (now used by subagent):
#   - Read, Write, Edit, Glob, Grep
---

# Planner Skill

Thin wrapper that delegates plan creation to `planner-agent` subagent.

**IMPORTANT**: This skill implements the skill-internal postflight pattern. After the subagent returns,
this skill handles all postflight operations (status update, artifact linking, git commit) before returning.
This eliminates the "continue" prompt issue between skill return and orchestrator.

## Context References

Reference (do not load eagerly):
- Path: `.claude/context/core/formats/return-metadata-file.md` - Metadata file schema
- Path: `.claude/context/core/patterns/postflight-control.md` - Marker file protocol
- Path: `.claude/context/core/patterns/file-metadata-exchange.md` - File I/O helpers
- Path: `.claude/context/core/patterns/jq-escaping-workarounds.md` - jq escaping patterns (Issue #1132)

Note: This skill is a thin wrapper with internal postflight. Context is loaded by the delegated agent.

## Trigger Conditions

This skill activates when:
- Task status allows planning (not_started, researched)
- /plan command is invoked
- Implementation approach needs to be formalized

---

## Execution Flow

### Stage 1: Input Validation

Validate required inputs:
- `task_number` - Must be provided and exist in state.json
- Task status must allow planning

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
language=$(echo "$task_data" | jq -r '.language // "general"')
status=$(echo "$task_data" | jq -r '.status')
project_name=$(echo "$task_data" | jq -r '.project_name')
description=$(echo "$task_data" | jq -r '.description // ""')

# Validate status
if [ "$status" = "completed" ]; then
  return error "Task already completed"
fi
```

---

### Stage 2: Preflight Status Update

Update task status to "planning" BEFORE invoking subagent.

**Update state.json**:
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg status "planning" \
   --arg sid "$session_id" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    status: $status,
    last_updated: $ts,
    session_id: $sid
  }' specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
```

**Update TODO.md**: Use Edit tool to change status marker from `[RESEARCHED]` or `[NOT STARTED]` to `[PLANNING]`.

---

### Stage 3: Create Postflight Marker

Create the marker file to prevent premature termination:

```bash
# Ensure task directory exists
padded_num=$(printf "%03d" "$task_number")
mkdir -p "specs/${padded_num}_${project_name}"

cat > "specs/${padded_num}_${project_name}/.postflight-pending" << EOF
{
  "session_id": "${session_id}",
  "skill": "skill-planner",
  "task_number": ${task_number},
  "operation": "plan",
  "reason": "Postflight pending: status update, artifact linking, git commit",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "stop_hook_active": false
}
EOF
```

---

### Stage 4: Prepare Delegation Context

Prepare delegation context for the subagent:

```json
{
  "session_id": "sess_{timestamp}_{random}",
  "delegation_depth": 1,
  "delegation_path": ["orchestrator", "plan", "skill-planner"],
  "timeout": 1800,
  "task_context": {
    "task_number": N,
    "task_name": "{project_name}",
    "description": "{description}",
    "language": "{language}"
  },
  "research_path": "{path to research report if exists}",
  "metadata_file_path": "specs/{NNN}_{SLUG}/.return-meta.json"
}
```

---

### Stage 5: Invoke Subagent

**CRITICAL**: You MUST use the **Task** tool to spawn the subagent.

**Required Tool Invocation**:
```
Tool: Task (NOT Skill)
Parameters:
  - subagent_type: "planner-agent"
  - prompt: [Include task_context, delegation_context, research_path, metadata_file_path]
  - description: "Execute planning for task {N}"
```

**DO NOT** use `Skill(planner-agent)` - this will FAIL.

The subagent will:
- Load planning context files
- Analyze task requirements and research
- Decompose into logical phases
- Identify risks and mitigations
- Create plan in `specs/{NNN}_{SLUG}/plans/`
- Write metadata to `specs/{NNN}_{SLUG}/.return-meta.json`
- Return a brief text summary (NOT JSON)

---

### Stage 6: Parse Subagent Return (Read Metadata File)

After subagent returns, read the metadata file:

```bash
metadata_file="specs/${padded_num}_${project_name}/.return-meta.json"

if [ -f "$metadata_file" ] && jq empty "$metadata_file" 2>/dev/null; then
    status=$(jq -r '.status' "$metadata_file")
    artifact_path=$(jq -r '.artifacts[0].path // ""' "$metadata_file")
    artifact_type=$(jq -r '.artifacts[0].type // ""' "$metadata_file")
    artifact_summary=$(jq -r '.artifacts[0].summary // ""' "$metadata_file")
else
    echo "Error: Invalid or missing metadata file"
    status="failed"
fi
```

---

### Stage 7: Update Task Status (Postflight)

If status is "planned", update state.json and TODO.md:

**Update state.json**:
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg status "planned" \
  '(.active_projects[] | select(.project_number == '$task_number')) |= . + {
    status: $status,
    last_updated: $ts,
    planned: $ts
  }' specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
```

**Update TODO.md**: Use Edit tool to change status marker from `[PLANNING]` to `[PLANNED]`.

**On partial/failed**: Keep status as "planning" for resume.

---

### Stage 8: Link Artifacts

Add artifact to state.json with summary.

**IMPORTANT**: Use two-step jq pattern to avoid Issue #1132 escaping bug. See `jq-escaping-workarounds.md`.

```bash
if [ -n "$artifact_path" ]; then
    # Step 1: Filter out existing plan artifacts (use "| not" pattern to avoid != escaping - Issue #1132)
    jq '(.active_projects[] | select(.project_number == '$task_number')).artifacts =
        [(.active_projects[] | select(.project_number == '$task_number')).artifacts // [] | .[] | select(.type == "plan" | not)]' \
      specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json

    # Step 2: Add new plan artifact
    jq --arg path "$artifact_path" \
       --arg type "$artifact_type" \
       --arg summary "$artifact_summary" \
      '(.active_projects[] | select(.project_number == '$task_number')).artifacts += [{"path": $path, "type": $type, "summary": $summary}]' \
      specs/state.json > /tmp/state.json && mv /tmp/state.json specs/state.json
fi
```

**Update TODO.md**: Add plan artifact link:
```markdown
- **Plan**: [implementation-{NNN}.md]({artifact_path})
```

---

### Stage 9: Git Commit

Commit changes with session ID:

```bash
git add -A
git commit -m "task ${task_number}: create implementation plan

Session: ${session_id}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

### Stage 10: Cleanup

Remove marker and metadata files:

```bash
rm -f "specs/${padded_num}_${project_name}/.postflight-pending"
rm -f "specs/${padded_num}_${project_name}/.postflight-loop-guard"
rm -f "specs/${padded_num}_${project_name}/.return-meta.json"
```

---

### Stage 11: Return Brief Summary

Return a brief text summary (NOT JSON). Example:

```
Plan created for task {N}:
- {phase_count} phases defined, {estimated_hours} hours estimated
- Key phases: {phase names}
- Created plan at specs/{NNN}_{SLUG}/plans/implementation-{NNN}.md
- Status updated to [PLANNED]
- Changes committed
```

---

## Error Handling

### Input Validation Errors
Return immediately with error message if task not found or status invalid.

### Metadata File Missing
If subagent didn't write metadata file:
1. Keep status as "planning"
2. Do not cleanup postflight marker
3. Report error to user

### Git Commit Failure
Non-blocking: Log failure but continue with success response.

### jq Parse Failure
If jq commands fail with INVALID_CHARACTER or syntax error (Issue #1132):
1. Log to errors.json:
```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg sid "$session_id" \
   --arg msg "jq parse error in postflight artifact linking" \
   --argjson task "$task_number" \
  '.errors += [{
    "id": ("err_" + ($ts | gsub("[^0-9]"; ""))),
    "timestamp": $ts,
    "type": "jq_parse_failure",
    "severity": "medium",
    "message": $msg,
    "context": {"session_id": $sid, "command": "/plan", "task": $task, "checkpoint": "GATE_OUT"},
    "recovery": {"suggested_action": "Use two-step jq pattern from jq-escaping-workarounds.md", "auto_recoverable": true},
    "fix_status": "unfixed"
  }]' specs/errors.json > /tmp/errors.json && mv /tmp/errors.json specs/errors.json
```
2. Retry with two-step pattern (already implemented in Stage 8)

### Subagent Timeout
Return partial status if subagent times out (default 1800s).
Keep status as "planning" for resume.

---

## Return Format

This skill returns a **brief text summary** (NOT JSON). The JSON metadata is written to the file and processed internally.

Example successful return:
```
Plan created for task 414:
- 5 phases defined, 2.5 hours estimated
- Covers: agent structure, execution flow, error handling, examples, verification
- Created plan at specs/414_create_planner_agent/plans/implementation-001.md
- Status updated to [PLANNED]
- Changes committed with session sess_1736700000_abc123
```

Example partial return:
```
Plan partially created for task 414:
- 3 of 5 phases defined before timeout
- Partial plan saved at specs/414_create_planner_agent/plans/implementation-001.md
- Status remains [PLANNING] - run /plan 414 to complete
```
