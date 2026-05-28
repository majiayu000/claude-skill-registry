---
name: plan-lower-code-complexity
description: This skill should be used when reducing the code complexity threshold of the codebase. It lowers the CyclomaticComplexity threshold by 2, identifies methods that exceed the new limit, generates a brief with refactoring strategies, and creates a plan with tasks to fix all violations.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]
---

# Lower Code Complexity

Reduces the CyclomaticComplexity threshold by 2 and fixes all violations.

## Step 1: Gather Requirements

1. **Read current threshold** from `.rubocop.yml` (`Metrics/CyclomaticComplexity` Max)
2. **Calculate new threshold**: current - 2 (e.g., 10 -> 8)
3. **Run RuboCop and flog** to find violations:
   ```bash
   bundle exec rubocop --only Metrics/CyclomaticComplexity,Metrics/PerceivedComplexity --format json 2>&1
   ```
   ```bash
   bundle exec flog --all --group app/ 2>&1 | head -50
   ```
4. **Note for each violation**:
   - File path and line number
   - Method name
   - Current complexity score (RuboCop and/or flog)

If no violations at new threshold, report success and exit.

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Reduce CyclomaticComplexity threshold from [current] to [new].

Methods exceeding threshold (ordered by complexity):
1. [file:method_name] (complexity: X, target: [new]) - Line Y
   - flog score: Z
2. ...

Configuration change: .rubocop.local.yml, Metrics/CyclomaticComplexity Max from [current] to [new]

Refactoring strategies: extract methods, early returns, extract conditions, use lookup hashes, replace conditionals with polymorphism

Verification: `bundle exec rubocop --only Metrics/CyclomaticComplexity --format simple 2>&1 | grep "offense" | wc -l` -> Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
