---
name: bl-record
description: Record changes as a new commit in git-branchless workflow
argument-hint: "[-m <message>] [--create-branch]"
---

# /bl-record - Git-Branchless Record

**Category:** Git Workflow

Record staged/unstaged changes as a new commit using git-branchless. Optionally create a branch for the commit.

## Usage

```
/bl-record [-m <message>] [--create-branch]
```

## Options

| Option | Description |
|--------|-------------|
| `-m <message>` | Commit message (required) |
| `--create-branch` | Create a branch for PR submission (uses `-c` flag) |

## Examples

```bash
# Record with message
/bl-record -m "feat: add user validation"

# Record and create branch for PR
/bl-record -m "fix: handle null input" --create-branch
```

## Execution Instructions

1. **Check Prerequisites**
   - Verify git-branchless is installed
   - Verify repository is initialized for branchless
   - Check we're in detached HEAD state

2. **Stage Changes (if needed)**
   - Run `git status` to check for changes
   - If unstaged changes exist, run `git add -A` to stage all

3. **Record the Commit**
   - If `--create-branch` is provided:
     ```bash
     git branchless record -c -m "<message>"
     ```
     Then immediately return to detached HEAD:
     ```bash
     git checkout --detach
     ```
   - Otherwise:
     ```bash
     git branchless record -m "<message>"
     ```

4. **Show Result**
   - Run `git sl` to display the updated stack
   - Confirm the new commit was added

## Flow Examples

```
User: /bl-record -m "feat: add user model"

Agent: Recording changes...

Staged changes:
  A src/models/user.py
  M src/models/__init__.py

Running: git branchless record -m "feat: add user model"

◆ abc1234 (main) initial commit
┃
● def5678 feat: add user model  ← New commit

Commit recorded successfully.
```

```
User: /bl-record -m "fix: validate email" --create-branch

Agent: Recording changes with branch creation...

Staged changes:
  M src/validators.py

Running: git branchless record -c -m "fix: validate email"
Branch created: fix-validate-email

Returning to detached HEAD...
Running: git checkout --detach

◆ abc1234 (main) initial commit
┃
● ghi9012 fix: validate email (fix-validate-email)  ← New commit with branch

Commit recorded with branch for PR submission.
Use /bl-submit to push the branch.
```

## Error Handling

| Error | Resolution |
|-------|------------|
| No changes to record | Inform user there's nothing to commit |
| Not in detached HEAD | Warn and suggest `git checkout --detach` |
| git-branchless not installed | Provide installation command |
| Repo not initialized | Suggest `/bl-init` |

## Why Detach After Branch Creation?

When using `-c` to create a branch, git-branchless checks out that branch. We immediately detach again to maintain the branchless workflow where you work in detached HEAD and only create branches when submitting PRs.
