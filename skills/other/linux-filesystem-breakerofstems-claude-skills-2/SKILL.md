---
name: linux-filesystem
description: Filesystem operations within workspace boundaries
---

# Linux Filesystem Skill

Safe filesystem operations bounded to workspace directories.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Navigate, read, and modify files within designated workspace directories.

## Commands

```bash
ls <path>
cat <file>
head <file>
tail <file>
grep <pattern> <path>
find <path> <options>
mkdir -p <path>
cp <source> <dest>
mv <source> <dest>
rm <file>
rm -r <directory>
```

## Workspace Boundary

**All operations restricted to**: `~/workspace/` and subdirectories

Before any operation, verify path is within bounds:
```bash
realpath /path/to/target | grep -q "^$HOME/workspace/" || echo "UNSAFE PATH"
```

## Workflow Examples

### Find Files

```bash
# Find by name
find ~/workspace/project -name "*.py" -type f

# Find recently modified
find ~/workspace/project -type f -mtime -1

# Find by content
grep -r "TODO" ~/workspace/project/
```

### Read Files

```bash
# Full file
cat ~/workspace/project/config.json

# First/last lines
head -20 ~/workspace/project/logs/app.log
tail -50 ~/workspace/project/logs/app.log

# Follow logs
tail -f ~/workspace/project/logs/app.log
```

### Modify Files

```bash
# Create directory
mkdir -p ~/workspace/project/src/utils

# Copy files
cp ~/workspace/project/config.example.json ~/workspace/project/config.json

# Move/rename
mv ~/workspace/project/old-name.py ~/workspace/project/new-name.py
```

### Delete (Use with Caution)

```bash
# Single file
rm ~/workspace/project/temp.txt

# Directory (show contents first)
ls ~/workspace/project/build/
rm -r ~/workspace/project/build/
```

## Policies

- **Verify path** is within workspace before any write/delete operation
- **List before delete** - always show what will be removed
- **No symlink escape** - verify symlinks don't point outside workspace
- **No `..` traversal** that escapes workspace
- Use `-i` flag for interactive confirmation on destructive operations when uncertain
