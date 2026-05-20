---
name: docs
description: Use when the user asks to generate or update architectural documentation, dev guides, or DEVGUIDE files for a codebase or directory.
invocation: agent
---

# Document Creator

Generate hierarchical architectural documentation (DEVGUIDE.md) using Claude Code's built-in LSP tools. Supports multiple directories with parallel agent execution.

## Arguments

Directory paths to document (one agent per directory):
- Single: `src/services/`
- Multiple: `src/services src/components src/lib`
- None: analyzes current directory (`.`)

## Instructions

### Step 1: Parse Input

Parse input to extract directory list:
- Split arguments by spaces
- If empty → use current directory (`.`)
- Validate each path exists as a directory

### Step 2: Check for Rules

Check if `.claude/rules` directory exists at project root:
- If rules exist → read each rules file, pass relevant info to agents
- If no rules exist → note for agents to create rules files

### Step 3: Determine Output Paths

For each directory:
- If no DEVGUIDE.md exists → `<target-dir>/DEVGUIDE.md`
- If exists → `<target-dir>/DEVGUIDE_2.md` (increment until unused)

### Step 4: Launch Agents

For EACH directory, launch a background agent:

**REQUIRED Task tool parameters:**
```
subagent_type: "arc:document-creator"
run_in_background: true
prompt: "Generate DEVGUIDE: <dir>\nOutput: <path>\nRules: <status>"
```

**Launch ALL agents in a single message for parallel execution.** Output a status message and **end your turn**.

### Step 5: Report Results

```
## DEVGUIDE Documentation Created (LSP)

| Directory | Output | Status |
|-----------|--------|--------|
| [dir1] | [output path] | CREATED |

Rules Status: [Found N rules / Created new rules]

Next Steps:
1. Review generated documentation
2. Commit the DEVGUIDE files
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Path not found | Report error, continue with others |
| Path is file | Report error, continue with others |
| Empty directory | Generate minimal guide |
