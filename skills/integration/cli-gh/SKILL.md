---
disable-model-invocation: false
name: cli-gh
user-invocable: false
description: This skill should be used when the user mentions "gh CLI", "gh command", asks to "view repository info", "trigger workflows", "search GitHub", "manage codespaces", "check PR status", "list issues", or asks about GitHub CLI usage and automation from the command line.
---

# GitHub CLI (gh)

## Overview

Expert guidance for GitHub CLI (gh) operations and workflows. Use this skill for command-line GitHub operations including pull request management, issue tracking, repository operations, workflow automation, and codespace management.

**Key capabilities:**

- Create and manage pull requests from the terminal
- Track and organize issues efficiently
- Search across all of GitHub (repos, issues, PRs)
- Manage labels and project organization
- Trigger and monitor GitHub Actions workflows
- Work with codespaces
- Automate repository operations and releases

## Safety Rules

**CRITICAL: This skill NEVER uses destructive gh CLI operations.**

This skill focuses exclusively on safe, read-only, or reversible GitHub operations. The following commands are **PROHIBITED** and must **NEVER** be used:

**Permanently destructive commands:**

- `gh repo delete` - Repository deletion
- `gh repo archive` - Repository archival
- `gh release delete` - Release deletion
- `gh release delete-asset` - Asset deletion
- `gh run delete` - Workflow run deletion
- `gh cache delete` - Cache deletion
- `gh secret delete` - Secret deletion
- `gh variable delete` - Variable deletion
- `gh label delete` - Label deletion
- `gh ssh-key delete` - SSH key deletion (can lock out users)
- `gh gpg-key delete` - GPG key deletion
- `gh codespace delete` - Codespace deletion
- `gh extension remove` - Extension removal
- `gh gist delete` - Gist deletion
- Bulk deletion operations using `xargs` with any destructive commands
- Shell commands: `rm -rf` (except for temporary file cleanup)

**Allowed operations:**

- Creating resources (PRs, issues, releases, labels, repos)
- Viewing and listing (status, logs, information, searches)
- Updating and editing existing resources
- Closing PRs/issues (reversible - can be reopened)
- Canceling workflow runs (stops execution without deleting data)
- Merging pull requests (after proper review)
- Read-only git operations (`git status`, `git log`, `git diff`)

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

# Update PR branch with base branch
gh pr update-branch 123
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

# Create branch to work on issue
gh issue develop 456 --checkout
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

# Sync fork
gh repo sync owner/repo

# Set default repository
gh repo set-default
```

## Search

Search across all of GitHub for repositories, issues, and pull requests.

### Search Repositories

```bash
# Search for repositories
gh search repos "machine learning" --language=python

# Search with filters
gh search repos --stars=">1000" --topic=kubernetes
```

### Search Issues

```bash
# Search issues across GitHub
gh search issues "bug" --label=critical --state=open

# Exclude results (note the -- to prevent flag interpretation)
gh search issues -- "memory leak -label:wontfix"
```

### Search Pull Requests

```bash
# Search PRs
gh search prs --author=@me --state=open

# Search with date filters
gh search prs "refactor" --created=">2024-01-01"
```

## Labels

Manage repository labels for issue and PR organization.

### List and View Labels

```bash
# List all labels in repository
gh label list
```

### Create and Edit Labels

```bash
# Create new label
gh label create "priority: high" --color FF0000 --description "High priority items"

# Edit existing label
gh label edit "bug" --color FFAA00 --description "Something isn't working"
```

### Clone Labels Between Repos

```bash
# Clone labels from another repository
gh label clone owner/source-repo
```

## Codespaces

Manage GitHub Codespaces directly from the terminal.

### List and Create Codespaces

```bash
# List codespaces
gh codespace list

# Create new codespace
gh codespace create --repo owner/repo
```

### Connect to Codespaces

```bash
# SSH into codespace
gh codespace ssh

# Open in VS Code
gh codespace code

# Open in JupyterLab
gh codespace jupyter
```

### Manage Codespace Files

```bash
# Copy files to/from codespace
gh codespace cp local-file.txt remote:~/path/
gh codespace cp remote:~/path/file.txt ./local-dir/

# View logs
gh codespace logs
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
```

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

## Quick Reference

Common gh operations at a glance:

| Operation        | Command                   | Common Flags                              |
| ---------------- | ------------------------- | ----------------------------------------- |
| Create PR        | `gh pr create`            | `--draft`, `--fill`, `--base`, `--title`  |
| List PRs         | `gh pr list`              | `--author @me`, `--label`, `--state`      |
| View PR          | `gh pr view <number>`     | `--web`, `--comments`                     |
| Merge PR         | `gh pr merge <number>`    | `--squash`, `--rebase`, `--delete-branch` |
| Create issue     | `gh issue create`         | `--title`, `--body`, `--label`            |
| List issues      | `gh issue list`           | `--assignee @me`, `--label`, `--state`    |
| View issue       | `gh issue view <number>`  | `--web`, `--comments`                     |
| Clone repo       | `gh repo clone <repo>`    | `--` (to pass git flags)                  |
| Fork repo        | `gh repo fork`            | `--clone`, `--remote`                     |
| View repo        | `gh repo view`            | `--web`                                   |
| Create release   | `gh release create <tag>` | `--title`, `--notes`, `--draft`           |
| Run workflow     | `gh workflow run <name>`  | `--ref`, `--field`                        |
| Watch run        | `gh run watch <id>`       | `--exit-status`                           |
| Search repos     | `gh search repos <query>` | `--language`, `--stars`                   |
| Create label     | `gh label create <name>`  | `--color`, `--description`                |
| Create codespace | `gh codespace create`     | `--repo`, `--branch`                      |
| SSH to codespace | `gh codespace ssh`        | `--codespace`                             |

## Additional Resources

### Reference Guides

For detailed patterns and advanced usage, see:

- **[Workflows & Actions](references/workflows-actions.md)** - GitHub Actions workflows, runs, cache management, and CI/CD integration patterns
- **[Advanced Features](references/advanced-features.md)** - Aliases, API access, extensions, secrets, SSH/GPG keys, organizations, projects, and advanced scripting
- **[Automation Workflows](references/automation-workflows.md)** - Common automation patterns, daily reports, release automation, and team collaboration workflows
- **[Troubleshooting](references/troubleshooting.md)** - Solutions for authentication, permissions, rate limiting, and common errors

### Example Scripts

Practical automation scripts (see `examples/` directory):

- `auto-pr-create.sh` - Automated PR creation workflow
- `issue-triage.sh` - Bulk issue labeling and assignment
- `workflow-monitor.sh` - Watch and notify on workflow completion
- `release-automation.sh` - Complete release workflow automation

### External Documentation

- **Official Manual**: https://cli.github.com/manual
- **GitHub Community**: https://github.com/cli/cli/discussions
- **API Documentation**: https://docs.github.com/en/rest
- **Extension Marketplace**: https://github.com/topics/gh-extension

## JSON Output

Use `--json` flag for structured output. **Always verify field names with `--help`** as they differ from GitHub API names.

```bash
# Check available JSON fields for any command
gh repo view --help | grep -A 50 "JSON FIELDS"
gh pr list --help | grep -A 50 "JSON FIELDS"
```

### Common JSON Field Corrections

| Wrong (API-style) | Correct (gh CLI) |
| ----------------- | ---------------- |
| `stargazersCount` | `stargazerCount` |
| `forksCount`      | `forkCount`      |
| `watchersCount`   | `watchers`       |
| `openIssuesCount` | `issues`         |

### Repository View Fields

```bash
# Common fields for gh repo view --json
gh repo view owner/repo --json name,description,stargazerCount,forkCount,updatedAt,url,readme
```

## Tips

1. Use `--web` flag to open items in browser for detailed view
2. Leverage interactive prompts by omitting parameters - most commands support interactive mode
3. Apply filters with `--author`, `--label`, `--state` to narrow down lists efficiently
4. Add `--json` flag to enable scriptable output for automation
5. **Always check `--help` for valid JSON field names** - they differ from GitHub API
6. Use `gh repo create --template` to scaffold from template repositories
7. Enable auto-merge with `gh pr merge --auto` for PRs that pass checks
