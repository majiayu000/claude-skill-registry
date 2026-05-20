---
name: mail-action-items
description: >-
  Extract action items, tasks, and to-dos from recent emails. Scan email bodies for requests, deadlines, approvals needed, and follow-ups. Use when user wants to know what they need to do based on their email, or asks "what do I need to act on?" Arguments: optional time range (default: last 3 days) or account filter.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Action Items — Extract Tasks from Email

Time window: **$ARGUMENTS** (default: last 3 days)

## Step 1: Find candidate emails with action signals

### Subject-line signals
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 259200))  # 3 days default; adjust per $ARGUMENTS

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID, m.read, m.is_urgent
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND m.automated_conversation != 2
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
  AND (
    s.subject LIKE '%action required%'
    OR s.subject LIKE '%please review%'
    OR s.subject LIKE '%approval%'
    OR s.subject LIKE '%approve%'
    OR s.subject LIKE '%sign off%'
    OR s.subject LIKE '%deadline%'
    OR s.subject LIKE '%due%'
    OR s.subject LIKE '%RSVP%'
    OR s.subject LIKE '%respond by%'
    OR s.subject LIKE '%feedback%'
    OR s.subject LIKE '%request%'
    OR m.is_urgent = 1
    OR m.flagged = 1
  )
ORDER BY m.is_urgent DESC, m.date_received DESC;" 2>/dev/null
```

### Urgent/flagged unread (always surface)
```bash
sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, m.ROWID
FROM messages m
JOIN subjects s ON m.subject = s.ROWID
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.read = 0 AND m.deleted = 0
  AND m.automated_conversation != 2
  AND m.unsubscribe_type = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Read bodies and extract action items
For each candidate email, parse the body:
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

Look for action-item patterns in the body text:
- "Please [verb]..." → direct request
- "Could you..." / "Can you..." → request
- "By [date]" / "Before [date]" / "Due [date]" → deadline
- "Let me know..." → response expected
- "Your approval is needed" / "Please approve" → approval required
- "Next steps:" / "Action items:" / "TODO:" → explicit task lists
- "Waiting on you" / "Pending your" → you're the blocker
- Meeting notes with "Suggested next steps" or your name + "will"

## Step 3: Deduplicate and prioritize
- Group by sender/thread
- Prioritize: overdue deadlines > urgent flagged > approval requests > general requests
- For Jira/project management alerts, extract ticket ID and description

## Output Format
**Action Items from Your Email (last 3 days)**

For each item:
- [ ] **Task description** — from [Sender], received [date]
  - Context: [1-line summary from email body]
  - Deadline: [if mentioned]

Group by: Overdue → Today → This week → No deadline
Mark items from unread emails with [UNREAD].
