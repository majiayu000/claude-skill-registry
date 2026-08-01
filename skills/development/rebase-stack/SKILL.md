---
name: rebase-stack
description: Use this skill when working with stacked diffs (Branch B based on Branch
  A, which is based on main).
---

# Rebase Stacked Diffs

Use this skill when working with stacked diffs (Branch B based on Branch A, which is based on main).

## Scenarios

This skill covers two scenarios:

1. **Base branch updated**: Branch A got new commits (e.g., from PR review feedback), and Branch B needs to incorporate those changes
2. **Base branch merged**: Branch A was merged to main, and Branch B needs to be rebased onto main

---

## Scenario 1: Rebase onto Updated Base Branch

Use when Branch A (the base) has new commits and Branch B needs to be updated to include them.

### When to Use

- Branch A has new commits (PR feedback, fixes, etc.)
- Branch B was based on an older version of Branch A
- You want Branch B to include Branch A's latest changes
- Branch A has NOT been merged to main yet

### Workflow

#### 1. Identify the Branches

```bash
# You should be on Branch B
git branch --show-current

# Fetch latest
git fetch origin

# See Branch A's recent commits
git log --oneline origin/branch-a -10
```

#### 2. Find the Original Base Point

Find where Branch B originally diverged from Branch A:

```bash
# This shows the commit where Branch B was created from Branch A
git merge-base HEAD origin/branch-a
```

#### 3. Rebase Using --onto

The `--onto` flag lets you transplant Branch B's unique commits onto the updated Branch A:

```bash
# Syntax: git rebase --onto <new-base> <old-base> <branch>
git rebase --onto origin/branch-a $(git merge-base HEAD origin/branch-a) HEAD
```

Or if you know the old base commit:

```bash
git rebase --onto origin/branch-a <old-base-commit> HEAD
```

#### 4. Resolve Any Conflicts

If Branch A's changes conflict with Branch B's changes:

1. Resolve the conflicts in the affected files
2. Stage: `git add <files>`
3. Continue: `git rebase --continue`

#### 5. Force Push

```bash
git push --force-with-lease origin branch-b
```

### Example

```bash
# On branch-b, which was based on branch-a at commit abc123
# branch-a now has new commits

$ git fetch origin
$ git rebase --onto origin/branch-a abc123 HEAD
Successfully rebased and updated refs/heads/branch-b.

$ git push --force-with-lease origin branch-b
```

### Alternative: Simple Rebase

If Branch B hasn't diverged much and you're okay with a linear history:

```bash
git rebase origin/branch-a
```

This works well when Branch A only added commits (no force-pushes or rebases).

---

## Scenario 2: Rebase onto Main After Base Merges

Use when Branch A has been merged to main, and Branch B needs to be rebased onto main (removing the now-redundant Branch A commits).

### When to Use

- Branch B was created from Branch A (not main)
- Branch A has been merged to main
- Branch B now shows as "diverged" from its remote
- PR for Branch B shows merge conflicts or "CONFLICTING" status
- `git log` shows commits from Branch A in Branch B's history

### Workflow

#### 1. Verify the Situation

```bash
# Check current branch status
git status

# See how the branch relates to main
git log --oneline --graph HEAD~20..HEAD

# Check if the PR is in a conflicting state
gh pr view --json mergeable,mergeStateStatus
```

If you see `"mergeStateStatus": "DIRTY"` or `"mergeable": "CONFLICTING"`, proceed.

#### 2. Fetch Latest and Start Rebase

```bash
git fetch origin main

# Start rebase onto main
git rebase origin/main
```

#### 3. Handle Already-Merged Commits

When git tries to apply commits that are already in main (via the merged base branch), you'll see conflicts. These commits should be **skipped**, not resolved.

**Signs a commit should be skipped:**
- The commit message matches one from the merged PR
- Git shows "patch contents already upstream"
- Conflicts are in files that were part of the base branch's changes

**For each conflicting commit that was already merged:**

```bash
git rebase --skip
```

**Git will automatically drop some commits** with messages like:
```
dropping abc123 Some commit message -- patch contents already upstream
```

This is expected and correct.

#### 4. Resolve Genuine Conflicts

If you encounter a conflict in code that is genuinely new to this branch:

1. Check if the conflict is from your branch's unique changes
2. Resolve the conflict manually
3. Stage the resolution: `git add <files>`
4. Continue: `git rebase --continue`

#### 5. Force Push the Rebased Branch

```bash
git push --force-with-lease origin <branch-name>
```

#### 6. Verify PR Status

```bash
gh pr view --json mergeable,mergeStateStatus
gh pr checks
```

The PR should now show:
- `"mergeable": "MERGEABLE"`
- `"mergeStateStatus": "BLOCKED"` (waiting for CI) or `"CLEAN"` (ready to merge)

### Example

```
$ git rebase origin/main
Rebasing (1/15)
CONFLICT (content): Merge conflict in src/feature.py
error: could not apply abc123... Add feature from base branch

# This commit was part of the base branch - skip it
$ git rebase --skip

Rebasing (2/15)
dropping def456 Another base branch commit -- patch contents already upstream
Rebasing (3/15)
...
Successfully rebased and updated refs/heads/my-branch.

$ git push --force-with-lease origin my-branch
```

---

## Troubleshooting

### "Would make commit empty"
The commit's changes are already in the target branch. Skip it:
```bash
git rebase --skip
```

### Accidentally resolved instead of skipping
If you resolved a conflict that should have been skipped:
```bash
git rebase --abort
# Start over
git rebase origin/main  # or origin/branch-a
```

### Not sure if commit should be skipped
Check if the commit exists in the target:
```bash
# Get the commit message from the conflict
git log --oneline -1 REBASE_HEAD

# Search for similar commits in main
git log --oneline origin/main | grep "<keywords from commit>"
```

### Lost track of the old base commit
If you don't know where Branch B originally diverged from Branch A:
```bash
# Look at the reflog to find when you created the branch
git reflog show branch-b | tail -5

# Or find common ancestors
git merge-base branch-b origin/branch-a
```

### Rebase got messy, start over
```bash
git rebase --abort
git reset --hard origin/branch-b  # Reset to remote state
# Try again
```

## Notes

- Always use `--force-with-lease` instead of `--force` when pushing
- The `--onto` flag is powerful for transplanting commits between branches
- After rebasing onto main (Scenario 2), Branch B should have fewer commits than before
- Consider using `git rebase -i` (interactive) if you need fine-grained control over which commits to keep
