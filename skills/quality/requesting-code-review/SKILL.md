---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Review your work systematically before declaring it complete.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in implementation
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## Self-Review Process

### Step 1: Gather Context

```bash
# What changed?
git diff HEAD~1

# What files?
git diff --name-only HEAD~1
```

### Step 2: Spec Compliance Check

- [ ] Does the implementation match requirements?
- [ ] Are all acceptance criteria met?
- [ ] Is the feature complete?

### Step 3: Code Quality Check

- [ ] Is the code readable and well-named?
- [ ] Is there any duplication to extract?
- [ ] Are edge cases handled?
- [ ] Are error messages helpful?

### Step 4: Test Quality Check

- [ ] Do tests cover the happy path?
- [ ] Do tests cover edge cases?
- [ ] Do tests cover error conditions?
- [ ] Are tests readable and maintainable?

### Step 5: Final Verification

- [ ] All tests pass
- [ ] No lint errors
- [ ] No console errors/warnings
- [ ] Changes committed with descriptive message

## Issue Severity

| Severity | Action |
|----------|--------|
| **Critical** | Fix immediately, don't proceed |
| **Important** | Fix before proceeding |
| **Minor** | Note for later, can proceed |

## Common Mistakes

- Skipping review because "it's simple"
- Ignoring critical issues
- Proceeding with unfixed important issues
- Not running tests before review
- Reviewing only the happy path

## Integration

Use after:
- Each task in `executing-plans`
- Each task in `subagent-driven-development`

Before:
- Creating pull request
- Merging to main branch
