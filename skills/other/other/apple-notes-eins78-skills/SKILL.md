---
name: apple-notes
description: Read Apple Notes via AppleScript. Use when asked to check, search, or read notes. READ ONLY — no creating or modifying notes.
---

# Apple Notes (Read Only)

Read notes via Notes.app AppleScript. **No creating, updating, or deleting notes.**

## Prerequisites

- Notes.app running and synced
- Automation permissions granted (System Settings → Privacy & Security → Automation → Terminal/Claude Code → Notes)
- If first access attempt times out, ask user to check for macOS permission dialog

## Scripts

### List folders

```bash
${CLAUDE_SKILL_DIR}/scripts/list-folders.sh              # All folders across all accounts
${CLAUDE_SKILL_DIR}/scripts/list-folders.sh iCloud       # Only iCloud folders
```

### List notes in a folder

```bash
${CLAUDE_SKILL_DIR}/scripts/list-notes.sh                        # iCloud/Notes (default)
${CLAUDE_SKILL_DIR}/scripts/list-notes.sh "Shopping"             # iCloud/Shopping
${CLAUDE_SKILL_DIR}/scripts/list-notes.sh "Notes" "Gmail"        # Gmail/Notes
```

Output: `note name | modification date` (one per line)

### Read a note

```bash
${CLAUDE_SKILL_DIR}/scripts/read-note.sh "Shopping List"             # Search all accounts
${CLAUDE_SKILL_DIR}/scripts/read-note.sh "Meeting Notes" "iCloud"    # Specific account
```

Returns metadata header + HTML body.

### Search notes by name

```bash
${CLAUDE_SKILL_DIR}/scripts/search-notes.sh "recipe"                 # Search all accounts
${CLAUDE_SKILL_DIR}/scripts/search-notes.sh "recipe" "iCloud"        # Specific account
```

Output: `note name | account/folder | modification date` (one per line)

## Direct Commands

For quick one-off access without scripts:

```bash
# List all iCloud folders
osascript -e 'tell application "Notes" to get name of every folder of account "iCloud"'

# List all note names in a folder
osascript -e 'tell application "Notes" to get name of every note in folder "Notes" of account "iCloud"'

# Read a note body (returns HTML)
osascript -e 'tell application "Notes" to get body of note "Note Name"'

# Count all notes
osascript -e 'tell application "Notes" to count every note'
```

## Notes

- Note bodies are returned as **HTML** — use for display or pipe through a converter for plain text
- Note names are **case-sensitive** in AppleScript queries
- Searching large numbers of notes can be slow — scope to a specific account when possible
- The `whose name contains` filter is case-insensitive
- Notes.app must be running — scripts will launch it if needed, but sync may take a moment
