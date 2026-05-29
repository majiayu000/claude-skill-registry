---
name: safe-file-ops
description: Safely delete and manage files and folders. Uses git rm for git-tracked files, moves other files to .trash directory. Automatically applied when deletion operations are needed.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Safe File Operations

## Purpose

A skill for safely deleting files and folders. Git-tracked files are removed using `git rm` for safe version control removal, while non-tracked files are moved to the `.trash` directory for possible recovery.

## Core Principles

1. **Git-tracked files**: Use `git rm` for safe deletion (maintains version history)
2. **Non-tracked files**: Move to `.trash/` directory (recoverable)
3. **Safety**: Never permanently delete - keep in trash for recovery
4. **Auto-detection**: Automatically detect if files are git-tracked

## Use Cases

- When you need to delete files or folders
- When cleaning up folders that are no longer needed
- When deleting a mix of git-tracked and non-tracked files

## Workflow

### Step 1: Collect File/Folder List

Confirm the paths of files or folders the user wants to delete:

```
Please provide the paths of files or folders you want to delete.
(e.g., src/old-component.ts, tests/deprecated/, docs/draft.md)
```

### Step 2: Check Git Tracking Status

Check if each file/folder is tracked by Git:

```bash
# Check if file is tracked by git
git ls-files --error-unmatch <filepath>

# Check git-tracked files in folder
git ls-files <folderpath>
```

### Step 3: Separate Handling

**Git-tracked files**:
```bash
# Delete file (remove from staging area)
git rm <filepath>

# Delete folder (recursively)
git rm -r <folderpath>
```

**Non-tracked files**:
```bash
# Create .trash directory (if not exists)
mkdir -p .trash

# Move file (avoid path conflicts)
mv <filepath> .trash/

# Move folder
mv <folderpath> .trash/
```

### Step 4: Report Summary

Report the list of processed files and their locations:

```
✅ Git-tracked files (deleted with git rm):
  - src/old-component.ts
  - lib/deprecated/

✅ Non-tracked files (moved to .trash/):
  - cache/temp.dat
  - logs/old-logs/

📁 All preserved files: .trash/
```

## Examples

### Example 1: Delete Single File

```bash
# Input: "Delete src/utils/legacy.ts"

# Check git status
$ git ls-files --error-unmatch src/utils/legacy.ts
src/utils/legacy.ts  # Git-tracked file confirmed

# Execute deletion
$ git rm src/utils/legacy.ts
rm 'src/utils/legacy.ts'

✅ Removed src/utils/legacy.ts from git.
```

### Example 2: Delete Mixed Files/Folders

```bash
# Input: "Delete build/ folder and temp.dat file"

# Check git status
$ git ls-files build/
build/index.html    # Git-tracked
build/bundle.js     # Git-tracked

$ git ls-files --error-unmatch temp.dat
# (No output - non-tracked file)

# Separate handling
$ git rm -r build/
$ mkdir -p .trash
$ mv temp.dat .trash/

✅ Git-tracked files (deleted with git rm):
  - build/

✅ Non-tracked files (moved to .trash/):
  - temp.dat
```

## Important Notes

1. **No permanent deletion**: All files are kept in recoverable state
2. **Git commit required**: Files deleted with `git rm` need to be committed
3. **.trash management**: Periodically cleaning `.trash/` directory is recommended
4. **Path conflicts**: Files with same name in `.trash/` will be overwritten

## Clean Up .trash

To empty the `.trash` directory:

```bash
# Completely delete .trash directory
rm -rf .trash/

# Or delete only files older than 30 days
find .trash/ -type f -mtime +30 -delete
```

## Related Operations

- **Undo**: Recover git-tracked files with `git checkout HEAD -- <file>`
- **Commit**: Commit deletions with `git commit -m "Remove old files"`
- **Cleanup**: Periodic `.trash/` directory cleaning recommended

---

**Reference**: This skill is based on Claude Code official Skills documentation.
(https://code.claude.com/docs/en/skills)
