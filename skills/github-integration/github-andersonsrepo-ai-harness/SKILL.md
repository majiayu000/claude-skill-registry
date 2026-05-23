---
name: github
description: Manage GitHub repos, PRs, issues, and code review.
user-invocable: true
argument-hint: "<pr|issue|repo> [subcommand] [args]"
context: fork
agent: ops
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# GitHub Integration

Current status:
!command gh pr list --limit 5 2>/dev/null && echo "---" && gh issue list --limit 5 2>/dev/null

## Commands

### `pr list` — List open pull requests
```bash
gh pr list --limit 10
```

### `pr view <number>` — View PR details
```bash
gh pr view <number>
```

### `pr create` — Create a new pull request
Walk the user through creating a PR:
1. Show current branch and recent commits with `gh pr create --web` or interactive
2. Ask for title and description
3. Run `gh pr create --title "..." --body "..."`

### `pr merge <number>` — Merge a pull request
**REQUIRES USER CONFIRMATION before executing.**
```bash
gh pr merge <number> --merge
```

### `issue list` — List open issues
```bash
gh issue list --limit 10
```

### `issue create` — Create a new issue
Ask user for title and body, then:
```bash
gh issue create --title "..." --body "..."
```

### `issue close <number>` — Close an issue
```bash
gh issue close <number>
```

### `issue comment <number>` — Comment on an issue
```bash
gh issue comment <number> --body "..."
```

### `repo` — View current repo info
```bash
gh repo view
```

## Notes

- All operations use the `gh` CLI (already authenticated via `gh auth`)
- The GitHub MCP server is also available for programmatic repo access
- Merge and close operations always require explicit user confirmation
