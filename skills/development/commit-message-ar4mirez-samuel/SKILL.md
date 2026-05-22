---
name: commit-message
description: |
  Generate descriptive commit messages by analyzing git diffs. Use when the user
  asks for help writing commit messages, reviewing staged changes, or wants to
  commit with a well-formatted message following conventional commits format.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Commit Message Generator

## Purpose

Generate well-formatted commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## When to Use

- User asks "help me write a commit message"
- User says "commit this" or "commit my changes"
- User wants to review staged changes before committing
- User asks for commit message suggestions
- User mentions "conventional commit" or asks about commit format

## Instructions

1. **Check staged changes**:
   ```bash
   git diff --staged
   ```

2. **If no staged changes**, check unstaged:
   ```bash
   git diff
   ```

3. **Analyze the changes** and identify:
   - **Type**: feat, fix, docs, refactor, test, chore, perf, ci, style, build
   - **Scope**: Affected area/module (optional but recommended)
   - **Description**: What changed and why

4. **Generate commit message** in format:
   ```
   type(scope): brief description

   Optional body with more details.
   - Bullet points for multiple changes
   - Explain the "why" not just "what"

   Optional footer for breaking changes or issue refs.
   ```

## Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes nor adds feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies, configs |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
| `style` | Formatting, whitespace (no code change) |
| `build` | Build system or external dependencies |

## Examples

### Example 1: Feature Addition

**Changes**: Added new user authentication endpoint

**Output**:
```
feat(auth): add user authentication endpoint

- Implement JWT-based authentication
- Add login and logout endpoints
- Include token refresh mechanism

Closes #123
```

### Example 2: Bug Fix

**Changes**: Fixed date display issue in reports

**Output**:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation.
Previous implementation used local time, causing incorrect
dates for users in different timezones.
```

### Example 3: Refactoring

**Changes**: Extracted duplicate validation logic

**Output**:
```
refactor(validation): extract common validation utilities

- Move email validation to shared utils
- Create reusable phone number validator
- Reduce code duplication across forms
```

### Example 4: Breaking Change

**Changes**: Changed API response format

**Output**:
```
feat(api)!: change response format to JSON:API spec

BREAKING CHANGE: API responses now follow JSON:API specification.
Clients need to update their response parsing logic.

Migration guide: docs/migration-v2.md
```

## Guidelines

- **First line**: Under 72 characters
- **Use imperative mood**: "add" not "added", "fix" not "fixed"
- **Scope is optional** but helps with changelogs
- **Body**: Explain "why" for non-obvious changes
- **Footer**: Reference issues, note breaking changes
- **Separate concerns**: One logical change per commit

## Co-Author Attribution

When AI assists with commits, include attribution:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```
