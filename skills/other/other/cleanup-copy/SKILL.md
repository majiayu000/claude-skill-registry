---
name: cleanup-copy
description: Delete an isolated project copy after changes have been merged back. Use after merge-back is complete.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Cleanup Copy

Safely removes a forked project copy and cleans up any remaining git references.

## What it does

1. **Validates** the copy exists
2. **Warns** if changes haven't been merged back (no `merge/<feature-name>` branch found)
3. **Warns** if there are uncommitted changes in the copy
4. **Removes** any leftover temporary remote in the original project
5. **Deletes** the copy directory
6. **Lists** remaining copies (if any)

## Usage

```
/cleanup-copy <feature-name>
```

## How to execute

**This must be run from the ORIGINAL project directory** (not the copy).

```bash
bash .claude/skills/cleanup-copy/scripts/cleanup-copy.sh "<feature-name>"
```

## Important

- Always run `/merge-back` BEFORE `/cleanup-copy` to avoid losing work
- The script warns about unmerged changes but proceeds with deletion
- If you need to keep the copy, simply don't run this command
- Shows remaining copies after cleanup so you know what's still active
