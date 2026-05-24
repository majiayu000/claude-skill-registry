---
name: github
description: Comprehensive GitHub operations via gh CLI. Manage repositories, issues, pull requests, Actions workflows, code security, discussions, projects, gists, notifications, and more. Use for any GitHub-related task including creating PRs, reviewing code, managing issues, monitoring CI/CD, and analyzing security alerts.
---

# GitHub Operations Skill

## Triggers

Use this skill when you see:
- github, gh, pull request, PR, issue, repository
- Actions, workflow, CI/CD, pipeline
- release, tag, milestone, project board
- code review, security alert, Dependabot
- gist, discussion, notification

## Instructions

### Authentication & Setup

```bash
# Check authentication status
gh auth status

# Login if needed
gh auth login

# Set default repository context
gh repo set-default owner/repo
```

### Pull Request Operations

```bash
# Create PR with full details
gh pr create --title "Title" --body "Description" --base main --head feature-branch

# Create PR from template
gh pr create --title "Title" --body-file .github/PULL_REQUEST_TEMPLATE.md

# List PRs
gh pr list --state open --limit 20
gh pr list --author @me --state all

# View PR details
gh pr view 123
gh pr view 123 --comments

# Review PR
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Changes needed"
gh pr review 123 --comment --body "Looks good overall"

# Merge PR
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --rebase
gh pr merge 123 --merge

# Check PR status
gh pr checks 123 --watch

# Checkout PR locally
gh pr checkout 123
```

### Issue Management

```bash
# Create issue
gh issue create --title "Bug: description" --body "Details" --label "bug,priority:high"

# List issues
gh issue list --state open --assignee @me
gh issue list --label "bug" --milestone "v1.0"

# View and update
gh issue view 456
gh issue edit 456 --add-label "in-progress"
gh issue close 456 --comment "Fixed in #123"

# Link issues to PRs
gh pr create --title "Fix #456" --body "Closes #456"
```

### Repository Management

```bash
# Clone repository
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1

# Create repository
gh repo create my-repo --public --description "Description"
gh repo create my-repo --private --template owner/template

# Fork repository
gh repo fork owner/repo --clone

# View repository info
gh repo view owner/repo
gh repo view --web
```

### GitHub Actions

```bash
# List workflows
gh workflow list

# View workflow runs
gh run list --workflow "CI"
gh run list --status failure

# View specific run
gh run view 12345
gh run view 12345 --log

# Trigger workflow
gh workflow run workflow.yml
gh workflow run workflow.yml -f input_name=value

# Cancel run
gh run cancel 12345

# Re-run failed jobs
gh run rerun 12345 --failed
```

### Releases & Tags

```bash
# Create release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"
gh release create v1.0.0 --generate-notes
gh release create v1.0.0 ./dist/* --prerelease

# List releases
gh release list

# Download release assets
gh release download v1.0.0

# Delete release
gh release delete v1.0.0 --yes
```

### Code Security

```bash
# View security alerts
gh api repos/{owner}/{repo}/code-scanning/alerts
gh api repos/{owner}/{repo}/dependabot/alerts

# View secret scanning alerts
gh api repos/{owner}/{repo}/secret-scanning/alerts
```

### API Access

```bash
# GraphQL query
gh api graphql -f query='query { viewer { login } }'

# REST API
gh api repos/{owner}/{repo}
gh api repos/{owner}/{repo}/pulls --method POST -f title="Title" -f body="Body" -f head="branch" -f base="main"

# Paginated results
gh api repos/{owner}/{repo}/issues --paginate
```

### Gists

```bash
# Create gist
gh gist create file.txt --public --desc "Description"
gh gist create file1.txt file2.txt

# List gists
gh gist list

# View gist
gh gist view gist_id
```

### Projects (v2)

```bash
# List projects
gh project list

# View project
gh project view 1

# Add issue to project
gh project item-add 1 --owner @me --url issue_url
```

## Best Practices

1. **PR Descriptions**: Always include context, testing steps, and screenshots for UI changes
2. **Issue Templates**: Use templates for consistent issue reporting
3. **Labels**: Maintain consistent labeling for filtering and automation
4. **Branch Protection**: Require reviews and passing checks before merge
5. **Commit Messages**: Reference issues in commits (e.g., "Fix #123")
6. **Draft PRs**: Use draft status for work-in-progress

## Common Workflows

### Feature Development
1. Create issue for tracking
2. Create feature branch
3. Make commits referencing issue
4. Create PR linking to issue
5. Request reviews
6. Address feedback
7. Merge and close issue

### Hotfix
1. Create branch from main/production
2. Make minimal fix
3. Create PR with urgent label
4. Fast-track review
5. Merge with squash
6. Tag release if needed
