---
name: sort-tasks
description: Sort tasks topologically by dependencies. Use after creating/modifying tasks or when you need to see execution order.
allowed-tools: Bash, Read
---

# Topological Task Sorter

Sort task files by their dependencies to determine optimal execution order. Detects circular dependencies and validates dependency references.

## Usage

```
/sort-tasks                              # Sort tasks in current phase
/sort-tasks <path>                       # Sort tasks in specific path
/sort-tasks --json                       # JSON output (for programmatic use)
/sort-tasks --markdown                   # Markdown table (for documentation)
```

## Arguments

- `$1` - Path to phase folder (default: `specification`)
- `--json` - Output as JSON
- `--markdown` - Output as Markdown table

## Process

### Step 1: Run the Sort Script

Execute the topological sort script:

```bash
node .claude/scripts/sort-tasks.mjs "<path>" [--json|--markdown]
```

### Step 2: Present Results

**For human-readable output** (default):
- Show numbered list of tasks in execution order
- Highlight entry points (tasks with no dependencies)
- Report any circular dependencies as errors
- Show warnings for missing dependency references

**For markdown output** (`--markdown`):
- Generate a table suitable for inclusion in documentation
- Include Order, Task ID, Name, and Dependencies columns

**For JSON output** (`--json`):
- Return structured data for programmatic use

## Output Format

### Human-Readable (Default)

```
✅ Topological order (N tasks):

1. task-01 - Solution Setup
2. task-02 - Shared Kernel (depends on: task-01)
3. task-03 - Contracts (depends on: task-01)
4. task-04 - Common (depends on: task-02)

⚡ Entry points (no dependencies): task-01

❌ Circular dependencies detected: task-05, task-06  (if any)
⚠️ Warnings:
   - Task "task-07" references unknown dependency "task-99"
```

### Markdown Table

```markdown
## Execution Order (Topological Sort)

| Order | Task ID | Name | Dependencies |
|-------|---------|------|--------------|
| 1 | task-01 | Solution Setup | - |
| 2 | task-02 | Shared Kernel | task-01 |
...
```

## Error Handling

- **No tasks found**: Report that no task files were found in the specified path
- **Circular dependencies**: List all tasks involved in cycles, exit with error
- **Missing dependencies**: Warn about referenced but non-existent task IDs

## Integration with dotnet-tech-lead

This skill is automatically called by the `dotnet-tech-lead` agent after:
1. Creating new task files
2. Modifying task dependencies
3. User requests re-sorting

The markdown output is included in the task summary presented to the user.

## Safety Rules

1. This is a **read-only operation** - no files are modified
2. Only reads task metadata from markdown files
3. Safe to run at any time without side effects
