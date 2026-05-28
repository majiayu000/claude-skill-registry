---
description: Validate skill directories against AgentSkills spec
allowed-tools: Bash, mcp__agent-skills-spec__*
---

# Validate Skills

Validate skill directories against the AgentSkills specification.

**Paths to validate:** $ARGUMENTS (default: `.claude/skills/`)

## Instructions

### Step 1: Run Validation

Execute the development-skills CLI command:
```bash
bunx @plaited/development-skills validate-skill $ARGUMENTS
```

If no arguments provided, defaults to `.claude/skills/`.

### Step 2: Report Results

Show the CLI output to the user. If there are errors, use the `agent-skills-spec` MCP server to get the latest specification and explain how to fix them.

### Step 3: Query Spec (if needed)

For clarification on validation rules, query the `agent-skills-spec` MCP server for the current specification.
