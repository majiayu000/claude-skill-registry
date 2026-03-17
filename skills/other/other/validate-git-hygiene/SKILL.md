---
name: validate-git-hygiene
description: Validate git commit messages, branch naming conventions, and repository hygiene. Returns structured output with validation results for commit format (conventional commits), branch naming, and best practices. Used for quality gates and git workflow validation.
---

# Validate Git Hygiene

Validates git repository hygiene including commit messages, branch names, and best practices.

## Usage

This skill validates git practices and returns structured results.

## Checks Performed

1. **Commit Message Format**
   - Conventional Commits format: `type(scope): description`
   - Valid types: feat, fix, docs, style, refactor, test, chore
   - Character limits (72 chars for title)

2. **Branch Naming**
   - Pattern validation (feat/*, fix/*, chore/*, etc.)
   - No invalid characters
   - Descriptive naming

3. **Repository Hygiene**
   - No uncommitted changes in working directory
   - No untracked sensitive files (.env, credentials)
   - Branch up to date with remote

## Output Format

### Success (All Checks Pass)

```json
{
  "status": "success",
  "git": {
    "commits": {
      "valid": 5,
      "invalid": 0,
      "issues": []
    },
    "branch": {
      "name": "feat/add-character-system",
      "valid": true,
      "pattern": "feat/*"
    },
    "hygiene": {
      "workingDirectory": "clean",
      "untrackedSensitive": []
    }
  },
  "canProceed": true
}
```

### Issues Found

```json
{
  "status": "warning",
  "git": {
    "commits": {
      "valid": 3,
      "invalid": 2,
      "issues": [
        {
          "commit": "abc123",
          "message": "fixed bug",
          "problem": "Missing type prefix (feat/fix/etc)"
        }
      ]
    },
    "branch": {
      "name": "my-feature",
      "valid": false,
      "pattern": null,
      "problem": "Should follow pattern: feat/fix/chore/etc"
    },
    "hygiene": {
      "workingDirectory": "dirty",
      "untrackedSensitive": [".env.local"]
    }
  },
  "canProceed": false,
  "details": "2 commit message issues and 1 sensitive file found"
}
```

## When to Use

- Pre-commit validation
- Branch creation workflows
- Conductor Phase 2/4 (Implementation/PR creation)
- Git workflow enforcement
- Code review preparation

## Requirements

- Git repository initialized
- Git command-line tools available
- Commits exist on current branch (for commit validation)
