---
name: generate-fix-suggestions
description: "Generate fix suggestions based on error patterns and best practices. Use when analyzing failures to get actionable remediation steps."
category: testing
mcp_fallback: none
user-invocable: false
---

# Generate Fix Suggestions from Errors

Analyze error patterns to suggest specific fixes and improvements.

## When to Use

- Test failures need concrete solutions
- Build errors require remediation steps
- Code review finding actionable recommendations
- Automating fix suggestions for common errors
- Creating PR comments with suggestions

## Quick Reference

```bash
# Categorize errors
grep "Error\|FAILED" output.log | sed 's/.*Error: //' | sort | uniq -c | sort -rn

# Get context around error
grep -B 3 -A 3 "AssertionError" output.log

# Extract error type
grep -o "Error[A-Za-z]*" output.log | sort | uniq -c

# Find patterns in multiple failures
for file in test_*.log; do
  echo "=== $file ==="
  grep "Error:" "$file" | head -3
done
```

## Fix Generation Workflow

1. **Analyze error**: Categorize error type and context
2. **Match pattern**: Compare against known error patterns
3. **Find root cause**: Determine what caused the error
4. **Generate suggestion**: Recommend specific fix
5. **Provide example**: Show before/after code if applicable
6. **Prioritize fixes**: High impact fixes first
7. **Report suggestions**: Organized by priority

## Common Error Patterns & Fixes

**Assertion Errors**:

- Pattern: `assert_equal(actual, expected)` fails
- Fix: Check expected value is correct, verify test logic
- Example: Update expected value or fix test setup

**Type Mismatches**:

- Pattern: `TypeError`, `AttributeError` in function call
- Fix: Check argument types, verify method exists
- Example: Add type annotation or check imports

**Out of Bounds**:

- Pattern: `IndexError` or array access failure
- Fix: Verify array size, check loop bounds
- Example: Initialize array properly before access

**Import/Module Errors**:

- Pattern: `ModuleNotFoundError`, `ImportError`
- Fix: Check module path, verify file exists
- Example: Add to `__init__.mojo` or fix path

**Memory/Initialization**:

- Pattern: Uninitialized variable, null pointer
- Fix: Ensure variable initialized before use
- Example: Add explicit initialization or use `var`

## Output Format

Report suggestions with:

1. **Error Summary** - What went wrong
2. **Root Cause** - Why it happened
3. **Fix Steps** - Numbered remediation steps
4. **Code Example** - Before/after code snippet
5. **Priority** - Critical/High/Medium/Low
6. **Testing** - How to verify fix works

## Priority Levels

**Critical** (fix immediately):

- Compilation errors
- All tests failing
- Core functionality broken
- Security issues

**High** (fix soon):

- Multiple tests failing
- Performance degradation
- Memory leaks
- Type safety issues

**Medium** (nice to have):

- Single test failing
- Code style issues
- Minor improvements
- Warnings

**Low** (backlog):

- Code polish
- Optional refactoring
- Documentation improvements

## Error Handling

| Problem | Solution |
|---------|----------|
| Unknown error type | Classify as "other", suggest general investigation |
| Insufficient context | Request more detailed error info |
| Multiple causes | Suggest fixes in priority order |
| No matching pattern | Flag for manual review |
| False positives | Verify suggestion with test run |

## References

- See extract-test-failures for error extraction
- See analyze-ci-failure-logs for CI-specific analysis
- See CLAUDE.md for code standards and error handling
