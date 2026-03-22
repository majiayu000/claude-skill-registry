---
name: web-monitor
description: Monitor web pages for content changes and get alerts. Track URLs, detect updates, view diffs. Use when asked to watch a website, track changes on a page, monitor for new posts/content, set up page change alerts, or check if a site has been updated. Supports CSS selectors for targeted monitoring.
---

# Web Monitor

Track web pages for changes. Stores snapshots, computes diffs, supports CSS selectors.

## Quick Start

```bash
# Add a URL to watch
uv run --with beautifulsoup4 python scripts/monitor.py add "https://example.com" --name "Example"

# Add with CSS selector (monitor specific section)
uv run --with beautifulsoup4 python scripts/monitor.py add "https://example.com/pricing" -n "Pricing" -s ".pricing-table"

# Check all watched URLs for changes
uv run --with beautifulsoup4 python scripts/monitor.py check

# Check one specific URL
uv run --with beautifulsoup4 python scripts/monitor.py check "Example"

# List watched URLs
uv run --with beautifulsoup4 python scripts/monitor.py list

# View last diff
uv run --with beautifulsoup4 python scripts/monitor.py diff "Example"

# View current snapshot
uv run --with beautifulsoup4 python scripts/monitor.py snapshot "Example" --lines 50

# Remove
uv run --with beautifulsoup4 python scripts/monitor.py remove "Example"
```

## Commands

| Command | Args | Description |
|---------|------|-------------|
| `add` | `<url> [-n name] [-s selector]` | Add URL to watch, take initial snapshot |
| `remove` | `<url-or-name>` | Stop watching a URL |
| `list` | `[-f json]` | List all watched URLs with stats |
| `check` | `[url-or-name] [-f json]` | Check for changes (all or one) |
| `diff` | `<url-or-name>` | Show last recorded diff |
| `snapshot` | `<url-or-name> [-l lines]` | Show current snapshot |

## Output Symbols

- 🔔 CHANGED — page content changed (shows diff preview)
- ✅ No changes
- 📸 Initial snapshot taken
- ❌ Error fetching

## Data

Stored in `~/.web-monitor/` (override with `WEB_MONITOR_DIR` env var):
- `watches.json` — watch list config
- `snapshots/` — stored page content + diffs

## Tips

- Use `--selector` to monitor specific elements (prices, article lists, etc.)
- Use `--format json` for programmatic checking (heartbeat integration)
- CSS selectors require beautifulsoup4 (included via `--with` flag)
- Text is normalized to reduce noise from timestamps, whitespace, ads
