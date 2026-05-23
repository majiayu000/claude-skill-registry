---
name: github-cli
description: Advanced GitHub CLI workflows for PR review, CI/CD debugging, Actions management, API queries, and code search. Use when the user needs to review PRs, debug failing checks, manage workflows, search across repos, or make complex gh API calls. Not needed for basic gh commands the agent already knows.
metadata:
  category: tooling
  tools: gh
---

# GitHub CLI Workflows

Advanced reference for GitHub CLI operations. Requires `gh` to be installed and authenticated.

**Documentation:** https://cli.github.com/manual/

For basic commands (create/list/view PRs, issues, repos, releases), see `references/basic-commands.md`.

## Prerequisites

If `gh` is not installed or not authenticated, instruct the user to run:

```bash
# Install: brew install gh (macOS) or see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
gh auth login
gh auth status
```

## PR Review & Inspection

```bash
# Review actions
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix..."
gh pr review 123 --comment --body "Looks good but..."

# Merge
gh pr merge 123 --squash --delete-branch

# Checks, diff, comments
gh pr checks 123
gh pr diff 123
gh api repos/{owner}/{repo}/pulls/123/comments
```

## Actions / Workflows

```bash
# List runs (optionally filter by workflow)
gh run list
gh run list --workflow build.yml

# Inspect a run
gh run view 12345
gh run view 12345 --log

# Re-run failures
gh run rerun 12345 --failed

# Watch a running workflow
gh run watch 12345
```

## API Access

```bash
# REST
gh api repos/{owner}/{repo}
gh api repos/{owner}/{repo}/issues --method POST --field title="New issue" --field body="Description"

# GraphQL
gh api graphql -f query='{ viewer { login } }'

# Pagination
gh api repos/{owner}/{repo}/pulls --paginate
```

## Search

```bash
gh search code "function_name" --repo owner/repo
gh search issues "bug" --repo owner/repo --state open
gh search prs "feature" --repo owner/repo --state open
```

## Tips

- Use `--json` flag with `--jq` for structured output: `gh pr list --json number,title --jq '.[].title'`
- Use `--web` to open any resource in your browser
- Set `GH_REPO` environment variable to avoid specifying `--repo` each time
- Use `gh alias set` to create custom shortcuts
- GitHub CLI respects `GITHUB_TOKEN` environment variable for authentication
