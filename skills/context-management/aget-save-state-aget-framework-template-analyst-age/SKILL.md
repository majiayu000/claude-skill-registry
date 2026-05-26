---
name: aget-save-state
description: Save workflow state for resume/recovery. Use at natural breakpoints before context-intensive operations, major refactors, or session interruptions.
---

## Save State Protocol

You are saving workflow state for session continuity.

**Renamed**: `/aget-checkpoint` → `/aget-save-state` per S-V-O naming convention (L584) and Microsoft Agent Framework "State" grounding.

### Input

$ARGUMENTS

### Mode Detection

| Input Pattern | Mode | Behavior |
|---------------|------|----------|
| Empty or blank | **Auto-name** | Generate timestamp-based checkpoint name (YYYYMMDD-HHMMSS) |
| Text provided | **Named** | Use provided name (sanitized: lowercase, hyphens for spaces) |

### Checkpoint Capture

Create checkpoint file at `sessions/checkpoints/<name>.checkpoint.yaml`:

1. **Session Context**:
   - Current session file path (if exists in `sessions/`)
   - Summary of current work focus (1-2 sentences)

2. **Active Tasks**:
   - In-progress tasks with status
   - Pending questions or decisions

3. **Artifacts**:
   - Recently modified files (from git status or session context)
   - Whether uncommitted git changes exist

4. **Resume Prompt**:
   - Human-readable summary for context recovery
   - Recommended next action

### Output Format

Write this YAML structure to `sessions/checkpoints/<name>.checkpoint.yaml`:

```yaml
checkpoint:
  name: "<name>"
  created: "<ISO 8601 timestamp>"
  agent: "private-cli-aget"
  version: "3.4.0"

context:
  session_file: "<path or null>"
  current_focus: "<1-2 sentence summary of current work>"
  active_tasks:
    - subject: "<task description>"
      status: "in_progress|pending"
  pending_questions:
    - "<unanswered question or decision needed>"

artifacts:
  modified_files:
    - path: "<file path>"
      summary: "<brief description of changes>"
  uncommitted_changes: true|false

resume_prompt: |
  Continue from checkpoint "<name>".

  Context: <summary of where you left off>

  Next action: <recommended next step>
```

### After Checkpoint Creation

1. Report checkpoint file location
2. Confirm what was captured
3. Provide the resume prompt for future reference

### Constraints

These are INVIOLABLE - you MUST NOT violate these constraints:

1. **NEVER** modify files in `specs/`, `governance/`, or `.aget/`
2. **NEVER** modify `planning/RESEARCH_BACKLOG.md`
3. **NEVER** create checkpoints outside `sessions/checkpoints/`
4. **NEVER** include sensitive data (credentials, API keys) in checkpoints
5. **DO** create `sessions/checkpoints/` directory if it doesn't exist
6. **DO** use ISO 8601 timestamp format
7. **DO** sanitize checkpoint names (replace spaces with hyphens, lowercase)
8. **DO** overwrite existing checkpoint if same name is used

### Rationale

Per AGET theoretical grounding:
- **Stigmergy** (Grasse): Checkpoint artifacts enable cross-session coordination
- **Extended Mind** (Clark/Chalmers): Externalizing state prevents cognitive loss
- **Session Continuity**: Enables break-and-continue workflow patterns
- **Context Recovery**: Checkpoints provide structured resume context

This skill implements the "save state, resume later" pattern for AGET session management.

### Traceability

| Link | Reference |
|------|-----------|
| Vocabulary | Checkpoint_Protocol (CLI_VOCABULARY.md v1.30.0) |
| Requirements | R-SKILL-005-001 through R-SKILL-005-011 |
| Skill Spec | SKILL-005 |
| L-docs | L570, L574, L575 |
| RQ | RQ-054 |
| Project | PROJECT_PLAN_AGET_CHECKPOINT_SKILL.md |
