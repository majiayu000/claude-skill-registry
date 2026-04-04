---
name: GitHub CLI
description: Expert help with GitHub CLI (gh) for managing pull requests, issues, repositories, workflows, and releases. Use this when working with GitHub operations from the command line, creating new releases, or bumping package versions.
---

# GitHub CLI (gh)

Expert guidance for GitHub CLI operations and workflows.

## Installation & Setup

```bash
# Login to GitHub
gh auth login

# Check authentication status
gh auth status

# Configure git to use gh as credential helper
gh auth setup-git
```

## Pull Requests

### Creating PRs
```bash
# Create PR interactively
gh pr create

# Create PR with title and body
gh pr create --title "Add feature" --body "Description"

# Create PR to specific branch
gh pr create --base main --head feature-branch

# Create draft PR
gh pr create --draft

# Create PR from current branch
gh pr create --fill  # Uses commit messages
```

### Viewing PRs
```bash
# List PRs
gh pr list

# List my PRs
gh pr list --author @me

# View PR details
gh pr view 123

# View PR in browser
gh pr view 123 --web

# View PR diff
gh pr diff 123

# Check PR status
gh pr status
```

### Managing PRs
```bash
# Checkout PR locally
gh pr checkout 123

# Review PR
gh pr review 123 --approve
gh pr review 123 --comment --body "Looks good!"
gh pr review 123 --request-changes --body "Please fix X"

# Merge PR
gh pr merge 123
gh pr merge 123 --squash
gh pr merge 123 --rebase
gh pr merge 123 --merge

# Close PR
gh pr close 123

# Reopen PR
gh pr reopen 123

# Ready draft PR
gh pr ready 123
```

### PR Checks
```bash
# View PR checks
gh pr checks 123

# Watch PR checks
gh pr checks 123 --watch
```

## Issues

### Creating Issues
```bash
# Create issue interactively
gh issue create

# Create issue with title and body
gh issue create --title "Bug report" --body "Description"

# Create issue with labels
gh issue create --title "Bug" --label bug,critical

# Assign issue
gh issue create --title "Task" --assignee @me
```

### Viewing Issues
```bash
# List issues
gh issue list

# List my issues
gh issue list --assignee @me

# List by label
gh issue list --label bug

# View issue details
gh issue view 456

# View in browser
gh issue view 456 --web
```

### Managing Issues
```bash
# Close issue
gh issue close 456

# Reopen issue
gh issue reopen 456

# Edit issue
gh issue edit 456 --title "New title"
gh issue edit 456 --add-label bug
gh issue edit 456 --add-assignee @user

# Comment on issue
gh issue comment 456 --body "Update"
```

## Repository Operations

### Repository Info
```bash
# View repository
gh repo view

# View in browser
gh repo view --web

# Clone repository
gh repo clone owner/repo

# Fork repository
gh repo fork owner/repo

# List repositories
gh repo list owner
```

### Repository Management
```bash
# Create repository
gh repo create my-repo --public
gh repo create my-repo --private

# Delete repository
gh repo delete owner/repo

# Sync fork
gh repo sync owner/repo

# Set default repository
gh repo set-default
```

## Workflows & Actions

### Viewing Workflows
```bash
# List workflows
gh workflow list

# View workflow runs
gh run list

# View specific run
gh run view 789

# Watch run
gh run watch 789

# View run logs
gh run view 789 --log
```

### Managing Workflows
```bash
# Trigger workflow
gh workflow run workflow.yml

# Cancel run
gh run cancel 789

# Rerun workflow
gh run rerun 789

# Download artifacts
gh run download 789
```

## Releases

### Creating Releases
```bash
# Create release
gh release create v1.0.0

# Create release with notes
gh release create v1.0.0 --notes "Release notes"

# Create release with files
gh release create v1.0.0 dist/*.tar.gz

# Create draft release
gh release create v1.0.0 --draft

# Generate release notes automatically
gh release create v1.0.0 --generate-notes
```

### Managing Releases
```bash
# List releases
gh release list

# View release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0

# Delete release
gh release delete v1.0.0
```

## Version Management (pki-manager specific)

**IMPORTANT**: When creating a new release for this project, you MUST bump the version in ALL THREE package.json files:
- `package.json` (root - authoritative source)
- `frontend/package.json`
- `backend/package.json`

### Version Bump Types (Semantic Versioning)

| Type | When to use | Example |
|------|-------------|---------|
| **patch** | Bug fixes, minor changes | `1.2.0` → `1.2.1` |
| **minor** | New features, backwards compatible | `1.2.0` → `1.3.0` |
| **major** | Breaking changes | `1.2.0` → `2.0.0` |

### Pre-Release Workflow

Before creating a release, you MUST:

1. **Check current version** in root package.json
2. **Determine bump type** based on changes since last release
3. **Update ALL package.json files** with the new version
4. **Commit version changes** with message: `chore: bump version to vX.Y.Z`
5. **Create git tag**: `git tag vX.Y.Z`
6. **Push tag**: `git push origin vX.Y.Z`
7. **Create GitHub release**: `gh release create vX.Y.Z --generate-notes`

### Complete Release Workflow

```bash
# 1. Determine current version
cat package.json | grep '"version"'
# Output: "version": "1.2.0"

# 2. Update versions in all package.json files
# For patch bump (1.2.0 → 1.2.1):
NEW_VERSION="1.2.1"

# Edit package.json (root)
# Edit frontend/package.json
# Edit backend/package.json
# All three must have the same version!

# 3. Commit version bump
git add package.json frontend/package.json backend/package.json
git commit -m "chore: bump version to v${NEW_VERSION}"

# 4. Create and push tag
git tag "v${NEW_VERSION}"
git push origin main
git push origin "v${NEW_VERSION}"

# 5. Create GitHub release with auto-generated notes
gh release create "v${NEW_VERSION}" --generate-notes

# Or with custom notes
gh release create "v${NEW_VERSION}" --notes "## What's Changed
- Feature A
- Bug fix B
- Improvement C"
```

### Version Synchronization Rules

**CRITICAL**: All three package.json files MUST have matching versions:

| File | Path | Must Match Root |
|------|------|-----------------|
| Root | `package.json` | ✓ (authoritative) |
| Frontend | `frontend/package.json` | ✓ |
| Backend | `backend/package.json` | ✓ |

### Checking Version Consistency

```bash
# Quick check all versions
echo "Root: $(cat package.json | grep '"version"' | head -1)"
echo "Frontend: $(cat frontend/package.json | grep '"version"' | head -1)"
echo "Backend: $(cat backend/package.json | grep '"version"' | head -1)"
```

### Release Checklist

Before releasing, verify:
- [ ] All tests pass (`pnpm test`)
- [ ] Build succeeds (`pnpm build`)
- [ ] All three package.json versions match
- [ ] Changes are committed to main branch
- [ ] No uncommitted changes (`git status`)
- [ ] Previous release tag exists for comparison

## Gists

```bash
# Create gist
gh gist create file.txt

# Create gist from stdin
echo "content" | gh gist create -

# List gists
gh gist list

# View gist
gh gist view <gist-id>

# Edit gist
gh gist edit <gist-id>

# Delete gist
gh gist delete <gist-id>
```

## Advanced Features

### Aliases
```bash
# Create alias
gh alias set pv "pr view"
gh alias set bugs "issue list --label bug"

# List aliases
gh alias list

# Use alias
gh pv 123
```

### API Access
```bash
# Make API call
gh api repos/:owner/:repo/issues

# With JSON data
gh api repos/:owner/:repo/issues -f title="Bug" -f body="Description"

# Paginated results
gh api --paginate repos/:owner/:repo/issues
```

### Extensions
```bash
# List extensions
gh extension list

# Install extension
gh extension install owner/gh-extension

# Upgrade extensions
gh extension upgrade --all
```

## Common Workflows

### Code Review Workflow
```bash
# List PRs assigned to you
gh pr list --assignee @me

# Checkout PR for testing
gh pr checkout 123

# Run tests, review code...

# Approve PR
gh pr review 123 --approve --body "LGTM!"

# Merge PR
gh pr merge 123 --squash
```

### Quick PR Creation
```bash
# Create feature branch, make changes, commit
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature

# Create PR from commits
gh pr create --fill

# View PR
gh pr view --web
```

### Issue Triage
```bash
# List open issues
gh issue list

# Add labels to issues
gh issue edit 456 --add-label needs-triage
gh issue edit 456 --add-label bug

# Assign issue
gh issue edit 456 --add-assignee @developer
```

## Configuration

```bash
# Set default editor
gh config set editor vim

# Set default git protocol
gh config set git_protocol ssh

# View configuration
gh config list

# Set browser
gh config set browser firefox
```

## Tips

1. **Use `--web` flag**: Open items in browser for detailed view
2. **Interactive prompts**: Most commands work interactively if you omit parameters
3. **Filters**: Use `--author`, `--label`, `--state` to filter lists
4. **JSON output**: Add `--json` flag for scriptable output
5. **Template repos**: Use `gh repo create --template` for templates
6. **Auto-merge**: Enable with `gh pr merge --auto`
