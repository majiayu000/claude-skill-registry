---
name: plan-reduce-max-lines
description: This skill should be used when reducing the maximum class/module lines threshold and fixing all violations. It updates the RuboCop configuration, identifies classes and modules exceeding the new limit, generates a brief with refactoring strategies, and creates a plan with tasks to split oversized files.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Reduce Max Lines

Target threshold: $ARGUMENTS lines per class/module

If no argument provided, prompt the user for a target.

## Step 1: Gather Requirements

1. **Read current config** from `.rubocop.yml` or `.rubocop.local.yml` (`Metrics/ClassLength` and `Metrics/ModuleLength`)
2. **Run RuboCop** with the target threshold to find violations:
   ```bash
   bundle exec rubocop --only Metrics/ClassLength,Metrics/ModuleLength --format json 2>&1
   ```
3. **Note for each violation**:
   - File path
   - Class/module name
   - Current line count

If no violations at $ARGUMENTS, report success and exit.

## Step 2: Compile Brief and Delegate

Compile the gathered information into a structured brief:

```
Reduce max class/module lines threshold to $ARGUMENTS.

Classes/modules exceeding threshold (ordered by line count):
1. [file:ClassName] - [current] lines (target: $ARGUMENTS)
2. ...

Configuration change: .rubocop.local.yml, Metrics/ClassLength Max to $ARGUMENTS, Metrics/ModuleLength Max to $ARGUMENTS

Refactoring strategies: extract concerns, extract service objects, remove duplication, delete dead code, simplify logic

Verification: `bundle exec rubocop --only Metrics/ClassLength,Metrics/ModuleLength --format simple 2>&1 | grep "offense" | wc -l` -> Expected: 0
```

Invoke `/plan-execute` with this brief to create the implementation plan.
