---
name: rebase
description: Rebase local changes on top of remote branch updates
argument-hint: "[--interactive]"
---

# rebase

**Category**: Development

## Usage

```bash
rebase [--interactive]
```

## Arguments

- `--interactive`: Use interactive rebase for more control over commits (optional)

## Description

Rebases your local commits on top of the latest remote changes for your active branch. This is useful when your colleague has pushed changes to the same branch and you want to incorporate them while keeping your commits on top.

## Execution Method

This command delegates to the `rebase-expert` agent (Haiku model) for fast execution.

**Delegation**: Use the Task tool with:
- `subagent_type`: `"git-workflow:rebase-expert"`
- `prompt`: Include the interactive flag if specified and current working directory

Example:
```
Task(subagent_type="git-workflow:rebase-expert", prompt="Run rebase in /path/to/repo")
```

---

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. **Verify Git State**
   - Check that we're in a git repository
   - Confirm the current branch is tracking a remote branch
   - Verify there are no uncommitted changes (offer to stash if needed)

2. **Fetch Latest Remote Changes**
   - Run `git fetch origin` to get the latest remote changes
   - Identify the tracking branch (e.g., `origin/main`)

3. **Check for Conflicts**
   - Run `git rebase --dry-run origin/<branch>` to detect potential conflicts
   - Warn user if conflicts are likely

4. **Execute Rebase**
   - Run `git rebase origin/<branch>` (or `git rebase -i` for interactive mode)
   - Monitor for conflicts during rebase
   - Provide guidance if conflicts occur

5. **Handle Conflicts (if any)**
   - Display conflicted files
   - Guide user through resolution
   - Verify rebase completion

6. **Confirm Success**
   - Show final commit log with new positions
   - Display summary of rebased commits

## Interactive Flow

### Step 1: Verify State

```
🔍 Checking repository state...

Current branch: feature/my-feature
Tracking branch: origin/feature/my-feature
Status: Clean (no uncommitted changes)
```

### Step 2: Fetch Remote Changes

```
📡 Fetching latest remote changes...

✅ Fetched successfully
Remote branch updated: origin/feature/my-feature
```

### Step 3: Check for Conflicts

```
🔎 Checking for potential conflicts...

✅ No conflicts expected
Your commits can be cleanly rebased on top of the remote changes.
```

### Step 4: Execute Rebase

```
⏳ Rebasing your changes...

Rebasing 3 commits...
✅ Successfully rebased!

Your commits are now on top of the latest remote changes.
```

### Step 5: Show Results

```
📊 Rebase complete!

New commit history:
  abc1234 (HEAD -> feature/my-feature) your third commit
  def5678 your second commit
  ghi9012 your first commit
  jkl3456 (origin/feature/my-feature) colleague's latest commit

Commits rebased: 3
```

## Conflict Handling

If conflicts occur during rebase:

```
⚠️  Conflicts detected during rebase!

Conflicted files:
  M  src/auth/login.py
  M  src/config.py

You can:
1. Resolve conflicts in your editor
2. Run `git add <file>` after resolving
3. Continue with `git rebase --continue`

Or abort with: git rebase --abort
```

## Error Handling

```
❌ Not in a git repository
   Navigate to a git repository and try again.

❌ Uncommitted changes detected
   Stash or commit your changes first:
   - `git stash` to temporarily save changes
   - `git add .` and `git commit` to commit them

❌ Current branch is not tracking a remote
   Set up tracking with: git branch -u origin/<branch>

❌ Rebase in progress
   Complete or abort the current rebase first:
   - `git rebase --continue` to complete
   - `git rebase --abort` to cancel
```

## When to Use Rebase vs Merge

**Use rebase when:**
- You want a linear commit history
- You're working on a feature branch with colleagues pushing updates
- You want your commits to appear on top of the latest changes

**Use merge when:**
- You want to preserve the complete history of both branches
- Multiple people are working on the same branch and you want a clear merge point
