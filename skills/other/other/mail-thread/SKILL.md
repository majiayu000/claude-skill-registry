---
name: mail-thread
description: >-
  Read and summarize a complete email thread or conversation. Show all messages in order, who said what, and what was decided. Use when user wants to read a specific email thread, catch up on a conversation, or understand what happened in an email chain. Arguments: subject line keywords, ROWID of any message in the thread, sender name, or conversation topic.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Thread — Read a Full Email Conversation

Thread: **$ARGUMENTS**

## Step 1: Find the thread
### Option A: Search by subject keyword
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
QUERY="<extracted from $ARGUMENTS>"

sqlite3 "$DB" "
SELECT m.ROWID, m.conversation_id, s.subject,
       datetime(m.date_received,'unixepoch','localtime') as dt,
       a.address as sender
FROM messages m
JOIN subjects  s ON m.subject = s.ROWID
JOIN addresses a ON m.sender  = a.ROWID
WHERE s.subject LIKE '%${QUERY}%' AND m.deleted=0
ORDER BY m.date_received DESC LIMIT 10;" 2>/dev/null
```

### Option B: If ROWID provided directly
```bash
sqlite3 "$DB" "
SELECT conversation_id FROM messages WHERE ROWID = <ROWID>;" 2>/dev/null
```

## Step 2: Get all messages in the thread by conversation_id
```bash
CONV_ID=<from step 1>

sqlite3 "$DB" "
SELECT m.ROWID,
       datetime(m.date_received,'unixepoch','localtime') as dt,
       a.address as sender, a.comment as name,
       s.subject, mb.url as mailbox, m.read
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.conversation_id = ${CONV_ID}
  AND m.deleted = 0
ORDER BY m.date_received ASC;" 2>/dev/null
```

## Step 3: Read all message bodies
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> <ROWID3> ...
```

## Step 4: Reconstruct the conversation
Present chronologically:
- Who sent each message and when
- Key content of each message (summarize long ones, quote short ones)
- Reply chain structure

## Step 5: Summarize the thread
After showing the conversation:
- What was the original question/issue?
- What was discussed/debated?
- What was decided or concluded?
- Are there any open questions or pending actions?
- Who is waiting on whom?

## Output Format
**Thread: [Subject]**
[N messages | started: date | participants: list]

---
**[Date] [Sender Name]** [→ Reply to: ...]
> [message content, summarized if long]

---
[repeat for each message]

---
**Summary:**
[2-3 sentence summary of the thread outcome]

**Status:** [Resolved / Ongoing / Waiting for response]
**Next action:** [if any]
