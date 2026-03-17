---
name: watching-filesystem
description: |
  Monitor a drop folder for new files using watchdog. Categorizes files by type
  and creates task files with suggested actions. Use when setting up file monitoring.
---

# Filesystem Watcher Skill

Monitors DropFolder for new files and creates task files.

## Quick Start

```bash
python scripts/run.py
```

## Configuration

- `WATCH_FOLDER` - Folder to monitor (default: DropFolder/)
- `FILE_DEBOUNCE` - Wait seconds before processing (default: 5)
- `DRY_RUN` - Test mode (default: false)

## Supported File Types

Documents, Spreadsheets, Images, Emails, Archives, Presentations

## Verification

Run: `python scripts/verify.py`
