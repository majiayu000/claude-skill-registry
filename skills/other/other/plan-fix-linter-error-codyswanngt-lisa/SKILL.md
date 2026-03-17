---
name: plan-fix-linter-error
description: This skill should be used when fixing all violations of one or more RuboCop cops across the codebase. It runs RuboCop, groups violations by cop and file, generates a brief with fix strategies, and creates a plan with tasks to implement the fixes.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Fix Linter Errors

Target cops: $ARGUMENTS

If no arguments provided, prompt the user for at least one RuboCop cop name.

## Step 1: Gather Requirements

1. **Parse cops** from $ARGUMENTS (space-separated)
2. **Run RuboCop** to collect all violations:
   ```bash
   bundle exec rubocop --format json 2>&1
   ```
3. **Group violations** by cop, then by file, noting:
   - File path and line numbers
   - Violation count per file
   - Sample offense messages

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Fix RuboCop violations for cops: $ARGUMENTS

Violations by cop:
- [CopName1]: X total violations across Y files
  - [file]: N violations (lines: ...)
  - ...
- [CopName2]: X total violations across Y files
  - ...

Fix strategies: extract methods, reduce complexity, apply auto-correct where safe

Verification: `bundle exec rubocop --format simple 2>&1 | grep -E "($ARGUMENTS)" | wc -l` -> Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
