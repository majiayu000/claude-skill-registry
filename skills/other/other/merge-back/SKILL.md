---
name: merge-back
description: Merge changes from an isolated project copy back to the original project. Use after finishing work in a forked copy.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Merge Back

Brings changes from a forked project copy back to the original project.

## What it does

1. **Validates** the copy exists and has no uncommitted changes
2. **Runs checks** (`pnpm check` or `pnpm test`) in the copy to ensure quality
3. **Adds** the copy as a temporary git remote in the original
4. **Merges** the copy's `work/<feature-name>` branch into a new `merge/<feature-name>` branch
5. **Cleans up** the temporary remote

## Usage

```
/merge-back <feature-name>
```

## How to execute

**This must be run from the ORIGINAL project directory** (not the copy).

```bash
bash .claude/skills/merge-back/scripts/merge-back.sh "<feature-name>"
```

Where `<feature-name>` matches the name used when running `/fork-project`.

## Important

- The copy must have all changes committed (no dirty working tree)
- Tests/checks are run in the copy before merging - if they fail, the merge is aborted
- If there are merge conflicts, the script stops and gives instructions for manual resolution
- After merging, you'll be on branch `merge/<feature-name>` - review before proceeding
- The merge preserves full commit history from the copy
