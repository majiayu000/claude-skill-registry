---
name: ship
description: Stage all changes, commit, and push. Use when user asks to "ship", "commit and push", "add all and push", or requests staging all changes, committing, and pushing.
---

# Ship Changes

## Context

Run in parallel:
- `git status` (never -uall)
- `git diff HEAD`
- `git log --oneline -10`

## Workflow

1. Review all changes from status and diff
2. Analyze recent commit style from log
3. Check for quality check commands:
   - If `package.json` exists, check for `lint` and `test` scripts
   - Run available checks in parallel: `npm run lint`, `npm test`
   - If no package.json, skip quality checks
4. If checks fail: report errors, STOP — do not commit or push
5. Generate commit message based on changed files matching repo style
6. Stage all files: `git add -A`
7. Commit with HEREDOC format
8. Push: `git push` (current branch)
9. Run `git status` after to verify

## Rules

- Stage ALL changes with `git add -A`
- Generate message from changed files, match repo style
- Only run npm commands if package.json exists with those scripts
- NEVER push if lint or tests fail
- NEVER force push (`-f` or `--force`)
- NEVER skip hooks
- NEVER commit secrets
- Push to current branch only
