---
name: apple-mail
description: Comprehensive guide for accessing and automating Apple Mail using AppleScript, including reading emails, sending messages, and managing mailboxes.
---

# Apple Mail AppleScript Skill

This skill provides comprehensive guidance on using AppleScript to automate Apple Mail operations, including reading emails, sending messages, and managing mailboxes.

## Core Principles

1. **Access mailboxes through account objects** - Don't try to access `inbox` directly on accounts
2. **Iterate through mailboxes to find the right one** - Mailbox names can vary (INBOX, Inbox, etc.)
3. **Use account name matching** - Match on account name rather than email address property
4. **Handle errors gracefully** - AppleScript errors can be cryptic, use trial and error with different approaches

## Common Query Patterns

### 1. List All Mail Accounts

Always start by listing accounts to verify the account exists and get the correct name:

```applescript
osascript <<'EOF'
tell application "Mail"
    set accountNames to {}
    repeat with acc in accounts
        set end of accountNames to (name of acc)
    end repeat
    return accountNames as string
end tell
EOF
```

**Example output:**
```
MonzoiCloudbrunofdcampos@gmail.commmbcfields@gmail.comcampos.bruno.fd@gmail.com
```

### 2. Read Last N Emails from an Account

The **correct pattern** for accessing emails from a specific account:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set inboxMsgs to messages of mbox
            set msgCount to count of inboxMsgs
            set numToFetch to 5
            if msgCount < 5 then set numToFetch to msgCount

            set output to ""
            repeat with i from 1 to numToFetch
                set msg to item i of inboxMsgs
                set output to output & "Email #" & i & return
                set output to output & "Subject: " & subject of msg & return
                set output to output & "From: " & sender of msg & return
                set output to output & "Date: " & (date received of msg as string) & return
                set output to output & return & "---" & return & return
            end repeat

            return output
        end if
    end repeat

    return "Inbox not found"
end tell
EOF
```

**Key lessons from trial and error:**
- ❌ **WRONG:** `inbox of targetAccount` (doesn't work, causes error -1728)
- ❌ **WRONG:** `address of acc` (address property doesn't exist reliably)
- ✅ **CORRECT:** `every mailbox of targetAccount` then iterate to find "INBOX" or "Inbox"

### 3. Read Email Content

Get the full body content of a specific email:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set msg to item 1 of messages of mbox
            set emailContent to content of msg
            return emailContent
        end if
    end repeat
end tell
EOF
```

### 4. Send an Email

Create and send a new email:

```applescript
osascript <<'EOF'
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"Your Subject", content:"Your email body here", visible:true}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
        send
    end tell
end tell
EOF
```

**Options:**
- `visible:true` - Shows the compose window before sending (useful for review)
- `visible:false` - Sends silently in the background

### 5. Reply to an Email

Reply to an existing email (preserves threading):

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            -- Find the message to reply to (e.g., by sender)
            set foundMessages to (messages of mbox whose sender contains "sender@example.com")
            set originalMsg to item 1 of foundMessages

            -- Create reply
            set theReply to reply originalMsg
            tell theReply
                set content to "Your reply message here"
                send
            end tell

            return "Reply sent successfully"
        end if
    end repeat
end tell
EOF
```

**Key points:**
- Use `reply originalMsg` to create a threaded reply (NOT `make new outgoing message`)
- The `reply` command automatically sets the recipient and subject with "Re:"
- Don't use `with opening window false` parameter, it causes syntax errors
- Set the content of the reply before sending

**Reply vs New Email:**
- ❌ **WRONG:** Creating new message to same recipient (breaks threading)
```applescript
set newMessage to make new outgoing message with properties {subject:"Re: Subject"}
```
- ✅ **CORRECT:** Using reply command on original message (maintains threading)
```applescript
set theReply to reply originalMsg
```

### 6. Search Emails by Subject

Find emails matching a subject keyword:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set foundMessages to (messages of mbox whose subject contains "keyword")
            set output to ""

            repeat with msg in foundMessages
                set output to output & "Subject: " & subject of msg & return
                set output to output & "From: " & sender of msg & return
                set output to output & "Date: " & (date received of msg as string) & return
                set output to output & "---" & return
            end repeat

            return output
        end if
    end repeat
end tell
EOF
```

### 7. Search Emails by Sender

Find all emails from a specific sender:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set foundMessages to (messages of mbox whose sender contains "sender@example.com")

            set output to "Found " & (count of foundMessages) & " messages" & return & return
            repeat with msg in foundMessages
                set output to output & subject of msg & return
            end repeat

            return output
        end if
    end repeat
end tell
EOF
```

### 8. Get Email Metadata Without Content

Get subject, sender, and date without loading full content (faster):

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set recentMsgs to items 1 thru 10 of messages of mbox
            set output to ""

            repeat with msg in recentMsgs
                set output to output & subject of msg & " | " & sender of msg & return
            end repeat

            return output
        end if
    end repeat
end tell
EOF
```

### 9. Check Unread Message Count

Count unread messages in inbox:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set unreadCount to count of (messages of mbox whose read status is false)
            return "Unread messages: " & unreadCount
        end if
    end repeat
end tell
EOF
```

### 10. Move Email to Mailbox

Move a message to a different mailbox:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    -- Find the source mailbox
    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" then
            set theMessage to item 1 of messages of mbox

            -- Find the destination mailbox
            repeat with destBox in allMailboxes
                if name of destBox is "Archive" then
                    move theMessage to destBox
                    return "Message moved to Archive"
                end if
            end repeat
        end if
    end repeat
end tell
EOF
```

### 11. Delete Emails by Criteria

Delete emails matching specific criteria:

```applescript
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount

    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" then
            set messagesToDelete to (messages of mbox whose subject contains "spam")

            repeat with msg in messagesToDelete
                delete msg
            end repeat

            return "Deleted " & (count of messagesToDelete) & " messages"
        end if
    end repeat
end tell
EOF
```

## Common Mailbox Names

Different email providers use different mailbox names:

### Gmail Accounts
- `INBOX` - Main inbox
- `[Gmail]/All Mail` - All mail archive
- `[Gmail]/Sent Mail` - Sent messages
- `[Gmail]/Trash` - Deleted items
- `[Gmail]/Drafts` - Draft messages
- `[Gmail]/Spam` - Spam folder

### iCloud Accounts
- `Inbox` - Main inbox (note the capitalisation)
- `Sent Messages` - Sent mail
- `Trash` - Deleted items
- `Drafts` - Draft messages

### Other Providers
- May use `Sent Items`, `Deleted Items`, etc.
- Always iterate through mailboxes and check names

## Email Message Properties

Common properties you can access on a message object:

```applescript
subject of msg              -- Email subject line
sender of msg              -- Sender email address
date received of msg       -- Date the email was received
date sent of msg          -- Date the email was sent
content of msg            -- Full email body (can be slow)
read status of msg        -- Boolean: true if read, false if unread
flagged status of msg     -- Boolean: true if flagged/starred
message id of msg         -- Unique message identifier
to recipients of msg      -- List of recipient objects
cc recipients of msg      -- List of CC recipient objects
all headers of msg        -- Raw email headers
message size of msg       -- Size in bytes
```

## Error Handling

### Common Errors and Solutions

**Error: "Can't get inbox of account"**
```applescript
-- ❌ WRONG: Trying to access inbox directly
tell application "Mail"
    set targetAccount to account "email@example.com"
    set inboxMsgs to messages of inbox of targetAccount  -- This fails!
end tell

-- ✅ CORRECT: Iterate through mailboxes
tell application "Mail"
    set targetAccount to account "email@example.com"
    set allMailboxes to every mailbox of targetAccount
    repeat with mbox in allMailboxes
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            set inboxMsgs to messages of mbox
        end if
    end repeat
end tell
```

**Error: "Can't get address of account"**
```applescript
-- ❌ WRONG: address property is unreliable
if address of acc contains "email@example.com" then

-- ✅ CORRECT: Use name property instead
if name of acc contains "email@example.com" then
```

**Error: "Can't get item 1 of every account"**
```applescript
-- ❌ WRONG: Don't try to access properties in bulk operations
repeat with acc in accounts
    if address of acc contains "..." then  -- This fails!

-- ✅ CORRECT: Get properties individually
repeat with acc in accounts
    set accName to name of acc
    if accName contains "..." then
```

**Error: Message not found or mailbox doesn't exist**
```applescript
-- Solution: Always check existence first
set allMailboxes to every mailbox of targetAccount
if (count of allMailboxes) = 0 then
    return "No mailboxes found for this account"
end if
```

## Best Practices

1. **Always list accounts first** when debugging:
   ```bash
   osascript -e 'tell application "Mail" to name of every account'
   ```

2. **Check mailbox names** before accessing:
   ```applescript
   set mailboxNames to name of every mailbox of targetAccount
   ```

3. **Use heredoc syntax** for multi-line AppleScript in bash:
   ```bash
   osascript <<'EOF'
   tell application "Mail"
       -- Your script here
   end tell
   EOF
   ```

4. **Handle case sensitivity** in mailbox names:
   ```applescript
   if name of mbox is "INBOX" or name of mbox is "Inbox" then
   ```

5. **Limit message retrieval** to avoid slowdowns:
   ```applescript
   set recentMsgs to items 1 thru 10 of messages of mbox
   ```

6. **Check message count** before iterating:
   ```applescript
   set msgCount to count of messages of mbox
   if msgCount < numToFetch then set numToFetch to msgCount
   ```

7. **Use `return` early** when you find what you need:
   ```applescript
   repeat with mbox in allMailboxes
       if name of mbox is "INBOX" then
           -- Process and return
           return result
       end if
   end repeat
   ```

## Performance Tips

1. **Don't load content unnecessarily** - Getting `content of msg` is slow
2. **Limit the number of messages** processed in one script
3. **Use filters** (`whose` clauses) to narrow results before processing
4. **Cache mailbox references** if doing multiple operations

## Security and Privacy Considerations

1. **Mail access requires permissions** - macOS will prompt for access on first use
2. **Be careful with automation** - Test sending scripts with visible:true first
3. **Respect user privacy** - Don't log sensitive email content
4. **Use specific searches** - Avoid processing entire mailboxes when possible

## Quick Reference Commands

```bash
# List all accounts
osascript -e 'tell application "Mail" to name of every account'

# Get inbox message count for an account
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    repeat with mbox in mailboxes of targetAccount
        if name of mbox is "INBOX" or name of mbox is "Inbox" then
            return count of messages of mbox
        end if
    end repeat
end tell
EOF

# Get unread count
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    repeat with mbox in mailboxes of targetAccount
        if name of mbox is "INBOX" then
            return count of (messages of mbox whose read status is false)
        end if
    end repeat
end tell
EOF

# List all mailbox names for an account
osascript <<'EOF'
tell application "Mail"
    set targetAccount to account "email@example.com"
    set mailboxNames to name of every mailbox of targetAccount
    return mailboxNames as string
end tell
EOF
```

## When to Use This Skill

Invoke this skill when you need to:
- Read emails from Apple Mail
- Send automated emails
- Reply to emails (maintaining thread context)
- Search for specific emails
- Manage mailboxes programmatically
- Count unread messages
- Move or delete emails based on criteria
- Extract email metadata
- Automate email workflows

## Integration with Other Workflows

When working with email automation:

1. **Email notifications** - Send alerts when specific events occur
2. **Data extraction** - Parse emails for specific information
3. **Email filtering** - Auto-file or delete emails based on rules
4. **Reporting** - Generate summaries of email activity
5. **Backup** - Export email data for archival

## Lessons Learned (Trial and Error)

The key insights from developing this skill:

1. **Don't use `inbox of account` directly** - Always iterate through mailboxes
2. **Account properties vary** - Use `name` not `address`
3. **Mailbox names vary by provider** - Check for both "INBOX" and "Inbox"
4. **Error -1728 usually means property doesn't exist** - Try a different property
5. **Bulk operations on `every X` can fail** - Get properties individually
6. **Use `items 1 thru N`** for safe list slicing with bounds checking
7. **Use `reply` command, not new messages** - To maintain threading, use `reply originalMsg` instead of creating a new outgoing message
8. **Don't use `with opening window` parameter** - The `reply` command doesn't support the `with opening window false` parameter, causes syntax errors

Remember: AppleScript error messages are often cryptic. When debugging, simplify the script to the minimum necessary and build up complexity gradually.
