---
name: review-pr
description: Review pull requests. Use when user asks to "review a PR", "/review-pr", or wants to review a pull request.
---

# Review Pull Request

## Context

Run in parallel:
- `gh pr view` - get PR details
- `gh pr diff` - get full diff

## Workflow

1. Get PR details and diff
2. Read changed files with surrounding context
3. Review for: logic errors, patterns, readability, missing tests
4. Provide feedback with file:line references

## Rules

- Review ALL changed files, not just the latest commit
- Use `gh` CLI for all GitHub operations
- Be specific: file:line + issue + suggested fix
- Separate critical issues from suggestions
