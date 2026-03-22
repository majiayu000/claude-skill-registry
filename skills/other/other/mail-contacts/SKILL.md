---
name: mail-contacts
description: >-
  Extract contacts and build a communication directory from email history. Find email addresses, frequency of contact, and relationship strength. Use when user wants to find someone's email address, see all contacts, or understand their communication network. Arguments: optional person name, company, domain, or "top contacts" / "recent contacts".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Mail Contacts — Email Directory from Communication History

Query: **$ARGUMENTS**

## Option A: Find a specific person's email address
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
NAME="<extracted from $ARGUMENTS>"

# Search senders
sqlite3 "$DB" "
SELECT DISTINCT a.address, a.comment as name, COUNT(*) as frequency
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
WHERE (a.comment LIKE '%${NAME}%' OR a.address LIKE '%${NAME}%')
  AND m.deleted=0
GROUP BY a.address ORDER BY frequency DESC LIMIT 10;" 2>/dev/null

# Search recipients (emails sent TO them)
sqlite3 "$DB" "
SELECT DISTINCT a.address, a.comment as name, COUNT(*) as frequency
FROM recipients r
JOIN addresses a ON r.address = a.ROWID
WHERE (a.comment LIKE '%${NAME}%' OR a.address LIKE '%${NAME}%')
GROUP BY a.address ORDER BY frequency DESC LIMIT 10;" 2>/dev/null
```

## Option B: Top contacts directory
```bash
sqlite3 "$DB" "
SELECT a.address, a.comment as name,
       COUNT(*) as emails_received,
       MAX(datetime(m.date_received,'unixepoch','localtime')) as last_contact
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Sent%'
  AND m.automated_conversation = 0
  AND m.unsubscribe_type = 0
GROUP BY a.address
ORDER BY emails_received DESC LIMIT 50;" 2>/dev/null
```

## Option C: All contacts from a company/domain
```bash
DOMAIN="<extracted from $ARGUMENTS>"
sqlite3 "$DB" "
SELECT DISTINCT a.address, a.comment as name, COUNT(*) as cnt
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
WHERE a.address LIKE '%@${DOMAIN}%' AND m.deleted=0
GROUP BY a.address ORDER BY cnt DESC;" 2>/dev/null
```

## Option D: Recent contacts (last 30 days)
```bash
SINCE=$(($(date +%s) - 2592000))
sqlite3 "$DB" "
SELECT DISTINCT a.address, a.comment,
       MAX(datetime(m.date_received,'unixepoch','localtime')) as last_seen
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE} AND m.deleted=0
  AND mb.url NOT LIKE '%Spam%'
  AND m.automated_conversation = 0
  AND m.unsubscribe_type = 0
GROUP BY a.address ORDER BY last_seen DESC LIMIT 30;" 2>/dev/null
```

## Output Format
For specific person search: show address(es), display name, frequency, last contact.
For directory: table with name, address, frequency, last contact.
Note: if multiple addresses for same person (aliases), group them.
For company domain: list all people at that company who've emailed you.
