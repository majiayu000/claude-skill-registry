---
name: mail-read
description: >-
  Read the full content of a specific email by ROWID, subject search, or description. Shows headers, body, and any attachment names. Use when user wants to read a specific email, see the full text of a message, or asks "what does that email say". Arguments: ROWID number, subject keywords, or a description of the email to find.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Read — Read a Specific Email

Looking for: **$ARGUMENTS**

## Step 1: Find the email
### If $ARGUMENTS is a number → treat as ROWID directly
```bash
ROWID="$ARGUMENTS"
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID, m.read, m.flagged
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.ROWID = ${ROWID};" 2>/dev/null
```

### If $ARGUMENTS is text → search by subject + sender
```bash
sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, mb.url, m.ROWID
FROM messages m
JOIN subjects s ON m.subject=s.ROWID
JOIN addresses a ON m.sender=a.ROWID
JOIN mailboxes mb ON m.mailbox=mb.ROWID
WHERE (s.subject LIKE '%QUERY%' OR a.address LIKE '%QUERY%' OR a.comment LIKE '%QUERY%')
  AND m.deleted=0
  AND mb.url NOT LIKE '%Spam%'
ORDER BY m.date_received DESC LIMIT 5;" 2>/dev/null
```
If multiple matches, show options and ask which one.

## Step 2: Get recipient list
```bash
sqlite3 "$DB" "
SELECT a.address, a.comment, r.type
FROM recipients r
JOIN addresses a ON r.address = a.ROWID
WHERE r.message = <ROWID>
ORDER BY r.type, r.position;" 2>/dev/null
```

## Step 3: Get attachment list
```bash
sqlite3 "$DB" "
SELECT att.name FROM attachments att
WHERE att.message = <ROWID>;" 2>/dev/null
```

## Step 4: Read the full body
First check summaries table for fast-path (no file I/O, available for ~5% of recent emails):
```bash
sqlite3 "$DB" "SELECT su.summary FROM messages m JOIN summaries su ON m.summary = su.ROWID WHERE m.ROWID = <ROWID>;" 2>/dev/null
```
If no summary, parse the emlx:
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID>
```

## Step 5: Find the raw file if needed
```bash
find ~/Library/Mail/V10/ -name "<ROWID>.emlx" 2>/dev/null | head -1
# If not found, try partial (IMAP lazy-load — body is still readable):
find ~/Library/Mail/V10/ -name "<ROWID>.partial.emlx" 2>/dev/null | head -1
```
The parser handles partial fallback automatically. Use raw find only for debugging.

## Output Format
**Email Details**

```
From:     [name] <address>
To:       [recipients]
CC:       [if any]
Date:     [datetime]
Subject:  [subject]
Account:  [derived from mailbox URL]
Attachments: [filenames if any]
```

---
[Full body text, formatted naturally]

---

Offer:
- "Want me to summarize this?" if long
- "Want me to find related emails in this thread?"
- "Should I help you draft a reply?"
