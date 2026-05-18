# PR templates

Select the template matching the PR type.

---

## Feature (feature/* -> develop)

**Title**: `feat(<scope>): <description>`

```markdown
## What
- [List of implemented features/components]
- [Main functionality highlights]

## Why
- [Business/operational impact]
- [Pain points resolved]

## Details
### Task X.Y: [Task title]
- [Implementation detail 1]
- [Implementation detail 2]
- **Requirements**: X, Y, Z

## Checklist
- [ ] Main feature implemented
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code review ready
```

---

## Release (develop -> main)

**Title**: `release: version X.Y with [main features]`

```markdown
## What
This release includes:
- [Feature set 1 - Task N]
- [Feature set 2 - Task M]

## Why
[Release motivation, milestone reached]

## Details
### Task N: [Feature name] (COMPLETE)
- **Task N.1**: [Description]
- **Task N.2**: [Description]
- **Requirements**: X, Y, Z

## Testing
- Coverage: XX%
- Integration tests: pass/fail

## Checklist
- [ ] All tasks completed
- [ ] No breaking changes (or documented)
- [ ] Migration guide prepared (if needed)
```

---

## Bugfix (fix/* -> develop)

**Title**: `fix(<scope>): <description>`

```markdown
## What
Fix for [problem description]

## Problem
[Bug description, how it manifests, impact]

## Solution
[Explanation of implemented solution]

## Testing
- [How the fix was tested]
- [Regression tests added]

## Checklist
- [ ] Bug resolved
- [ ] Regression tests added
- [ ] No side effects introduced
```

---

## Hotfix (hotfix/* -> main)

**Title**: `hotfix(<scope>): <critical fix>`

```markdown
## HOTFIX

### Issue
[Description of critical production issue]

### Root cause
[Identified cause]

### Fix
[Implemented solution]

### Impact
- Affected users: [estimate]
- Downtime: [if applicable]

### Rollback plan
[Rollback plan if needed]

## Checklist
- [ ] Fix tested in staging
- [ ] Approval for urgent deploy
- [ ] Post-deploy monitoring planned
```

---

## Refactoring (refactor/* -> develop)

**Title**: `refactor(<scope>): <description>`

```markdown
## What
Refactoring of [component/module]

## Why
- [Motivation: performance, maintainability, technical debt]

## Changes
- [Change 1]
- [Change 2]

## Impact
- **Functional**: None (behavior unchanged)
- **Performance**: [expected improvements]
- **Maintainability**: [benefits]

## Checklist
- [ ] Functional behavior unchanged
- [ ] Existing tests passing
- [ ] New tests added (if needed)
```

---

## Documentation (docs/*)

**Title**: `docs(<scope>): <description>`

```markdown
## What
Documentation update for [area]

## Changes
- [Document 1]: [change type]
- [Document 2]: [change type]

## Motivation
[Why this documentation is needed]
```

---

## CI/CD and infrastructure

**Title**: `ci(<scope>): <description>` or `chore(<scope>): <description>`

```markdown
## What
[Pipeline/infrastructure change]

## Changes
- [Change 1]
- [Change 2]

## Impact
- Build time: [variation]
- Deploy process: [variation]

## Testing
[How it was verified]
```
