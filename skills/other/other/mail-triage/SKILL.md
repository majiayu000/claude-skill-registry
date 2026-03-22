---
name: mail-triage
description: >-
  Intelligent inbox triage — surface the most important emails across all accounts, prioritized by urgency and requiring attention. Use when user wants a smart overview of what needs their attention, asks "what's important in my email", or wants help deciding what to read first. Arguments: optional time window (default: last 48 hours) or account filter.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Triage — Smart Priority Overview

Triaging: **$ARGUMENTS** (default: last 48 hours)

## Step 1: Pull all candidate emails
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 172800))  # 48 hours; adjust per $ARGUMENTS

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID,
       m.read, m.flagged, m.is_urgent, m.size, m.conversation_id,
       m.automated_conversation, m.unsubscribe_type
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Junk%' AND mb.url NOT LIKE '%Sent%'
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Score each email for priority

**High priority signals (+points):**
- is_urgent = 1: +10
- flagged = 1: +8
- read = 0: +3
- Subject contains: urgent, ASAP, action required, critical, deadline, review, approve: +5 each
- automated_conversation = 0 AND unsubscribe_type = 0 (likely real person): +4
- From work/EWS account: +2
- Large message (>50KB): +1 (likely real content)
- Subject contains reply indicators (RE:, FW:): +2

**Low priority signals (−points):**
- automated_conversation = 2 (bulk automated — newsletters, monitoring, CI/CD): −8
- unsubscribe_type > 0 (has List-Unsubscribe header — mailing list): −5
- Subject starts with PROBLEM:, OK:, ALARM:, CRIT: −8 (monitoring)
- Already read: −5

**Compute a score per email, then bucket:**
- Score ≥ 10: Critical
- Score 5–9: Important
- Score 1–4: Normal
- Score ≤ 0: Noise

## Step 3: Read bodies for top-priority items
For Critical and Important emails (score ≥ 5):
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

Extract key info: what is being asked, any deadlines, any amounts.

## Step 4: Check for conversation context
For unread replies, check if it's a continuation of a thread you started:
```bash
sqlite3 "$DB" "
SELECT COUNT(*) FROM messages m
JOIN mailboxes mb ON m.mailbox=mb.ROWID
WHERE m.conversation_id=<CONV_ID>
  AND mb.url LIKE '%Sent%';" 2>/dev/null
```
If you sent something in this thread → higher priority (someone replied to you).

## Output Format
**Critical — Act Now:**
[list with 1-line context from body]

**Important — Handle Today:**
[list with subject and sender]

**Normal — Read When Convenient:**
[count + brief list]

**Noise (filtered):** X emails
[breakdown: Y monitoring alerts, Z newsletters, W CI/CD]

Total: X emails in window. Estimated action time: [estimate based on count].
Offer to read any specific email or start replying.
