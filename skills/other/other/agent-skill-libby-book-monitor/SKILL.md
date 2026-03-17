---
name: libby-book-monitor
version: 1.0.0
description: Track book availability on Libby/OverDrive libraries. Search library catalogues, manage a watchlist, and get notified when books are added. Use for "libby", "check libby", "libby watchlist", "is book on libby", "book available", "overdrive", "library catalogue", "ספרייה", "ספרים".
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-libby-book-monitor
metadata: {"openclaw": {"emoji": "📚", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---

# Libby/OverDrive Book Monitor

Track book availability on Libby/OverDrive libraries. Search catalogues, manage a watchlist, and get notified when books are added to your library's collection.

> **Disclaimer**: This is an unofficial tool, not affiliated with or endorsed by OverDrive/Libby. Catalogue data queries APIs that power the website and may not reflect actual availability. This tool does NOT borrow books or place holds. Provided "as is" without warranty of any kind.

## Quick Start

```bash
# Search a library catalogue
python3 {baseDir}/scripts/libby-book-monitor.py search telaviv "Project Hail Mary"

# Add a book to your watchlist
python3 {baseDir}/scripts/libby-book-monitor.py watch "Kafka on the Shore" --author "Haruki Murakami"

# Check your watchlist against the API
python3 {baseDir}/scripts/libby-book-monitor.py check

# Show your watchlist
python3 {baseDir}/scripts/libby-book-monitor.py list
```

## Commands

| Command | Description |
|---------|-------------|
| `search <library> <query>` | Search a library catalogue by title/author |
| `watch <title>` | Add a book to the watchlist |
| `unwatch <title>` | Remove a book from the watchlist |
| `list` | Show the watchlist with status |
| `check` | Check all watchlist books against the API |

## Options

| Option | Commands | Description |
|--------|----------|-------------|
| `--profile <name>` | all | Separate watchlist per user |
| `--author <name>` | watch | Specify book author |
| `--library <code>` | watch | Library code (default: from config) |
| `--notify` | check | Only print newly found books (for cron) |
| `--data-dir <path>` | all | Custom data directory |

## Profiles

Use `--profile` to maintain separate watchlists for different people:

```bash
python3 {baseDir}/scripts/libby-book-monitor.py --profile jane watch "Dune"
python3 {baseDir}/scripts/libby-book-monitor.py --profile bob check --notify
```

## Configuration

Default library is `telaviv` Israel Digital. Edit `~/.libby-book-monitor/config.json` to change:

```json
{
  "default_library": "nypl",
  "libraries": {
    "nypl": "New York Public Library"
  }
}
```

The library code is the subdomain from your library's OverDrive site (e.g., `nypl.overdrive.com` -> `nypl`).

## Cron Integration

Run a daily check that only outputs when books are newly found:

```bash
python3 {baseDir}/scripts/libby-book-monitor.py --profile jane check --notify
```

If any new books are found, send the results to the user.

## Notes

- Works with non-Latin scripts (Hebrew, Arabic, CJK, etc.)
- Books are considered "found" when `isOwned: true` in the API response
- 1-second delay between API calls when checking multiple books
- No external dependencies (Python stdlib only)
- Data stored in `~/.libby-book-monitor/` (configurable via `--data-dir` or `$LIBBY_BOOK_MONITOR_DATA`)
