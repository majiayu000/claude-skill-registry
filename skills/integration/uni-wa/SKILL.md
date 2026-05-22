---
name: uni-wa
description: |
  WhatsApp messaging via uni CLI. Use when user wants to send WhatsApp messages,
  read WhatsApp chats, or manage WhatsApp. Commands: send, read, edit, delete, react, forward, chats, auth.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# WhatsApp (uni wa)

WhatsApp messaging via Baileys. Fast daemon architecture (~35ms per command).

## Setup

```bash
uni wa auth                             # Authenticate with pairing code
uni wa logout                           # Logout
uni wa status                           # Check daemon status
uni wa stop                             # Stop daemon
```

## Send Messages

```bash
uni wa send me "Hello!"                 # Send to self (saved messages)
uni wa send 919876543210 "Hi"           # Send to phone number
uni wa send me "Check this" --file photo.jpg   # Send file with caption
uni wa send me "Reply" --reply ABC123   # Reply to message
```

## Read Messages

```bash
uni wa read me                          # Read from saved messages
uni wa read me -n 20                    # Last 20 messages
uni wa read 919876543210                # Read from contact
```

## Edit/Delete/React

```bash
uni wa edit me ABC123 "Fixed typo"      # Edit message
uni wa delete me ABC123                 # Delete message
uni wa react me ABC123 "👍"             # React to message
```

## Forward

```bash
uni wa forward me 919876543210 ABC123   # Forward message
```

## List Chats

```bash
uni wa chats                            # List recent chats
uni wa chats -n 50                      # More results
```

## Notes

- `me` = your own saved messages
- Phone numbers: country code + number, no + or spaces (e.g., `919876543210`)
- Message IDs: use `--json` output to get IDs for edit/delete/react
- `--json` flag for machine-readable output
