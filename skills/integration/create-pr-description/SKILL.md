---
name: create-pr-description
description: Generate a structured PR description from staged git changes when the user asks to create, write, or draft a pull request description
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[optional: PR title or linked issue number]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: git, pr, documentation
---

# Create PR Description

## Overview

Generate a comprehensive, reviewer-friendly pull request description by analyzing staged git changes, commit history, and project conventions. The output is a ready-to-paste PR body that explains the "why" behind every change.

## Workflow

1. **Read project context** — Check for `.chalk/docs/engineering/` files, especially PR conventions, coding style, and architecture docs. If a conventions file exists, follow its PR template. If not, use the default structure below.

2. **Gather git context** — Run these commands to understand the change:
   - `git diff --cached --stat` for an overview of changed files
   - `git diff --cached` for the full staged diff
   - `git log --oneline -10` for recent commit context
   - `git branch --show-current` for the branch name
   - If `$ARGUMENTS` contains an issue number, read the issue details if accessible

3. **Analyze the diff** — Before writing anything, categorize the changes:
   - Identify the primary intent (feature, bugfix, refactor, chore, docs)
   - Group file changes by concern (e.g., "API changes", "UI updates", "test additions", "config changes")
   - Note any files that are deleted, renamed, or have significant permission changes
   - Flag potential risks: new dependencies, migration files, API contract changes, security-sensitive files

4. **Determine change type and scope** — This shapes the description tone:
   - **Feature**: Emphasize user-facing behavior and motivation
   - **Bugfix**: Describe the bug, root cause, and fix approach
   - **Refactor**: Explain what stays the same (behavior) and what changes (structure)
   - **Chore/Config**: Keep it brief, focus on why now

5. **Write the PR description** — Use the structure defined in the Output section. Every section must add value; omit sections that genuinely do not apply rather than filling them with "N/A".

6. **Output the description** — Print the full PR description in a markdown code block so the user can copy it. If the user has a PR already open, suggest the `gh pr edit` command to update it.

## Output

```markdown
## Summary

<!-- 1-2 sentences. What does this PR do and why? -->

## Motivation

<!-- Why is this change needed? Link to the problem, user feedback, or product requirement. -->
<!-- If fixing a bug: what was the broken behavior? What triggers it? -->

## Changes

<!-- Group changes by concern. Use sub-headers for large PRs. -->

### <Concern 1, e.g., "API Layer">
- Change description with enough context to understand without reading the diff

### <Concern 2, e.g., "Database">
- Change description

## Testing

<!-- What was tested? How can a reviewer verify? -->
- [ ] Unit tests added/updated
- [ ] Manual testing performed (describe steps)
- [ ] Edge cases considered: <list them>

## Screenshots

<!-- For UI changes only. Remove this section if no UI changes. -->
<!-- Before/after screenshots or screen recordings -->

## Reviewer Notes

<!-- Where should the reviewer start reading? -->
<!-- What's the trickiest part of this change? -->
<!-- Any concerns or tradeoffs you want a second opinion on? -->

## Related Issues

<!-- Use closing keywords: Fixes #123, Closes #456, Resolves #789 -->
<!-- Or just references: Related to #123, Part of #456 -->

---

### Checklist

- [ ] Tests pass locally (`npm test` / `pytest` / equivalent)
- [ ] No new console errors or warnings
- [ ] Accessibility checked (if UI changes)
- [ ] Documentation updated (if behavior changes)
- [ ] Migration tested (if schema changes)
- [ ] Feature flag configured (if gradual rollout)
```

## Adapting to Change Type

### Feature PRs
- Motivation section is mandatory and should reference the user problem
- Testing section must include manual verification steps
- Screenshots section is required for any UI changes

### Bugfix PRs
- Summary must state the bug clearly: "Users experienced X when doing Y"
- Motivation must include root cause analysis
- Testing must describe how to reproduce the original bug and verify the fix
- Add "Regression risk" note in Reviewer Notes

### Refactor PRs
- Summary must explicitly state "No behavior change"
- Changes section should show before/after patterns
- Testing should explain how behavior preservation was verified

### Dependency Updates
- List all updated packages with version ranges
- Note any breaking changes from changelogs
- Flag transitive dependency changes

## Writing Quality Rules

- **Summary**: Lead with the user-visible or system-visible impact. Not "Updated the handler" but "Fix timeout errors when uploading files larger than 50MB."
- **Changes**: Each bullet should answer "what changed and why" not just "what file changed." Bad: "Modified `auth.ts`". Good: "Added token refresh retry logic to handle intermittent auth failures."
- **Testing**: Specific and reproducible. Bad: "Tested locally." Good: "Created a 100MB file upload, verified no timeout after 60s. Tested with expired token, confirmed retry succeeds."
- **Reviewer Notes**: Be honest about complexity. If something is hacky, say so and explain why. Reviewers trust authors who flag their own concerns.

## Anti-patterns

- **Empty PR descriptions** — Every PR must explain "why." Even a one-line fix has a reason.
- **Diff-as-description** — Do not just restate what the diff shows. The reviewer can read the diff. Explain intent, tradeoffs, and context that is not in the code.
- **All "what" no "why"** — "Added error handling to processPayment" is useless. "Added error handling to processPayment because silent failures were causing orphaned transactions" is useful.
- **No test evidence** — If you say "tested locally," describe what you tested. Unnamed testing is the same as no testing.
- **Missing issue links** — If this PR addresses an issue, link it with closing keywords. Do not make reviewers search for the connection.
- **Wall of text** — Use structure. A 500-word paragraph is harder to review than 10 bullets grouped by concern.
- **Burying breaking changes** — API contract changes, migration requirements, and config changes must be called out prominently, not hidden in a bullet list.
- **Omitting rollback context** — For risky changes, explain how to revert if something goes wrong.
