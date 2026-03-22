---
name: mail-newsletter
description: >-
  Identify newsletters and mailing lists in email, show volume per sender, and help clean up subscriptions. Use when user wants to see what newsletters they're subscribed to, audit mailing lists, or identify email noise. Arguments: optional time range or "unsubscribe" to surface opt-out links.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Newsletter — Subscription and Mailing List Audit

Analysis: **$ARGUMENTS** (default: last 90 days)

## Step 1: Detect newsletters via unsubscribe_type (most accurate)
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 7776000))  # 90 days

sqlite3 "$DB" "
SELECT a.address, a.comment as name,
       m.unsubscribe_type,
       COUNT(*) as count,
       SUM(CASE WHEN m.read=1 THEN 1 ELSE 0 END) as read_count,
       ROUND(100.0 * SUM(m.read) / COUNT(*), 0) as read_pct,
       MAX(datetime(m.date_received,'unixepoch','localtime')) as latest
FROM messages m
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
  AND m.unsubscribe_type > 0
GROUP BY a.address
ORDER BY count DESC;" 2>/dev/null
```

## Step 2: Catch high-volume bulk senders without unsubscribe headers
```bash
sqlite3 "$DB" "
SELECT a.address, a.comment, COUNT(*) as cnt,
       ROUND(100.0 * SUM(m.read) / COUNT(*), 0) as read_pct
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted=0
  AND m.automated_conversation = 2
  AND m.unsubscribe_type = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Sent%'
GROUP BY a.address
HAVING cnt >= 10
ORDER BY cnt DESC LIMIT 20;" 2>/dev/null
```

## Step 3: Group by mailing list (list_id_hash)
To see distinct mailing lists (e.g. a company using multiple sender addresses):
```bash
sqlite3 "$DB" "
SELECT m.list_id_hash, COUNT(*) as cnt, COUNT(DISTINCT a.address) as sender_variants,
       MAX(a.comment) as name_sample
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted=0
  AND m.list_id_hash IS NOT NULL AND m.list_id_hash != 0
GROUP BY m.list_id_hash
ORDER BY cnt DESC LIMIT 20;" 2>/dev/null
```

## Step 4: If "unsubscribe" requested, find opt-out links
For senders with low read rates (< 30%), find unsubscribe links in body:
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID>
```
Look for `unsubscribe` URLs in the body text.

## Step 5: Calculate noise impact
Total emails from newsletter/automated senders vs. total inbox volume = % noise.

## Output Format
**Newsletter/Mailing List Audit — [PERIOD]**

| Sender | Emails | Read Rate | Verdict |
|---|---|---|---|
| newsletter@service.com | 45 | 12% | Rarely read |
| updates@useful.com | 28 | 89% | Engaged |

**Unsubscribe Candidates** (high volume + low read rate):
[list with unsubscribe links if available]

Total newsletter volume: X emails = Y% of inbox
Estimated time saved if unsubscribed from low-engagement ones: [estimate]
