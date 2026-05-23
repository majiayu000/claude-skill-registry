---
name: rtm
description: Manage Remember The Milk tasks — list, add, complete, delete, search, prioritize, tag, move, and annotate tasks with notes. Use when the user asks about tasks, todos, to-do lists, reminders, or Remember The Milk.
metadata:
  {
    "openclaw":
      {
        "emoji": "🐄",
        "requires":
          {
            "env": ["RTM_API_KEY", "RTM_SHARED_SECRET"],
          },
        "credentials":
          {
            "env": ["RTM_API_KEY", "RTM_SHARED_SECRET"],
            "files": ["~/.rtm_token"],
          },
      },
  }
---

# Remember The Milk

CLI tool at `scripts/rtm.py` for full RTM task management. Stdlib only — no pip dependencies.

## Setup

1. Get API credentials at https://www.rememberthemilk.com/services/api/keys.rtm
2. Set env vars `RTM_API_KEY` and `RTM_SHARED_SECRET` (via OpenClaw config `skills.entries.rtm.env`)
3. Run `scripts/rtm.py auth` — opens a URL, authorize, press Enter. Token saves to `~/.rtm_token`

**Sub-agents:** Env vars are not inherited. Pass them explicitly:
```bash
RTM_API_KEY=... RTM_SHARED_SECRET=... python3 scripts/rtm.py <command>
```

## Security

- **Env vars:** `RTM_API_KEY` and `RTM_SHARED_SECRET` are required at runtime. Configure via OpenClaw skill env, not hardcoded.
- **Auth token:** Stored as plain text at `~/.rtm_token` after interactive auth. This file grants full access to the linked RTM account. Protect it accordingly — restrict file permissions (`chmod 600`) or remove after use if not needed persistently.
- **Network:** All API calls go to `api.rememberthemilk.com` and `www.rememberthemilk.com` only. No other outbound connections.
- **Permissions:** The auth flow requests `delete` permission (RTM's highest tier) to support task deletion. Use a dedicated API key with minimum needed scope if preferred.

## Commands

```bash
# Auth (interactive, one-time)
scripts/rtm.py auth

# Lists
scripts/rtm.py lists              # show active lists
scripts/rtm.py lists --all        # include archived

# Tasks
scripts/rtm.py tasks                          # all incomplete
scripts/rtm.py tasks --list LIST_ID           # filter by list
scripts/rtm.py tasks --filter "priority:1"    # RTM filter syntax
scripts/rtm.py tasks --no-notes               # hide notes

# Add (--parse enables Smart Add for dates/tags/priority)
scripts/rtm.py add "Buy groceries" --list LIST_ID --parse
# Smart Add: "Buy milk ^tomorrow #shopping !1" sets due, tag, priority

# Complete / Delete
scripts/rtm.py complete LIST_ID SERIES_ID TASK_ID
scripts/rtm.py delete LIST_ID SERIES_ID TASK_ID

# Priority (1=high, 2=medium, 3=low, N=none)
scripts/rtm.py set-priority LIST_ID SERIES_ID TASK_ID 1

# Due date (natural language parsed by RTM)
scripts/rtm.py set-due LIST_ID SERIES_ID TASK_ID "next friday"

# Move between lists
scripts/rtm.py move FROM_LIST_ID TO_LIST_ID SERIES_ID TASK_ID

# Tags
scripts/rtm.py add-tags LIST_ID SERIES_ID TASK_ID "tag1,tag2"

# Search (RTM filter syntax)
scripts/rtm.py search "tag:work AND status:incomplete"

# Notes
scripts/rtm.py notes-add LIST_ID SERIES_ID TASK_ID "text" --title "Title"
scripts/rtm.py notes-delete NOTE_ID
```

## Task output format

Task output includes IDs needed for write operations:
```
  Task Name [P1] (due: 2025-03-15) #tag1 #tag2
    list=12345 series=67890 task=11111
    📝 Note Title (note_id=99999)
    Note body text here
```

## RTM filter syntax

Common filters: `status:incomplete`, `priority:1`, `tag:tagname`, `due:today`, `dueBefore:tomorrow`, `list:Inbox`, `isTagged:true`, `addedWithin:"1 week"`. Combine with `AND`, `OR`, `NOT`.

Full reference: https://www.rememberthemilk.com/help/answers/search/advanced.rtm

## Reliability

- All API calls have a 15-second timeout with automatic retry (up to 3 attempts with backoff)
- Transient network errors are retried; permanent API errors exit immediately
- Write operations (add, complete, delete, etc.) auto-create timelines
