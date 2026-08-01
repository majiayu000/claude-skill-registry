---
name: smalltalk-debugger
description: 'This skill should be used when debugging Smalltalk code, including:'
---

---
name: smalltalk-debugger
description: Systematic debugging guide for Pharo Smalltalk development. Provides expertise in error diagnosis (MessageNotUnderstood, KeyNotFound, SubscriptOutOfBounds, AssertionFailure), incremental code execution with eval tool, intermediate value inspection, error handling patterns (on:do: blocks), stack trace analysis, UI debugger window detection (read_screen for hung operations), and debug-fix-reimport workflow. Use when encountering Pharo test failures, Smalltalk exceptions, unexpected behavior, timeout or non-responsive operations, need to verify intermediate values, execute code incrementally for diagnosis, or troubleshoot Tonel import errors.
---

# Smalltalk Debugger

Systematic debugging techniques for Pharo Smalltalk development using AI editors.

## Core Debugging Workflow

When tests fail or errors occur, follow this systematic approach:

### 1. Identify Error Location

From error message, confirm:
- **Error type** (MessageNotUnderstood, KeyNotFound, etc.)
- **Stack trace** - where error occurred
- **Expected vs Actual** - what went wrong

### 2. Verify with Partial Execution

Use `/st:eval` tool to execute relevant code incrementally.

**Basic error capture pattern:**
```smalltalk
| result |
result := Array new: 2.
[ | ret |
  ret := objA doSomething.
  result at: 1 put: ret printString.
] on: Error do: [:ex | result at: 2 put: ex description].
^ result
```

**Interpreting results:**
- `result at: 1` - Normal result (success case)
- `result at: 2` - Error description (failure case)

### 3. Check Intermediate Values

Inspect state at each step:

```smalltalk
| step1 step2 |
step1 := self getData.
step2 := step1 select: [:each | each isValid].
{
    'step1 count' -> step1 size.
    'step2 count' -> step2 size.
    'step2 result' -> step2 printString
} asDictionary printString
```

### 4. Fix and Re-test

1. **Fix in Tonel file** (never in Pharo)
2. **Re-import** with `import_package`
3. **Re-test** with `run_class_test`

## When Operations Stop Responding

If MCP tool calls hang or timeout with no response, a **debugger window may have opened in the Pharo image**. Since the debugger is invisible from the AI editor, operations will appear stuck.

### Detecting Hidden Debuggers

Use the `read_screen` tool to capture the Pharo UI state:

```
mcp__smalltalk-interop__read_screen: target_type='world'
```

This captures all morphs including debugger windows. Look for:
- Window titles containing "Debugger", "Error", or "Exception"
- UI hierarchy showing debugger-related components
- Error messages or stack traces in window content

### Resolution Steps

1. **Notify the user**: Inform them that a debugger window appears to be open in Pharo
2. **Request manual intervention**: Ask the user to:
   - Check their Pharo image for open debugger windows
   - Close any debugger windows
   - Review the error shown in the debugger to understand the root cause
3. **Address root cause**: Once the debugger is closed, investigate and fix the underlying error using standard debugging techniques
4. **Retry operation**: Re-run the failed MCP operation

**Note**: The Pharo debugger cannot be controlled remotely through MCP tools. User intervention in the Pharo image is required.

For complete UI debugging guidance, see [UI Debugging Reference](references/ui-debugging.md).

## Essential Debugging Patterns

### Pattern 1: Execute with Error Handling

Safely test code that might fail:

```smalltalk
| result |
result := Array new: 2.
[
    | obj |
    obj := MyClass new name: 'Test'.
    result at: 1 put: obj process printString.
] on: Error do: [:ex |
    result at: 2 put: ex description
].
^ result
```

### Pattern 2: Inspect Object State

Check what object contains:

```smalltalk
{
    'class' -> obj class name.
    'value' -> obj printString.
    'size' -> obj size.
    'isEmpty' -> obj isEmpty
} asDictionary printString
```

### Pattern 3: Debug Collection Operations

Track data flow through transformations:

```smalltalk
| items filtered mapped |
items := self getItems.
filtered := items select: [:each | each isValid].
mapped := filtered collect: [:each | each name].
{
    'items size' -> items size.
    'filtered size' -> filtered size.
    'mapped' -> mapped printString
} asDictionary printString
```

## Common Error Types Quick Reference

### MessageNotUnderstood
**Cause**: Method doesn't exist or typo in method name
**Debug**: Check spelling, search implementors
```
mcp__smalltalk-interop__search_implementors: 'methodName'
```

### KeyNotFound
**Cause**: Accessing non-existent Dictionary key
**Debug**: List keys, use at:ifAbsent:
```smalltalk
dict keys printString
dict at: #key ifAbsent: ['default']
```

### SubscriptOutOfBounds
**Cause**: Collection index out of range
**Debug**: Check size, use at:ifAbsent:
```smalltalk
collection size printString
collection at: index ifAbsent: [nil]
```

### ZeroDivide
**Cause**: Division by zero
**Debug**: Check denominator before dividing
```smalltalk
count = 0 ifTrue: [0] ifFalse: [sum / count]
```

### AssertionFailure (in tests)
**Cause**: Test expectation doesn't match actual
**Debug**: Execute test code with `/st:eval`, check if package imported

For complete error patterns and solutions, see [Error Patterns Reference](references/error-patterns.md).

## Object Inspection Quick Guide

### Basic Inspection
```smalltalk
" Object class "
obj class printString

" Instance variables "
obj instVarNames

" Check method exists "
obj respondsTo: #methodName
```

### Collection Inspection
```smalltalk
" Size and elements "
collection size
collection printString

" Safe first/last "
collection ifEmpty: [nil] ifNotEmpty: [:col | col first]
```

### Dictionary Inspection
```smalltalk
" Keys and values "
dict keys
dict values

" Safe access "
dict at: #key ifAbsent: ['default']
```

For comprehensive inspection techniques, see [Inspection Techniques Reference](references/inspection-techniques.md).

## Debugging Best Practices

### 1. Divide into Small Steps
Break problems into incremental steps and verify each:

```smalltalk
" Step 1: Verify object creation "
obj := MyClass new.
obj printString

" Step 2: Verify method call "
result := obj doSomething.
result printString
```

### 2. Always Use printString
When returning objects via JSON/MCP:

```smalltalk
✅ obj printString
✅ collection printString
✅ dict printString

❌ obj  " Don't return raw objects "
```

### 3. Check Intermediate Values
Never assume - verify at each step:

```smalltalk
intermediate := obj step1.
" Check here "
result := intermediate step2.
" Check here too "
```

### 4. Use Error Handling
Always capture errors with `on:do:`:

```smalltalk
[
    risky operation
] on: Error do: [:ex |
    " Handle or log error "
    ex description
]
```

### 5. Fix in Tonel, Not Pharo
- ✅ Edit `.st` file → Import → Test
- ❌ Edit in Pharo → Export → Commit

## Debugging Tools

### Primary Tool: `/st:eval`

Execute any Smalltalk code for testing and verification:

```
mcp__smalltalk-interop__eval: 'Smalltalk version'
mcp__smalltalk-interop__eval: '1 + 1'
mcp__smalltalk-interop__eval: 'MyClass new doSomething printString'
```

### Code Inspection Tools

```
mcp__smalltalk-interop__get_class_source: 'ClassName'
mcp__smalltalk-interop__get_method_source: class: 'ClassName' method: 'methodName'
mcp__smalltalk-interop__search_implementors: 'methodName'
mcp__smalltalk-interop__search_references: 'methodName'
```

## Practical Examples

### Example 1: Test Failure

**Error**: `Expected 'John Doe' but got 'John nil'`

**Debug process**:
1. Execute test code with `/st:eval`
2. Check if lastName was set
3. Inspect method implementation
4. Identify missing `^ self` in setter
5. Fix in Tonel file
6. Re-import and re-test

### Example 2: KeyNotFound

**Error**: `KeyNotFound: key #age not found`

**Debug process**:
1. List dictionary keys: `dict keys`
2. Check if age key exists: `dict includesKey: #age`
3. Use safe access: `dict at: #age ifAbsent: [0]`
4. Fix initialization to include age key

For complete debugging scenarios with step-by-step solutions, see [Debug Scenarios Examples](examples/debug-scenarios.md).

## Troubleshooting Checklist

When debugging, systematically check:

- [ ] Read complete error message
- [ ] Use `/st:eval` to test incrementally
- [ ] Inspect all intermediate values
- [ ] Check method implementation
- [ ] Verify package was imported
- [ ] Edit Tonel file (not Pharo)
- [ ] Re-import after fixing
- [ ] Re-run tests

## Complete Documentation

This skill provides focused debugging guidance. For comprehensive information:

- **[Error Patterns Reference](references/error-patterns.md)** - All error types with solutions
- **[Inspection Techniques](references/inspection-techniques.md)** - Complete object inspection guide
- **[Debug Scenarios](examples/debug-scenarios.md)** - Real-world debugging examples

## Summary

**Core debugging cycle:**

```
Error occurs
    ↓
Identify error type
    ↓
Use /st:eval to test incrementally
    ↓
Inspect intermediate values
    ↓
Identify root cause
    ↓
Fix in Tonel file
    ↓
Re-import
    ↓
Re-test → Success or repeat
```

**Remember**: Systematic approach, incremental testing, fix in Tonel, always re-import.
