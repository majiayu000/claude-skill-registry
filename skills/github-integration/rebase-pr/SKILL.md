---
name: rebase-pr
description: Rebase a PR on its base branch, fix conflicts, and verify build
argument-hint: <PR number>
---

# Rebase PR

Simple workflow to rebase a PR on its base branch, resolve conflicts, and push.

## Usage

```
/rebase-pr 19882
```

## Workflow

### Step 1: Validate PR

```bash
gh pr view <PR> --repo AztecProtocol/aztec-packages --json state,headRefName,baseRefName
```

**Abort if:**
- `state` is not `OPEN` → "PR #\<N> is \<state>, nothing to rebase."

Note the `baseRefName` (usually `next` or `merge-train/*`).

### Step 2: Checkout and Rebase

```bash
gh pr checkout <PR>
git fetch origin <base-branch>
git rebase origin/<base-branch>
```

### Step 3: Resolve Conflicts (if any)

If there are conflicts:

1. **Identify conflicting files**:
   ```bash
   git status
   ```

2. **Resolve each conflict**: Edit the files to resolve conflicts

3. **Stage resolved files**:
   ```bash
   git add <resolved-file>
   ```

4. **Continue rebase**:
   ```bash
   git rebase --continue
   ```

5. **Repeat** until rebase completes

**Important**: Always REBASE, never merge.

### Step 4: Bootstrap (if needed)

Check if changes exist outside `yarn-project`:
```bash
git diff origin/<base-branch>...HEAD --name-only | grep -v '^yarn-project/'
```

If yes, run bootstrap from repo root:
```bash
(cd $(git rev-parse --show-toplevel) && BOOTSTRAP_TO=yarn-project ./bootstrap.sh)
```

### Step 5: Verify Build

Run from `yarn-project`:

```bash
yarn build
```

If there are build errors from the rebase, fix them.

### Step 6: Quality Checklist

Format and lint ALL packages:

```bash
yarn format
yarn lint
```

### Step 7: Commit and Push

If there are changes from build fixes or conflict resolution, commit and push.

If the PR targets `next`, amend to keep it as a single commit:

```bash
git add .
git commit --amend --no-edit
git push --force-with-lease
```

Otherwise, create a normal commit:

```bash
git add .
git commit -m "fix: resolve rebase conflicts"
git push --force-with-lease
```

## Key Points

- **Rebase, don't merge**: Always use `git rebase`, never `git merge`
- **Amend only for PRs targeting `next`**: Other PRs use normal commits
- **Bootstrap when needed**: Only if there are changes outside yarn-project
- **Verify build**: Always run `yarn build` after rebase
- **Force push with lease**: Use `--force-with-lease` for safety
