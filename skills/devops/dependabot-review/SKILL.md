---
name: dependabot-review
description: Reviews open Dependabot PRs, classifies by risk (patch/minor/major, security, lockfile-only), and merges safe ones or advises on what to do. Use when user mentions "dependabot", "dependabot PRs", "dependency updates", "merge dependabot", "review dependabot", "dependency PRs", "bump PRs", "update dependencies", or runs /dependabot-review command.
model: sonnet
---

# Dependabot PR Review

Triage, classify, and merge open Dependabot PRs with risk-based assessment.

## Auto-Invoke Triggers

This skill activates when:

1. **Keywords**: "dependabot", "dependabot PRs", "dependency updates", "merge dependabot", "review dependabot", "dependency PRs", "bump PRs", "update dependencies"
2. **Command**: `/dependabot-review`

---

## Arguments

- *(no args)* — Triage mode: list all open Dependabot PRs with risk classification
- `--merge-safe` — Merge all PRs classified as SAFE TO MERGE (asks for target branch first)
- `--pr <number>` — Deep-dive analysis of a single Dependabot PR
- `--base <branch>` — Target branch for retargeting PRs before merge (skips the prompt)

---

## Prerequisites

- GitHub CLI (`gh`) authenticated with repo access
- Repository must have open Dependabot PRs

Verify:

```bash
gh auth status
```

---

## Workflow

### Step 1: Fetch Open Dependabot PRs

```bash
gh pr list \
  --author "app/dependabot" \
  --state open \
  --json number,title,labels,headRefName,baseRefName,mergeable,isDraft,createdAt,statusCheckRollup \
  --limit 50
```

If `--pr <number>` was provided, fetch that single PR instead:

```bash
gh pr view <number> \
  --json number,title,body,labels,headRefName,baseRefName,mergeable,isDraft,createdAt,statusCheckRollup,additions,deletions
```

If no Dependabot PRs are found, report "No open Dependabot PRs found" and stop.

### Step 2: Enrich Each PR

For each PR, gather additional data:

**Files changed** (for lockfile-only detection):

```bash
gh pr diff <number> --name-only
```

**CI status**: Extract from `statusCheckRollup` in the JSON. Classify as:
- `pass` — all checks SUCCESS or SKIPPED
- `fail` — any check FAILURE
- `pending` — any check IN_PROGRESS or QUEUED
- `none` — no checks ran

### Step 3: Classify Each PR

Apply the risk matrix to each PR:

**Parse version info from PR title:**

Dependabot titles follow: `build(deps): bump <package> from <old> to <new> in <path>`

For grouped updates: `build(deps): bump the <group> group across N directory with M updates`

**Determine semver delta:**
- Compare major versions: different → `major`
- Compare minor versions: different → `minor`
- Otherwise → `patch`
- Grouped PRs: check PR body for the update table; if any update is major → treat entire PR as `major`

**Apply classification rules:**

#### SAFE TO MERGE
All of these must be true:
- CI: `pass` (or `none` for lockfile-only changes)
- Mergeable: `MERGEABLE`
- AND one of:
  - Semver: `patch` (any dependency)
  - Semver: `minor` AND package matches known-safe pattern
  - Files changed: lockfile only (`*-lock.*`, `*.lock`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `Cargo.lock`, `gradle.lockfile`)
  - Ecosystem: `github_actions` AND semver: `minor` or `patch`

**Known-safe patterns** (safe at minor):
- `@types/*` — TypeScript type definitions
- `eslint-*`, `prettier`, `@typescript-eslint/*` — linters/formatters
- `@testing-library/*`, `@playwright/test`, `vitest` — test tooling
- `actions/*`, `docker/*`, `hashicorp/*` — CI actions (minor only)

#### REVIEW RECOMMENDED
- CI: `pass` AND mergeable: `MERGEABLE`
- AND one of:
  - Semver: `minor` AND direct production dependency
  - Grouped PR with no major bumps
  - Package on framework watchlist (even at minor)

**Framework watchlist** (always flag for review at minor+):
- `next`, `react`, `react-dom`, `svelte`, `vue`, `angular`
- `spring-boot`, `kotlin`, `gradle`
- `supabase-js`, `@supabase/*`
- `mapbox-gl`, `framer-motion`

#### REQUIRES HUMAN REVIEW
- Any `major` semver bump
- Grouped PR containing any major bump

#### Security Override
Security-labeled PRs stay in their normal risk tier (a security patch is still SAFE, a security minor is still REVIEW, etc.) but are **always flagged with an urgency callout** at the top of the report. Security + major = HUMAN REVIEW.

#### BLOCKED
- CI: `fail` → note possible root causes (Dependabot lacks repo secrets, pre-existing failures)
- Mergeable: `CONFLICTING` → suggest `@dependabot rebase`
- Mergeable: `UNKNOWN` → suggest waiting for GitHub to compute

### Step 4: Present Triage Report

Format the report as:

```
## Dependabot PR Triage — {owner}/{repo}
{N} open PRs found

### SAFE TO MERGE ({count})
| PR | Package | From → To | Type | Scope | CI | Files |
|----|---------|-----------|------|-------|----|-------|
| #142 | eslint | 8.56 → 8.57 | patch | dev | pass | lockfile |

### REVIEW RECOMMENDED ({count})
| PR | Package | From → To | Type | Reason | CI |
|----|---------|-----------|------|--------|----|
| #140 | next | 14.1 → 14.2 | minor | framework watchlist | pass |

### REQUIRES HUMAN REVIEW ({count})
| PR | Package | From → To | Type | Reason |
|----|---------|-----------|------|--------|
| #131 | spring-boot | 3.2 → 4.0 | major | major version bump |

### BLOCKED ({count})
| PR | Package | Issue | Suggested Action |
|----|---------|-------|-----------------|
| #129 | gradle | CI fail | Check Dependabot secrets / pre-existing lint errors |
| #127 | pnpm group | conflict | `@dependabot rebase` |
```

After the report, ask the user what they want to do using natural conversation.

### Step 5: Execute Actions

**If user chooses to merge safe PRs (or `--merge-safe` flag):**

1. **Ask for target branch**: "What branch should these PRs target? (e.g., main, develop)"
   - Skip if `--base` was provided
2. **Retarget if needed**: For each PR where `baseRefName` differs from the target:
   ```bash
   gh pr edit <number> --base <target-branch>
   ```
3. **Approve and merge each safe PR**:
   ```bash
   gh pr review <number> --approve --body "Auto-approved: safe dependency update"
   gh pr merge <number> --squash
   ```
   If squash fails (repo doesn't allow squash):
   ```bash
   gh pr merge <number> --merge
   ```
   If merge commits also fail:
   ```bash
   gh pr merge <number> --rebase
   ```

**If user chooses to rebase conflicted PRs:**

```bash
gh pr comment <number> --body "@dependabot rebase"
```

**If user chooses single PR deep-dive (`--pr <number>`):**

Present:
- Package name, old version → new version
- Semver classification and risk tier
- Release notes excerpt (from PR body)
- Files changed list
- CI check details (which passed, which failed)
- Recommendation with reasoning

### Step 6: Summary

After all actions, present:

```
## Summary
- Merged: {N} PRs ({list numbers})
- Rebased: {N} PRs ({list numbers})
- Skipped: {N} PRs ({reasons})
- Remaining: {N} PRs requiring human review
```

---

## CI Failure Diagnostics

When a Dependabot PR has failing CI, check these common causes before blaming the dependency update:

1. **Missing secrets**: Dependabot PRs run with read-only `GITHUB_TOKEN` and cannot access repo Actions secrets. Only Dependabot-specific secrets (Settings > Security > Dependabot secrets) are available. Look for errors like "Missing required environment variable" or auth failures.

2. **Lockfile-only changes**: If the PR only changes lockfiles (`pnpm-lock.yaml`, `package-lock.json`, etc.), it cannot cause lint, type-check, or build failures. Flag these as pre-existing issues.

3. **Pre-existing failures**: Check if the same CI checks fail on the base branch. If so, the failure is not caused by the dependency update.

---

## Important Notes

1. **Triage is read-only by default** — no merges happen unless the user explicitly requests it or uses `--merge-safe`
2. **Always ask for target branch** before merging — never assume main or develop
3. **Grouped PRs**: Parse the update table in the PR body to identify individual packages and their semver bumps
4. **Security PRs**: Always surface these prominently regardless of semver level
5. **`@dependabot rebase`**: The preferred fix for lockfile conflicts — Dependabot regenerates the lockfile against the current base

---

## Progressive Disclosure

For more details, see:
- [WORKFLOW.md](WORKFLOW.md) — Detailed 5-phase methodology
- [EXAMPLES.md](EXAMPLES.md) — Real-world triage scenarios
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and solutions

## Version

1.0.0
