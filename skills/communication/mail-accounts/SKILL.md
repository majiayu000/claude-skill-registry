---
name: mail-accounts
description: List all Apple Mail synced accounts with email addresses, message counts, folder structure, and account types. Use when user asks what email accounts are synced, how many emails they have, or wants an overview of their mail setup.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Mail Accounts — Discover All Synced Accounts

List every account synced in Apple Mail with identity, type, and stats.

## Steps

### 1. Get all account UUIDs
```bash
ls ~/Library/Mail/V10/ | grep -v MailData | grep -v "^$"
```

### 2. For each UUID, identify the email address and account type
Query the most frequent recipient address (most reliable identity signal):
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"

for UUID in $(ls ~/Library/Mail/V10/ | grep -v MailData); do
  # Account type from mailbox URL prefix
  TYPE=$(sqlite3 "$DB" "SELECT url FROM mailboxes WHERE url LIKE '%${UUID}%' LIMIT 1;" 2>/dev/null | grep -oE '^[a-z]+')

  # Sender of Sent mail = this account's address (reliable; avoids mailing list CC pollution)
  EMAIL=$(sqlite3 "$DB" "
    SELECT a.address
    FROM messages m
    JOIN mailboxes mb ON m.mailbox=mb.ROWID
    JOIN addresses a ON m.sender=a.ROWID
    WHERE mb.url LIKE '%${UUID}%'
      AND (mb.url LIKE '%Sent%' OR mb.url LIKE '%sent%')
      AND a.address LIKE '%@%'
    GROUP BY a.address ORDER BY COUNT(*) DESC LIMIT 1;" 2>/dev/null)

  # Fallback if no Sent mail: most frequent To: recipient in INBOX
  if [ -z "$EMAIL" ]; then
    EMAIL=$(sqlite3 "$DB" "
      SELECT a.address
      FROM messages m
      JOIN mailboxes mb ON m.mailbox=mb.ROWID
      JOIN recipients r ON r.message=m.ROWID
      JOIN addresses a ON r.address=a.ROWID
      WHERE mb.url LIKE '%${UUID}%/INBOX%' AND r.type = 0
      GROUP BY a.address ORDER BY COUNT(*) DESC LIMIT 1;" 2>/dev/null)
  fi

  # Total message count
  TOTAL=$(sqlite3 "$DB" "
    SELECT COUNT(*) FROM messages m
    JOIN mailboxes mb ON m.mailbox=mb.ROWID
    WHERE mb.url LIKE '%${UUID}%' AND m.deleted=0;" 2>/dev/null)

  # Unread count
  UNREAD=$(sqlite3 "$DB" "
    SELECT COUNT(*) FROM messages m
    JOIN mailboxes mb ON m.mailbox=mb.ROWID
    WHERE mb.url LIKE '%${UUID}%' AND m.deleted=0 AND m.read=0;" 2>/dev/null)

  echo "${UUID}|${TYPE}|${EMAIL}|${TOTAL}|${UNREAD}"
done
```

### 3. List mailbox folders for each account
```bash
sqlite3 "$DB" "
  SELECT DISTINCT url FROM mailboxes
  WHERE url LIKE '%UUID_HERE%'
  ORDER BY url;" 2>/dev/null
```

### 4. Get per-account message volume over time
```bash
sqlite3 "$DB" "
  SELECT mb.url,
    strftime('%Y-%m', datetime(m.date_received,'unixepoch','localtime')) as month,
    COUNT(*) as cnt
  FROM messages m
  JOIN mailboxes mb ON m.mailbox=mb.ROWID
  WHERE mb.url LIKE '%UUID_HERE%' AND m.deleted=0
  GROUP BY month ORDER BY month DESC LIMIT 24;" 2>/dev/null
```

## Output Format
Present as a table:

| Account | Type | Total | Unread |
|---|---|---|---|
| user@gmail.com | Gmail/IMAP | 58,996 | 42 |
| user@company.com | Exchange | 68,466 | 7 |

Then list folder structure per account if helpful.
Note accounts that have high unread counts as potentially needing attention.
