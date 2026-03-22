---
name: mail-core
description: Background technical knowledge for reading Apple Mail data locally on macOS. Auto-loaded when any mail-* skill executes. Contains architecture, query patterns, and parsing techniques for ~/Library/Mail/V10/.
disable-model-invocation: false
user-invocable: false
allowed-tools: Bash
---

# Apple Mail Local Data — Technical Reference

## Storage Root
```
~/Library/Mail/V10/
├── MailData/Envelope Index     ← SQLite, central index of ALL mail across all accounts
└── <UUID>/                     ← one directory per synced account
    └── <Mailbox>.mbox/.../Data/[0/5/1/]Messages/<ROWID>.emlx
```

## Critical: emlx File Location
The Data/ subfolder depth is unpredictable (Data/Messages/, Data/1/Messages/, Data/0/4/1/Messages/, Data/0/5/1/Messages/). **Always locate by ROWID using find:**
```bash
find ~/Library/Mail/V10/ -name "<ROWID>.emlx" 2>/dev/null | head -1
```

Two emlx variants exist:
- `<ROWID>.emlx` — full message downloaded (headers + complete body)
- `<ROWID>.partial.emlx` — IMAP lazy-load: headers + truncated body (Apple Mail downloaded the start but not everything). Body is usually readable; just may cut off near the end.

The shared parser (`~/.claude/skills/_mail-shared/parser.py`) tries full emlx first, then falls back to partial automatically. Do not treat partial files as "not cached" — read them and extract what body is available.

## SQLite Database
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
sqlite3 "$DB" "..."
```

### Key Tables
| Table | Key Columns |
|---|---|
| messages | ROWID, date_received (Unix epoch), date_sent (Unix epoch), sender→addresses, subject→subjects, mailbox→mailboxes, read, flagged, deleted, size, conversation_id, is_urgent, automated_conversation, unsubscribe_type, list_id_hash, summary→summaries |
| mailboxes | ROWID, url (format: `imap://UUID/INBOX`, `ews://UUID/Inbox`), total_count (reliable), unread_count (EWS only, IMAP always 0) |
| addresses | ROWID, address (email string), comment (display name) |
| subjects | ROWID, subject (text) |
| recipients | message, address, type (0=To, 1=CC) |
| attachments | message, name (filename) |
| summaries | ROWID, summary (full body text — Apple-extracted, sparse: ~5% of recent messages) |
| conversations | thread grouping via conversation_id on messages |

### Automation & Newsletter Columns (replaces address regex)
```
automated_conversation:
  0 = unclassified (includes real humans AND some bots — not a clean human flag)
  1 = transactional automated (Jira, Slack notifications — can accept replies)
  2 = bulk automated (newsletters, monitoring, bank notifications, CI/CD, marketing)

unsubscribe_type:
  0   = no unsubscribe header (humans, transactional)
  1   = has List-Unsubscribe RFC header (newsletters, marketing — most reliable)
  2,3,6,7 = other list/subscription header variants
  NULL = not yet classified (treat like 0 for filtering)
```
Use the right filter for the context:
- **"Reply needed from a human"** (mail-needs-reply): `automated_conversation = 0 AND unsubscribe_type = 0`
- **"Humans + transactional" (Jira, Slack, bank alerts)**: `automated_conversation IN (0,1) AND unsubscribe_type = 0`
- **"Anything non-bulk" (action items, digest Tier 1+2)**: `automated_conversation != 2`
- **"Pure noise" (newsletters, monitoring, CI/CD)**: `automated_conversation = 2` OR `unsubscribe_type > 0`
- **"Newsletter specifically"**: `unsubscribe_type > 0`

Note: `automated_conversation = 1` includes Jira, Slack notifications — they can be action items but humans don't expect a reply to them. Use `= 0` for "needs human reply" contexts.

### Fast-Path Stats
- `mailboxes.total_count` — accurate all-time total per mailbox, no COUNT(*) needed
- `mailboxes.unread_count` — **only accurate for EWS/Exchange**; IMAP accounts always 0. Use `COUNT(*) WHERE read=0` for IMAP unread.
- `messages.summary` FK → `summaries.summary` text — fast body preview without emlx parsing, but only populated for ~5% of messages (mostly last 2-3 days). Use as fast-path when available.

### list_id_hash
Numeric hash of the mailing list ID. 39k+ rows populated. Same hash = same mailing list. Use `GROUP BY list_id_hash` to find distinct mailing lists and their volume.

### Date Format
`date_received` is **standard Unix epoch** (NOT Apple's 2001 Core Data offset):
```sql
datetime(m.date_received, 'unixepoch', 'localtime')
-- Last N hours:
WHERE m.date_received >= (strftime('%s','now') - 3600 * N)
-- Yesterday:
WHERE datetime(m.date_received,'unixepoch','localtime') >= date('now','-1 day')
  AND datetime(m.date_received,'unixepoch','localtime') <  date('now')
```

### Standard Query Template
```sql
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as sender_name,
       mb.url as mailbox, m.ROWID, m.read, m.flagged, m.size
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
  AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Junk%'
  AND mb.url NOT LIKE '%Draft%'
ORDER BY m.date_received DESC;
```

### Account Type from mailbox URL
- `imap://UUID/...` → Gmail or IMAP
- `ews://UUID/...` → Exchange/Outlook (work)
- iCloud: imap with INBOX.mbox structure

### Discover All Account UUIDs
```bash
ls ~/Library/Mail/V10/ | grep -v MailData
```

### Identify Which UUID = Which Email
```sql
SELECT a.address, COUNT(*) as cnt
FROM messages m
JOIN mailboxes mb ON m.mailbox = mb.ROWID
JOIN recipients r ON r.message = m.ROWID
JOIN addresses a ON r.address = a.ROWID
WHERE mb.url LIKE '%UUID_HERE%' AND r.type IN (0,1)
GROUP BY a.address ORDER BY cnt DESC LIMIT 3;
```

## emlx Parsing (Python)
```python
import email, re

def parse_emlx(path):
    with open(path, 'rb') as fh:
        fh.readline()          # skip byte count (emlx-specific)
        content = fh.read()
    msg = email.message_from_bytes(content)
    body = ""
    for part in msg.walk():
        ct = part.get_content_type()
        if ct in ('text/plain', 'text/html'):
            payload = part.get_payload(decode=True)
            if payload:
                b = payload.decode('utf-8', errors='replace')
                if len(b) > len(body):
                    body = b   # prefer the largest part
    # Strip HTML
    body = re.sub(r'<style[^>]*>.*?</style>', ' ', body, flags=re.DOTALL|re.IGNORECASE)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'&nbsp;', ' ', body)
    body = re.sub(r'&amp;', '&', body)
    body = re.sub(r'&#\d+;', '', body)
    return re.sub(r'\s+', ' ', body).strip()
```

## Noise Filters
Prefer column-based filters over address regex — they are indexed and more accurate:
- **`automated_conversation = 2`** — bulk automated (newsletters, monitoring, CI/CD, bank notifications)
- **`unsubscribe_type > 0`** — newsletter/mailing list (has unsubscribe header)
- **Folders to always exclude:** Spam, Trash, Junk, Drafts, Sent (via `mb.url NOT LIKE '%Spam%'` etc.)

For subject-based noise: `PROBLEM:`, `OK:`, `ALARM:`, `CRIT:` prefixes indicate monitoring alerts.

Note: `searchable_messages.message_body_indexed` is an INTEGER flag (indexing status), NOT body text. Do not use it for content retrieval.

## Shared Parser Script
A reusable parser lives at `~/.claude/skills/_mail-shared/parser.py`. Use it with:
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> [ROWID2 ...]
```
Returns JSON array with body text and attachment filenames per ROWID.
