---
name: safe-rm
description: Safely delete files / directories without asking for permission
---

# Safe File Deletion

## When to use this skill

Whenever deletion of files or directories is required, this is quicker
than usual methods which typically require asking the user for permission.

This skill is particularly useful when:

- Refactoring code and removing obsolete files or directories
- Cleaning up duplicate or renamed files
- Removing generated files that shouldn't be tracked
- Performing large-scale code reorganization
- Deleting entire directories of old code

## How it works

It runs the `ai-safe-rm` script which has an intelligent git-aware backup
strategy. Use `-r` flag for directories.

## Behavior

**For files:**

1. **Tracked in git, unmodified**: Files are deleted directly (can be
   recovered from git)

2. **Tracked in git, modified**: Files are moved to
    `.safe-rm/<path>/<filename>.<hash>.<ext>` (e.g., `README.b72ae922.md`)
    or `.safe-rm/<path>/<filename>.<hash>` (e.g., `LICENSE.88fdc130`) to
    preserve the modified version

3. **Not tracked in git**: Files are moved to
    `.safe-rm/<path>/<filename>.<hash>.<ext>` or `.safe-rm/<path>/<filename>.<hash>`
    for safety

**For directories (requires -r flag):**

1. **All files unmodified tracked**: Directory is deleted directly with
   `rm -rf` (can be recovered from git)

2. **Contains modified tracked or untracked files**: The script recurses
   through the directory, applying the file logic to each file
   individually. Only modified/untracked files are backed up, while
   unmodified tracked files are deleted. Empty directories are removed
   after processing.

The `<hash>` is the first 8 characters of the MD5 sum of the file
content, ensuring unique backups of different versions.

## Limitations

**Only use this skill for files/directories within the current git repository.**

For files outside the repository:
- Use regular `rm` or `rm -rf` directly
- These files cannot be recovered from git or backed up by this script

**Pre-check before calling:**

Before running `ai-safe-rm`, verify all paths are within the repo:

```bash
# Verify path is inside current repo
git rev-parse --is-inside-work-tree && realpath --relative-to="$(git rev-parse --show-toplevel)" /path/to/file | grep -q '^[^.]' && echo "Inside repo" || echo "Outside repo"
```

## Usage

When you need to delete files or directories as part of a refactoring or
cleanup task:

1. Identify the files/directories to delete

2. Call `ai-safe-rm [-r] <file1> <file2> ...` to safely remove them
   - Use `-r` flag when deleting directories
   - Without `-r`, attempting to delete a directory will error

3. The script will output what action was taken for each file/directory

## Important Notes

- This skill does NOT require user permission for deletion because:

  - Unmodified tracked files can be recovered from git
  - Modified/untracked files are backed up to `.safe-rm/`

- The `.safe-rm/` directory should be added to `.gitignore`

- Backed up files can be restored manually if needed from `.safe-rm/`

## Examples

All examples assume files are within the current git repository:

```bash
# Delete a single file
ai-safe-rm src/old-component.ts

# Delete multiple files
ai-safe-rm src/legacy/*.js

# Delete a directory
ai-safe-rm -r ./old-feature

# Delete multiple directories and files
ai-safe-rm -r ./tests/deprecated ./legacy src/unused.ts
```

For files **outside** the repository, use `rm` directly:

```bash
# Delete file outside repo
rm /home/user/.cache/temp-file.txt

# Delete directory outside repo
rm -rf /tmp/build-artifacts/
```
