---
name: ac-commit-manager
description: Manage git commits for autonomous coding. Use when committing feature implementations, creating descriptive commits, managing git workflow, or handling version control.
---

# AC Commit Manager

Manage git commits for completed feature implementations.

## Purpose

Creates well-structured git commits after each feature completion, ensuring proper version control and clear project history.

## Quick Start

```python
from scripts.commit_manager import CommitManager

manager = CommitManager(project_dir)
result = await manager.commit_feature("auth-001")
```

## Commit Workflow

```
1. VALIDATE → Ensure changes are safe to commit
2. STAGE    → Stage relevant files
3. MESSAGE  → Generate descriptive commit message
4. COMMIT   → Create the commit
5. VERIFY   → Verify commit was created
6. TAG      → Optional: tag milestone commits
```

## Commit Message Format

```
feat(auth): implement user registration (#auth-001)

- Add registration endpoint with email/password
- Implement password hashing with bcrypt
- Add input validation for email format
- Create user model and database migration

Test: All 5 acceptance criteria passing
Coverage: 92%

Feature: auth-001
Status: passes
```

## Commit Result

```json
{
  "success": true,
  "commit_hash": "abc123def456",
  "feature_id": "auth-001",
  "message": "feat(auth): implement user registration",
  "files_changed": [
    "src/auth/register.py",
    "src/models/user.py",
    "tests/test_auth_001.py"
  ],
  "stats": {
    "insertions": 145,
    "deletions": 12,
    "files_changed": 3
  }
}
```

## Commit Categories

Based on feature category:
- `feat`: New features
- `fix`: Bug fixes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `docs`: Documentation
- `chore`: Maintenance tasks
- `perf`: Performance improvements

## Pre-Commit Checks

```python
# Run validation before commit
validation = await manager.pre_commit_check()
if validation.can_commit:
    await manager.commit_feature(feature_id)
```

Checks include:
- No uncommitted sensitive files
- All tests pass
- Linting passes
- No merge conflicts

## Atomic Commits

Each feature gets exactly one commit:
- Includes implementation + tests
- Self-contained and revertable
- Descriptive message with context

## Configuration

```json
{
  "require_tests_pass": true,
  "require_lint_pass": true,
  "auto_stage_tests": true,
  "message_template": "{{type}}({{scope}}): {{description}}",
  "protected_files": [".env", "credentials.*"],
  "sign_commits": false
}
```

## Rollback Support

```python
# Rollback last commit
await manager.rollback_last_commit()

# Rollback to specific feature
await manager.rollback_to_feature("auth-003")
```

## Integration

- Uses: `ac-code-validator` for pre-commit checks
- Input: Completed features from `ac-task-executor`
- Updates: `ac-state-tracker` with commit info

## API Reference

See `scripts/commit_manager.py` for full implementation.
