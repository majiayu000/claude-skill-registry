---
name: stock-monitor
description: "Monitor product availability and get restock alerts for Shopify stores. This skill should be used when checking if a product is in stock, watching for restocks, setting up back-in-stock alerts, or tracking product availability. Supports SMS, Slack, and terminal notifications on status transitions. Keywords: out of stock, sold out, back in stock, restock alert, notify when available, watch product."
argument-hint: "[URL or 'check' or 'list']"
---

# Stock Monitor

Track product availability on Shopify stores. Get notified via SMS, Slack, or terminal when out-of-stock items come back.

## Quick Start

```bash
# Add a product to watch (auto-detects name from Shopify)
python3 ~/.claude/skills/stock-monitor/scripts/stock_watch.py add "https://store.com/products/item?variant=123" --notify sms --target "+1XXXXXXXXXX"

# Check all watched items
python3 ~/.claude/skills/stock-monitor/scripts/stock_check.py

# One-off check (no watchlist needed)
python3 ~/.claude/skills/stock-monitor/scripts/stock_check.py --url "https://store.com/products/item?variant=123"
```

## Scripts

### stock_watch.py — Manage Watchlist

| Command | Purpose |
|---------|---------|
| `stock_watch.py add URL [--name NAME] [--notify sms\|slack\|terminal] [--target PHONE\|#CHANNEL]` | Add product to watch |
| `stock_watch.py list` | Show all watched items with status |
| `stock_watch.py remove ID` | Remove a watch |
| `stock_watch.py pause ID` / `resume ID` | Pause or resume checking |

### stock_check.py — Run Checks

| Flag | Purpose |
|------|---------|
| *(no flags)* | Check all active watches |
| `--id N` | Check specific watch |
| `--url URL` | One-off URL check, no DB write |
| `--dry-run` | Check without sending notifications |
| `--json` | JSON output for piping |

## Notification Channels

- **terminal** (default): Colored output to stdout
- **sms**: Dispatches via `~/.claude/skills/sms/scripts/sms_send.py`
- **slack**: Dispatches via `~/.claude/skills/slack/scripts/slack_post.py`

Notifications fire only on **out_of_stock → in_stock transitions** to avoid noise on repeated checks.

## Scheduling

Run `stock_check.py` manually, or schedule recurring checks:

- **Session loop**: `/loop 30m python3 ~/.claude/skills/stock-monitor/scripts/stock_check.py`
- **Persistent cron**: See `references/launchd-setup.md` for a macOS launchd plist that runs checks when Claude is closed.

## How It Works

Shopify stores expose product data at `/products/{handle}.js` with per-variant `available` booleans. The skill fetches this JSON, finds the target variant by ID, and compares against the last known status in SQLite. No scraping, no browser rendering, no rate-limit concerns.

## Data

SQLite DB at `~/.claude/skills/stock-monitor/data/stock_monitor.db` with two tables: `watches` (watchlist) and `check_log` (check history with transition tracking).
