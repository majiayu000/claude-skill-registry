---
name: codemap
description: Use when the user wants to map, visualize, or understand codebase structure. Generates hierarchical code maps using LSP analysis with create and update modes.
invocation: agent
---

# Code Map Creator

Generate or update a hierarchical code map using Claude Code's built-in LSP tools. Maps functions, classes, variables, and imports in a nested tree structure.

## Modes

### Create Mode (default)
```
/arc:specialized:codemap src/
/arc:specialized:codemap . --ignore "node_modules,dist"
```

### Update Mode
```
/arc:specialized:codemap --update .claude/maps/code-map-src-a3f9e.json --diff
/arc:specialized:codemap --update .claude/maps/code-map-src-a3f9e.json --pr 456
```

## Instructions

### Step 1: Parse Input and Detect Mode

Parse input to determine mode:

**Update Mode** (if `--update` present):
1. Extract codemap path after `--update`
2. Detect diff source (`--diff`, `--pr <id>`)
3. Get list of changed files via Bash

**Create Mode** (default):
1. Root directory (required, first argument, default `.`)
2. Ignore patterns (optional `--ignore`)

### Step 2: Launch Agent

**REQUIRED Task tool parameters:**

**Create Mode:**
```
subagent_type: "arc:codemap-creator"
run_in_background: true
prompt: "MODE: create\nRoot: <root_dir>\nIgnore: <patterns or none>"
```

**Update Mode:**
```
subagent_type: "arc:codemap-creator"
run_in_background: true
prompt: "MODE: update\nCodemap: <codemap_path>\nChanged files:\n- file1.ts\n- file2.ts"
```

Output a status message and **end your turn**.

### Step 3: Report Result

**Create Mode:**
```
## Code Map Created (LSP)

**Root**: <root_dir>
**Map**: .claude/maps/code-map-<name>-<hash5>.json

| Metric | Count |
|--------|-------|
| Directories | X |
| Files | X |
| Symbols | X |
```

**Update Mode:**
```
## Code Map Updated (LSP)

**Map**: <codemap_path>
**Files Updated**: X | **Added**: X | **Removed**: X
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Root directory not found | Report error, suggest valid paths |
| Codemap not found | Report error, suggest create mode |
| No changed files | Report "already up to date" |
