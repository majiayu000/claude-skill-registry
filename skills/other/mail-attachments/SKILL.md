---
name: mail-attachments
description: >-
  Find emails with attachments across all accounts, searchable by filename, extension, or sender. Use when user is looking for a document, PDF, spreadsheet, image, or any file sent by email. Arguments: optional filename/extension filter (e.g. "pdf", "contract", "invoice.xlsx", "from:boss"), time range, or size filter.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Mail Attachments — Find Emails with Files

Search: **$ARGUMENTS**

## Step 1: Search attachment filenames in the index
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
TERM="<extracted from $ARGUMENTS, or % for all>"

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       att.name as filename, mb.url as mailbox, m.ROWID, m.size
FROM messages m
JOIN subjects    s   ON m.subject   = s.ROWID
JOIN addresses   a   ON m.sender    = a.ROWID
JOIN mailboxes   mb  ON m.mailbox   = mb.ROWID
JOIN attachments att ON att.message = m.ROWID
WHERE att.name LIKE '%TERM%'
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
  AND mb.url NOT LIKE '%Trash%'
ORDER BY m.date_received DESC
LIMIT 50;" 2>/dev/null
```

## Step 2: Filter by extension
For specific types, add to WHERE:
- PDF: `AND (att.name LIKE '%.pdf' OR att.name LIKE '%.PDF')`
- Spreadsheet: `AND (att.name LIKE '%.xlsx' OR att.name LIKE '%.csv' OR att.name LIKE '%.xls')`
- Image: `AND (att.name LIKE '%.png' OR att.name LIKE '%.jpg' OR att.name LIKE '%.jpeg')`
- Document: `AND (att.name LIKE '%.doc%' OR att.name LIKE '%.pdf')`

## Step 3: Filter by size (large attachments)
```sql
AND m.size > 1000000   -- messages > ~1MB
```

## Step 4: Get all attachments on a specific message
```bash
sqlite3 "$DB" "
SELECT att.name, m.size
FROM attachments att
JOIN messages m ON att.message = m.ROWID
WHERE m.ROWID = <ROWID>;" 2>/dev/null
```

## Step 5: Find the actual file on disk
Attachment files are stored alongside their .emlx:
```bash
# Find the emlx first
EMLX=$(find ~/Library/Mail/V10/ -name "<ROWID>.emlx" 2>/dev/null | head -1)
# Attachments are in the same directory or in an Attachments subfolder
EMLX_DIR=$(dirname "$EMLX")
ls "$EMLX_DIR"
find "$EMLX_DIR" -not -name "*.emlx" -not -name "*.plist" 2>/dev/null
```

## Output Format
Show as table:
| Date | Sender | Subject | Filename | Size |
|---|---|---|---|---|

Group by file type if searching broadly.
Note the email ROWID so user can request to read the message.
If attachment files are locally cached, show their path.
