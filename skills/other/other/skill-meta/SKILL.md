---
name: skill-meta
description: Interactive system builder. Invoke for /meta command to create tasks for .claude/ system changes.
allowed-tools: Task, Bash, Edit, Read, Write
# Original context (now loaded by subagent):
#   - .claude/docs/guides/component-selection.md
#   - .claude/docs/guides/creating-commands.md
#   - .claude/docs/guides/creating-skills.md
#   - .claude/docs/guides/creating-agents.md
# Original tools (now used by subagent):
#   - Read, Write, Edit, Glob, Grep, Bash(git, jq, mkdir), AskUserQuestion
---

# Meta Skill

Thin wrapper that delegates system building to `meta-builder-agent` subagent. This skill handles all three modes of /meta: interactive interview, prompt analysis, and system analysis.

**IMPORTANT**: This skill implements the skill-internal postflight pattern. After the subagent returns,
this skill handles all postflight operations (git commit if tasks created) before returning.
This eliminates the "continue" prompt issue between skill return and orchestrator.

## Context References

Reference (do not load eagerly):
- Path: `.claude/context/core/formats/return-metadata-file.md` - Metadata file schema
- Path: `.claude/context/core/patterns/postflight-control.md` - Marker file protocol
- Path: `.claude/context/core/patterns/file-metadata-exchange.md` - File I/O helpers

Note: This skill is a thin wrapper with internal postflight. Context is loaded by the delegated agent.

## Trigger Conditions

This skill activates when:
- /meta command is invoked (with any arguments)
- User requests system building or task creation for .claude/ changes
- System analysis is requested (--analyze flag)

---

## Execution

### 1. Input Validation

Validate and classify mode from arguments:

**Mode Detection Logic**:
```bash
# Parse arguments
args="$ARGUMENTS"

# Determine mode
if [ -z "$args" ]; then
  mode="interactive"
elif [ "$args" = "--analyze" ]; then
  mode="analyze"
else
  mode="prompt"
  prompt="$args"
fi
```

No task_number validation needed - /meta creates new tasks rather than operating on existing ones.

### 2. Context Preparation

Prepare delegation context:

```json
{
  "session_id": "sess_{timestamp}_{random}",
  "delegation_depth": 1,
  "delegation_path": ["orchestrator", "meta", "skill-meta"],
  "timeout": 7200,
  "mode": "interactive|prompt|analyze",
  "prompt": "{user prompt if mode=prompt, null otherwise}"
}
```

### 3. Invoke Subagent

**CRITICAL**: You MUST use the **Task** tool to spawn the subagent.

The `agent` field in this skill's frontmatter specifies the target: `meta-builder-agent`

**Required Tool Invocation**:
```
Tool: Task (NOT Skill)
Parameters:
  - subagent_type: "meta-builder-agent"
  - prompt: [Include mode, prompt if provided, delegation_context]
  - description: "Execute meta building in {mode} mode"
```

**DO NOT** use `Skill(meta-builder-agent)` - this will FAIL.
Agents live in `.claude/agents/`, not `.claude/skills/`.
The Skill tool can only invoke skills from `.claude/skills/`.

The subagent will:
- Load component guides on-demand based on mode
- Execute mode-specific workflow:
  - **Interactive**: Run 7-stage interview with AskUserQuestion
  - **Prompt**: Analyze request and propose task breakdown
  - **Analyze**: Inventory existing components and provide recommendations
- Create task entries (TODO.md, state.json, task directories) for non-analyze modes
- Return standardized JSON result

### 4. Return Validation

Validate return matches `subagent-return.md` schema:
- Status is one of: completed, partial, failed, blocked
- Summary is non-empty and <100 tokens
- Artifacts array present (task directories for interactive/prompt modes)
- Metadata contains session_id, agent_type, delegation info

### 5. Return Propagation

Return validated result to caller without modification.

---

## Return Format

See `.claude/context/core/formats/subagent-return.md` for full specification.

### Expected Return: Interactive Mode (tasks created)

```json
{
  "status": "tasks_created",
  "summary": "Created 3 tasks for command creation workflow: research, implementation, and testing phases.",
  "artifacts": [
    {
      "type": "task",
      "path": "specs/430_create_export_command/",
      "summary": "Task directory for new command"
    },
    {
      "type": "task",
      "path": "specs/431_export_command_tests/",
      "summary": "Task directory for tests"
    }
  ],
  "metadata": {
    "session_id": "sess_1736700000_abc123",
    "agent_type": "meta-builder-agent",
    "delegation_depth": 1,
    "delegation_path": ["orchestrator", "meta", "meta-builder-agent"],
    "mode": "interactive",
    "tasks_created": 2
  },
  "next_steps": "Run /research 430 to begin research on first task"
}
```

### Expected Return: Analyze Mode (read-only)

```json
{
  "status": "analyzed",
  "summary": "System analysis complete. Found 9 commands, 9 skills, 6 agents, and 15 active tasks.",
  "artifacts": [],
  "metadata": {
    "session_id": "sess_1736700000_xyz789",
    "agent_type": "meta-builder-agent",
    "delegation_depth": 1,
    "delegation_path": ["orchestrator", "meta", "meta-builder-agent"],
    "mode": "analyze",
    "component_counts": {
      "commands": 9,
      "skills": 9,
      "agents": 6,
      "active_tasks": 15
    }
  },
  "next_steps": "Review analysis and run /meta to create tasks if needed"
}
```

### Expected Return: User Cancelled

```json
{
  "status": "cancelled",
  "summary": "User cancelled task creation at confirmation stage. No tasks created.",
  "artifacts": [],
  "metadata": {
    "session_id": "sess_1736700000_def456",
    "agent_type": "meta-builder-agent",
    "delegation_depth": 1,
    "delegation_path": ["orchestrator", "meta", "meta-builder-agent"],
    "mode": "interactive",
    "cancelled": true
  },
  "next_steps": "Run /meta again when ready to create tasks"
}
```

---

## Error Handling

### Input Validation Errors
Return immediately with failed status if arguments are malformed.

### Subagent Errors
Pass through the subagent's error return verbatim.

### User Cancellation
Return completed status (not failed) when user explicitly cancels at confirmation stage.

### Timeout
Return partial status if subagent times out (default 7200s for interactive sessions).
