---
name: workflow-patterns
model: standard
version: 2.0.0
description: >
  Systematic task implementation using TDD, phase checkpoints, and structured commits.
  Ensures quality through red-green-refactor cycles, 80% coverage gates, and verification
  protocols before proceeding.
tags: [tdd, workflow, quality, testing, git, checkpoints, implementation]
---

# Workflow Patterns

Implement tasks systematically using TDD (Test-Driven Development) with phase checkpoints and verification protocols. Ensures quality at every step.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install workflow-patterns
```


## WHAT This Skill Does

Provides a structured approach to implementing tasks:
- TDD cycle (red → green → refactor) for each task
- Quality gates (tests, coverage, linting) before marking complete
- Phase checkpoints requiring user approval
- Git commits with rich metadata for traceability

## WHEN to Use

**Use for:**
- Implementing features from a plan
- Following TDD methodology
- Tasks requiring quality verification
- Projects with coverage requirements
- Team workflows needing traceability

**Skip for:**
- Quick fixes or trivial changes
- Exploratory prototyping
- Projects without test infrastructure

**Keywords:** TDD, implementation, testing, coverage, checkpoints, verification, red-green-refactor

## The TDD Task Lifecycle

11 steps for each task:

### Step 1: Select Next Task

Read the plan and identify the next pending `[ ]` task. Select tasks in order within the current phase. Do not skip ahead.

### Step 2: Mark as In Progress

Update the plan to mark the task as `[~]`:

```markdown
- [~] **Task 2.1**: Implement user validation
```

### Step 3: RED — Write Failing Tests

Write tests that define expected behavior **before** implementation:

- Create test file if needed
- Cover happy path
- Cover edge cases
- Cover error conditions
- Run tests — they should **FAIL**

```python
def test_validate_email_valid():
    user = User(email="test@example.com")
    assert user.validate_email() is True

def test_validate_email_invalid():
    user = User(email="invalid")
    assert user.validate_email() is False
```

### Step 4: GREEN — Implement Minimum Code

Write the minimum code to make tests pass:

- Focus on making tests green, not perfection
- Avoid premature optimization
- Keep implementation simple
- Run tests — they should **PASS**

### Step 5: REFACTOR — Improve Clarity

With green tests, improve the code:

- Extract common patterns
- Improve naming
- Remove duplication
- Simplify logic
- Run tests after each change — must stay **GREEN**

### Step 6: Verify Coverage

Check test coverage meets the 80% target:

```bash
pytest --cov=module --cov-report=term-missing
```

If coverage is below 80%:
- Identify uncovered lines
- Add tests for missing paths
- Re-run coverage check

### Step 7: Document Deviations

If implementation deviated from plan or added dependencies:
- Update tech-stack.md with new dependencies
- Note deviations in plan task comments
- Update spec if requirements changed

### Step 8: Commit Implementation

Create focused commit:

```bash
git commit -m "feat(user): implement email validation

- Add validate_email method to User class
- Handle empty and malformed emails
- Add comprehensive test coverage

Task: 2.1"
```

### Step 9: Update Plan with SHA

Mark task complete with commit SHA:

```markdown
- [x] **Task 2.1**: Implement user validation `abc1234`
```

### Step 10: Commit Plan Update

```bash
git commit -m "docs: update plan - task 2.1 complete"
```

### Step 11: Repeat

Continue to next task until phase is complete.

## Phase Completion Protocol

When all tasks in a phase are complete:

### 1. Identify Changed Files

```bash
git diff --name-only <last-checkpoint-sha>..HEAD
```

### 2. Ensure Test Coverage

For each modified file:
- Verify tests exist for new/changed code
- Run coverage for modified modules
- Add tests if coverage < 80%

### 3. Run Full Test Suite

```bash
pytest -v --tb=short
```

All tests must pass.

### 4. Generate Verification Checklist

```markdown
## Phase 1 Verification

- [ ] User can register with valid email
- [ ] Invalid email shows appropriate error
- [ ] Database stores user correctly
```

### 5. WAIT for User Approval

Present checklist:

```
Phase 1 complete. Please verify:
1. [x] Test suite passes (automated)
2. [x] Coverage meets target (automated)
3. [ ] Manual verification items (requires human)

Respond with 'approved' to continue.
```

**Do NOT proceed without explicit approval.**

### 6. Create Checkpoint Commit

```bash
git commit -m "checkpoint: phase 1 complete

Verified:
- All tests passing
- Coverage: 87%
- Manual verification approved"
```

### 7. Record Checkpoint SHA

Update plan checkpoints table:

```markdown
## Checkpoints

| Phase   | SHA     | Date       | Status   |
|---------|---------|------------|----------|
| Phase 1 | def5678 | 2025-01-15 | verified |
| Phase 2 |         |            | pending  |
```

## Quality Gates

Before marking any task complete:

| Gate | Requirement |
|------|-------------|
| Tests | All existing tests pass, new tests pass |
| Coverage | New code has 80%+ coverage |
| Linting | No linter errors |
| Types | Type checker passes (if applicable) |
| Security | No secrets in code, input validation present |

## Git Commit Format

```
<type>(<scope>): <subject>

<body>

Task: <task-id>
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Code change without feature/fix
- `test` — Adding tests
- `docs` — Documentation
- `chore` — Maintenance

## Handling Deviations

### Scope Addition
Discovered requirement not in spec:
- Document in spec as new requirement
- Add tasks to plan
- Note addition in task comments

### Scope Reduction
Feature deemed unnecessary:
- Mark tasks as `[-]` (skipped) with reason
- Update spec scope section
- Document decision rationale

### Technical Deviation
Different approach than planned:
- Note deviation in task comment
- Update tech-stack.md if dependencies changed
- Document why original approach was unsuitable

```markdown
- [x] **Task 2.1**: Implement validation `abc1234`
  - DEVIATION: Used library instead of custom code
  - Reason: Better edge case handling
  - Impact: Added email-validator to dependencies
```

## Error Recovery

### Tests Fail After GREEN

1. Do NOT proceed to REFACTOR
2. Identify which test started failing
3. Revert to last known GREEN state
4. Re-approach the implementation

### Checkpoint Rejected

1. Note rejection reason in plan
2. Create tasks to address issues
3. Complete remediation tasks
4. Request checkpoint approval again

### Blocked by Dependency

1. Mark task as `[!]` with blocker description
2. Check if other tasks can proceed
3. Document expected resolution

## Task Status Symbols

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Pending |
| `[~]` | In progress |
| `[x]` | Complete |
| `[-]` | Skipped |
| `[!]` | Blocked |

## Best Practices

1. **Never skip RED** — Always write failing tests first
2. **Small commits** — One logical change per commit
3. **Immediate updates** — Update plan right after task completion
4. **Wait for approval** — Never skip checkpoint verification
5. **Coverage discipline** — Don't accept below target
6. **Sequential phases** — Complete phases in order
7. **Document deviations** — Note any changes from plan
8. **Clean state** — Each commit leaves code working

## NEVER Do

1. **NEVER skip the RED phase** — writing tests first is non-negotiable in TDD
2. **NEVER proceed past checkpoints without approval** — wait for explicit user confirmation
3. **NEVER commit code that doesn't pass tests** — every commit must be a working state
4. **NEVER accept coverage below 80%** — add tests until threshold is met
5. **NEVER hide deviations from the plan** — document all changes from original spec
6. **NEVER skip phases or reorder them** — phases are sequential for a reason
7. **NEVER forget to record commit SHAs** — traceability requires linking tasks to commits
