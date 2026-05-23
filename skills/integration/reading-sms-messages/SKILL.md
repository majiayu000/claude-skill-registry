---
name: reading-sms-messages
description: Read SMS and iMessage from macOS Messages app. Use when getting 2FA codes, checking recent texts, or searching message history.
allowed-tools: Read, Bash
---

# SMS Reader

**Location**: `~/Library/Messages/chat.db` (macOS Messages database)

**CLI**: `python -m tools.sms_reader.cli`

## Commands

```bash
# Get 2FA code from last 5 minutes
python -m tools.sms_reader.cli 2fa
python -m tools.sms_reader.cli 2fa --minutes 10 --sender "+1555"
python -m tools.sms_reader.cli 2fa --detailed  # full message info as JSON

# Recent messages
python -m tools.sms_reader.cli recent
python -m tools.sms_reader.cli recent --limit 10 --sender "+1555" --since-minutes 30

# Search messages by content
python -m tools.sms_reader.cli search "verification"
python -m tools.sms_reader.cli search "code" --limit 5

# List senders
python -m tools.sms_reader.cli senders
python -m tools.sms_reader.cli senders --limit 10 --since-days 7
```

## Requirements

- macOS with Messages app
- Full Disk Access for Python (System Settings > Privacy & Security > Full Disk Access)
