---
name: plan-fix-linter-error
description: This skill should be used when fixing all violations of one or more ESLint rules across the codebase. It runs the linter, groups violations by rule and file, generates a brief with fix strategies, and creates a plan with tasks to implement the fixes.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Fix Linter Errors

Target rules: $ARGUMENTS

If no arguments provided, prompt the user for at least one lint rule name.

## Step 1: Gather Requirements

1. **Parse rules** from $ARGUMENTS (space-separated)
2. **Run linter** to collect all violations:
   ```bash
   bun run lint 2>&1
   ```
3. **Group violations** by rule, then by file, noting:
   - File path and line numbers
   - Violation count per file
   - Sample error messages

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Fix ESLint violations for rules: $ARGUMENTS

Violations by rule:
- [rule-name-1]: X total violations across Y files
  - [file]: N violations (lines: ...)
  - ...
- [rule-name-2]: X total violations across Y files
  - ...

Fix strategies: extract functions, early returns, apply formatting, add types

Verification: `bun run lint 2>&1 | grep -E "($ARGUMENTS)" | wc -l` → Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
