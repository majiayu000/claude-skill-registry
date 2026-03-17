---
name: assistant-pro
description: Personal assistant operating routines (brief, inbox digest, auth health, daily planning, lightweight heartbeat alerts) with low token overhead.
metadata: {"openclaw":{"emoji":"🧾","os":["darwin","linux"],"requires":{"bins":["bash","jq","gog"]}}}
---

# Assistant Pro

Use this skill for day-to-day assistant operations with controlled token usage.

## Slash command mapping

- `/brief`
  - Run: `bash "$HOME/openclaw_pro/workspace/scripts/assistant_brief.sh"`
  - Purpose: quick snapshot (`gmail`, `calendar`, `status`)

- `/inbox`
  - Run: `bash "$HOME/openclaw_pro/workspace/scripts/assistant_inbox_digest.sh"`
  - Purpose: unread mail digest only

- `/authfix`
  - Run: `bash "$HOME/openclaw_pro/workspace/scripts/google_auth_check.sh"`
  - Purpose: detect OAuth failure and return one exact reauth command

- `/dayplan`
  - Run `/brief` first, then return 6-line max:
    1) current time
    2) calendar event count
    3) top 1-3 events
    4) unread mail count
    5) top 1-3 unread senders/subjects
    6) one action line

- `/models`
  - Run: `bash "$HOME/openclaw_pro/workspace/scripts/assistant_models.sh"`
  - Purpose: show current `main/coder/writer` model map

- `/remember`
  - Run: `bash "$HOME/openclaw_pro/workspace/scripts/oc_memory_note.sh" <category> "<title>" "<body>"`
  - Purpose: persist important user context into OC-Memory notes

- `/syllabus`
  - Run: `bash "$HOME/openclaw_pro/workspace/scripts/syllabus_pinpoint.sh" "$HOME/Desktop/syllabus"`
  - Purpose: parse syllabus docs (PDF/DOCX/Image OCR) and return pinpoint schedule/deadline items

## Heartbeat use

- Run: `bash "$HOME/openclaw_pro/workspace/scripts/assistant_heartbeat_probe.sh"`
- Default output: `HEARTBEAT_OK`
- Alert output: `HEARTBEAT_ALERT=google_reauth` (throttled to once per 12h)

## Response policy

- Keep assistant updates short and actionable.
- If status is `auth_required`, include exactly one repair command line.
- Do not expose secrets or token values.
- If Gmail/Calendar is unavailable, report partial results instead of hard failure.
