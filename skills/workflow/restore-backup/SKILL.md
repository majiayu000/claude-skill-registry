---
name: restore-backup
description: Restores the project from a specified backup directory.
---

# Restore Backup Skill

This skill allows you to restore the project files from a previously created backup directory.

## Capabilities

- Restores files from a source backup directory to the current workspace.
- Uses `rsync` to efficiently copy files and preserve permissions.
- Automatically excludes `.git` and `node_modules` from the restore process (keeps the current ones if the backup doesn't have them, or prevents overwriting them if it does).

## Usage

Run the python script with the path to the backup directory:

```bash
python .agent/skills/restore-backup/scripts/restore.py <BACKUP_PATH>
```

## Example

```bash
python .agent/skills/restore-backup/scripts/restore.py /path/to/backup_full_2023...
```
