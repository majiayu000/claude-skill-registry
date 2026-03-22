---
name: gh
description: "Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management. Trigger for requests to use gh, manage GitHub repos, PRs, or issues from the CLI."
---

# GitHub CLI (gh)

## Overview
Use `gh` for authenticated GitHub operations from the terminal. Prefer explicit, idempotent commands and report URLs back to the user.

## Quick checks
- Auth status:
```bash
gh auth status
```
- Current repo context:
```bash
gh repo view --json nameWithOwner,url,defaultBranchRef
```

## Core workflows

### Repo create (private by default)
```bash
gh repo create OWNER/NAME --private --confirm --description "..."
```
If running inside a local repo, use `--source . --remote origin --push`.

### Clone / fork
```bash
gh repo clone OWNER/NAME
```
```bash
gh repo fork OWNER/NAME --clone
```

### Issues
- List:
```bash
gh issue list --limit 20
```
- Create:
```bash
gh issue create --title "..." --body "..."
```
- Comment:
```bash
gh issue comment <num> --body "..."
```

### Pull requests
- Create from current branch:
```bash
gh pr create --title "..." --body "..."
```
- List:
```bash
gh pr list --limit 20
```
- View:
```bash
gh pr view <num> --web
```
- Merge (use explicit method):
```bash
gh pr merge <num> --merge
```

### Releases
```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "..."
```

## Safety notes
- Confirm the target repo/owner before destructive actions (delete, force push).
- For private repos, ensure `--private` is set on create.
- Prefer `--confirm` to avoid interactive prompts in automation.
