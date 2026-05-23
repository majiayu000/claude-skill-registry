---
version: 1.0.0
name: tool-agentsandbox-merge
description: >
  Merge agentsandbox session work back into the current branch. Reviews changes made
  by Claude in a agentsandbox worktree, presents a diff summary, and merges (or
  cherry-picks) commits into the target branch. Run from the target branch (e.g. main).
  Use when the user says "merge agentsandbox", "merge cb", "pull in cb work", or
  invokes /tool-agentsandbox-merge.
disable-model-invocation: true
user-invocable: true
argument-hint: "[session-name] [--review | --merge | --cherry-pick | --squash]"
---

# Agentsandbox Merge

Merge work from a agentsandbox session worktree into the current branch.

> **Workflow:** `cb <session>` creates a worktree on branch `agentsandbox/<source>-<session>`.
> This skill merges that branch back into the current branch after review.

## When to Use

- After a `cb` (agentsandbox) session produced useful code changes
- When you want to review and selectively merge agentsandbox work
- When you need to squash agentsandbox commits into a clean history

## Prerequisites

- You are on the **target branch** (e.g., `main`, `feature-x`)
- The agentsandbox session has committed work on its branch
- The agentsandbox worktree still exists (not yet cleaned up with `cbc`)

## Step 1: Identify Session

If no session name provided, discover available agentsandbox sessions:

```bash
# List agentsandbox branches
git branch --list "agentsandbox/*" | sed 's/^[* ]*//'

# Or list agentsandbox task dirs
ls -1 ~/Repository/agentsandbox/ 2>/dev/null
```

Present the list and ask the user to pick one. Show for each:
- Branch name
- Commit count ahead of current branch
- Last commit message and date

```bash
# For each agentsandbox branch, show summary
for branch in $(git branch --list "agentsandbox/*" --format="%(refname:short)"); do
  ahead=$(git rev-list --count HEAD.."$branch" 2>/dev/null || echo 0)
  last_msg=$(git log -1 --format="%s (%ar)" "$branch" 2>/dev/null)
  echo "  $branch  ↑$ahead  $last_msg"
done
```

## Step 2: Review Changes

Show what the agentsandbox session produced:

```bash
CB_BRANCH="agentsandbox/<source>-<session>"

# Commit log
git log --oneline HEAD.."$CB_BRANCH"

# Full diff summary
git diff --stat HEAD..."$CB_BRANCH"

# File-by-file changes
git diff HEAD..."$CB_BRANCH"
```

Present a summary:

```
AGENTSANDBOX SESSION REVIEW — {session-name}
==========================================
Branch: {CB_BRANCH}
Commits: {count} ahead of {current branch}
Files changed: {count}

Commits:
  abc1234  Add user profile endpoint
  def5678  Add profile tests
  ghi9012  Fix validation edge case

Files:
  M  src/Api/Endpoints/ProfileEndpoints.cs
  A  src/Api/Models/ProfileRequest.cs
  A  tests/Api.Tests/ProfileEndpointTests.cs

Options:
  [m]erge     — merge all commits (preserves history)
  [s]quash    — squash into single commit
  [c]herry    — cherry-pick specific commits
  [d]iff      — show full diff for review
  [q]uit      — cancel
```

Wait for user input.

## Step 3: Apply Changes

### Option: Merge (default)

```bash
# Merge the agentsandbox branch
git merge "$CB_BRANCH" --no-ff -m "Merge agentsandbox session: $SESSION_NAME"
```

If merge conflicts occur:
1. List conflicted files
2. For each conflict, show the diff and ask the user how to resolve
3. After all resolved: `git add` and `git merge --continue`

### Option: Squash

```bash
# Squash merge — all commits become one
git merge --squash "$CB_BRANCH"

# Commit with a summary message
git commit -m "feat: <description from user or generated from commit messages>"
```

### Option: Cherry-pick

Show the commit list with numbers and let the user pick:

```bash
# List commits
git log --oneline HEAD.."$CB_BRANCH" | nl

# Cherry-pick selected commits
git cherry-pick <commit-hash>
```

## Step 4: Verify

After merge/squash/cherry-pick:

```bash
# Build
dotnet build 2>&1 | tail -10

# Tests
dotnet test 2>&1 | tail -20
```

If verification fails, offer to:
1. Fix the issues
2. Revert the merge: `git reset --hard HEAD~1`

## Step 5: Cleanup Prompt

After successful merge:

```
Merge complete. The agentsandbox worktree and branch are still around.

  cleanup?  [y]es — remove worktree + branch + task dir
             [n]o  — keep for reference
             [b]ranch only — remove worktree, keep branch
```

### Cleanup: Yes

```bash
SESSION="<session-name>"
CB_BRANCH="agentsandbox/<source>-<session>"
REPO_ROOT="$(git rev-parse --show-toplevel)"

# For bare+worktree repos, go up one level
if [[ -f "$REPO_ROOT/../.bare" || -f "$REPO_ROOT/../.git" ]]; then
  REPO_ROOT="$(cd "$REPO_ROOT/.." && pwd)"
fi

WT_DIR="$REPO_ROOT/agentsandbox-$SESSION"

# Remove worktree
git worktree remove --force "$WT_DIR" 2>/dev/null

# Delete branch
git branch -D "$CB_BRANCH" 2>/dev/null

# Prune stale worktree metadata
git worktree prune

# Remove task dir
rm -rf "$HOME/Repository/agentsandbox/$SESSION"

echo "Cleaned up session: $SESSION"
```

### Cleanup: Branch Only

```bash
# Remove worktree but keep the branch
git worktree remove --force "$WT_DIR" 2>/dev/null
git worktree prune
rm -rf "$HOME/Repository/agentsandbox/$SESSION"
```

## Flags

| Flag | Behavior |
|------|----------|
| `--review` | Show changes only, don't merge (default if no flag) |
| `--merge` | Merge with merge commit (preserves history) |
| `--squash` | Squash all commits into one |
| `--cherry-pick` | Interactive cherry-pick |

## Multi-Repo Sessions

Agentsandbox sessions can span multiple repos (via `workspace.json`). The `.repos` file in the task dir lists all involved repos:

```bash
cat "$HOME/Repository/agentsandbox/$SESSION/.repos"
```

For multi-repo sessions, repeat Steps 2-4 for each repo. Present a combined review first, then merge repo by repo.

## Edge Cases

- **No commits on agentsandbox branch:** Nothing to merge — report and exit
- **Source branch diverged:** Show divergence and recommend `--squash` or rebase
- **Worktree already removed:** Can still merge if branch exists — use branch directly
- **Uncommitted changes in worktree:** Warn and ask if they should be committed first
