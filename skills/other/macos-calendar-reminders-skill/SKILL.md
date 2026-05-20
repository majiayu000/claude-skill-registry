---
name: macos-calendar-reminders-skill
description: Manage Apple Calendar events and Apple Reminders on macOS via calctl.py and remindctl.py — self-contained EventKit CLI scripts. Use when the user wants to create, query, update, or delete calendar events or reminders on macOS.
compatibility: macOS only (darwin). Requires uv (brew install uv). Python 3.12+ auto-resolved by uv.
metadata:
  author: openclaw
  version: "3.0.0"
allowed-tools: Bash(uv:*) Read
---

# macOS Calendar & Reminders

Two CLI tools for **Apple Calendar** (`calctl.py`) and **Apple Reminders** (`remindctl.py`). Dependencies auto-installed by `uv`.

Full reference: [`calctl.md`](references/calctl.md) · [`remindctl.md`](references/remindctl.md) · [`authorization.md`](references/authorization.md)

---

## Routing

| Scenario | Tool |
|----------|------|
| Time blocks (meetings, appointments, events) | calctl — Calendar |
| Tasks / deadlines / todos | remindctl — Reminder |

Use `list` to discover available calendars and reminder lists before creating items.

---

## Quick Reference

```bash
# Calendar
uv run scripts/calctl.py list
uv run scripts/calctl.py get --calendar all --start 2026-03-16 --end 2026-03-22
uv run scripts/calctl.py create --calendar Work --title "Meeting" --start 2026-03-20T14:00:00 --end 2026-03-20T15:00:00
uv run scripts/calctl.py search --query "review"
uv run scripts/calctl.py update --id "<event_id>" --start 2026-03-20T15:00:00 --end 2026-03-20T16:00:00
uv run scripts/calctl.py delete --calendar Work --id "<event_id>"

# Reminders
uv run scripts/remindctl.py list
uv run scripts/remindctl.py get today
uv run scripts/remindctl.py get week --list Work
uv run scripts/remindctl.py create --title "Submit report" --list Work --due 2026-03-20T23:59:00 --priority high
uv run scripts/remindctl.py search --query "assignment"
uv run scripts/remindctl.py update --id "<id>" --due 2026-03-21T23:59:00
uv run scripts/remindctl.py complete --id "<id>"
uv run scripts/remindctl.py delete --id "<id>" --confirm
```

---

## Authorization

On first use, run `status --authorize` to trigger the macOS permission prompt:

```bash
uv run scripts/calctl.py status --authorize
uv run scripts/remindctl.py status --authorize
```

If permission is denied or the prompt doesn't appear, read [`authorization.md`](references/authorization.md) to guide the user through manual setup. Do **not** retry in a loop.
