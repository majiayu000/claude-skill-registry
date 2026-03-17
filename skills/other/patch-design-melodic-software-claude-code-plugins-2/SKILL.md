---
name: patch-design
description: Create minimal, surgical patch plans for targeted fixes. Use when fixing specific issues from review, creating focused patches, or avoiding scope creep in fix implementations.
allowed-tools: Read, Grep
---

# Patch Design Skill

Create minimal, surgical patch plans for targeted fixes.

## When to Use

- Fixing specific issues from review
- Creating focused bug fixes
- Addressing blockers without scope creep
- Making targeted improvements

## Core Principle

> "This is a PATCH - keep the scope minimal. Only fix what's described in the issue and nothing more."

## Design Workflow

### Step 1: Understand the Specific Issue

Parse the issue clearly:

- **What is broken?** (specific behavior)
- **How should it work?** (expected behavior)
- **What evidence exists?** (screenshots, errors)

Do NOT expand scope beyond the reported issue.

### Step 2: Analyze Current State

Review the relevant code:

```bash
# Find relevant files
git diff --stat
grep -r "related_function" src/

# Read the specific code
cat src/component/file.ts
```

### Step 3: Determine Minimum Fix

Ask: "What is the smallest change that fixes this?"

| Approach | Lines | Risk |
| --- | --- | --- |
| Surgical fix | 1-10 | Low |
| Targeted fix | 10-50 | Medium |
| Refactor | 50+ | High |

**Always prefer surgical fixes** for patches.

### Step 4: Create Patch Plan

Document the precise fix:

```markdown
# Patch: [Concise title]

## Issue Summary
**Problem**: [What's broken]
**Solution**: [Minimal fix]

## Files to Modify
- `path/to/file.ts`: [Specific change]

## Implementation Steps

### Step 1: [Specific action]
[Exact code change]

### Step 2: [Specific action]
[Exact code change]

## Validation
- [Command to verify fix]
- [How to confirm success]

## Patch Scope
- Lines of code: ~X
- Risk level: low
- Testing: [minimal/standard]
```

### Step 5: Define Validation

Every patch needs verification:

```markdown
## Validation

1. Run specific test: `npm test path/to/test`
2. Manual verification: [steps]
3. Visual check: [if applicable]
```

## Patch Plan Template

```markdown
# Patch: [Brief description]

## Metadata
- Issue: [Source of this patch request]
- Severity: [blocker/tech_debt]

## Issue Summary
**Original Spec**: [Link if available]
**Problem**: [Brief description of what's wrong]
**Solution**: [Brief description of the fix]

## Files to Modify
[Only files that need changes - be specific]

- `src/component/Button.tsx`: Fix disabled state

## Implementation Steps

IMPORTANT: Execute every step in order.

### Step 1: [Specific change]

<!-- markdownlint-disable MD033 -->

```jsx
// Before
<button onClick={handleClick}>

// After
<button onClick={handleClick} disabled={isLoading}>
```

<!-- markdownlint-enable MD033 -->

### Step 2: [Next change if needed]

[Details]

## Validation

Execute to confirm patch is complete:

- `npm test src/component/Button.test.tsx`
- Manual: Click button, verify disabled during load

## Patch Scope

- **Lines changed**: ~5
- **Risk level**: low
- **Testing**: Run component tests

## Anti-Patterns to Avoid

### Scope Creep

```markdown
# BAD: Expanding scope
While fixing the button, I noticed the form could use
refactoring, so I'll also update the validation logic,
improve the error messages, and add loading states to
all other buttons too.
```

### Vague Changes

```markdown
# BAD: Vague plan
## Implementation
- Fix the button issue
- Make it work correctly
- Test to confirm
```

### No Validation

```markdown
# BAD: No verification
## Implementation
1. Change the code
2. Done
```

## Best Practices

1. **One issue, one patch**: Don't bundle fixes
2. **Minimal scope**: Only change what's needed
3. **Specific steps**: Exact code changes
4. **Clear validation**: How to verify success
5. **Risk assessment**: Lines changed, testing needed

## Integration with Review

Patches typically come from review issues:

```text
/review → Identifies blocker
  ↓
/patch → Creates surgical fix plan
  ↓
/implement → Executes patch
  ↓
/review → Verifies fix (re-review)
```

## Memory References

- @issue-severity-classification.md - What triggers patches
- @review-vs-test.md - Review identifies patch needs
- @one-agent-one-purpose.md - Patches are focused by nature

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
