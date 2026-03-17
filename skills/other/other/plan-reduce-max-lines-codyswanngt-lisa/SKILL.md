---
name: plan-reduce-max-lines
description: This skill should be used when reducing the maximum file lines threshold and fixing all violations. It updates the eslint threshold configuration, identifies files exceeding the new limit, generates a brief with refactoring strategies, and creates a plan with tasks to split oversized files.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Reduce Max Lines

Target threshold: $ARGUMENTS lines per file

If no argument provided, prompt the user for a target.

## Step 1: Gather Requirements

1. **Read current config** from eslint thresholds (eslint.thresholds.json or similar)
2. **Run lint** with the new threshold to find violations:
   ```bash
   bun run lint 2>&1 | grep "max-lines"
   ```
3. **Note for each violation**:
   - File path
   - Current line count

If no violations at $ARGUMENTS, report success and exit.

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Reduce max file lines threshold to $ARGUMENTS.

Files exceeding threshold (ordered by line count):
1. [file] - [current] lines (target: $ARGUMENTS)
2. ...

Configuration change: eslint.thresholds.json, maxLines to $ARGUMENTS

Refactoring strategies: extract modules, remove duplication, delete dead code, simplify logic

Verification: `bun run lint 2>&1 | grep "max-lines" | wc -l` → Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
