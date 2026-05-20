---
name: plan-reduce-max-lines-per-function
description: This skill should be used when reducing the maximum lines per method threshold and fixing all violations. It updates the RuboCop configuration, identifies methods exceeding the new limit, generates a brief with refactoring strategies, and creates a plan with tasks to split oversized methods.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Reduce Max Lines Per Method

Target threshold: $ARGUMENTS lines per method

If no argument provided, prompt the user for a target.

## Step 1: Gather Requirements

1. **Read current config** from `.rubocop.yml` or `.rubocop.local.yml` (`Metrics/MethodLength`)
2. **Run RuboCop** with the target threshold to find violations:
   ```bash
   bundle exec rubocop --only Metrics/MethodLength --format json 2>&1
   ```
3. **Note for each violation**:
   - File path and line number
   - Method name
   - Current line count

If no violations at $ARGUMENTS, report success and exit.

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Reduce max lines per method threshold to $ARGUMENTS.

Methods exceeding threshold (ordered by line count):
1. [file:method_name] (lines: X, target: $ARGUMENTS) - Line Y
2. ...

Configuration change: .rubocop.local.yml, Metrics/MethodLength Max to $ARGUMENTS

Refactoring strategies: extract methods, early returns, extract conditions, use lookup hashes, consolidate logic

Verification: `bundle exec rubocop --only Metrics/MethodLength --format simple 2>&1 | grep "offense" | wc -l` -> Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
