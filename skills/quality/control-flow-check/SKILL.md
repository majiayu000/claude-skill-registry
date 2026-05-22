---
name: control-flow-check
description: Audits Go code for control flow excellence - early returns, minimal nesting, small blocks. Checks for happy path readability, guard clauses, and refactoring opportunities. Use before committing Go code or during refactoring.
version: 1.0.0
---

# Go Control Flow Check Skill

## Purpose

Audit Go code for control flow best practices based on RMS Go coding standards. This skill identifies control flow anti-patterns and suggests refactoring opportunities to improve readability and maintainability.

## What This Skill Checks

### 1. Early Return Pattern (Priority: HIGH)

**Golden Rule**: Use early returns for error cases and edge conditions to keep the happy path at the lowest indentation level.

**Good Pattern**:

```go
func ProcessTask(task *Task) error {
    if task == nil {
        return errors.New("task is nil")
    }
    if !task.IsValid() {
        return errors.New("invalid task")
    }

    // Happy path at lowest indentation
    result := task.Execute()
    return result.Save()
}
```

**Bad Pattern**:

```go
func ProcessTask(task *Task) error {
    if task != nil {
        if task.IsValid() {
            // Happy path nested 2 levels
            result := task.Execute()
            return result.Save()
        } else {
            return errors.New("invalid task")
        }
    } else {
        return errors.New("task is nil")
    }
}
```

### 2. Nesting Depth (Priority: HIGH)

**Golden Rule**: Maximum 2-3 levels of nesting. Deeper nesting indicates need for refactoring.

**Detection Pattern**:

- Count opening braces `{` in nested structures
- Flag any function with nesting > 3 levels
- Suggest extraction of nested logic into helper functions

### 3. Block Size (Priority: MEDIUM)

**Golden Rule**: If/else blocks should be < 10 lines. Large blocks need extraction.

**Detection Pattern**:

- Measure lines between `if {` and closing `}`
- Measure lines between `else {` and closing `}`
- Flag blocks > 10 lines for extraction

### 4. Guard Clauses (Priority: MEDIUM)

**Golden Rule**: Validate inputs and preconditions at function start with early returns.

**Good Pattern**:

```go
func UpdateTask(ctx rms.Ctx, taskID string, updates map[string]interface{}) error {
    // Guard clauses at top
    if taskID == "" {
        return errors.New("taskID required")
    }
    if len(updates) == 0 {
        return errors.New("no updates provided")
    }

    // Main logic after guards
    task, err := fetchTask(ctx, taskID)
    // ...
}
```

### 5. Else Statements (Priority: LOW)

**Guidance**: Prefer early returns over else statements when possible.

**Refactoring Pattern**:

```go
// Before
func IsValid(x int) bool {
    if x > 0 {
        return true
    } else {
        return false
    }
}

// After
func IsValid(x int) bool {
    if x > 0 {
        return true
    }
    return false
}
```

## Step-by-Step Execution

### Step 1: Identify Go Files to Check

```bash
# Find all Go files in the repository
find . -name "*.go" -not -path "*/vendor/*" -not -path "*/mock*" -not -path "*_test.go"
```

### Step 2: Read Target Go Files

Use the Read tool to examine Go files, focusing on:

- Function definitions
- Control flow structures (if/else, switch, for, select)
- Error handling patterns

### Step 3: Analyze Each Function

For each function, check:

**A. Early Return Pattern**

1. Identify error cases and edge conditions
2. Verify they appear at function start with early returns
3. Verify happy path is at lowest indentation
4. Flag violations with line numbers

**B. Nesting Depth**

1. Track indentation level as you scan through function
2. Count maximum nesting depth
3. Flag any depth > 3 levels
4. Identify the nested section causing the issue

**C. Block Size**

1. For each if/else block, count lines between braces
2. Flag blocks > 10 lines
3. Note what the block is doing (for extraction suggestion)

**D. Guard Clauses**

1. Check if input validation is at function start
2. Verify validations use early returns
3. Flag missing guard clauses for required inputs

**E. Unnecessary Else**

1. Find if-return followed by else-return patterns
2. Suggest removing else and de-indenting
3. Find if-return followed by else-continue logic patterns

### Step 4: Generate Report

Create a structured report:

```markdown
## Control Flow Audit: [file_path]

### ✅ Functions Following Best Practices

- `FunctionName` ([file:line]) - Early returns, minimal nesting

### ⚠️ Issues Found

#### HIGH Priority: Excessive Nesting

- **Function**: `ComplexFunction` ([file:line])
  - **Issue**: Nesting depth of 4 levels at line X
  - **Location**: Lines X-Y
  - **Suggestion**: Extract nested logic into `helperFunction`

#### HIGH Priority: Missing Early Returns

- **Function**: `ProcessData` ([file:line])
  - **Issue**: Happy path nested 2 levels, error checks not using early returns
  - **Location**: Lines X-Y
  - **Suggestion**: Add guard clauses at function start

#### MEDIUM Priority: Large Block

- **Function**: `HandleRequest` ([file:line])
  - **Issue**: If block spans 15 lines (lines X-Y)
  - **Suggestion**: Extract to `validateAndProcess` helper

#### LOW Priority: Unnecessary Else

- **Function**: `IsAuthorized` ([file:line])
  - **Issue**: Else after return at line X
  - **Suggestion**: Remove else, de-indent remaining code
```

### Step 5: Suggest Refactoring

For each issue found, provide:

1. **Current code snippet** (showing the problem)
2. **Refactored code snippet** (showing the solution)
3. **Explanation** (why the refactoring improves readability)

### Step 6: Summary Statistics

```markdown
## Summary

- Files checked: X
- Functions analyzed: Y
- Issues found: Z
  - HIGH priority: A
  - MEDIUM priority: B
  - LOW priority: C
- Clean functions: W
```

## Integration Points

This skill is invoked by:

- **`quality-check`** skill for Go projects
- **`safe-commit`** skill (via quality-check)
- Directly when refactoring Go code

## Exit Criteria

- All Go functions analyzed
- Report generated with line-specific issues
- Refactoring suggestions provided for all issues
- Summary statistics calculated

## Example Usage

```bash
# Manual invocation
/skill control-flow-check

# Automatic invocation via quality-check
/skill quality-check  # Detects Go project, invokes control-flow-check
```

## References

- RMS Go Coding Standards: Control Flow Excellence
- Go Code Reviewer Agent: Golden Rules
- Early Return Pattern: https://medium.com/@matryer/line-of-sight-in-code-186dd7cdea88
