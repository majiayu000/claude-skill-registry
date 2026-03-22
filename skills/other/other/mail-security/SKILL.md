---
name: mail-security
description: >-
  Find security-related emails — login alerts, 2FA changes, password resets, new device notifications, suspicious activity, and account security events across all accounts. Use when user asks about security alerts in their email, account access notifications, or wants to review security events. Arguments: optional time range or account/service filter.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Security — Account Security Events

Scanning: **$ARGUMENTS** (default: last 30 days)

## Query
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 2592000))  # 30 days

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender,
       mb.url as mailbox, m.ROWID, m.read
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND (
    s.subject LIKE '%security alert%'
    OR s.subject LIKE '%sign-in%'
    OR s.subject LIKE '%sign in%'
    OR s.subject LIKE '%new sign%'
    OR s.subject LIKE '%login%'
    OR s.subject LIKE '%new device%'
    OR s.subject LIKE '%new login%'
    OR s.subject LIKE '%access from%'
    OR s.subject LIKE '%password%'
    OR s.subject LIKE '%two-factor%'
    OR s.subject LIKE '%two factor%'
    OR s.subject LIKE '%2FA%'
    OR s.subject LIKE '%2-step%'
    OR s.subject LIKE '%authenticator%'
    OR s.subject LIKE '%verification code%'
    OR s.subject LIKE '%suspicious%'
    OR s.subject LIKE '%unusual activity%'
    OR s.subject LIKE '%unauthorized%'
    OR s.subject LIKE '%account compromised%'
    OR s.subject LIKE '%verify your%'
    OR s.subject LIKE '%confirm your%'
    OR s.subject LIKE '%account locked%'
    OR s.subject LIKE '%reset your password%'
    OR s.subject LIKE '%forgot password%'
    OR s.subject LIKE '%recovery%'
    -- Senders
    OR a.address LIKE '%security@%'
    OR a.address LIKE '%accounts.google%'
    OR a.address LIKE '%account-security%'
    OR a.address LIKE '%noreply@%stripe%'
    OR a.address LIKE '%auth@%'
  )
ORDER BY m.date_received DESC;" 2>/dev/null
```

## Step 2: Parse for details
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

Extract from body:
- Service/platform name
- Event type (new login, 2FA enabled, password changed, etc.)
- Location/IP address of the event
- Device/browser info
- Timestamp of the security event (vs. email timestamp)
- Whether it offers a "this wasn't me" link

## Step 3: Flag suspicious events
Raise concern if:
- Login from unexpected location or country
- Multiple password reset emails in a short window
- 2FA changes you don't remember
- "New device" login you don't recognize
- Account recovery initiated you didn't start

## Output Format
**Security Events — [PERIOD]**

Group by type:
- 2FA Changes
- Password Resets
- New Device Logins
- Login from new location
- Suspicious Activity Alerts

For each event: Service | Event | Location/Device | Date | Status (read/unread)

Flag: any unread security alerts (you may not have seen them).
Flag: any events from unexpected locations.
Note: total count by account/service.
