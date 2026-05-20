---
name: apple-notes
description: Read Apple Notes content and execute checklist-driven automations in order. Use when a user asks to run tasks from an Apple Note (especially a checklist note like "AGENT TODO LIST"), or to fetch a specific note body for automation.
---

# Apple Notes

Run Apple Notes-driven automations with deterministic, sequential execution.

## Quick Start

```bash
scripts/run_checklist_note.sh "AGENT TODO LIST"
```

If no title is provided, the script defaults to `AGENT TODO LIST`.

## Fast Path: `run ToDos`

When the request is `run ToDos` (or `run todos`), execute the default checklist immediately:

```bash
scripts/run_checklist_note.sh "AGENT TODO LIST"
```

Skip preflight CRUD/search steps unless the user asks for them explicitly.

For direct Notes CRUD/search operations:

```bash
scripts/manage_notes.sh search --query "visionOS" --field any --limit 20
```

## Workflow

1. Resolve note by exact title across all Notes accounts/folders.
2. Extract checklist `<li>` items in source order and detect completion state.
3. Run only unchecked items (completed items are skipped).
4. Dispatch each unchecked item through natural shortcuts or skill routing.
5. After each successful action, mark that checklist item as completed in Notes.
6. Stop on first failure (non-zero exit).

## Checklist Syntax

- Natural shortcuts:
  - `Say <phrase>`
  - `Confetti`
  - `Record my screen for <N> seconds`
- Skill routing:
  - `<skill-name>: <args>`
  - Example: `open-meteo-weather: --location "Boston, MA"`
  - Example: `apple-reminders: today --json`
  - Example: `apple-notes: search --query "visionOS" --field any`

## Supported Skills Via `<skill-name>: <args>`

- `apple-notes`
- `apple-reminders`
- `bird-x`
- `browser-use`
- `confetti`
- `discord`
- `ffmpeg-video-editor`
- `git-search`
- `imsg`
- `launchd-non-apple-jobs`
- `mailapp-send-email`
- `open-meteo-weather`
- `openai-docs`
- `opml-reader`
- `playwright`
- `say`
- `screen-recorder`
- `swiftui-performance-audit`
- `video-transcript-downloader`
- `yahoo-finance`
- `youtube`
- `yt-video-downloader`
- `skill-creator`
- `skill-installer`

Tool-centric skills and skills missing required local CLIs are dispatched via `codex exec` fallback.

Matching is case-insensitive. Empty checklist lines are skipped.

## Apple Notes CRUD/Search

Use `scripts/manage_notes.sh` to create, read, update, delete, search, and list Apple Notes.

Examples:

```bash
scripts/manage_notes.sh create --title "My Note" --body "<div>Hello</div>"
scripts/manage_notes.sh read --title "My Note" --format plaintext
scripts/manage_notes.sh update --title "My Note" --title-new "My Renamed Note" --body "<div>Updated</div>"
scripts/manage_notes.sh search --query "Updated" --field any --limit 20
scripts/manage_notes.sh delete --title "My Renamed Note"
scripts/manage_notes.sh list --limit 50
```

## scripts/

- `run_checklist_note.sh`: Read an Apple Note and execute supported checklist items sequentially.
- `dispatch_skill_item.sh`: Dispatch one checklist item to a supported skill action.
- `manage_notes.sh`: Create, read, update, delete, search, and list Apple Notes.
- `manage_notes.applescript`: AppleScript backend used by `manage_notes.sh`.
