---
name: daily-notes
description: Manages daily notes with M-D-YYYY format (e.g., 1-1-2026.md). Use when the user asks to view recent notes, create daily notes, read today's notes, summarize the week, or references @notes/ or dates. Can fetch last 7 days of notes. Notes location is configurable in Settings > Storage.
version: 1
---

# Daily Notes Management

## Overview

This skill manages daily notes stored in the workspace's notes directory using the `M-D-YYYY.md` format (e.g., `1-1-2026.md`, `12-31-2025.md`).

## Date Format

All daily notes follow this format:
- **Format**: `M-D-YYYY.md`
- **No leading zeros**: `1-1-2026.md` not `01-01-2026.md`
- **Examples**:
  - January 1, 2026 -> `1-1-2026.md`
  - December 31, 2025 -> `12-31-2025.md`
  - March 5, 2026 -> `3-5-2026.md`

## Getting the Notes Directory

The notes location is configurable in Settings > Storage. To get the correct path, query the workspace paths API:

```bash
curl http://localhost:1234/api/workspace/paths
# Returns: { "success": true, "data": { "notes": "/path/to/notes", ... } }
```

Or use `jq` to extract just the notes path:
```bash
NOTES_DIR=$(curl -s http://localhost:1234/api/workspace/paths | jq -r '.data.notes')
```

## CLI Usage

The skill provides a shell script. Set the `NOTES_DIR` environment variable to the workspace's notes path (obtained from the API above).

```bash
NOTES_DIR=/path/to/workspace/notes .claude/skills/daily-notes/daily-note.sh <command> [arguments]
```

### Commands

#### get-today
Get or create today's daily note.
```bash
./daily-note.sh get-today
```

#### get-note [date]
Get a specific date's note.
```bash
./daily-note.sh get-note 1-1-2026
```

#### get-last-x [duration]
Get notes from the last N days.
```bash
./daily-note.sh get-last-x 7days
./daily-note.sh get-last-x 30days
```

#### get-range [start] [end]
Get notes between two dates (ISO format).
```bash
./daily-note.sh get-range 2026-01-01 2026-01-07
```

## How Claude Should Use This Skill

**Important**: Always set the `NOTES_DIR` environment variable to the workspace's notes path before running the script.

### When User Asks About Recent Work
```
User: "What have I been working on this week?"
-> Run: NOTES_DIR=/path/to/notes ./daily-note.sh get-last-x 7days
-> Parse content and provide summary
```

### When User Wants to Add to Today's Note
```
User: "Add this to my daily note: Completed feature X"
-> Run: NOTES_DIR=/path/to/notes ./daily-note.sh get-today
-> Use Edit tool to append content
```

## Best Practices

1. **Always set NOTES_DIR** - Don't rely on the default path
2. **Handle missing notes gracefully** - Not every day has a note
3. **Preserve existing content** - Use Edit tool, not Write when modifying
4. **Support natural language dates** - Convert to `M-D-YYYY` format
