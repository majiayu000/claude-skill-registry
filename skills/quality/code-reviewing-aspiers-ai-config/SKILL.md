---
name: code-reviewing
description: Review code for quality, security, and maintainability. Use after code changes are completed and ready for review.
---

# Code Review

Review code for quality, security, and maintainability.

## When to Use This Skill

Use this skill:
- After code changes are completed and ready for review
- Before staging changes for commit
- As a proactive quality check during development

## Context

When invoked, examine:

- Current git status: `git status`
- Current git diff (staged and unstaged changes): `git diff --no-ext-diff HEAD`
- Current branch: `git branch --show-current`
- Recent commits: `git log --oneline -40`

## Review Checklist

Examine all modified files and check:

- **NO DUPLICATED CODE!** - Extract common logic into reusable functions
- **Functions 30 lines or shorter** - Break down complex functions
- **Well-named functions and variables** - Clear, descriptive names
- **Simple and readable code** - Avoid unnecessary complexity
- **Proper error handling** - Handle edge cases and failures gracefully
- **No exposed secrets or API keys** - Use environment variables or config
- **Input validation implemented** - Validate all external inputs
- **Good test coverage** - Tests for critical paths
- **Performance considerations** - No obvious O(n²) or worse patterns

## Feedback Organization

Provide feedback organized by priority:

1. **Critical issues (MUST FIX)**: Security vulnerabilities, bugs, broken functionality
2. **Warnings (SHOULD FIX)**: Code quality, maintainability concerns
3. **Suggestions (CONSIDER)**: Improvements that would be nice to have

For each issue, include:
- Specific location (file, line number)
- Description of the problem
- Example of how to fix it

## Output

Provide a structured review:

```
## Critical Issues

- [File:line] Description of issue
  - How to fix: ...

## Warnings

- [File:line] Description of concern
  - Suggestion: ...

## Suggestions

- [File:line] Nice-to-have improvement
```

If no issues found: "Code review passed. No issues identified."
