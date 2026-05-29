---
name: quill-cli
description: Use when exporting meeting notes or transcripts from Quill Meetings app, listing recent meetings, searching meeting history, or piping meeting data to other tools
---

# Quill CLI

Export meeting notes and transcripts from the Quill Meetings macOS app.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `quill list` | List recent meetings |
| `quill list --limit 50` | List more meetings |
| `quill list --since 7d` | Meetings from last 7 days |
| `quill list --search "standup"` | Filter by title |
| `quill export --latest --notes` | Export latest meeting notes |
| `quill export --latest --transcript` | Export latest transcript |
| `quill export "Meeting Title" --notes` | Export by title |
| `quill export abc123 --notes` | Export by ID (full or short) |

## Preferred Export Order

When exporting meetings, use this priority:
1. **First:** Try `--note-title "Eric Binnion"` (partial match finds notes prefixed with this)
2. **Fallback:** Use `--transcript` if no matching note exists

```bash
# Preferred - matches notes like "Eric Binnion - Summary", etc.
quill export --latest --notes --note-title "Eric Binnion"

# Fallback if no Eric Binnion note exists
quill export --latest --transcript
```

## Common Workflows

**Get latest meeting notes to clipboard:**
```bash
quill export --latest --notes --note-title "Eric Binnion" | pbcopy
```

**Export transcript to file:**
```bash
quill export --latest --transcript > transcript.md
```

**Find and export specific meeting:**
```bash
quill list --search "planning"  # Find meeting ID
quill export abc123 --notes --note-title "Eric Binnion"
```

**Select different note template:**
```bash
quill export --latest --notes --note-title "Product"
```

## Options

**Global:**
- `--db-path <path>` - Override Quill data directory

**List:**
- `-l, --limit <n>` - Number of meetings (default: 20, max: 500)
- `-s, --since <duration>` - Time filter (`7d`, `24h`, `2w`)
- `--search <query>` - Title substring match

**Export:**
- `-n, --notes` - Export AI-generated notes (default)
- `-t, --transcript` - Export full transcript with timestamps
- `--latest` - Most recent meeting
- `--note-title <title>` - Select note template by partial match

## Configuration Priority

1. CLI flag: `--db-path /path`
2. Environment: `QUILL_DATA_DIR=/path`
3. Config file: `~/.quillrc` with `{"dataDir": "/path"}`
4. Default: `~/Library/Application Support/Quill/`

## Installation

```bash
cd ~/Repos/quill-cli
npm install && npm link
```

Run `quill --help` for full command details.
