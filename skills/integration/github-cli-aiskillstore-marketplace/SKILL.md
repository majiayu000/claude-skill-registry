---
name: github-cli
description: Encourages proactive use of GitHub CLI (gh) for gathering context on PRs, issues, comments, and repository information when working with GitHub-related tasks.
---

# GitHub CLI Context Gathering

This skill encourages proactive use of the GitHub CLI (`gh`) to gather rich context when working with GitHub-related tasks.

## Core Philosophy

When the user mentions **PRs, issues, branches, code reviews, comments, or anything GitHub-related**, proactively use `gh` commands to gather context rather than relying solely on local git commands.

**Local git** tells you about commits and branches.
**GitHub CLI** tells you about the *conversation* around those changes — PR descriptions, review comments, issue discussions, CI status, and more.

## When to Use gh Proactively

Use `gh` commands when the user mentions or asks about:

- **PRs / Pull Requests** — view, diff, comments, reviews, checks
- **Issues** — view, comments, labels, assignees
- **Code reviews** — review comments, requested changes
- **CI/CD status** — check runs, workflow status
- **Repository information** — branches, releases, collaborators
- **GitHub links** — any `github.com` URL can be inspected via `gh`

## Key Commands Reference

### Pull Requests

```bash
# View PR details (description, status, checks)
gh pr view PR_NUMBER

# View PR diff
gh pr diff PR_NUMBER

# List PR comments
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments

# List review comments (inline code comments)
gh api repos/OWNER/REPO/pulls/PR_NUMBER/reviews

# Check PR status and CI checks
gh pr checks PR_NUMBER

# List open PRs
gh pr list

# List PRs by author
gh pr list --author USERNAME
```

### Issues

```bash
# View issue details
gh issue view ISSUE_NUMBER

# List issue comments
gh api repos/OWNER/REPO/issues/ISSUE_NUMBER/comments

# List open issues
gh issue list

# Search issues
gh issue list --search "QUERY"
```

### Repository Information

```bash
# View repo details
gh repo view

# List branches
gh api repos/OWNER/REPO/branches

# View recent releases
gh release list

# View workflow runs
gh run list
```

### Working with GitHub URLs

When given a GitHub URL, extract the relevant information and use `gh`:

```bash
# From: https://github.com/monzo/analytics/pull/123
gh pr view 123 --repo monzo/analytics

# From: https://github.com/monzo/analytics/issues/456
gh issue view 456 --repo monzo/analytics
```

## Context Gathering Patterns

### Before Reviewing a PR

```bash
# Get the full picture
gh pr view PR_NUMBER           # Description and status
gh pr diff PR_NUMBER           # What changed
gh pr checks PR_NUMBER         # CI status
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments  # Discussion
```

### Investigating an Issue

```bash
gh issue view ISSUE_NUMBER     # Issue details
gh api repos/OWNER/REPO/issues/ISSUE_NUMBER/comments  # Discussion
```

### Understanding Branch Context

```bash
# What PRs exist for this branch?
gh pr list --head BRANCH_NAME

# What's the status of my PR?
gh pr status
```

## Integration with Git Commands

Combine `gh` with local git for full context:

```bash
# Local: What commits are on this branch?
git log origin/master..HEAD --oneline

# GitHub: What's the PR discussion saying?
gh pr view --comments
```

## Tips

1. **Use `--json` for structured output** when you need to parse data:
   ```bash
   gh pr view PR_NUMBER --json title,body,reviews,comments
   ```

2. **Use `gh api` for anything not covered by high-level commands** — it gives direct access to the GitHub API

3. **Specify `--repo OWNER/REPO`** when working outside the repo directory or when ambiguous

4. **Default to gathering context first** — read the PR description and comments before diving into code

## When to Invoke This Skill

This skill should guide behaviour whenever GitHub-related context would be valuable. You don't need to explicitly invoke it — just remember to reach for `gh` when the user mentions:

- PRs, pull requests, merge requests
- Issues, tickets, bugs
- Code reviews, review comments
- CI checks, pipelines, workflows
- Branches in the context of collaboration
- Any GitHub URL
