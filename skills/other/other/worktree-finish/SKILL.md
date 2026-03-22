---
name: worktree-finish
description: Merge a worktree feature branch into main and clean up the worktree. Use after finishing work in a worktree created by /worktree-start.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Worktree Finish

Brings changes from a feature worktree back into main, then removes the worktree and branch.

## What it does

1. **Validates** the worktree exists and has no uncommitted changes
2. **Runs checks** in the worktree (auto-detects test/check scripts)
3. **Merges** `work/<feature-name>` directly into `main`
4. **Removes** the worktree directory and deletes the branch
5. **Cleans up** `.worktrees/` dir if empty

## Usage

```
/worktree-finish <feature-name>
```

## How to execute

**This must be run from the ORIGINAL project directory** (not the worktree).

```bash
bash .claude/skills/worktree-finish/scripts/worktree-finish.sh "<feature-name>"
```

Where `<feature-name>` matches the name used with `/worktree-start`.

## Important

- The worktree must have all changes committed (no dirty working tree)
- Tests/checks are run in the worktree before merging — if they fail, the merge is aborted
- Merges directly into `main` (no intermediate review branch)
- If there are merge conflicts, the script stops and provides manual resolution steps
- Use `git reset --hard ORIG_HEAD` to undo the merge if needed
- The merge preserves full commit history from the worktree branch
- Unlike `merge-back`, no temporary remotes are needed — branch is already local
