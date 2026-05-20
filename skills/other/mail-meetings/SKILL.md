---
name: mail-meetings
description: >-
  Find meeting invites, calendar events, and meeting-related emails (notes, agendas, reschedules). Use when user asks about meetings in their email, upcoming invites, or wants to see meeting notes. Arguments: optional time range or "upcoming", "today", "this week".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Meetings — Calendar Invites and Meeting Emails

Period: **$ARGUMENTS** (default: last 7 days)

## Query
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 604800))  # 7 days; adjust per $ARGUMENTS

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID, m.read
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND (
    s.subject LIKE '%invitation%'
    OR s.subject LIKE '%invite%'
    OR s.subject LIKE '%meeting%'
    OR s.subject LIKE '%standup%'
    OR s.subject LIKE '%retro%'
    OR s.subject LIKE '%sync%'
    OR s.subject LIKE '%call%'
    OR s.subject LIKE '%agenda%'
    OR s.subject LIKE '%(Updated invitation)%'
    OR s.subject LIKE '%has invited you%'
    OR s.subject LIKE '%calendar%'
    OR s.subject LIKE '%@ %'
    OR a.address LIKE '%calendar%'
    OR a.address LIKE '%gemini-notes%'
    OR a.address LIKE '%meet-recordings%'
  )
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Categorize meeting emails
Parse bodies to extract:
- **New invites**: "You have been invited to..." — extract meeting title, date/time, organizer
- **Updated invites**: time or attendee changes
- **Cancelled meetings**: "has been cancelled"
- **Meeting notes/summaries**: from Gemini Notes, Otter.ai, Notion, etc.
- **Agendas**: ahead of meetings

```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

## Step 3: For upcoming meetings, extract key fields
From invite body, find:
- Meeting title
- Date and time (look for `@`, `on [date]`, time patterns)
- Organizer
- Video link (Zoom, Google Meet, Teams URLs)
- Location

## Output Format
Group by type:

**Upcoming Meetings (invites received):**
| Meeting | When | Organizer | Link |
|---|---|---|---|

**Updated/Changed Meetings:**
[list changes]

**Meeting Notes received:**
[list summaries with key decisions/action items extracted]

**Cancelled:**
[list cancellations]

For each meeting note, pull out "Suggested next steps" or "Action items" sections if present.
