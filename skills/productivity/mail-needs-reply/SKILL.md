---
name: mail-needs-reply
description: >-
  Find emails that are waiting for a reply — unread messages from real people that haven't been responded to. Use when user asks what they haven't replied to, what's waiting for their response, or wants to find unanswered emails. Arguments: optional time window (default: last 7 days) or account filter.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Needs Reply — Unanswered Emails

Looking for: unread emails from humans (not bots) with no follow-up in your Sent.

## Step 1: Get unread emails from non-automated senders
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
# Use SQLite date expressions — never compute Unix epochs manually.

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID, m.conversation_id,
       m.date_received
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE datetime(m.date_received,'unixepoch','localtime') >= date('now','-7 days','localtime')
  AND m.read = 0
  AND m.deleted = 0
  AND m.automated_conversation = 0
  AND m.unsubscribe_type = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Junk%' AND mb.url NOT LIKE '%Sent%'
ORDER BY m.date_received ASC;" 2>/dev/null
```

## Step 2: Check if a reply exists in the same conversation
For each candidate, check if there's a sent message in the same conversation:
```bash
sqlite3 "$DB" "
SELECT COUNT(*) FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.conversation_id = <CONVERSATION_ID>
  AND (mb.url LIKE '%Sent%' OR mb.url LIKE '%sent%')
  AND m.date_received > <ORIGINAL_DATE>;" 2>/dev/null
```
If count > 0, you already replied — skip this email.

## Step 3: Age-based prioritization
Group by urgency:
- **Overdue (>3 days unread):** oldest first — likely forgotten
- **Aging (1-3 days):** need attention soon
- **Recent (<1 day):** just came in

## Step 4: Read the most overdue ones
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2>
```

## Output Format
**Emails Waiting for Your Reply**

For each:
- **Age** | **From** | **Subject** | [brief context from body if readable]

Group: Overdue → Aging → Recent
Total count up front. Note longest-waiting email specifically.
Offer to draft a reply to any of them.
