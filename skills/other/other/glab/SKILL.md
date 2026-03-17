---
name: glab
description: Expert guidance for using the GitLab CLI (glab) to manage GitLab issues, merge requests, CI/CD pipelines, repositories, and other GitLab operations from the command line. Use this skill when the user needs to interact with GitLab resources or perform GitLab workflows.
license: MIT
compatibility: opencode
---

# GitLab CLI (glab) Skill

Provides guidance for using `glab`, the official GitLab CLI, to perform GitLab operations from the terminal.

## When to Use This Skill

Invoke when the user needs to:

- Create, review, or manage merge requests
- Work with GitLab issues
- Monitor or trigger CI/CD pipelines
- Clone or manage repositories
- Perform any GitLab operation from the command line

## Prerequisites

Verify glab installation before executing commands:

```bash
glab --version
```

If not installed, inform the user and provide platform-specific installation guidance.

## Authentication Quick Start

Most glab operations require authentication:

```bash
# Interactive authentication
glab auth login

# Check authentication status
glab auth status

# For self-hosted GitLab
glab auth login --hostname gitlab.example.org

# Using environment variables
export GITLAB_TOKEN=your-token
export GITLAB_HOST=gitlab.example.org  # for self-hosted
```

## Core Workflows

### Creating a Merge Request

```bash
# 1. Ensure branch is pushed
git push -u origin feature-branch

# 2. Create MR
glab mr create --title "Add feature" --description "Implements X"

# With reviewers and labels
glab mr create --title "Fix bug" --reviewer=alice,bob --label="bug,urgent"
```

### Reviewing Merge Requests

```bash
# 1. List MRs awaiting your review
glab mr list --reviewer=@me

# 2. Checkout MR locally to test
glab mr checkout <mr-number>

# 3. After testing, approve
glab mr approve <mr-number>

# 4. Add review comments
glab mr note <mr-number> -m "Please update tests"
```

### Managing Issues

```bash
# Create issue with labels
glab issue create --title "Bug in login" --label=bug

# Link MR to issue
glab mr create --title "Fix login" --description "Closes #<issue-number>"

# List your assigned issues
glab issue list --assignee=@me
```

### Monitoring CI/CD

```bash
# Watch pipeline in progress
glab pipeline ci view

# Check pipeline status
glab ci status

# View logs if failed
glab ci trace

# Retry failed pipeline
glab ci retry

# Lint CI config before pushing
glab ci lint
```

## Common Patterns

### Working Outside Repository Context

When not in a Git repository, specify the repository:

```bash
glab mr list -R owner/repo
glab issue list -R owner/repo
```

### Self-Hosted GitLab

Set hostname for all commands:

```bash
export GITLAB_HOST=gitlab.example.org
# or per-command
glab repo clone gitlab.example.org/owner/repo
```

### Automation and Scripting

Use JSON output for parsing:

```bash
glab mr list --output=json | jq '.[] | .title'
```

### Using the API Command

The `glab api` command provides direct GitLab API access:

```bash
# Basic API call
glab api projects/:id/merge_requests

# IMPORTANT: Pagination uses query parameters in URL, NOT flags
# ❌ WRONG: glab api --per-page=100 projects/:id/jobs
# ✓ CORRECT: glab api "projects/:id/jobs?per_page=100"

# Auto-fetch all pages
glab api --paginate "projects/:id/pipelines/123/jobs?per_page=100"

# POST with data
glab api --method POST projects/:id/issues --field title="Bug" --field description="Details"
```

## Best Practices

1. **Verify authentication** before executing commands: `glab auth status`
2. **Use `--help`** to explore command options: `glab <command> --help`
3. **Link MRs to issues** using "Closes #123" in MR description
4. **Lint CI config** before pushing: `glab ci lint`
5. **Check repository context** when commands fail: `git remote -v`

## Common Commands Quick Reference

**Merge Requests:**

- `glab mr list --assignee=@me` - Your assigned MRs
- `glab mr list --reviewer=@me` - MRs for you to review
- `glab mr create` - Create new MR
- `glab mr checkout <number>` - Test MR locally
- `glab mr approve <number>` - Approve MR
- `glab mr merge <number>` - Merge approved MR

**Issues:**

- `glab issue list` - List all issues
- `glab issue create` - Create new issue
- `glab issue close <number>` - Close issue

**CI/CD:**

- `glab pipeline ci view` - Watch pipeline
- `glab ci status` - Check status
- `glab ci lint` - Validate .gitlab-ci.yml
- `glab ci retry` - Retry failed pipeline

**Repository:**

- `glab repo clone owner/repo` - Clone repository
- `glab repo view` - View repo details
- `glab repo fork` - Fork repository

## Progressive Disclosure

For detailed command documentation, refer to:

- **references/commands-detailed.md** - Comprehensive command reference with all flags and options
- **references/quick-reference.md** - Condensed command cheat sheet
- **references/troubleshooting.md** - Detailed error scenarios and solutions

Load these references when:

- User needs specific flag or option details
- Troubleshooting authentication or connection issues
- Working with advanced features (API, schedules, variables, etc.)

## Common Issues Quick Fixes

**"command not found: glab"** - Install glab or verify PATH

**"401 Unauthorized"** - Run `glab auth login`

**"404 Project Not Found"** - Verify repository name and access permissions

**"not a git repository"** - Navigate to repo or use `-R owner/repo` flag

**"source branch already has a merge request"** - Use `glab mr list` to find existing MR

For detailed troubleshooting, load **references/troubleshooting.md**.

## Notes

- glab auto-detects repository context from Git remote
- Most commands have `--web` flag to open in browser
- Use `--output=json` for scripting and automation
- Multiple GitLab accounts can be authenticated simultaneously
- Commands respect Git configuration and current repository context
