---
name: pr-sweep
description: Use when you want to sweep all open pull requests across all repos, triage their status, run code reviews on unreviewed PRs, merge what's ready, fix quick blockers, and produce a full status report. Trigger when the user says "check my PRs", "close out open PRs", "what's the status of my PRs", "sweep my PRs", "PR sweep", "pull request sweep", or wants a cross-repo PR status report. Future: pairs with the loop skill for ongoing automated PR management.
---

# Pull Request Sweep

A cross-repo PR sweep: discover → enrich → triage → review → act → report.

**Announce at start:** "I'm using the pr-sweep skill to sweep all open PRs."

---

## Step 1: Discover All Open PRs

```bash
gh search prs \
  --author @me \
  --state open \
  --json number,title,url,isDraft,repository,headRefName,baseRefName,reviewDecision \
  --limit 100
```

Parse the result into a working list. **Skip drafts immediately** — they're not ready for action.

If you have more than 20 non-draft PRs, report the count and ask the user if they want to proceed or filter by repo.

---

## Step 2: Enrich Each PR

For each non-draft PR, fetch CI and merge state in parallel (dispatch subagents or batch calls):

```bash
# CI status
gh pr checks <number> --repo <owner/repo> --json name,state,conclusion

# Merge state (up-to-date, behind, conflicting, etc.)
gh pr view <number> --repo <owner/repo> --json mergeStateStatus,mergeable
```

Build a status object per PR:

```
{
  repo, number, title, url,
  ciStatus: passing | failing | pending | none,
  mergeState: clean | behind | dirty | blocked,
  reviewDecision: APPROVED | CHANGES_REQUESTED | REVIEW_REQUIRED | null
}
```

---

## Step 3: Triage

Classify each PR into one category (in priority order — first match wins):

| Category | Condition |
|----------|-----------|
| `MERGE_READY` | CI passing, review approved or not required, merge state clean |
| `PENDING_CI` | CI still running, everything else clean |
| `NEEDS_REVIEW` | No reviews yet (reviewDecision null or REVIEW_REQUIRED) |
| `BEHIND_BASE` | Merge state is `behind` |
| `CI_FAILING` | CI has failed conclusions |
| `CHANGES_REQUESTED` | Reviewer has requested changes |
| `CONFLICTING` | Merge state is `dirty` (merge conflicts) |
| `BLOCKED` | Anything else preventing merge |

Show the triage table to the user and wait for confirmation before taking any action:

```
PR Triage
─────────────────────────────────────────────────────────────
MERGE_READY    owner/repo #42  feat: add caching layer
NEEDS_REVIEW   owner/repo #38  fix: auth token refresh
BEHIND_BASE    other/repo #11  refactor: split service
CI_FAILING     other/repo #9   feat: new export format
CHANGES_REQUESTED  repo #7     fix: race condition
─────────────────────────────────────────────────────────────
Plan: merge 1, review 1, rebase 1, attempt CI fix 1, flag 1.
Proceed?
```

Wait for the user to confirm before proceeding to Step 4. This is important — the sweep can merge multiple PRs and rebase branches across repos, so the user should know what's coming.

---

## Step 4: Code Review (for NEEDS_REVIEW PRs)

For each `NEEDS_REVIEW` PR, invoke the `review` skill to review the changes.

**If there are multiple NEEDS_REVIEW PRs:** dispatch code review subagents in parallel — one per PR — then collect all results before proceeding to Step 5. This is the most expensive step; parallelizing keeps total time reasonable.

The review covers:
- Baseline: correctness, security, error handling, performance, naming, test coverage
- Codebase-specific: read the target repo's CLAUDE.md for any `## Code Review`, `## Standards`, or `## Gotchas` sections

Each review produces:
```
[owner/repo #N] Code Review
MUST FIX: <issue> — file:line
SUGGESTION: <issue>
CLEAN — no blocking issues
```

After review, re-classify:
- No MUST FIX items → move to `MERGE_READY` (if CI also passing)
- Has MUST FIX items → move to `BLOCKED` (with review notes)

---

## Step 5: Act

Work through categories in this order:

### MERGE_READY → Merge

```bash
gh pr merge <number> --repo <owner/repo> --squash --delete-branch
```

### BEHIND_BASE → Rebase

```bash
gh pr checkout <number> --repo <owner/repo>
BASE=$(gh pr view <number> --repo <owner/repo> --json baseRefName --jq '.baseRefName')
git fetch origin $BASE
git rebase origin/$BASE
git push --force-with-lease
```

Then re-check CI. If CI passes and no other blockers → merge. If CI fails → reclassify as `CI_FAILING`.

### CI_FAILING → Attempt Quick Fix

1. Read the failure output: `gh run view --log-failed --repo <owner/repo>`
2. **Quick fix** (lint, format, import, typo): check out the PR branch, fix, commit, push
3. **Complex failure**: flag it — don't attempt a fix. Note it in the report.

### PENDING_CI → Wait and Recheck Once

Poll using `--watch` with a timeout, then check the result:
```bash
gh pr checks <number> --repo <owner/repo> --watch --fail-fast
```

If still pending or if the command times out, leave as-is and flag in the report.

### CHANGES_REQUESTED / CONFLICTING / BLOCKED → Flag Only

These require human judgment. Note them clearly in the report — no auto-action.

---

## Step 6: Final Report

After all actions complete, produce a full report:

```
PR Sweep Complete
══════════════════════════════════════════════════════════════
MERGED (2)
  ✓ owner/repo #42  feat: add caching layer
  ✓ owner/repo #38  fix: auth token refresh — reviewed, no blockers

REBASED (1)
  ↺ other/repo #11  refactor: split service — rebased on main, CI running

FIXED & MERGED (1)
  ✓ other/repo #9   feat: new export format — lint fix applied, merged

NEEDS YOUR ATTENTION (2)
  ✗ repo #7   fix: race condition — CHANGES_REQUESTED by @alice
      Action needed: address review feedback

  ✗ repo #5   feat: dashboard — CI failing (complex: flaky integration test)
      Action needed: investigate test flakiness before merging

CODE REVIEW FINDINGS
  repo #38 — SUGGESTION: consider extracting token refresh logic to a helper
══════════════════════════════════════════════════════════════
Merged: 3  |  Pending: 1  |  Needs attention: 2
```

Surface suggestions from code reviews in the report even if they weren't blocking — they may inform follow-up work.

---

## Rules

**Never:**
- Act on draft PRs
- Force-push to main/master
- Merge with failing CI
- Attempt to auto-resolve CHANGES_REQUESTED — that's a human conversation

**Always:**
- Triage and show the table before taking any action
- Squash merge
- Parallelize code review subagents when multiple PRs need review
- Clean up PR branches after merge (`--delete-branch`)

---

## Future: Pairing with Loop

This skill is designed to work with `/loop` for ongoing PR babysitting:

```
/loop 30m /pr-sweep
```

This is not yet recommended due to token costs, but the skill is designed to be idempotent — running it multiple times is safe. Already-merged PRs won't appear in the next sweep.
