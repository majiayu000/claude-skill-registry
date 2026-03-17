---
name: resolve-main-conflicts
description: Resolve git merge or rebase conflicts when syncing a branch with main. Use when the user asks to resolve conflicts with main, merge main, rebase on main, fix merge conflicts, sync with main, or update branch from main.
---

# Resolve Conflicts with Main Branch

Sync the current branch with `main` and resolve any merge or rebase conflicts.

## Prerequisites

- Current branch is **not** `main` or `master` (if it is, create a feature branch first).
- Working directory is clean, or user is aware uncommitted changes may need stashing.

## Workflow

### Step 1: Confirm Branch and Status

```bash
git branch --show-current
git status
```

**If there are uncommitted changes**, **ALWAYS use the AskQuestion tool:**

- Title: "Uncommitted Changes Detected"
- Question: "You have uncommitted changes. How would you like to proceed?"
- Options:
  - id: "stash", label: "Stash them and continue"
  - id: "abort", label: "Abort, I'll commit them first"

Based on the response:

- "stash" → Run `git stash push -m "WIP before syncing with main"` and continue
- "abort" → Stop the workflow

### Step 2: Fetch Latest Main

```bash
git fetch origin main
```

Use `master` instead of `main` if the default branch is `master` in this repo.

### Step 3: Choose Merge vs Rebase

- **Merge**: Preserves full history, creates a merge commit. Safer for shared branches.
- **Rebase**: Linear history, no merge commit. Prefer for local/feature branches.

Default to **merge** unless the user asks for rebase or the project convention is rebase.

**Merge:**

```bash
git merge origin/main
```

**Rebase:**

```bash
git rebase origin/main
```

### Step 4: Detect Conflicts

If the command exits with a conflict (non-zero exit or message like "CONFLICT"):

```bash
git status
```

Note every file listed as "both modified" or "Unmerged paths".

### Step 5: Resolve Each Conflicted File

For each conflicted file:

1. **Open the file** and find conflict markers:
   - `<<<<<<< HEAD` (your branch)
   - `=======`
   - `>>>>>>> origin/main` (or commit hash)

2. **Decide the correct result**: keep one side, combine both, or write new content. Remove the markers and leave the intended final text.

3. **Stage the resolved file:**

   ```bash
   git add <path>
   ```

**If the user wants to accept one side entirely** for a file:

- Keep current branch version:
  ```bash
  git checkout --ours <path>
  git add <path>
  ```
- Keep main's version:
  ```bash
  git checkout --theirs <path>
  git add <path>
  ```

(For rebase, "ours" is the branch being rebased onto, "theirs" is the current branch—semantics are reversed vs merge. Prefer editing the file when unsure.)

### Step 6: Complete the Operation

**After merge:**

```bash
git status   # confirm no unmerged paths
git commit -m "Merge origin/main into <branch-name>"
```

**After rebase:**

```bash
git status   # confirm clean
git rebase --continue
```

If more conflicts appear, repeat from Step 4. To abort rebase:

```bash
git rebase --abort
```

### Step 7: Verify

```bash
git log --oneline -5
git status
```

Confirm history looks correct and working tree is clean.

## Optional: Restore Stash

If you stashed in Step 1:

```bash
git stash list
git stash pop
```

Resolve any stash conflicts the same way (edit markers, then `git add`).

## Safety Rules

- **Do not force push** to fix conflicts unless the user explicitly requests it (e.g. after rebase on a shared branch).
- **Do not run `git merge --abort` or `git rebase --abort`** unless the user asks to cancel the sync.
- Prefer resolving by editing files so the user sees and approves the result; use `--ours`/`--theirs` only when the user clearly wants one side entirely.
