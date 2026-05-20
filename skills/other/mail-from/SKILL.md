---
name: mail-from
description: >-
  Show all emails from a specific person, email address, or domain. Summarize the relationship and communication history. Use when user asks about emails from someone, or wants to see what a specific sender has sent them. Arguments: person name, email address, or domain (e.g. "john@company.com", "amazon.com", "my boss Sarah").
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail From — All Emails From a Sender

Sender query: **$ARGUMENTS**

## Steps

### 1. Find matching senders
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
QUERY="$ARGUMENTS"  # treat as search term against address + comment fields

sqlite3 "$DB" "
SELECT DISTINCT a.address, a.comment, COUNT(*) as cnt
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE (a.address LIKE '%${QUERY}%' OR a.comment LIKE '%${QUERY}%')
  AND m.deleted = 0
GROUP BY a.address
ORDER BY cnt DESC
LIMIT 10;" 2>/dev/null
```

If multiple matches, show options and ask which one (or proceed with all if they're clearly the same person/org).

### 2. Get all emails from the matched address(es)
```bash
sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, mb.url as mailbox, m.ROWID, m.read, m.flagged
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE a.address LIKE '%SENDER%'
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
  AND mb.url NOT LIKE '%Trash%'
ORDER BY m.date_received DESC
LIMIT 100;" 2>/dev/null
```

### 3. Compute relationship stats
```bash
sqlite3 "$DB" "
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN m.read = 0 THEN 1 ELSE 0 END) as unread,
  SUM(CASE WHEN m.flagged = 1 THEN 1 ELSE 0 END) as flagged,
  MIN(datetime(m.date_received,'unixepoch','localtime')) as first_email,
  MAX(datetime(m.date_received,'unixepoch','localtime')) as latest_email,
  strftime('%Y-%m', datetime(m.date_received,'unixepoch','localtime')) as busiest_month
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE a.address LIKE '%SENDER%' AND m.deleted = 0
GROUP BY busiest_month
ORDER BY COUNT(*) DESC LIMIT 1;" 2>/dev/null
```

### 4. Read recent emails if user wants details
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

## Output Format
Lead with relationship summary:
- **X emails** from [name/address], spanning [date range]
- First contact: [date] — Latest: [date]
- Unread: X | Flagged: X

Then list recent emails (last 10-20) as a table.
Group older emails by month if there are many.
Highlight unread and flagged ones.
Offer to read any specific email or summarize the thread.
