---
name: mail-work
description: >-
  Show work emails only, filtered to Exchange/EWS accounts and corporate email domains. Digest with priorities. Use when user asks about work email, work inbox, or wants to separate work from personal mail. Arguments: optional date range or "today", "yesterday", "this week".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Work — Work Email Digest

Period: **$ARGUMENTS** (default: today)

## Step 1: Identify work accounts
Work accounts are EWS/Exchange (detected by `ews://` prefix in mailbox URL), plus any IMAP account with a corporate domain (not gmail.com, icloud.com, yahoo.com, hotmail.com, outlook.com).

```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"

# EWS/Exchange accounts (most reliable work indicator)
EWS_UUIDS=$(sqlite3 "$DB" "
  SELECT DISTINCT substr(url, instr(url,'://')+3, instr(substr(url,instr(url,'://')+3),'/')-1)
  FROM mailboxes WHERE url LIKE 'ews://%';" 2>/dev/null)

# All mailbox URLs for work accounts
sqlite3 "$DB" "SELECT DISTINCT url FROM mailboxes WHERE url LIKE 'ews://%';" 2>/dev/null
```

## Step 2: Date filter
```bash
# Parse $ARGUMENTS
# today: date('now')
# yesterday: date('now','-1 day') to date('now')
# this week: date('now', 'weekday 1', '-7 days') or similar
# default: today

DATE_FILTER="datetime(m.date_received,'unixepoch','localtime') >= '$(date +%Y-%m-%d) 00:00:00'"
```

## Step 3: Query work mail
```bash
sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID, m.read, m.flagged, m.is_urgent
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE ${DATE_FILTER}
  AND m.deleted = 0
  AND mb.url LIKE 'ews://%'
  AND mb.url NOT LIKE '%Spam%'
  AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Junk%'
  AND mb.url NOT LIKE '%Draft%'
ORDER BY m.is_urgent DESC, m.read ASC, m.date_received DESC;" 2>/dev/null
```

## Step 4: Read bodies of important emails
For emails that look substantive, prioritize by automated_conversation:
- `automated_conversation = 0` = likely real person → read first
- `automated_conversation = 1` = transactional (Jira, Slack) → skim
- `automated_conversation = 2` = bulk automated → count only unless urgent

```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2>
```

## Categorization for Work Mail
- **Escalations/Alerts**: incidents, P1/P2/P3 alerts, on-call, outages (automated_conversation=2 OK)
- **Action Required**: review, approve, sign off, merge request, deploy
- **Meetings**: invites, updates, cancellations, meeting notes/summaries
- **Reports**: daily/weekly reports, incident reports, uptime summaries
- **External**: emails from outside the company domain
- **Internal Chatter**: announcements, FYIs, newsletters (automated_conversation=2)

## Output Format
Group by category. Highlight unread. Surface anything urgent or needing a response.
Include a "still needs reply" flag for emails older than 24h that are unread.
