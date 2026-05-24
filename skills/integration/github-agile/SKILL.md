---
name: github-agile
description: "Diagnose GitHub-driven agile workflow problems and guide feature branch development. This skill should be used when the user asks to 'set up GitHub workflow', 'initialize project on GitHub', 'clean up issues', 'fix the backlog', 'create PR', or needs help with GitHub CLI, branches, issues, or PRs. Keywords: GitHub, issues, PR, pull request, branches, workflow, backlog, milestone, labels, gh CLI."
license: MIT
compatibility: Requires GitHub CLI (gh) installed and authenticated.
metadata:
  author: jwynia
  version: "1.0"
---

# GitHub Agile

Diagnose GitHub-driven agile workflow problems. Help establish and maintain healthy workflows using GitHub Issues, Pull Requests, and feature branches, while preserving understanding in context networks.

## When to Use This Skill

Use this skill when:
- Setting up a new project on GitHub
- Organizing a chaotic backlog
- Establishing branch and PR workflow
- Syncing GitHub state with context network
- Troubleshooting GitHub CLI issues

Do NOT use this skill when:
- Working on code implementation
- Pure requirements or architecture work (use those skills first)
- Non-GitHub version control workflows

## Core Principle

**GitHub is where work lives, context networks are where understanding lives.** Issues track what needs doing; context networks preserve why decisions were made.

## Prerequisites

- **GitHub CLI** installed (`brew install gh` / `apt install gh` / `winget install GitHub.cli`)
- **Authenticated** (`gh auth login` then `gh auth status`)
- **Repository linked** (`gh repo view` succeeds)

Run `scripts/gh-verify.ts` to diagnose environment issues.

## Diagnostic States

### Setup Track

**GH0: No GitHub CLI** - `gh` command not found
- Install per platform, then `gh auth login`

**GH1: Repository Not Initialized** - No git repo or no GitHub remote
- `git init` if needed
- `gh repo create <name> --source=. --push`

**GH2: Workflow Not Established** - No labels, templates, or branch protection
- Run `scripts/gh-init-project.ts --labels standard --templates --protection`

### Workflow Track

**GH3: Backlog Chaos** - Many unlabeled issues, no priorities clear
- Run `scripts/gh-audit.ts` to assess
- Apply MoSCoW prioritization
- Create "icebox" for deferred items
- Create milestone for current focus

**GH4: Feature Branch Violations** - Commits directly to main
- Enable branch protection
- Establish naming: `feature/{issue-number}-description`
- Use `gh issue develop {number}` to create branch

**GH5: PR Without Context** - Minimal PR descriptions, no linked issues
- Create `.github/pull_request_template.md`
- Require: Summary, Related Issue, Why, How to Test

**GH6: Stale Issues/PRs** - Old items with no activity
- Audit: `gh issue list --json number,updatedAt`
- Close or icebox stale items

**GH7: Context Network Gap** - GitHub active but context network outdated
- Run `scripts/gh-sync-context.ts`
- Update `context/status.md` with current state

**GH8: Workflow Healthy** - Issues labeled, PRs linked, context current

## Key Workflows

### Feature Development

```bash
# 1. Create issue (if not exists)
gh issue create --title "Feature: X" --body "..."

# 2. Create branch from issue
gh issue develop {number} --base main

# 3. Make commits referencing issue
git commit -m "feat(scope): description (#123)"

# 4. Create PR
gh pr create --fill

# 5. Merge
gh pr merge --squash
```

### Project Initialization

```bash
# Verify CLI
deno run --allow-run scripts/gh-verify.ts

# Create repo (if new)
gh repo create my-project --source=. --private --push

# Initialize labels, templates, protection
deno run --allow-run --allow-read --allow-write scripts/gh-init-project.ts \
  --labels standard --templates --protection
```

### Backlog Cleanup

```bash
# Audit current state
deno run --allow-run scripts/gh-audit.ts --stale 30

# List for triage
gh issue list --state open --json number,title,labels,updatedAt
```

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `gh-verify.ts` | Check CLI installation and auth | `deno run --allow-run scripts/gh-verify.ts` |
| `gh-init-project.ts` | Initialize labels, templates, protection | `deno run --allow-run --allow-read --allow-write scripts/gh-init-project.ts` |
| `gh-audit.ts` | Audit backlog health | `deno run --allow-run scripts/gh-audit.ts` |
| `gh-sync-context.ts` | Generate context updates from GitHub | `deno run --allow-run --allow-write scripts/gh-sync-context.ts` |

## Anti-Patterns

### The Issue Graveyard
**Problem:** Issues created and never closed, 200+ open issues.
**Fix:** Regular grooming. If it won't be done in 90 days, icebox or close.

### The Context-Free PR
**Problem:** PRs with no description or linked issue.
**Fix:** PR template with required sections.

### The Branch Protection Bypass
**Problem:** Committing directly to main "just this once."
**Fix:** Branch protection exists for a reason. Enforce it.

### The Disconnected Context
**Problem:** Context network not updated, becomes fiction.
**Fix:** End-of-session ritual: update `status.md`.

## GitHub ↔ Context Network Boundary

**Lives in GitHub:** Issues, PRs, Discussions, Actions, Labels, Milestones

**Lives in Context Network:** ADRs, `decisions.md`, `status.md`, `architecture.md`

**Cross-Reference:** Requirements linked from issues, ADRs referenced in PRs

## Templates

Issue templates and PR template are in `assets/`:
- `issue-feature.md` - Feature request template
- `issue-bug.md` - Bug report template
- `issue-task.md` - Task template
- `pull-request.md` - PR template
- `labels-standard.json` - Standard label definitions

## Related Skills

- **requirements-analysis** - Provides validated requirements to create issues from
- **system-design** - ADRs referenced in PRs, component map informs issue breakdown
- **agile-workflow** - Orchestrates the full development cycle
