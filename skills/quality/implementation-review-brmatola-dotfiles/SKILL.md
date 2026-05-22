---
name: implementation-review
description: Use after implementing a plan to verify completeness, correctness, and merge safety - the post-implementation gate
---

# Implementation Review

## Overview

Verify implementation is complete, correct, and safe to merge. This is the merge readiness gate.

**Core principle:** Catch issues before merge, not after.

**Announce at start:** "I'm using the implementation-review skill to audit this implementation."

**Plan location:** `plans/active/{plan-name}/`

## The Process

### Step 1: Load Context

1. Read original plan from `plans/active/{plan-name}/`
2. Get current branch name
3. Find base branch (main/master)

```bash
git branch --show-current
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
```

### Step 2: Gather Implementation Data

Get all commits since diverging from base:

```bash
git log --oneline $(git merge-base HEAD main)..HEAD
```

Get all changed files:

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD
```

### Step 3: Evaluate Against Criteria

**Correctness:**
- [ ] Implementation matches plan intent?
- [ ] Any drift from plan (features added/removed)?
- [ ] All tasks from plan completed?

**Completeness:**
- [ ] Success criteria from plan met?
- [ ] All expected files exist?
- [ ] Nothing half-done or TODO'd?

**Quality:**
- [ ] Code follows project patterns?
- [ ] No obvious bugs?
- [ ] Error handling present where needed?

**Safety:**
- [ ] Tests passing?
- [ ] No regressions in existing tests?
- [ ] No security issues introduced?
- [ ] No debug code left (console.log, print, etc.)?

### Step 4: Run Checks

Run test suite:
```bash
# Detect and run appropriate test command
npm test || cargo test || pytest || go test ./...
```

Check for debug code:
```bash
git diff $(git merge-base HEAD main)..HEAD | grep -E "(console\.log|print\(|debugger|TODO|FIXME)" || echo "None found"
```

### Step 5: Produce Verdict

Output this format:

```
## Implementation Review: {plan-name}

### Verdict: MERGE READY | NEEDS FIXES | MAJOR ISSUES

### Plan Compliance
- [X] Task 1: [Description] - Implemented correctly
- [X] Task 2: [Description] - Implemented correctly
- [ ] Task 3: [Description] - Partial/Missing [reason]

### Test Results
- Suite: {X}/{Y} passing
- Coverage: {Z}% (if available)

### Quality Checks
- [X] No debug code (console.log, print, etc.)
- [X] Follows project patterns
- [X] Error handling present

### Issues Found
- **[Severity: blocker|major|minor]**: [Description]
  - Location: [file:line]
  - Suggested fix: [How to address]

### Recommendation
[Ready to merge / Fix these N issues first]
```

## Verdict Meanings

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| **MERGE READY** | Safe to merge | Finish branch (merge/PR) |
| **NEEDS FIXES** | Minor issues to address | Fix, re-review |
| **MAJOR ISSUES** | Significant problems | May need plan revision |

## Issue Severity

| Severity | Meaning |
|----------|---------|
| **blocker** | Cannot merge until fixed (test failure, security issue) |
| **major** | Should fix before merge (missing functionality, bad pattern) |
| **minor** | Nice to fix but not blocking (style, minor improvements) |

## Red Flags

**Never:**
- Approve with failing tests
- Skip debug code check
- Ignore plan drift without noting it

**Always:**
- Run actual test suite
- Compare against original plan
- Check for leftover debug artifacts

## Integration

**Invoked by:**
- **gremlins:worktree-workflow** (audit phase) - Post-implementation gate
- Standalone for any implementation review

**Follows:**
- **gremlins:executing-plans** - Reviews output of implementation

**Leads to:**
- **gremlins:finishing-a-development-branch** - When MERGE READY
- **gremlins:reach-opportunities** - When user opts in after passing

**vs verification-before-completion:**
- Use **implementation-review** as the workflow gate (comprehensive, plan-aware)
- Use **verification-before-completion** for quick ad-hoc checks outside workflow
