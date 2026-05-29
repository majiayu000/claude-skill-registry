---
name: specstory-organize
description: Organize SpecStory AI coding sessions in .specstory/history into year/month folders. Run when user says "organize my history", "clean up specstory", "sort my sessions", or "organize specstory files".
license: Apache-2.0
metadata:
  author: SpecStory, Inc.
  version: "1.0.0"
  argument-hint: "[--dry-run]"
allowed-tools: Bash, Read
---

# SpecStory Organize

Organizes your `.specstory/history` directory by moving session files into `YYYY/MM/` subdirectories based on the timestamp in each filename.

## How It Works

1. **Scans** `.specstory/history/` for markdown files
2. **Extracts** the date from filenames (e.g., `2026-01-22_19-20-56Z-fix-bug.md`)
3. **Creates** year/month folders (e.g., `2026/01/`)
4. **Moves** files into the appropriate subdirectory
5. **Reports** what was moved

## Why Organize?

Over time, your history directory can accumulate hundreds of session files. Organizing by date makes it easier to:
- Find sessions from a specific time period
- Archive old sessions
- Keep your project directory clean

## Usage

### Slash Command

| User says | Action |
|-----------|--------|
| `/specstory-organize` | Organize all files (default) |
| `/specstory-organize dry run` | Preview changes without moving |
| `/specstory-organize --dry-run` | Preview changes without moving |

### Direct Script Usage

```bash
# From project root
python skills/specstory-organize/scripts/organize.py

# Preview what would be moved (no changes made)
python skills/specstory-organize/scripts/organize.py --dry-run
```

## Output

```
SpecStory History Organizer
===========================

Found 47 files to organize in .specstory/history/

Moving files:
  2026-01-15_10-30-22Z-refactor-auth.md -> 2026/01/
  2026-01-15_14-22-01Z-fix-tests.md -> 2026/01/
  2026-01-22_19-20-56Z-add-feature.md -> 2026/01/
  2025-12-28_09-15-33Z-cleanup.md -> 2025/12/
  ...

Summary:
--------
Files moved: 47
  2026/01/: 23 files
  2025/12/: 18 files
  2025/11/: 6 files

Your history is now organized!
```

## Dry Run Output

When using `--dry-run`:

```
SpecStory History Organizer (DRY RUN)
=====================================

Would organize 47 files in .specstory/history/

Preview:
  2026-01-15_10-30-22Z-refactor-auth.md -> 2026/01/
  2026-01-15_14-22-01Z-fix-tests.md -> 2026/01/
  ...

No files were moved. Run without --dry-run to apply changes.
```

## Present Results to User

After running the organize script:

1. **Confirm success** - Tell the user how many files were organized
2. **Show the breakdown** - List how many files went to each month
3. **Note any skips** - If files couldn't be parsed (no date in filename), mention them

### Example Response

```
Done! I organized 47 session files in your `.specstory/history/` directory:

- **2026/01/**: 23 files
- **2025/12/**: 18 files
- **2025/11/**: 6 files

Your history files are now sorted by year and month, making it much easier
to find sessions from specific time periods.
```

## Notes

- Files without a recognizable date pattern in the filename are skipped
- The script uses the filename timestamp, not the file's modification time
- Already-organized files (in subdirectories) are not moved again
- Compatible with Python 2.7+ and Python 3.x
