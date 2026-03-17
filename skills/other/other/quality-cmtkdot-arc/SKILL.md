---
name: quality
description: Use when the user asks to analyze code quality, identify anti-patterns, refactor for maintainability, or improve existing code. Uses LSP-powered semantic analysis.
invocation: agent
---

# Code Quality Analysis (LSP-Powered)

Analyze code quality using Claude Code's built-in LSP for semantic understanding. Generates architectural improvement plans.

**Use the right skill:**
- **Code quality** → `quality` (this skill)
- **New features** → plan via `/arc:core:plan`
- **Bug fixes** → `bug`

## Arguments

File paths to analyze (one agent per file):
- Single file: `src/services/auth_service`
- Multiple files: `src/agent src/hitl src/app`

## Instructions

### Step 1: Parse Input

Parse input to extract file list. Validate each path exists.

### Step 2: Launch Agents

For EACH file, launch a background agent:

**REQUIRED Task tool parameters:**
```
subagent_type: "arc:quality-plan-creator"
run_in_background: true
prompt: "Analyze code quality: <file-path>"
```

**Launch ALL agents in a single message for parallel execution.** Output a status message like "Analyzing N files..." and **end your turn**. The system wakes you when agents finish.

### Step 3: Report Results

```
## Code Quality Analysis Complete (LSP-Powered)

| File | Current | Projected | Issues | Changes Required |
|------|---------|-----------|--------|------------------|
| [path] | 6.8/10 | 9.2/10 | [N] | Yes |

Plans: openspec/plans/YY-MM-DD-quality-*.md

Next Steps:
1. Review plan files
2. Execute: `/arc:core:execute --source plan --plan-path <plan-path>`
```

## Error Handling

| Scenario | Action |
|----------|--------|
| File not found | Report error, continue with others |
| LSP unavailable | Fall back to static analysis |
| No issues found | Report clean bill of health |
