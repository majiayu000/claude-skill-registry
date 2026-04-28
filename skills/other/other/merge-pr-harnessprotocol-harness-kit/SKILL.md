---
name: merge-pr
description: Use when a pull request is ready to merge — verifies CI and review status, syncs with the base branch, confirms with the user, then squash merges and cleans up. Trigger when the user says "merge this", "merge this PR", "squash merge", or "merge it". Works on any open PR — does not require /open-pr to have created it. If no PR exists, redirects to /open-pr. Does NOT deploy to any environment.
---

# Merge PR

Takes a ready PR and lands it: verify → sync → confirm → squash merge → cleanup.

**Announce at start:** "I'm using the merge-pr skill to merge this PR."

---

## Step 1: Identify the PR

Check for an open PR on the current branch, or use a user-specified PR number:

```bash
# Current branch
gh pr view --json number,title,url,state,baseRefName,headRefName 2>/dev/null

# Or if user specified #N:
gh pr view <N> --json number,title,url,state,baseRefName,headRefName
```

**No PR found:** Stop and redirect:
> "No open PR found on this branch. Use `/open-pr` to create one first."

**PR found:** Note the PR number, title, base branch, and URL. Continue.

---

## Step 2: Verify Readiness

Check CI status and review state:

```bash
gh pr checks <N>
gh pr view <N> --json reviews --jq '.reviews[] | select(.state == "CHANGES_REQUESTED")'
```

**CI failing:** Stop and report which checks are failing. Do not merge.
> "CI is failing on [check names]. Fix these before merging, or use `/open-pr` to address them."

**CHANGES_REQUESTED review:** Stop and report who requested changes.
> "PR has CHANGES_REQUESTED from [reviewer]. Resolve this before merging."

**All clear:** Continue.

---

## Step 3: Base Branch Sync

Check whether the base branch has moved since branching:

```bash
BASE=$(gh pr view <N> --json baseRefName --jq '.baseRefName')
git fetch origin $BASE
git log HEAD..origin/$BASE --oneline
```

**New commits exist:** Rebase and force-push:

```bash
git rebase origin/$BASE
git push --force-with-lease
```

If rebase has conflicts, resolve them, then `git rebase --continue`. After force-push, re-verify CI passes before continuing.

**No new commits:** Skip.

---

## Step 4: Confirm with User

Before merging, confirm:

```
Ready to squash merge PR #<N> ("<title>") into <base>.
All checks passed. Proceed?
```

Wait for confirmation. If the user says to always proceed without asking (e.g. "auto-merge", "no need to confirm"), skip this prompt for the rest of the session.

---

## Step 5: Squash Merge and Cleanup

Once confirmed:

```bash
gh pr merge <N> --squash --delete-branch
```

After merge, sync locally:

```bash
git checkout $BASE
git pull
git branch -d <feature-branch> 2>/dev/null || true
```

Report: "PR #<N> merged. Branch cleaned up. Done."

---

## Quick Reference

| Step | Action | Block on failure? |
|------|--------|-------------------|
| 1. Identify PR | Current branch or `#N` | Yes — redirect to /open-pr |
| 2. Verify readiness | CI + review state | Yes — fix first |
| 3. Base sync | Rebase if behind | Yes — resolve conflicts |
| 4. Confirm | Wait for user | Yes — wait |
| 5. Squash merge | `gh pr merge --squash` + cleanup | — |

## Rules

**Never:**
- Merge with failing CI
- Merge with CHANGES_REQUESTED
- Force-push to main/master directly
- Skip user confirmation (unless user explicitly opted out for the session)

**Always:**
- Squash merge
- Delete the branch after merge
- Sync locally after merge
- If no PR exists, redirect to `/open-pr`
