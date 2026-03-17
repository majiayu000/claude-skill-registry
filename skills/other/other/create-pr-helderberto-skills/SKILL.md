---
name: create-pr
description: Create GitHub pull requests. Use when user asks to "create a pull request", "open a PR", "/create-pr", or requests creating pull requests.
---

# Pull Request

## Context

Run in parallel:
- `git status` (never -uall)
- `git diff HEAD`
- Branch tracking status
- `git diff [base-branch]...HEAD` and `git log`

## Template Locations

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/PULL_REQUEST_TEMPLATE/`
- `docs/pull_request_template.md`
- `pull_request_template.md`

## Workflow

1. Search for PR template
2. Read template if found
3. Review ALL commits (not just latest)
4. Draft title (<70 chars) and body:
   - Use template structure if available
   - Otherwise: Summary + Test plan
5. In parallel:
   - Create branch if needed
   - Push with `-u` if needed
   - Create PR with `gh pr create` using HEREDOC

## Rules

- Use PR template if available
- Analyze ALL commits
- Return PR URL
- Use `gh` CLI
