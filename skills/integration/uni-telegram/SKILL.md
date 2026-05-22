---
name: uni-telegram
description: |
  Telegram messaging via uni CLI. Use when user wants to send Telegram messages,
  read Telegram chats, search Telegram, or manage Telegram contacts. Commands: send, read, edit, delete, forward, react, search, chats, contacts, download, auth.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Telegram (uni telegram)

Telegram user API via MTProto - full account access (not bot).

## Setup

```bash
uni telegram auth                       # Authenticate with phone + OTP
uni telegram logout                     # Logout
```

## List Chats

```bash
uni telegram chats                      # List all chats
uni telegram chats -n 50                # More results
uni telegram chats --archived           # Archived chats
```

## Read Messages

```bash
uni telegram read @username             # Read messages from user
uni telegram read "Family Group" -n 50  # Read from group
uni telegram read me                    # Saved messages
uni telegram read me -n 20              # Last 20 saved messages
```

## Send Messages

```bash
uni telegram send @username "Hello!"    # Send to user
uni telegram send +1234567890 "Hi"      # Send to phone
uni telegram send me "Note to self"     # Send to saved messages
uni telegram send me --file photo.jpg   # Send file
uni telegram send me "caption" -f doc.pdf  # File with caption
uni telegram send me "reply" --reply 123   # Reply to message
```

## Edit/Delete/Forward/React

```bash
uni telegram edit me 123 "new text"     # Edit message
uni telegram delete me 123              # Delete single message
uni telegram delete me 100-110          # Delete range of messages
uni telegram delete me "test msg"       # Delete by text search
uni telegram delete me "test" -n 5      # Delete up to 5 matches
uni telegram forward me 123 @friend     # Forward message
uni telegram react @user 123 "👍"       # React to message
```

## Search

```bash
uni telegram search "meeting"           # Search all chats
uni telegram search "project" -c @user  # Search in specific chat
```

## Contacts

```bash
uni telegram contacts                   # List contacts
uni telegram contacts "john"            # Search contacts
```

## Download Media

```bash
uni telegram download @username 12345   # Download media
uni telegram download "Group" 67890 -o ./  # Specify output dir
```

## Notes

- `me` = saved messages
- Use `@username` or phone number or chat title
- Message IDs: use search or read with `--json` to get IDs
