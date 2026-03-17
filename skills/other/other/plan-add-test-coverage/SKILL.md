---
name: plan-add-test-coverage
description: This skill should be used when increasing test coverage to a specified threshold percentage. It runs the coverage report, identifies files with the lowest coverage, generates a brief with coverage gaps, and creates a plan with tasks to add the missing tests.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Increase Test Coverage

Target threshold: $ARGUMENTS%

If no argument provided, prompt the user for a target.

## Step 1: Gather Requirements

1. **Find coverage config** (jest.config.js, vitest.config.ts, .nycrc, etc.)
2. **Run coverage report** to get current state:
   ```bash
   bun run test:cov 2>&1 | head -100
   ```
3. **Identify the 20 files with lowest coverage**, noting:
   - File path
   - Current coverage % (lines, branches, functions)
   - Which lines/branches are uncovered

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Increase test coverage from [current]% to $ARGUMENTS%.

Files needing coverage (ordered by coverage gap):
1. [file] - [current]% coverage (target: $ARGUMENTS%)
   - Uncovered: [lines]
   - Missing branch coverage: [lines]
2. ...

Configuration: [config file path], update thresholds to $ARGUMENTS%

Verification: `bun run test:cov` → Expected: All thresholds pass at $ARGUMENTS%
```

Invoke `/plan-execute` with this brief to create the implementation plan.
