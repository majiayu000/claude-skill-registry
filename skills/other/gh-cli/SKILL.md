---
name: gh-cli
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  GitHub CLI (gh) for repos, issues, PRs, actions, releases. Use when working
  with GitHub or running gh commands.
practices:
- pragmatic-programmer
---
<!-- TOC: Quick Start | THE EXACT PROMPT | Essential Commands | AGENTS.md Blurb | When to Use | References -->

# gh-cli — GitHub CLI

> **Core Capability:** Interact with GitHub repositories and services from the command line using `gh`.

## Quick Start

```bash
# Install
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Check auth
gh auth status

# Login
gh auth login

# Clone repo
gh repo clone owner/repo
```

---

## THE EXACT PROMPT — Pull Request Workflow

```bash
# Create PR from current branch
gh pr create --fill

# Create PR with title/body
gh pr create --title "Add feature" --body "Description"

# View PR
gh pr view 45
gh pr view 45 --web

# Checkout PR locally
gh pr checkout 45

# Review PR
gh pr review 45 --approve
gh pr review 45 --request-changes --body "Please fix X"

# Merge PR
gh pr merge 45 --squash
gh pr merge 45 --merge --delete-branch
```

---

## THE EXACT PROMPT — Issues

```bash
# List issues
gh issue list

# Create issue
gh issue create --title "Bug: Login fails" --body "Description"

# View issue
gh issue view 123

# Close issue
gh issue close 123

# Comment on issue
gh issue comment 123 --body "Working on this"

# Add labels
gh issue edit 123 --add-label "bug,priority:high"
```

---

## THE EXACT PROMPT — Actions (CI/CD)

```bash
# List workflow runs
gh run list

# View run details
gh run view 12345

# Watch run in progress
gh run watch 12345

# View logs
gh run view 12345 --log

# Rerun failed jobs
gh run rerun 12345 --failed

# Run workflow manually
gh workflow run deploy.yml -f environment=production
```

---

## THE EXACT PROMPT — Releases

```bash
# Create release
gh release create v1.0.0 --title "Version 1.0" --generate-notes

# Upload assets
gh release upload v1.0.0 ./dist/app.zip

# Download assets
gh release download v1.0.0
```

---

## Essential Commands

| Category | Command | Description |
|----------|---------|-------------|
| Repo | `gh repo clone owner/repo` | Clone repository |
| Repo | `gh repo create my-repo --public` | Create new repo |
| PR | `gh pr create --fill` | Create PR from branch |
| PR | `gh pr checkout 45` | Checkout PR locally |
| PR | `gh pr merge 45 --squash` | Merge with squash |
| Issue | `gh issue create --title "X"` | Create issue |
| Issue | `gh issue list` | List issues |
| Actions | `gh run list` | List workflow runs |
| Actions | `gh run watch` | Watch current run |
| Release | `gh release create v1.0` | Create release |

---

## Quick PR Workflow

```bash
# Create branch, commit, push, create PR
git checkout -b feature/my-feature
# ... make changes ...
git add . && git commit -m "Add feature"
git push -u origin feature/my-feature
gh pr create --fill

# Review and merge
gh pr checkout 45
gh pr review --approve
gh pr merge --squash --delete-branch
```

---

## AGENTS.md Blurb

Copy this to your project's AGENTS.md:

```markdown
### GitHub CLI (gh)

The `gh` CLI is configured and authenticated.

Common tasks:

- Create PR: `gh pr create --fill`
- List open PRs: `gh pr list`
- Check CI status: `gh pr checks`
- Create issue: `gh issue create --title "..." --body "..."`

Repo: `https://github.com/<OWNER>/<REPO>`
```

---

## When to Use

- Creating PRs without leaving the terminal
- Automating issue creation in scripts
- Checking CI status: `gh pr checks`
- Viewing PR comments: `gh pr view 123 --comments`
- Watching actions run: `gh run watch`

---

## References

| Topic | Reference |
|-------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| API & GraphQL | [API.md](references/API.md) |
| Common workflows | [WORKFLOWS.md](references/WORKFLOWS.md) |
