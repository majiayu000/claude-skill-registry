---
name: review-and-qa
description: Review the changes for <commit|branch|pr> and create a QA review plan
---

# Review Changes

Review the changes for: $ARGUMENTS.

## Instructions

Perform a two-phase review:

1. **Code review** - Review quality, architecture, and best practices.
2. **QA review** - Create manual test cases to validate behavior.

## Phase 1: Code review

Analyze the code changes for:

## PR checklist

### Required for all PRs

- [ ] **Small diff** - One logical change. If the PR does multiple things, split it.
- [ ] **Tests included** - New functionality has tests. Bug fixes have regression tests.
- [ ] **No secrets** - No tokens, passwords, or credentials in the code.

### If user-facing changes

- [ ] **Docs updated** - The README or relevant documentation reflects the change.
- [ ] **Examples work** - Code examples in the documentation are tested and copy-paste ready.
- [ ] **Error messages helpful** - New errors explain what went wrong and how to fix it.

### If breaking changes

- [ ] **Migration notes** - Provide clear before and after examples showing how to upgrade.
- [ ] **Changelog entry** - Follow conventional commits for release notes.
- [ ] **Deprecation warnings** - If keeping an old API temporarily, warn users.

### If adding dependencies

- [ ] **Justified** - No existing solution exists in the codebase.
- [ ] **License compatible** - Use MIT or a compatible license.
- [ ] **Maintained** - Use an active project with recent updates.
- [ ] **Size reasonable** - Avoid adding significant bundle weight.

### Quality and clean code

- [ ] Functions are small and single-purpose.
- [ ] Variable and function names are descriptive.
- [ ] No dead code or commented-out blocks exist.
- [ ] No magic numbers exist (use constants).
- [ ] Error messages are helpful.

### Architecture and design

- [ ] Changes fit existing patterns in the codebase.
- [ ] No unnecessary coupling exists between modules.
- [ ] Proper separation of concerns exists (actions vs. commands vs. utils).
- [ ] Types and interfaces are defined appropriately.

### Reusability and centralization

- [ ] Duplicated logic is extracted to shared utilities.
- [ ] Existing helpers are used where applicable.
- [ ] New utilities are generic enough for reuse.
- [ ] Constants are centralized (not scattered).

### Best practices

- [ ] Async and await are used consistently (no mixed patterns).
- [ ] Errors are propagated correctly (not swallowed).
- [ ] Edge cases are handled (null, empty, invalid input).
- [ ] No security issues exist (injection, secrets exposure).

### Output format (code review)

```markdown
## Code review summary

[LGTM / Needs changes / Blocking issues]

## Issues found

### [Critical/Major/Minor]: Issue title

**File:** `path/to/file.ts:123`
**Problem:** Description.
**Suggestion:** How to fix.
```

## Phase 2: QA review

### Test case structure

Refer to the [Test Plan Template](./templates/test-plan.md) and the [Test Plan Example](./examples/assets-test-plan.md) for test plan structure guidance.

### Coverage requirements

Create test cases for:

1. **Happy path** - Normal successful operation.
2. **Negative cases** - Invalid input, unauthorized access, and missing data.
3. **Edge cases** - Empty input, large input, and special characters.
4. **Error recovery** - What happens when things fail mid-operation.
