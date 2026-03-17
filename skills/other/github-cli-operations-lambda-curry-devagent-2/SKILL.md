---
name: GitHub CLI Operations
description: >-
  Use GitHub CLI (gh) to interact with GitHub repositories, pull requests,
  issues, and workflows. Use when: (1) Reading PR details, diffs, or metadata,
  (2) Listing or filtering PRs and issues, (3) Creating PR comments or linking to
  issues, (4) Checking CI status or mergeability, (5) Extracting issue references
  from PR descriptions, or (6) Any GitHub repository operation via command line.
  Requires GitHub CLI installed and authenticated.
---

# GitHub CLI Operations

Use GitHub CLI (`gh`) to interact with GitHub repositories, pull requests, issues, and workflows.

## Prerequisites

- GitHub CLI installed: `brew install gh` (macOS) or see [cli.github.com](https://cli.github.com)
- Authenticated: `gh auth login` (one-time setup)
- Repository context: Run commands from within a git repository or specify `--repo owner/repo`

## Quick Start

**Get PR details:**
```bash
gh pr view <pr-number> --json title,body,author,state
```

**Get PR diff:**
```bash
gh pr diff <pr-number>
```

**Extract Linear issue references:**
```bash
gh pr view <pr-number> --json body --jq '.body' | grep -oE 'LIN-[0-9]+'
```

## Usage Patterns for PR Review

### Get PR Context

Get PR title, description, and metadata:
```bash
gh pr view <pr-number> --json title,body,author,state,baseRefName,headRefName
```

Get changed files:
```bash
gh pr view <pr-number> --json files --jq '.files[].path'
```

Get diff for specific file:
```bash
gh pr diff <pr-number> -- path/to/file
```

### Check PR Status

Check CI status:
```bash
gh pr checks <pr-number>
```

Check if PR is mergeable:
```bash
gh pr view <pr-number> --json mergeable,mergeStateStatus
```

### Link to Linear Issues

Extract issue references from PR body:
```bash
gh pr view <pr-number> --json body --jq '.body' | grep -oE 'LIN-[0-9]+'
```

## Integration with Linear

When reviewing PRs, extract Linear issue references from:
- PR title: Look for `LIN-123` or `[LIN-123]` patterns
- PR body: Search for Linear issue links or IDs
- PR comments: Check for issue mentions

Then use Linear MCP functions to fetch issue details and requirements.

## Reference Documentation

- **Command Reference**: See [commands.md](references/commands.md) for complete GitHub CLI command reference
- **GitHub CLI Manual**: [cli.github.com/manual](https://cli.github.com/manual)
