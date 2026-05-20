---
name: github
description: GitHub operations — issues, PRs, commits, code search, CI/CD via gh CLI
user-invocable: true
---

# GitHub Skill — arifOS_bot

Triggers: "github", "open issue", "create pr", "pull request", "gh", "ci", "workflow",
          "code search", "repo", "commit history", "check runs", "release"

Authenticated as: `ariffazil` via `GH_TOKEN` (gh CLI, HTTPS protocol)

---

## Repos You Own

| Repo | Path on VPS | Purpose |
|------|-------------|---------|
| `ariffazil/arifOS` | `/mnt/arifos` | Main constitutional kernel |
| `ariffazil/openclaw-workspace` | `~/.openclaw/workspace` | This workspace (backed up nightly) |
| `ariffazil/APEX-THEORY` | `/mnt/apex` | Thermodynamic AI theory |
| `ariffazil/AGI_ASI_bot` | remote only | Telegram bot source |

---

## Issues

```bash
# List open issues
gh issue list -R ariffazil/arifOS --state open --limit 20

# Create issue
gh issue create -R ariffazil/arifOS \
  --title "Title here" \
  --body "Description" \
  --label "bug"

# View issue
gh issue view 42 -R ariffazil/arifOS

# Close issue with comment
gh issue close 42 -R ariffazil/arifOS --comment "Fixed in commit abc123"

# Search issues
gh issue list -R ariffazil/arifOS --search "floor enforcement"
```

## Pull Requests

```bash
# List open PRs
gh pr list -R ariffazil/arifOS --state open

# Create PR (from current branch)
cd /mnt/arifos
gh pr create \
  --title "feat: description" \
  --body "$(cat <<'PRBODY'
## Summary
- What changed and why

## Test plan
- [ ] pytest tests/ -v passes
- [ ] arifos health returns 13 tools

🤖 Opened by arifOS_bot
PRBODY
)"

# View PR
gh pr view 12 -R ariffazil/arifOS

# Merge PR (squash)
gh pr merge 12 -R ariffazil/arifOS --squash --delete-branch
```

## Code Search

```bash
# Search across all your repos
gh search code "constitutional_decorator" --owner ariffazil

# Search in specific repo
gh search code "seal_vault" -R ariffazil/arifOS

# Find files
gh api "repos/ariffazil/arifOS/contents/" | jq '.[].name'
gh api "search/code?q=repo:ariffazil/arifOS+THRESHOLDS" | jq '.items[].path'
```

## CI/CD — Workflow Runs

```bash
# List recent runs
gh run list -R ariffazil/arifOS --limit 10

# View run status
gh run view <run-id> -R ariffazil/arifOS

# Watch live run
gh run watch <run-id> -R ariffazil/arifOS

# Re-run failed jobs
gh run rerun <run-id> -R ariffazil/arifOS --failed

# Trigger workflow manually
gh workflow run deploy.yml -R ariffazil/arifOS
```

## Commits & Branches

```bash
# Recent commits
gh api repos/ariffazil/arifOS/commits | jq '.[:5][] | {sha: .sha[:8], message: .commit.message, date: .commit.author.date}'

# Create branch
cd /mnt/arifos && git checkout -b feature/my-feature

# Push branch (HTTPS via gh credential helper)
cd /mnt/arifos
git remote set-url origin https://github.com/ariffazil/arifOS.git
git push origin feature/my-feature

# List branches
gh api repos/ariffazil/arifOS/branches | jq '.[].name'
```

## Releases & Tags

```bash
# List releases
gh release list -R ariffazil/arifOS

# Create release
gh release create v2026.3.1 -R ariffazil/arifOS \
  --title "arifOS v2026.3.1" \
  --notes "Release notes here" \
  --target main

# Download release asset
gh release download v2026.3.1 -R ariffazil/arifOS
```

## Notifications & Activity

```bash
# Check notifications
gh api notifications | jq '.[] | {repo: .repository.name, reason: .reason, title: .subject.title}'

# Repo activity
gh api repos/ariffazil/arifOS/events --paginate | jq '.[:5][] | {type, actor: .actor.login}'
```

## Quick Shortcuts

```bash
# Full repo status snapshot
gh repo view ariffazil/arifOS --json name,description,stargazerCount,openIssuesCount,defaultBranchRef

# Open in browser (if browser available)
gh repo view ariffazil/arifOS --web

# Clone a new repo to /mnt/
gh repo clone ariffazil/SOME-REPO /mnt/some-repo
```

---

## Constitution Note (F1/F11)

- PRs and issues are **reversible** — create freely.
- Force-pushing to `main` requires F13 confirmation.
- Deleting branches with unmerged work → 888_HOLD.
- Never commit `.env`, `openclaw.json`, or credential files.

*arifOS_bot — GitHub skill via gh CLI v2.63.1*
