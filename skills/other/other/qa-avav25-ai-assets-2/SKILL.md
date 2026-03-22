---
name: qa
description: Quality assurance workflow for validating features, writing or improving tests, reporting bugs, and checking coverage or acceptance criteria.
---

# QA

Use this workflow for verification and test quality work.

## 1. Determine the QA Task

Classify the request as one of:

- Feature verification
- Bug report
- Test creation
- Test improvement
- Exploratory testing
- Coverage review

## 2. Gather Context

Read:

1. `TESTING.md` if present
2. Root `AGENTS.md`
3. Relevant scoped `AGENTS.md`
4. Feature brief, bug report, or changed code in scope
5. Existing tests for the target area

## 3. Execute the Task

### Feature Verification

- Map acceptance criteria to observable behavior
- Check happy path, edge cases, and error paths
- Record pass, fail, or partial status with evidence

### Bug Report

- Reproduce the issue
- Capture logs, errors, and minimal repro
- Write a structured report with expected vs actual behavior

### Test Creation or Improvement

- Identify coverage gaps
- Write or improve tests using the project's existing patterns
- Prefer deterministic tests and narrow scope first

### Exploratory Testing

- Identify risky or recently changed areas
- Explore happy path, invalid input, state transitions, and regressions
- Record issues with severity and reproduction steps

### Coverage Review

- Review current coverage signals
- Identify important untested logic
- Recommend the next highest-value tests

## 4. Apply the Quality Gate

Check:

- Existing tests still pass
- New tests are deterministic
- Acceptance criteria are covered where relevant
- Bug reports include evidence and reproduction steps

## 5. Report

Summarize:

- What was tested
- Issues found
- Tests added or improved
- Coverage impact if relevant
- Recommended next steps

## Integration

- Companion skills: `testing-procedures`, `run-tests`, `test-local`
- Common follow-up: `bugfix`, `feature-dev`, `pre-commit`