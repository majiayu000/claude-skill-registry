---
name: check-inbox
context: fork
model: haiku
description: Check Outlook inbox and update daily note with message summary
---

# Skill: Check Inbox

**Command:** `/check-inbox`
**Model:** Haiku (coordinator) / any (note creation)
**Agent:** main

## Description

Check Outlook inbox for unread messages using Playwright. Extracts sender, subject, time, and flags from the DOM, then optionally updates the daily note with an inbox summary.

## Prerequisites

- Playwright installed (`@playwright/test` in devDependencies)
- Microsoft Edge installed
- Authenticated session (run `npm run inbox:check` without `--headless` once to authenticate)

## Usage

```
/check-inbox                    # Check unread messages (default)
/check-inbox flagged            # Check flagged messages
/check-inbox all                # Check all messages (no filter)
/check-inbox to-me              # Messages addressed directly to me
/check-inbox --no-daily         # Don't update daily note
```

## Workflow

### Step 1: Capture inbox data

Run the inbox check script:

```bash
node .claude/scripts/outlook-inbox.js --headless
```

For other filters:
```bash
node .claude/scripts/outlook-inbox.js --headless --filter flagged
node .claude/scripts/outlook-inbox.js --headless --filter all
node .claude/scripts/outlook-inbox.js --headless --filter to-me
```

This outputs:
- **JSON message data** at `.claude/logs/inbox-messages-{filter}-{timestamp}.json`
- **Screenshot** at `.claude/logs/inbox-screenshot-{filter}-{timestamp}.png`

If the script fails with "Session expired", re-run without `--headless`:
```bash
node .claude/scripts/outlook-inbox.js
```

### Step 2: Read and present results

1. Find the most recent inbox JSON file:
   ```
   .claude/logs/inbox-messages-unread-*.json
   ```
2. Read the JSON and screenshot
3. Present to the user as a summary table:

```
Inbox — 3 unread messages (10:56 AM)

| Sender               | Subject                       | Time     | Flags   |
|----------------------|-------------------------------|----------|---------|
| Alex Johnson  | Accepted: What is AlertHub   | 10:05 AM | MEETING |
| Chris Taylor      | Re: Pen re-test               | 9:57 AM  |         |
| Udemy Business       | New courses are waiting...    | 10:30 AM |         |
```

### Step 3: Match senders to vault

For each message, search for matching Person notes:
- Search `People/*.md` files for sender name matches
- If found, link to the Person note in the summary
- If not found, note the sender as unlinked

### Step 4: Update daily note (unless --no-daily)

Add or update an `## Inbox` section in today's daily note (`Daily/YYYY/YYYY-MM-DD.md`):

```markdown
## Inbox

**3 unread** at 10:56 AM

- **Accepted: What is AlertHub** — [[Alex Johnson|Alex Johnson]] (10:05 AM) [MEETING]
- **Re: Pen re-test** — Chris Taylor (9:57 AM)
- **New courses are waiting for you!** — Udemy Business (10:30 AM)
```

Rules for the daily note update:
- If an `## Inbox` section already exists, **replace it** with the latest data
- Place it after `## Meetings` and before `## Notes`
- Link senders to Person notes where they exist
- Include flags in brackets: `[MEETING]`, `[ATTACH]`, `[FLAG]`

### Step 5: Suggest actions (optional)

If the user asks, suggest actions for each message:
- Meeting acceptances → link to the meeting note if it exists
- External emails (CAUTION banner) → flag for attention
- Flagged messages → create Task notes if needed

## Available Filters

| Filter | CLI Flag | Description |
|--------|----------|-------------|
| `unread` | `--filter unread` | Unread messages only (default) |
| `flagged` | `--filter flagged` | Flagged messages only |
| `to-me` | `--filter to-me` | Messages addressed directly to me |
| `has-files` | `--filter has-files` | Messages with attachments |
| `mentions-me` | `--filter mentions-me` | Messages where I'm @mentioned |
| `calendar-invites` | `--filter calendar-invites` | Meeting invites only |
| `all` | `--filter all` | All messages (no filter) |

## Scheduling

Inbox checks run automatically via launchd at 9:00, 12:00, and 15:00 on weekdays.
- Job: `com.vault.inbox-check`
- Script: `.claude/scripts/outlook-inbox.js --headless`
- Logs: `.claude/logs/inbox-check.log`

The JSON output accumulates in `.claude/logs/` — the skill always reads the most recent file.

## Authentication

Same persistent browser context as calendar sync (`.claude/browser-data/`, gitignored). If the session expires during a scheduled run, the next interactive `/check-inbox` will prompt for re-authentication.

## Related Skills

- [[.claude/skills/sync-calendar/SKILL.md|/sync-calendar]] — Calendar sync (same Playwright approach)
- [[.claude/skills/daily/SKILL.md|/daily]] — Daily note creation
- [[.claude/skills/email/SKILL.md|/email]] — Process individual emails into vault notes
