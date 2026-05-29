---
name: plan-review-implementation
description: Review completed implementation, identify issues, and either create fix plans or mark complete. Use after plan-implement has executed work.
allowed-tools: Read, Edit, Glob, Grep
disable-model-invocation: true
---

Review the latest implementation iteration and either create a fix plan or mark complete.

## Pre-flight Check

1. **Read PLANS.md** - Understand the full plan and iteration history
2. **Read CLAUDE.md** - Understand project standards and conventions

## Identify What to Review

Find the **latest "Iteration N"** section that has:
- "Completed" subsection (implementation was done)
- NO "Review Findings" subsection (not yet reviewed)

If no iteration needs review → Inform user and stop.

## Review Process

### Step 1: Identify Implemented Code

From the iteration's "Completed" section, list all files that were:
- Created
- Modified
- Added tests to

### Step 2: Thorough Code Review

Read each implemented file and check for:

| Category | What to Look For |
|----------|------------------|
| **BUG** | Logic errors, off-by-one, null handling, race conditions |
| **EDGE CASE** | Unhandled scenarios, boundary conditions |
| **SECURITY** | Injection vulnerabilities, exposed secrets, missing auth |
| **TYPE** | Type mismatches, unsafe casts, missing type guards |
| **ERROR** | Missing error handling, swallowed exceptions |
| **CONVENTION** | Violations of CLAUDE.md rules |

### Step 3: Evaluate Severity

Not all findings require fixes. Consider:

**Fix Required:**
- Would cause runtime errors
- Could corrupt data
- Security vulnerability
- Test doesn't actually test the behavior
- Violates CLAUDE.md critical rules

**Not a Fix (document but don't create fix plan):**
- Style preferences not in CLAUDE.md
- Theoretical edge cases that can't occur
- "Nice to have" improvements
- Future enhancements

## Document Findings

### If Issues Found

Add to the current Iteration section:

```markdown
### Review Findings
- BUG: [description] (`file.ts:line`)
- EDGE CASE: [description] (`file.ts:line`)
- SECURITY: [description] (`file.ts:line`)

### Fix Plan

#### Fix 1: [Title matching the BUG above]
1. Write test in [file].test.ts for [scenario that reproduces the bug]
2. Implement fix in [file].ts

#### Fix 2: [Title matching the EDGE CASE above]
1. Write test...
2. Implement fix...
```

### If No Issues Found

Add to the current Iteration section, then append final status:

```markdown
### Review Findings
None - all implementations are correct and follow project conventions.

---

## Status: COMPLETE

All tasks implemented and reviewed successfully. Ready for human review.
```

## Issue Categories Reference

| Tag | Description | Severity |
|-----|-------------|----------|
| `BUG` | Logic errors causing incorrect behavior | High |
| `EDGE CASE` | Unhandled scenario that could occur | Medium |
| `SECURITY` | Vulnerability or exposure risk | High |
| `TYPE` | Type safety issues | Medium |
| `ERROR` | Missing or incorrect error handling | Medium |
| `CONVENTION` | Violation of CLAUDE.md rules | Low-Medium |

## Rules

- **Do not modify source code** - Review only, document findings
- **Be specific** - Include file paths and line numbers for every issue
- **One fix per issue** - Each Review Finding must have a matching Fix task
- **Fix Plan follows TDD** - Test first for each fix
- **Never modify previous sections** - Only add to current iteration or append status
- **Mark COMPLETE only when confident** - No known bugs, all conventions followed
- If no iteration needs review, inform the user and stop
