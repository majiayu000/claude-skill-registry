---
name: review
description: |
  Code review for quality, security, and best practices. Use when:
  - User asks to "review", "check", "look at" code
  - Before merging, committing, or shipping
  - User mentions PR, pull request, changes, diff
  - User wants feedback on implementation
  - After implementing a feature (self-review)
context: fork
agent: reviewer
---

# Code Review

Reviews against the full Darkroom quality checklist defined in the reviewer agent.

Focus areas: TypeScript strictness, React patterns, accessibility, performance, security, file structure.

## Get Changes

```bash
# Unstaged changes
git diff

# Staged changes
git diff --staged

# Specific file
git diff path/to/file
```

## Output Format

```
## Summary
[1-2 sentence overview]

## Critical Issues
- [Must fix before merge]

## Warnings
- [Should fix, but not blocking]

## Suggestions
- [Nice to have improvements]

## Verdict
[APPROVED / NEEDS CHANGES / BLOCKED]
```

## Remember

- Be constructive, not just critical
- Explain WHY something is an issue
- Suggest specific fixes
- If you find a pattern worth remembering, store it as a learning
