---
name: archive-cleanup
description: Automatically archive old documents from active/daily/ to archive/ based on file age. Archives files older than specified days into archive/YYYY-MM/ directories.
---

# Archive Cleanup Skill

Archive old documents to keep active workspace clean.

## Usage

```bash
# Basic usage (current directory)
bash scripts/archive-cleanup.sh

# With custom workspace
WORKSPACE_DIR=/path/to/workspace bash scripts/archive-cleanup.sh

# With custom age threshold (days)
ARCHIVE_AGE_DAYS=14 bash scripts/archive-cleanup.sh

# Full customization
WORKSPACE_DIR=/data ARCHIVE_AGE_DAYS=30 DAILY_DIR=notes ARCHIVE_DIR=backup bash scripts/archive-cleanup.sh
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKSPACE_DIR` | `.` (current directory) | Base workspace directory |
| `DAILY_DIR` | `active/daily` | Source directory to scan |
| `ARCHIVE_DIR` | `archive` | Target archive directory |
| `ARCHIVE_AGE_DAYS` | `7` | Days before archiving |

## Archive Logic

- Scans `$DAILY_DIR` for `*.md` files
- Archives files modified more than `$ARCHIVE_AGE_DAYS` days ago
- Organizes archives into `$ARCHIVE_DIR/YYYY-MM/` based on filename date
