---
name: plan
tags:
  technology: [python, typescript, javascript]
  feature: [workflow, documentation]
  priority: high
summary: Create task breakdown with acceptance criteria, file scope, and test plan
version: 1
---

# Plan

## When to use

- You have a product mission + docs and need a clear task breakdown
- Starting implementation of a new feature
- Need to estimate effort and dependencies

## Instructions

1. Extract acceptance criteria and constraints from discovery phase

2. Create tasks (T1..TN) with:
   - **User story + criteria**: What the user should be able to do
   - **Files to create/modify**: Specific paths
   - **Tests to add/run**: Test file locations and descriptions
   - **Dependencies**: Which tasks depend on others

3. Keep tasks small and parallelizable:
   - Each task should be completable in one session
   - Minimize dependencies between tasks
   - Group related changes together

## Task Format

```markdown
## Task T1: [Title]

### User Story
As a [user], I want to [action], so that [benefit].

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Files
- CREATE: `src/module.py`
- MODIFY: `src/existing.py`

### Tests
- `tests/test_module.py::test_feature`

### Dependencies
- None (can start immediately)
```

## Planning Checklist

- [ ] All acceptance criteria covered by tasks
- [ ] Each task has clear file scope
- [ ] Each task has defined tests
- [ ] Dependencies are documented
- [ ] Tasks are small enough for one session
