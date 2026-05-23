---
name: git-commit-conventional
description: Generate conventional commit messages with strict formatting rules
version: 1.1.0
tags: [git, conventional-commits, standard]
owner: engineering
status: active
---

# Git Commit Conventional Skill

## Overview

Generate conventional commit messages for staged changes.

## Usage

```
/git-commit-conventional
```

## Identity
**Role**: Commit Message Author
**Objective**: Generate a commit message for the *currently staged* changes that strictly follows the Conventional Commits specification.

## Rules & Standards

### Format
```text
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Allowed Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- `ci`: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
- `chore`: Other changes that don't modify src or test files

### Scope Determination
- **Dynamic**: The scope should be the directory name or component name affected (e.g., `auth`, `ui`, `api`).
- **Specific**: Avoid broad scopes like `global` or `app` unless truly global.

### Subject Rules
- Use strict **imperative mood** ("add" not "added", "fix" not "fixed").
- Max 50 characters.
- No period at the end.
- Lowercase first letter.

## Workflow
1.  **Read Staged Diff**: `git diff --cached`.
2.  **Analyze Intent**: What does this change achieve?
3.  **Draft Message**: Apply the formatting rules.
4.  **Review**: Check against constraints (max length, imperative mood).

## Examples
- **Good**: `feat(auth): implement jwt signing`
- **Bad**: `Fixed login bug.` (Not conventional, past tense, period)
- **Bad**: `feat(User): Added user.` (Capitalized scope/subject, past tense)

## Error Handling
- If the diff includes multiple unrelated changes, suggest splitting the commit (ref: `git-committer-atomic`).
- If no files are staged, abort and ask user to stage files.

## Outputs

- Conventional commit message aligned to staged changes.

## Related Skills

- `/git-committer-atomic` - Plan atomic commits
