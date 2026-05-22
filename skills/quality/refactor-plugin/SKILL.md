---
description: Start a complete plugin refactoring workflow. Analyzes plugin structure, creates refactoring plan with tasks, and guides through execution.
argument-hint: <plugin-path>
user-invocable: true
---

# Plugin Refactoring Workflow

Start a comprehensive plugin refactoring workflow for the specified plugin.

## Arguments

- `$ARGUMENTS`: Path to the plugin directory to refactor (e.g., `./plugins/python3-development`)

## Workflow Overview

This command orchestrates the complete refactoring workflow:

1. **Assessment** - Analyze plugin structure and identify issues
2. **Design** - Create refactoring design specification
3. **Planning** - Generate task file with dependencies
4. **Execution** - Run tasks via specialized agents
5. **Validation** - Verify refactoring quality

## Instructions

### Step 1: Validate Input

If no plugin path provided:

```text
ERROR: No plugin path provided.
Usage: /plugin-creator:refactor <plugin-path>
Example: /plugin-creator:refactor ./plugins/python3-development
```

### Step 2: Verify Plugin Exists

Check that the path contains a valid plugin:

- `.claude-plugin/plugin.json` exists
- OR `skills/` directory exists

### Step 3: Run Assessment

Invoke the assessor skill to analyze the plugin:

```text
Skill(skill="plugin-creator:assessor", args="$ARGUMENTS")
```

This generates:

- Plugin Assessment Report
- Refactoring Design Map at `.claude/plan/refactor-design-{slug}.md`
- Task File at `.claude/plan/tasks-refactor-{slug}.md`

### Step 4: Review Plan

After assessment completes, display:

```text
================================================================================
                    REFACTORING PLAN READY FOR REVIEW
================================================================================

Plugin: $ARGUMENTS
Assessment Score: [X/100]

Plan Files Created:
- Design: .claude/plan/refactor-design-{slug}.md
- Tasks: .claude/plan/tasks-refactor-{slug}.md

Tasks Summary:
- Total tasks: [N]
- Skill splits: [N]
- Agent optimizations: [N]
- Documentation improvements: [N]

Next Steps:
1. Review the plan files
2. Run `/plugin-creator:implement-refactor {slug}` to execute
================================================================================
```

### Step 5: Await User Decision

Ask user:

- **Continue**: Proceed to implementation
- **Review**: Open plan files for review
- **Abort**: Cancel refactoring

## Related Commands

- `/plugin-creator:implement-refactor` - Execute tasks from plan
- `/plugin-creator:ensure-complete` - Validate completed refactoring
- `/plugin-creator:count-lines` - Quick line count check

## Example Usage

```bash
# Start refactoring a plugin
/plugin-creator:refactor ./plugins/python3-development

# Start refactoring current directory plugin
/plugin-creator:refactor .
```
