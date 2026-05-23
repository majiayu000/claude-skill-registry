---
name: plan-reduce-max-lines-per-function
description: This skill should be used when reducing the maximum lines per function threshold and fixing all violations. It updates the eslint threshold configuration, identifies functions exceeding the new limit, generates a brief with refactoring strategies, and creates a plan with tasks to split oversized functions.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Reduce Max Lines Per Function

Target threshold: $ARGUMENTS lines per function

If no argument provided, prompt the user for a target.

## Step 1: Gather Requirements

1. **Read current config** from eslint thresholds (eslint.thresholds.json or similar)
2. **Run lint** with the new threshold to find violations:
   ```bash
   bun run lint 2>&1 | grep "max-lines-per-function"
   ```
3. **Note for each violation**:
   - File path and line number
   - Function name
   - Current line count

If no violations at $ARGUMENTS, report success and exit.

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Reduce max lines per function threshold to $ARGUMENTS.

Functions exceeding threshold (ordered by line count):
1. [file:function] (lines: X, target: $ARGUMENTS) - Line Y
2. ...

Configuration change: eslint.thresholds.json, maxLinesPerFunction to $ARGUMENTS

Refactoring strategies: extract functions, early returns, extract conditions, use lookup tables, consolidate logic

Verification: `bun run lint 2>&1 | grep "max-lines-per-function" | wc -l` → Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
