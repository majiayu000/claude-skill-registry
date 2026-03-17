---
name: plan-add-test-coverage
description: This skill should be used when increasing test coverage to a specified threshold percentage. It runs the test suite with SimpleCov, identifies files with the lowest coverage, generates a brief with coverage gaps, and creates a plan with tasks to add the missing tests.
allowed-tools: ["Read", "Bash", "Glob", "Grep"]

---

# Increase Test Coverage

Target threshold: $ARGUMENTS%

If no argument provided, prompt the user for a target.

## Step 1: Gather Requirements

1. **Find coverage config** (`.simplecov` or `spec/spec_helper.rb`)
2. **Run test suite with coverage** to get current state:
   ```bash
   bundle exec rspec 2>&1 | tail -50
   ```
3. **Check SimpleCov output** in `coverage/index.html` or console output
4. **Identify the 20 files with lowest coverage**, noting:
   - File path
   - Current coverage % (lines, branches)
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

Configuration: .simplecov, update minimum_coverage to $ARGUMENTS%

Verification: `bundle exec rspec` -> Expected: SimpleCov reports >= $ARGUMENTS% coverage
```

Invoke `/plan-execute` with this brief to create the implementation plan.
