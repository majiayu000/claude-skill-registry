---
name: claude-review
description: Review code changes using Hyperlane monorepo coding standards. Use when reviewing PRs, checking your own changes, or doing self-review before committing.
---

# Code Review Skill

Use this skill to review code changes against Hyperlane monorepo standards.

## When to Use

- Before committing changes (self-review)
- When asked to review a PR or diff
- To check if changes follow project patterns

## Instructions

Read and apply the guidelines from `.github/prompts/code-review.md` to review the code changes.

### For PR Reviews

When reviewing a PR, deliver feedback using `/inline-pr-comments` to post inline comments on specific lines.

**Delivery format:**

1. **Inline comments** - For all issues on lines IN the diff
2. **Summary body** - For:
   - Overall assessment
   - Architecture concerns
   - Issues found OUTSIDE the diff (use "## Observations Outside This PR" section)

GitHub API limitation: Can only post inline comments on changed lines. Issues in unchanged code go in the summary body.

### For Self-Review

When reviewing your own changes before committing:

1. Run `git diff` to see changes
2. Apply the code review guidelines
3. Fix issues directly rather than commenting

Security issues should use `/claude-security-review` or `/claude-tob-review` instead.
