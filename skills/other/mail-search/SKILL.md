---
name: mail-search
description: >-
  Search Apple Mail across all synced accounts by keyword, subject, sender, or any combination. Use when user asks to find an email, search for a message, or look for something in their mail. Arguments: search terms, optionally with sender:, subject:, from:, account: prefixes, and time filters like "last 30 days" or "this year".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Search — Full-Text Search Across All Accounts

Search query: **$ARGUMENTS**

## Argument Parsing
Parse $ARGUMENTS for modifiers:
- `from:name@domain.com` or `sender:` → filter by sender
- `subject:keyword` → filter subject only
- `account:gmail` or `account:work` → restrict to account type
- `last N days/weeks` → time filter
- Anything else → search both subject and sender

## Query

```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
TERM="<extracted search term>"  # URL-encode % as %% in shell

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID, m.read,
       CASE WHEN m.size > 0 THEN m.size ELSE 0 END as size
FROM messages m
JOIN subjects  s  ON m.subject  = s.ROWID
JOIN addresses a  ON m.sender   = a.ROWID
JOIN mailboxes mb ON m.mailbox  = mb.ROWID
WHERE m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
  AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Junk%'
  AND (
    s.subject LIKE '%TERM%'
    OR a.address LIKE '%TERM%'
    OR a.comment LIKE '%TERM%'
  )
ORDER BY m.date_received DESC
LIMIT 50;" 2>/dev/null
```

For sender-only search:
```sql
WHERE a.address LIKE '%TERM%' OR a.comment LIKE '%TERM%'
```

For subject-only search:
```sql
WHERE s.subject LIKE '%TERM%'
```

For recipient search (TO/CC):
```sql
JOIN recipients r ON r.message = m.ROWID
JOIN addresses ra ON r.address = ra.ROWID
WHERE ra.address LIKE '%TERM%'
```

## Reading Email Bodies
If user wants to read specific results, find the emlx and parse:
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID>
```

## Output Format
Show results as a table:
| Date | From | Subject | Account | Read |
|---|---|---|---|---|

If more than 20 results, summarize by sender/thread and ask if they want to narrow down.
For each result, note the account it belongs to (extract UUID from mailbox URL to identify account).
Offer to read any specific email if user asks.
