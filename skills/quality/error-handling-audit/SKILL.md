---
name: error-handling-audit
description: Audits Go code for error handling best practices - proper wrapping with %w, preserved context, meaningful messages, no error swallowing. Use before committing Go code or during error handling reviews.
version: 1.0.0
---

# Go Error Handling Audit Skill

## Purpose

Audit Go code for error handling best practices based on RMS Go coding standards. This skill ensures errors are properly wrapped, context is preserved, and error handling follows idiomatic Go patterns.

## What This Skill Checks

### 1. Error Wrapping with %w (Priority: CRITICAL)

**Golden Rule**: Always wrap errors with `fmt.Errorf(..., %w, err)` to preserve error chain for errors.Is() and errors.As().

**Good Pattern**:

```go
func FetchTask(ctx rms.Ctx, id string) (*Task, error) {
    task, err := db.GetTask(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("failed to fetch task %s: %w", id, err)
    }
    return task, nil
}
```

**Bad Patterns**:

```go
// ❌ Using %v (destroys error chain)
return nil, fmt.Errorf("failed to fetch task: %v", err)

// ❌ No wrapping at all
return nil, err

// ❌ String concatenation
return nil, errors.New("failed to fetch task: " + err.Error())
```

**CRITICAL EXCEPTIONS**:

- Use `%v` at API boundaries where error chain should not leak
- Use `%v` for logging where you want formatted output
- Use unwrapped return only when error message is clear from context

### 2. Error Context (Priority: HIGH)

**Golden Rule**: Error messages must provide enough context to debug issues without source code access.

**Good Context**:

```go
// Include relevant IDs, values, operation
return fmt.Errorf("failed to update task %s for partner %s: %w", taskID, partnerID, err)

// Include what was expected vs actual
return fmt.Errorf("expected task state 'active', got '%s': %w", task.State, err)
```

**Bad Context**:

```go
// ❌ Too vague
return fmt.Errorf("operation failed: %w", err)

// ❌ No context
return fmt.Errorf("error: %w", err)

// ❌ Missing critical IDs
return fmt.Errorf("failed to update task: %w", err)
```

### 3. Error Message Format (Priority: MEDIUM)

**Golden Rule**: Follow consistent error message formatting for operational clarity.

**Format Standards**:

- Lowercase start (unless proper noun)
- No trailing punctuation
- Present tense
- Include action + resource + identifiers

**Good Messages**:

```go
"failed to fetch task %s"
"invalid partner ID: must be non-empty"
"task %s not found in workflow %s"
"cannot transition task from %s to %s"
```

**Bad Messages**:

```go
"Failed to fetch task"          // ❌ Capitalized
"task not found."               // ❌ Trailing period
"couldn't get the task"         // ❌ Informal contraction
"Error fetching task!"          // ❌ Exclamation, capitalized
```

### 4. Error Swallowing (Priority: CRITICAL)

**Golden Rule**: Never silently ignore errors. Log or return every error.

**Acceptable Patterns**:

```go
// Return error
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}

// Log and continue (with justification)
if err := cache.Set(key, value); err != nil {
    // Non-critical: cache miss acceptable
    logger.Warn("cache set failed", "error", err)
}

// Explicitly ignore with comment
_ = file.Close() // Error already handled in deferred cleanup
```

**Unacceptable Patterns**:

```go
// ❌ Silent ignore
err := doSomething()

// ❌ Blank identifier without comment
_ = doSomething()

// ❌ Ignored in conditional
if doSomething() != nil {
    // No handling
}
```

### 5. Error Creation (Priority: MEDIUM)

**Golden Rule**: Use appropriate error creation method for the situation.

**When to use what**:

```go
// Simple static error - use errors.New()
errors.New("task ID required")

// Error with formatting - use fmt.Errorf()
fmt.Errorf("invalid task ID: %s", id)

// Wrapping existing error - use fmt.Errorf with %w
fmt.Errorf("failed to save task: %w", err)

// Sentinel error (for errors.Is) - define as var
var ErrTaskNotFound = errors.New("task not found")
```

**RMS Standards**:

- NO `github.com/pkg/errors` - use stdlib only
- NO custom error types unless absolutely necessary
- Use `commonpb.Error` for gRPC error responses

### 6. Panic Usage (Priority: CRITICAL)

**Golden Rule**: No panics except during program startup/initialization.

**Acceptable Panic**:

```go
func init() {
    if os.Getenv("REQUIRED_VAR") == "" {
        panic("REQUIRED_VAR environment variable not set")
    }
}
```

**Unacceptable Panic**:

```go
func ProcessTask(task *Task) {
    if task == nil {
        panic("task is nil")  // ❌ Use error return instead
    }
}
```

## Step-by-Step Execution

### Step 1: Identify Go Files to Audit

```bash
# Find all Go files (exclude tests for now, as they have different rules)
find . -name "*.go" -not -path "*/vendor/*" -not -path "*/mock*" -not -path "*_test.go"
```

### Step 2: Read Target Go Files

Use Read tool to examine Go files, focusing on:

- Error handling blocks (`if err != nil`)
- Error creation (`errors.New`, `fmt.Errorf`)
- Function returns with error types
- Panic statements

### Step 3: Analyze Error Handling Patterns

For each error handling instance, check:

**A. Error Wrapping**

1. Find all `fmt.Errorf` calls with error arguments
2. Check if using `%w` (good) or `%v/%s` (bad)
3. Flag all instances using `%v` or `%s` with error arguments
4. Check for unwrapped returns (naked `return err`)

**B. Error Context**

1. Examine error message text
2. Verify it includes:
   - Operation being performed
   - Resource identifiers (IDs, names)
   - Relevant state information
3. Flag vague messages like "error", "failed", "operation failed"

**C. Error Message Format**

1. Check capitalization (should be lowercase)
2. Check for trailing punctuation (should have none)
3. Check for informal language (contractions, exclamations)
4. Verify consistent phrasing

**D. Error Swallowing**

1. Find all error assignments (`err :=`, `err =`)
2. Verify every assigned error is checked
3. For blank identifier `_`, verify explanatory comment exists
4. Flag any unchecked errors

**E. Error Creation**

1. Verify appropriate method used (errors.New vs fmt.Errorf)
2. Check for pkg/errors imports (forbidden in RMS code)
3. Flag custom error types (should be rare)

**F. Panic Usage**

1. Find all `panic()` calls
2. Verify they only appear in init() or main() startup code
3. Flag any panic in regular function bodies

### Step 4: Generate Report

Create a structured report:

```markdown
## Error Handling Audit: [file_path]

### ✅ Functions With Correct Error Handling

- `FunctionName` ([file:line]) - Proper wrapping, good context

### 🚨 CRITICAL Issues

#### Error Wrapping with %v Instead of %w

- **Function**: `FetchTask` ([file:line])
  - **Issue**: Using %v destroys error chain
  - **Location**: Line X: `fmt.Errorf("failed: %v", err)`
  - **Fix**: Change to `fmt.Errorf("failed: %w", err)`

#### Error Swallowing

- **Function**: `ProcessTask` ([file:line])
  - **Issue**: Error assigned but never checked
  - **Location**: Line X: `err := doSomething()`
  - **Fix**: Add error check or use `_` with comment

#### Panic in Runtime Code

- **Function**: `UpdateTask` ([file:line])
  - **Issue**: Panic used outside initialization
  - **Location**: Line X: `panic("task is nil")`
  - **Fix**: Return error instead

### ⚠️ HIGH Priority Issues

#### Insufficient Error Context

- **Function**: `SaveTask` ([file:line])
  - **Issue**: Error message lacks identifiers
  - **Location**: Line X: `fmt.Errorf("save failed: %w", err)`
  - **Fix**: Add task ID: `fmt.Errorf("failed to save task %s: %w", taskID, err)`

#### Unwrapped Error Return

- **Function**: `DeleteTask` ([file:line])
  - **Issue**: Error returned without wrapping
  - **Location**: Line X: `return err`
  - **Fix**: Add context: `return fmt.Errorf("failed to delete task %s: %w", taskID, err)`

### ℹ️ MEDIUM Priority Issues

#### Error Message Formatting

- **Function**: `ValidateTask` ([file:line])
  - **Issue**: Capitalized error message
  - **Location**: Line X: `errors.New("Task is invalid")`
  - **Fix**: Lowercase: `errors.New("task is invalid")`

#### Suboptimal Error Creation

- **Function**: `CheckTask` ([file:line])
  - **Issue**: Using fmt.Errorf without formatting
  - **Location**: Line X: `fmt.Errorf("invalid task")`
  - **Fix**: Use simpler: `errors.New("invalid task")`
```

### Step 5: Provide Fix Examples

For each issue, provide:

````markdown
#### Example Fix: Error Wrapping

**Before** (destroys error chain):

```go
func FetchTask(ctx rms.Ctx, id string) (*Task, error) {
    task, err := db.GetTask(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("failed to fetch task: %v", err)  // ❌
    }
    return task, nil
}
```
````

**After** (preserves error chain):

```go
func FetchTask(ctx rms.Ctx, id string) (*Task, error) {
    task, err := db.GetTask(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("failed to fetch task %s: %w", id, err)  // ✅
    }
    return task, nil
}
```

**Why**: Using %w preserves the error chain for errors.Is() and errors.As(), and adds task ID for debugging context.

````

### Step 6: Summary Statistics

```markdown
## Summary
- Files audited: X
- Functions checked: Y
- Issues found: Z
  - CRITICAL: A (must fix before commit)
  - HIGH: B (should fix before commit)
  - MEDIUM: C (fix during refactoring)
- Clean functions: W
````

## Integration Points

This skill is invoked by:

- **`quality-check`** skill for Go projects
- **`safe-commit`** skill (via quality-check)
- Directly when reviewing error handling

## Exit Criteria

- All Go error handling patterns analyzed
- Report generated with line-specific issues
- Fix examples provided for all critical/high issues
- Summary statistics calculated
- CRITICAL issues block commit (should be enforced by invoking skill)

## Example Usage

```bash
# Manual invocation
/skill error-handling-audit

# Automatic invocation via quality-check
/skill quality-check  # Detects Go project, invokes error-handling-audit
```

## References

- RMS Go Coding Standards: Error Handling
- Go Code Reviewer Agent: Error Handling Rules
- Go Blog: Error Wrapping - https://go.dev/blog/go1.13-errors
- Go Wiki: Errors - https://github.com/golang/go/wiki/Errors
