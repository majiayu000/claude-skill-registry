---
name: GitHub
description: Wrapper scripts for GitHub CLI (gh) commands to access issues, PRs, and authentication status. Supports cross-repository operations. Use when direct gh commands are blocked.
allowed-tools:
  - Bash
  - Read
---

# GitHub

This skill provides wrapper scripts for GitHub operations. Scripts automatically use curl with GITHUB_TOKEN when available, falling back to gh CLI otherwise. All issue commands support `-R owner/repo` for cross-repository operations.

## Available Scripts

### Authentication

```bash
bash .claude/skills/github/scripts/gh-auth.sh" status
```

### Issues

```bash
# List issues
bash .claude/skills/github/scripts/gh-issue.sh" list
bash .claude/skills/github/scripts/gh-issue.sh" list --state all -L 10

# View issue
bash .claude/skills/github/scripts/gh-issue.sh" view 123

# Create issue
bash .claude/skills/github/scripts/gh-issue.sh" create --title "Bug report" --body "Description"

# Add comment
bash .claude/skills/github/scripts/gh-issue.sh" comment 123 --body "My comment"

# Close issue
bash .claude/skills/github/scripts/gh-issue.sh" close 123

# Assign to yourself
bash .claude/skills/github/scripts/gh-issue.sh" assign 123
```

### Cross-Repository Issue Operations

Use `-R` or `--repo` to target a different repository:

```bash
# List issues in another repo
bash .claude/skills/github/scripts/gh-issue.sh" -R owner/repo list

# View issue in another repo
bash .claude/skills/github/scripts/gh-issue.sh" -R owner/repo view 123

# Create issue in another repo
bash .claude/skills/github/scripts/gh-issue.sh" -R owner/repo create --title "Bug report" --body "Description"

# Add comment to issue in another repo
bash .claude/skills/github/scripts/gh-issue.sh" -R owner/repo comment 123 --body "My comment"

# Close issue in another repo
bash .claude/skills/github/scripts/gh-issue.sh" -R owner/repo close 123
```

### Pull Requests

```bash
# List PRs
bash .claude/skills/github/scripts/gh-pr.sh" list
bash .claude/skills/github/scripts/gh-pr.sh" list --state all -L 10

# View PR
bash .claude/skills/github/scripts/gh-pr.sh" view 123

# Create PR
bash .claude/skills/github/scripts/gh-pr.sh" create --title "My PR" --body "Description" --base main
```

## Authentication Methods

1. **GITHUB_TOKEN** (preferred for remote): Set in `.env` file, scripts use curl with GitHub API
2. **gh CLI** (fallback): Uses gh's own authentication when token not available

The session-start hook automatically configures GITHUB_TOKEN in `.env` for remote environments.
