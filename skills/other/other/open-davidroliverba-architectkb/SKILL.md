---
name: open
context: fork
description: Open a note in Obsidian from Claude Code
model: haiku
---

# /open - Open in Obsidian

Opens a vault note in Obsidian directly from Claude Code.

## Usage

```
/open <note name>             # Open by name (fuzzy match)
/open daily                   # Open today's daily note
/open Concept - CAMO          # Open a specific note
/open Meeting - 2026-02-11    # Open by partial name
```

## Instructions

### 1. Resolve the Note

Determine what the user wants to open:

- **"daily" or "today"** — resolve to `Daily/YYYY/YYYY-MM-DD` using today's date
- **Exact filename** — use as provided
- **Partial name** — use Glob to find the matching file:

```bash
# Find by partial name
```

Use the Glob tool with pattern `**/*<name>*.md` to find the file. If multiple matches, pick the most likely one or ask the user.

### 2. Build the URI Path

Convert the file path to a URI-encoded relative path (from vault root):

- Strip the vault root prefix
- Strip the `.md` extension
- URL-encode spaces as `%20`
- URL-encode forward slashes as `%2F`

**Examples:**
- `Daily/2026/2026-02-11.md` → `Daily%2F2026%2F2026-02-11`
- `Concept - Context Engineering.md` → `Concept%20-%20Context%20Engineering`
- `Meetings/2026/Meeting - 2026-02-11 Stand Up.md` → `Meetings%2F2026%2FMeeting%20-%202026-02-11%20Stand%20Up`

### 3. Open in Obsidian

Run this command with `dangerouslyDisableSandbox: true` (required for inter-process communication):

```bash
open "obsidian://open?vault=BA-DavidOliver-ObsidianVault&file=<encoded_path>"
```

**The sandbox must be disabled** — the `open` command needs macOS Launch Services to activate Obsidian, which is blocked in sandbox mode.

### 4. Confirm

Tell the user which note was opened. If Obsidian is not running, the error will mention `procNotFound` — tell the user to start Obsidian first.

## Special Cases

| Input | Resolves To |
|-------|-------------|
| `daily` / `today` | `Daily/YYYY/YYYY-MM-DD` (today's date) |
| `yesterday` | `Daily/YYYY/YYYY-MM-DD` (yesterday's date) |
| A person's name | `People/<Name>.md` |
| A type prefix (e.g. `ADR - `) | Search in the appropriate folder |

## Troubleshooting

**"procNotFound" error**
→ Obsidian is not running. Ask the user to start it.

**"operation not permitted" error**
→ Sandbox was not disabled. Ensure `dangerouslyDisableSandbox: true` is set on the Bash call.

**Wrong note opened**
→ Multiple files matched. Use a more specific name or provide the full path.
