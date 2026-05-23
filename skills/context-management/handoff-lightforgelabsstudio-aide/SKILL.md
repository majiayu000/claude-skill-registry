---
name: handoff
description: Generate a session handoff note for context resets or multi-day work.
---

# Handoff

Produce a concise, resumable handoff note. Focus on next actions, not a status report.

## Inputs

Ask the user for: completed tasks (file:line refs), mid-flight TODOs, blockers, ordered next actions, validation status.

Auto-collect:

- `git branch --show-current` and `git log --oneline -5`
- `gh pr status` and `git status --short`

## Output format

```markdown
# Session Handoff: <task name>

**Date:** <today> | **Branch:** <branch> | **PR:** #<n> | **Issue:** #<n>

## Context
<1-2 sentence summary>
## Completed
- <specific change with file:line>
## In Progress
- <specific TODO, mid-flight>
## Blockers
- <blocker or "none">
## Next Actions
1. <first step on resume>
## Validation
Tests: passing | failing (<failures>) | Lint: passing | failing
```

## Where to post

Ask the user — post to PR comment, issue comment, or print only. Never commit.

```bash
gh pr comment <n> --body-file handoff.md
gh issue comment <n> --body-file handoff.md
```
