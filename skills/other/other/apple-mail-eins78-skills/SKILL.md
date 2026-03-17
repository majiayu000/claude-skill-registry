---
name: apple-mail
description: Read email via Apple Mail.app and AppleScript. Use when asked to check, search, or read emails. READ ONLY — no sending or modifying emails.
---

# Apple Mail (Read Only)

Read email via Mail.app AppleScript. **No sending or modifying emails.**

## Prerequisites

- Mail.app running and logged in
- Automation permissions granted (System Settings → Privacy & Security → Automation → Terminal/Claude Code → Mail)
- If first access attempt times out, ask user to check for macOS permission dialog

## Account & Machine Context

See `docs/email-accounts.md` for which accounts are configured on which machines.

## Commands

### List accounts

```bash
osascript -e 'tell application "Mail" to get name of every account'
```

### Count unread messages

```bash
osascript -e 'tell application "Mail" to count (messages of inbox whose read status is false)'
```

### Recent inbox messages (last 10)

```bash
osascript -e 'tell application "Mail"
  set recentMsgs to messages 1 thru 10 of inbox
  repeat with msg in recentMsgs
    set msgInfo to "From: " & (sender of msg) & " | Subject: " & (subject of msg) & " | Date: " & (date sent of msg)
    log msgInfo
  end repeat
end tell'
```

### Get message content by index

```bash
osascript -e 'tell application "Mail"
  set msg to message 1 of inbox
  return "From: " & (sender of msg) & "\nSubject: " & (subject of msg) & "\nDate: " & (date sent of msg) & "\n\n" & (content of msg)
end tell'
```

### Search messages by subject

```bash
osascript -e 'tell application "Mail"
  set foundMsgs to (messages of inbox whose subject contains "keyword")
  count foundMsgs
end tell'
```

### Search and read first match

```bash
osascript -e 'tell application "Mail"
  set foundMsgs to (messages of inbox whose subject contains "keyword")
  if (count foundMsgs) > 0 then
    set msg to item 1 of foundMsgs
    return "From: " & (sender of msg) & "\nSubject: " & (subject of msg) & "\nDate: " & (date sent of msg) & "\n\n" & (content of msg)
  else
    return "No messages found"
  end if
end tell'
```

### Search across all mailboxes

```bash
osascript -e 'tell application "Mail"
  set foundMsgs to (messages of every mailbox of every account whose subject contains "keyword")
  -- Note: this can be slow across many accounts
end tell'
```

### List mailboxes for an account

```bash
osascript -e 'tell application "Mail" to get name of every mailbox of account "Gmail"'
```

## Notes

- AppleScript `messages of inbox` returns a unified inbox across all accounts
- Messages are indexed newest-first (message 1 = most recent)
- `content of msg` returns plain text body; `source of msg` returns raw MIME
- Large mailboxes can be slow — use `whose` clauses to filter
- Timeout: use `with timeout of 60 seconds` for slow queries
