---
name: git-commits
description: Git commit workflow and message format. Use when making commits, asking about commit conventions, or after completing code changes. Enforces atomic commits with structured messages (type/scope/summary + what/why body).
---

# Git Commits

## WORKFLOW

1. Run command to see all modified files `git status --porcelain`
2. Run brief diff command to understand changes `git diff`
3. Commit ALL (skip staging) using commit format below
4. Push changes
5. Then stop

## Format
```
<type>(<scope>): <summary>
<body with what changed and why>
```
- Title (first line): Required - follows `<type>(<scope>): <summary>` format
- Body (after blank line): REQUIRED - for each changed file, add a parent bullet with the file path, then nested bullets for what changed and why.

## Example
```
  <type>(<scope>): <summary>

  src/components/button.js
    - What: Added Button with size props.
    - Why: Enable dynamic size adjustments for a customizable UI.

  tests/button.test.js
    - What: Created tests for Button sizing.
    - Why: Ensure reliable rendering and detect regressions.
```

## SCOPE

Specifies area of change:
- auth, user, dashboard, api, database, ui, transfer, etc.

## ANTI-PATTERNS

- NEVER skip the body - it documents intent
