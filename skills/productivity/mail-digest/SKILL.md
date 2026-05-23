---
name: mail-digest
description: >-
  Email digest for any time period — today, yesterday, last N hours/days, this week, a specific date, or while-I-was-away ranges. Categorizes by urgency, surfaces unread, flags financial/security emails, filters noise. Auto-invoke when user asks about email for any time period: "what came in today", "catch me up", "any emails this week", "what did I miss", "emails from yesterday", "last 3 hours", "since Monday".
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Digest — Email Summary for Any Time Period

Period: **$ARGUMENTS** (default: today)

## Step 1: Parse the time expression into a Unix timestamp range

Interpret $ARGUMENTS naturally. Map to START and END unix timestamps:

| Expression | START | END |
|---|---|---|
| "today" / (empty) | midnight today local | now |
| "yesterday" | midnight yesterday | midnight today |
| "last 2 hours" | now − 7200s | now |
| "last N hours" | now − N×3600s | now |
| "last N days" | now − N×86400s | now |
| "this week" | last Monday midnight | now |
| "last week" | Monday of prev week | last Sunday midnight |
| "since Monday" | most recent Monday midnight | now |
| "YYYY-MM-DD" | that date midnight | that date 23:59:59 |
| "catch me up" / "while I was away" | infer from context or ask — default last 5 days |

```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"

# Use SQLite date expressions directly — never compute Unix epochs manually (wrong year risk).
# "today"       → >= date('now','localtime')
# "yesterday"   → >= date('now','-1 day','localtime') AND < date('now','localtime')
# "last 48h"    → >= datetime('now','-48 hours')
# "last 7 days" → >= date('now','-7 days','localtime')
# Apply the range in the WHERE clause below using datetime() comparisons.
```

## Step 2: Pull all messages in the window

```bash
sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url as mailbox, m.ROWID,
       m.read, m.flagged, m.is_urgent, m.size,
       m.automated_conversation, m.unsubscribe_type
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE datetime(m.date_received,'unixepoch','localtime') >= date('now','localtime')
  -- adjust the expression above based on $ARGUMENTS
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
  AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Junk%'
  AND mb.url NOT LIKE '%Draft%'
  AND mb.url NOT LIKE '%Sent%'
ORDER BY m.is_urgent DESC, m.date_received DESC;" 2>/dev/null
```

## Step 3: Categorize

**Tier 1 — Needs Attention (read these):**
- `is_urgent = 1`
- `flagged = 1`
- `read = 0` AND `automated_conversation != 2` AND `unsubscribe_type = 0` (real person, unread)
- Subject contains: urgent, action required, ASAP, deadline, critical, review, approve, response needed

**Tier 2 — FYI (skim):**
- `automated_conversation = 1` (transactional — Jira, Slack, bank receipts)
- Reports, summaries, meeting notes, calendar invites
- Security alerts (login, 2FA, password) — even if automated
- Financial: receipts, payment confirmations, invoices

**Tier 3 — Noise (count only, don't enumerate):**
- `automated_conversation = 2` — bulk automated emails
- `unsubscribe_type > 0` — newsletter/mailing list emails
- Monitoring subjects: PROBLEM:, OK:, ALARM:, CRIT:
- Break down by type: monitoring alerts, newsletters, marketing

For Tier 3, just report: "X automated emails (Y monitoring, Z CI/CD, W marketing)"

## Step 4: Read bodies for Tier 1 items

For Tier 1 emails, get body preview. Check summaries table first (fast, no file I/O):
```bash
sqlite3 "$DB" "
SELECT m.ROWID, su.summary
FROM messages m
JOIN summaries su ON m.summary = su.ROWID
WHERE m.ROWID IN (<ROWID1>,<ROWID2>,...)" 2>/dev/null
```
For any ROWIDs without a summary entry, fall back to emlx parsing:
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```
Pull the first ~200 chars of meaningful body content as a preview for each.

## Step 5: Surface special categories

Always call out explicitly if found in the window:
- **Financial**: subjects containing payment, receipt, invoice, transfer, transaction, billing → note count and total if parseable
- **Security**: login alerts, 2FA changes, password resets → flag every one
- **Meetings**: calendar invites or reschedules
- **Unread from humans**: these are the most likely to need action

## Output Format

**Email Digest — [RESOLVED DATE RANGE]**
`Total: X | Unread: Y | Flagged: Z | Accounts: N`

---

**Needs Attention** (X)
| Time | From | Subject | Preview |
|---|---|---|---|

**FYI** (X)
| Time | From | Subject |
|---|---|---|

**Financial** (X emails)
- Brief list of transactions if detectable from subjects

**Security** (X events)
- Brief list

**Noise filtered:** X total (breakdown by type)

---

If the window has zero emails: say so and suggest a wider range.
If the window has >200 emails: summarize by sender domain and ask if they want to drill into a category.
Offer at the end: "Want me to read any of these, or dive into a specific category?"
