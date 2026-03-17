---
name: _util-changelog
description: Append a changelog entry to a note. Called by write skills after modifying files.
disable-model-invocation: true
allowed-tools: Read, Write
---

# Append Changelog Sub-Skill

Appends a timestamped changelog entry to a note file. Entries are reverse-chronological (newest first).

## Input Arguments

Arguments are passed as key-value pairs:
- `path`: Full path to the note file
- `skill`: Name of the skill making the change (e.g., "planning-daily")
- `action`: Verb summarizing the action (e.g., "Rewrote", "Added", "Updated")
- `sections`: Comma-separated list of section names affected (optional)
- `summary`: Additional context (optional)

## Instructions

Generate the current timestamp in format `YYYY-MM-DD HH:mm` (24-hour).

Build the changelog entry in this format: `- {timestamp} **{skill}** — {action}{sections_text}{summary_text}`, where sections_text includes section names if provided, and summary_text includes additional context if provided.

Read the existing content of the file. If the file doesn't exist, return an error indicating the file must exist before appending changelog entries.

Locate the `## Changelog` heading (case-insensitive). If the section exists, insert the entry at the top of the list after the heading, skipping any italicized placeholder text. If the section doesn't exist, append a new Changelog section at the end of the file.

Write the modified content back to the file.

Return structured output in a markdown code block:

**Success:**
```json
{
  "success": true,
  "path": "/path/to/note.md",
  "entry": "- `2026-02-15 09:32` **planning-daily** — Rewrote Focus section",
  "created_section": false
}
```

**Error:**
```json
{
  "success": false,
  "error": "write_failed",
  "message": "Failed to write changelog entry"
}
```

## Safety

- Always read before write to preserve existing content
- Never delete existing changelog entries
- Only append to the Changelog section
