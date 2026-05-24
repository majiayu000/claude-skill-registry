---
name: gh-cli
description: GitHub CLI (gh) mastery for issues, PRs, releases, actions, gists, and repo management. Use when user asks to "create a PR", "list issues", "check CI status", "create a release", "view workflow runs", "create a gist", "clone a repo", "fork a repo", or any GitHub operations from the command line.
---

# GitHub CLI

Master the `gh` CLI for GitHub operations without leaving the terminal.

## Core Commands

### Pull Requests

```bash
# Create PR from current branch
gh pr create --title "Title" --body "Description"

# Create PR with template
gh pr create --fill  # Uses commit messages

# Create draft PR
gh pr create --draft

# List PRs
gh pr list
gh pr list --state all --author @me

# View/checkout PR
gh pr view 123
gh pr checkout 123

# Merge PR
gh pr merge 123 --squash --delete-branch

# Review PR
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"
```

### Issues

```bash
# Create issue
gh issue create --title "Bug" --body "Description"
gh issue create --label bug,urgent --assignee @me

# List issues
gh issue list
gh issue list --label "bug" --state open

# View/close
gh issue view 456
gh issue close 456 --comment "Fixed in #123"
```

### Releases

```bash
# Create release
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes"

# Create with auto-generated notes
gh release create v1.0.0 --generate-notes

# Upload assets
gh release create v1.0.0 ./dist/*.zip

# List releases
gh release list
```

### Actions/Workflows

```bash
# List workflow runs
gh run list

# View run details
gh run view 12345

# Watch running workflow
gh run watch

# Rerun failed jobs
gh run rerun 12345 --failed

# Trigger workflow
gh workflow run deploy.yml -f environment=production
```

### Repository

```bash
# Clone
gh repo clone owner/repo

# Create new repo
gh repo create my-repo --public --clone

# Fork
gh repo fork owner/repo --clone

# View repo
gh repo view owner/repo --web
```

### Gists

```bash
# Create gist
gh gist create file.txt --public
gh gist create file1.txt file2.txt --desc "My gist"

# List gists
gh gist list

# Edit gist
gh gist edit <gist-id>
```

## Advanced Patterns

### API Access

```bash
# GET request
gh api repos/owner/repo/issues

# POST request
gh api repos/owner/repo/issues -f title="Bug" -f body="Details"

# GraphQL
gh api graphql -f query='{ viewer { login } }'

# Pagination
gh api repos/owner/repo/issues --paginate
```

### JSON Output & jq

```bash
# Get PR as JSON
gh pr view 123 --json title,state,author

# List with specific fields
gh pr list --json number,title,author --jq '.[] | "\(.number): \(.title)"'
```

### Aliases

```bash
# Create alias
gh alias set pv 'pr view'
gh alias set co 'pr checkout'

# Use alias
gh pv 123
```

## Reference

For detailed command options: `references/commands.md`
