---
name: atlas
description: >-
  Automate control of the ChatGPT Atlas desktop app on macOS via AppleScript.
  Manage tabs (list, open, close, focus, reload), search bookmarks, and query
  browsing history from Chromium-style local storage. Trigger when the user
  explicitly asks to control Atlas tabs, bookmarks, or history on macOS and the
  ChatGPT Atlas app is installed. Do not trigger for general browser tasks,
  non-macOS environments, or when the Atlas app is not present.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - automation
    - macos
    - applescript
    - browser
  provenance:
    upstream_source: "atlas"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:20:06+00:00"
    generator_version: "1.0.0"
    intent_confidence: 0.77
---

# Atlas Control (macOS)

Automate tab management, bookmark queries, and history search for the ChatGPT Atlas desktop app using a bundled Python CLI that drives AppleScript on macOS.

## Overview

This skill wraps the ChatGPT Atlas desktop application with a Python CLI (`atlas_cli.py`) that communicates via `osascript` (AppleScript) for window/tab control and reads Chromium-style local storage for bookmarks and history.

**What it automates:**
- Tab listing, opening, closing, focusing, and reloading across Atlas windows
- Bookmark retrieval with folder hierarchy and text search
- Browsing history queries with date filtering and keyword search
- Atlas app detection and AppleScript capability probing

**Prerequisites:**
- macOS with `osascript` on PATH
- ChatGPT Atlas installed in `/Applications` or `~/Applications`
- Automation permission granted in System Settings > Privacy & Security > Automation
- Python 3.12+ (invoked via `uv run --python 3.12`)

## Triggers

### When to Use

Invoke this skill when:
- The user asks to list, open, close, focus, or reload Atlas tabs
- The user wants to search or list Atlas bookmarks
- The user wants to query Atlas browsing history
- The user asks about Atlas app status or installed version

### When Not to Use

Do not invoke when:
- The user refers to a standard web browser (Chrome, Safari, Firefox)
- The environment is not macOS (AppleScript is unavailable)
- The user asks about ChatGPT the web app (not the Atlas desktop client)

## Process

### Step 1: Set Up the CLI Path

Resolve the path to `atlas_cli.py` relative to the skill installation directory:

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills/atlas}"
ATLAS_CLI="$SKILL_DIR/scripts/atlas_cli.py"
```

All CLI commands use `uv run --python 3.12 python "$ATLAS_CLI"` as the invocation prefix.

### Step 2: Verify Atlas Is Installed

```bash
uv run --python 3.12 python "$ATLAS_CLI" app-name
```

This prints `ChatGPT Atlas` if the app bundle exists in `/Applications` or `~/Applications`. If it fails, the user must install Atlas first.

### Step 3: Execute the Requested Operation

**Tab operations:**

```bash
# List all open tabs (table format)
uv run --python 3.12 python "$ATLAS_CLI" tabs

# List tabs as JSON (for programmatic processing)
uv run --python 3.12 python "$ATLAS_CLI" tabs --json

# Open a new tab
uv run --python 3.12 python "$ATLAS_CLI" open-tab "https://chatgpt.com/"

# Focus a specific tab (window_id and tab_index from tabs output)
uv run --python 3.12 python "$ATLAS_CLI" focus-tab <window_id> <tab_index>

# Close a tab
uv run --python 3.12 python "$ATLAS_CLI" close-tab <window_id> <tab_index>

# Reload a tab
uv run --python 3.12 python "$ATLAS_CLI" reload-tab <window_id> <tab_index>
```

**Bookmark operations:**

```bash
# List bookmarks (default limit: 200)
uv run --python 3.12 python "$ATLAS_CLI" bookmarks --limit 100

# Search bookmarks by text
uv run --python 3.12 python "$ATLAS_CLI" bookmarks --search "docs"

# Output as JSON
uv run --python 3.12 python "$ATLAS_CLI" bookmarks --search "openai" --json
```

**History operations:**

```bash
# Search history by keywords
uv run --python 3.12 python "$ATLAS_CLI" history --search "openai docs" --limit 50

# History for today only (local time)
uv run --python 3.12 python "$ATLAS_CLI" history --today --limit 200 --json

# Full history dump
uv run --python 3.12 python "$ATLAS_CLI" history --limit 500
```

## Verification

### Success Indicators

- `app-name` returns `ChatGPT Atlas` without error
- `tabs` produces a table with columns: `A`, `window_id`, `tab`, `title`, `url`
- `bookmarks` returns rows with: `folder`, `name`, `url`, `date_added`
- `history` returns rows with: `last_visited_at`, `title`, `url`
- Tab manipulation commands (`open-tab`, `focus-tab`, `close-tab`, `reload-tab`) print a confirmation message

### Failure Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `osascript is not available on PATH` | Not running macOS | This skill requires macOS; cannot run on Linux/Windows |
| `Could not find ChatGPT Atlas` | App not installed | Install ChatGPT Atlas from OpenAI |
| AppleScript error `-1743` | Missing Automation permission | Grant permission: System Settings > Privacy & Security > Automation |
| `does not appear to expose window/tab scripting` | Atlas version lacks AppleScript support | Update Atlas or check version compatibility |
| `SQLite database not found` | No browsing history yet | Open Atlas and browse pages first to populate history |
| `Local State file not found` | Atlas profile data missing | Launch Atlas at least once to create profile data |

## Data Paths

Atlas stores Chromium-style profile data under:

```
~/Library/Application Support/com.openai.atlas/browser-data/host/
```

Key locations:
- **Local State**: `browser-data/host/Local State` (JSON, contains `profile.last_used`)
- **History**: `browser-data/host/<profile>/History` (SQLite, table `urls`)
- **Bookmarks**: `browser-data/host/<profile>/Bookmarks` (JSON, Chromium format)

The active profile is resolved from `profile.last_used` in Local State, falling back to `Default`.

If history appears stale, check the beta data root as well:

```
~/Library/Application Support/com.openai.atlas.beta/browser-data/host/
```

The CLI copies the SQLite History database to a temporary location before querying to avoid lock contention with the running Atlas process.

## Examples

### Example 1: List Open Tabs and Find Duplicates

```
User: List all my Atlas tabs and call out duplicates.
Assistant: Let me list the open Atlas tabs.

[Runs: uv run --python 3.12 python "$ATLAS_CLI" tabs --json]

You have 12 tabs across 2 windows:

Window 1 (id: 4201):
  1. ChatGPT — https://chatgpt.com/
  2. OpenAI Docs — https://platform.openai.com/docs
  3. ChatGPT — https://chatgpt.com/  [DUPLICATE of tab 1]

Window 2 (id: 4205):
  1. GitHub — https://github.com/
  ...

Found 1 duplicate: "ChatGPT" appears in window 4201 tabs 1 and 3.
```

### Example 2: Search History for Recent Visits

```
User: What OpenAI pages did I visit today?
Assistant: Searching today's Atlas history for "openai"...

[Runs: uv run --python 3.12 python "$ATLAS_CLI" history --today --search "openai" --limit 50]

Today's OpenAI visits (3 results):
  2026-02-04 09:12  OpenAI Platform Docs    https://platform.openai.com/docs
  2026-02-04 10:45  API Reference           https://platform.openai.com/docs/api-reference
  2026-02-04 14:30  Pricing                 https://openai.com/pricing
```

### Example 3: Close a Specific Tab

```
User: Close the pricing tab.
Assistant: I'll find and close that tab.

[Runs: uv run --python 3.12 python "$ATLAS_CLI" tabs --json]
Found "Pricing" at window_id=4205, tab_index=3.

[Runs: uv run --python 3.12 python "$ATLAS_CLI" close-tab 4205 3]
Closed window id 4205, tab 3.
```

## Safety

### Idempotency

Tab listing, bookmark queries, and history searches are read-only and fully idempotent. Tab manipulation operations (open, close, focus, reload) are not idempotent:
- `close-tab` on an already-closed tab raises an AppleScript error
- `open-tab` creates a new tab each time it runs

### Reversibility

- Closed tabs cannot be reopened to the same position (use `open-tab` with the URL)
- Bookmark and history queries are read-only and leave no side effects
- Tab focus changes are immediately reversible by focusing a different tab

### Prerequisites Checklist

- [ ] Running on macOS
- [ ] ChatGPT Atlas installed in `/Applications` or `~/Applications`
- [ ] Terminal has Automation permission for Atlas in System Settings
- [ ] Python 3.12+ available via `uv`

## CLI Reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `app-name` | (none) | Print detected Atlas app name |
| `tabs` | `--json` | List open tabs across all windows |
| `open-tab` | `<url>` | Open a new tab with the given URL |
| `focus-tab` | `<window_id> <tab_index>` | Bring a tab to focus |
| `close-tab` | `<window_id> <tab_index>` | Close a specific tab |
| `reload-tab` | `<window_id> <tab_index>` | Reload a specific tab |
| `bookmarks` | `--search <text> --limit <n> --json` | List or search bookmarks |
| `history` | `--search <text> --today --limit <n> --json` | Search browsing history |

## Notes

- The `window_id` and `tab_index` values come from the `tabs` command output. Always list tabs first before operating on specific ones.
- History timestamps use Chrome's epoch (microseconds since 1601-01-01). The CLI converts them to local time automatically.
- The `--json` flag on `tabs`, `bookmarks`, and `history` outputs machine-readable JSON arrays for programmatic processing.
