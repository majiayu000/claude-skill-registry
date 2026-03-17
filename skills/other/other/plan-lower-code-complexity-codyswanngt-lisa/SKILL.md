---
name: plan-lower-code-complexity
description: This skill should be used when reducing the cognitive complexity threshold of the codebase. It lowers the threshold by 2, identifies functions that exceed the new limit, generates a brief with refactoring strategies, and creates a plan with tasks to fix all violations.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Lower Code Complexity

Reduces the cognitive complexity threshold by 2 and fixes all violations.

## Step 1: Gather Requirements

1. **Read current threshold** from eslint config (cognitive-complexity rule)
2. **Calculate new threshold**: current - 2 (e.g., 15 -> 13)
3. **Run lint** with the new threshold to find violations:
   ```bash
   bun run lint 2>&1 | grep "cognitive-complexity"
   ```
4. **Note for each violation**:
   - File path and line number
   - Function name
   - Current complexity score

If no violations at new threshold, report success and exit.

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Reduce cognitive complexity threshold from [current] to [new].

Functions exceeding threshold (ordered by complexity):
1. [file:function] (complexity: X, target: [new]) - Line Y
2. ...

Configuration change: [eslint config path], cognitive-complexity from [current] to [new]

Refactoring strategies: extract functions, early returns, extract conditions, use lookup tables

Verification: `bun run lint 2>&1 | grep "cognitive-complexity" | wc -l` → Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.