---
name: mail-stats
description: >-
  Email volume statistics, trends, and patterns. Show daily/weekly/monthly volume, peak periods, read rates, and account breakdowns. Use when user asks about email statistics, how much email they get, trends, or wants analytics on their inbox. Arguments: optional time range or specific metric like "by day", "by account", "unread rate".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Mail Stats — Email Analytics

Analysis: **$ARGUMENTS** (default: last 30 days overview)

## Volume by day (last 30 days)
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 2592000))

sqlite3 "$DB" "
SELECT date(datetime(m.date_received,'unixepoch','localtime')) as day,
       COUNT(*) as total,
       SUM(CASE WHEN m.read=0 THEN 1 ELSE 0 END) as unread
FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
GROUP BY day ORDER BY day;" 2>/dev/null
```

## Volume by week (last 12 weeks)
```bash
sqlite3 "$DB" "
SELECT strftime('%Y-W%W', datetime(m.date_received,'unixepoch','localtime')) as week,
       COUNT(*) as total
FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= (strftime('%s','now') - 7257600)
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Sent%'
GROUP BY week ORDER BY week;" 2>/dev/null
```

## Volume by hour of day (when do emails arrive?)
```bash
sqlite3 "$DB" "
SELECT strftime('%H', datetime(m.date_received,'unixepoch','localtime')) as hour,
       COUNT(*) as cnt
FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
GROUP BY hour ORDER BY hour;" 2>/dev/null
```

## By account
```bash
sqlite3 "$DB" "
SELECT mb.url,
       COUNT(*) as total,
       SUM(CASE WHEN m.read=0 THEN 1 ELSE 0 END) as unread,
       ROUND(100.0 * SUM(m.read) / COUNT(*), 1) as read_rate_pct
FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
GROUP BY substr(mb.url, 1, instr(mb.url || '/', '/', 8))
ORDER BY total DESC;" 2>/dev/null
```

## All-time totals (fast path via mailboxes)
```bash
# total_count is pre-maintained per mailbox — no COUNT(*) needed for totals
sqlite3 "$DB" "
SELECT SUM(total_count) as total_indexed,
       SUM(unread_count) as reported_unread
FROM mailboxes
WHERE url NOT LIKE '%Spam%' AND url NOT LIKE '%Trash%' AND url NOT LIKE '%Sent%';" 2>/dev/null

# Note: unread_count is accurate for EWS/Exchange accounts only; IMAP always shows 0.
# For accurate total unread, use:
sqlite3 "$DB" "
SELECT COUNT(*) as total_unread
FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.deleted=0 AND m.read=0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Sent%';" 2>/dev/null

sqlite3 "$DB" "
SELECT SUM(CASE WHEN m.flagged=1 THEN 1 ELSE 0 END) as total_flagged,
       MIN(datetime(m.date_received,'unixepoch','localtime')) as oldest,
       MAX(datetime(m.date_received,'unixepoch','localtime')) as newest
FROM messages m WHERE m.deleted=0;" 2>/dev/null
```

## Output Format
**Email Statistics**

All-time: X total messages across Y accounts, oldest: [date]

Last 30 days:
- Average per day: N
- Busiest day: [date] (N emails)
- Quietest: [date]
- Peak hour: [hour] UTC+offset
- Read rate: X%
- Overall unread: N

Daily volume chart (ASCII or table).
Per-account breakdown.
Trends: increasing/decreasing compared to previous period if calculable.
