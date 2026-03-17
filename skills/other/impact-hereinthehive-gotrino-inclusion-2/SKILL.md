---
name: impact
description: Analyze system-wide impact of changes before making them. Use before modifying shared utilities, changing APIs, or refactoring core functionality.
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Impact Analysis

Analyze the system-wide impact of proposed or recent changes before you make them.

## Philosophy

Code doesn't exist in isolation. A "small fix" in a shared utility can break ten components. A type change can cascade through the entire codebase.

> "What else depends on this? What might break?"

This skill isn't about being cautious—it's about being **informed**. Make changes with full knowledge of their ripple effects.

## When to Use

Run `/impact` before:
- Modifying shared utilities or types
- Changing API signatures
- Refactoring core functionality
- Deleting or renaming exports
- Making changes that "seem small but might ripple"

## Input

The user will provide:
- File path(s) being changed, OR
- Function/class/type name being modified, OR
- Description of planned change

If nothing provided, analyze uncommitted changes.

## Process

### 1. Identify Change Scope

Determine what's being modified:
- File(s) affected
- Exports being changed (functions, types, classes)
- API signatures being modified
- Data structures being altered

### 2. Find Direct Dependents

Search for code that directly uses the modified code:
- Files that import from the changed file
- Functions/components that call the modified code
- Types that extend or reference modified types

### 3. Check Test Coverage

Find related tests:
- Unit tests for the modified code
- Integration tests that exercise this path
- Tests that might need updating

### 4. Trace Downstream Effects

Follow the impact chain:
- Direct dependents → their dependents
- API routes that expose this functionality
- UI components that consume this data

## Output Format

Keep it **compact**. Tables for findings, clear risk assessment.

```markdown
## Impact Analysis: [Change Description]

**Scope**: [What's being changed]
**Risk Level**: Low | Medium | High

---

### Direct Dependents

| File | Usage | Risk |
|------|-------|------|
| `consumer.ts:45` | Calls `modifiedFunction()` | Medium |
| `component.tsx:23` | Uses `ModifiedType` | Low |

### Test Coverage

**Tests found:**
- `__tests__/file.test.ts` - Direct unit tests ✓

**Tests that may need updates:**
- `integration/flow.test.ts` - Uses affected flow

### Breaking Change Assessment

| Check | Status |
|-------|--------|
| Public API changes | Yes / No |
| Type signature changes | Yes / No |
| Behavioral changes | Yes / No |
| Database/schema changes | Yes / No |

---

### Recommendations

1. **Before changing**: [Specific prep work]
2. **Update alongside**: [Files that need coordinated changes]
3. **Tests to run**: [Specific test commands]
4. **Communicate to**: [Teams or people who should know]

### Summary

[1-2 sentences: X dependents found, Y tests affected, overall risk level and why]
```

## Why This Matters

Impact analysis prevents:
- **Surprise breakages** in unrelated parts of the codebase
- **Incomplete migrations** where some consumers are missed
- **Test failures** that could have been anticipated
- **Team friction** when changes affect others' work

The five minutes spent on impact analysis saves hours of debugging and rollbacks.
