---
name: dingtalk-bridge
description: "DingTalk group chat bridge for Claude Code. Send markdown/text messages to DingTalk groups, receive @mentions and auto-execute via Claude CLI, run a 24/7 Stream bot. Triggers: dingtalk, send dingtalk, dingtalk bot, dingtalk message, send group message, 钉钉, 发群消息, 钉钉机器人"
allowed-tools: Bash
---

# DingTalk Bridge Skill

Bridges Claude Code with DingTalk group chat via the DingTalk Stream SDK + OpenAPI.

## Capabilities

| Feature | Description |
|---------|-------------|
| **Send Markdown** | Send rich markdown messages to a DingTalk group |
| **Send Text** | Send plain text messages |
| **Stream Bot** | 24/7 listener: receive @mentions, execute via `claude -p`, reply with results |
| **Auto Conv Discovery** | Conversation ID auto-saved on first @mention |
| **Keepalive** | 20s WebSocket ping prevents DingTalk 30-min timeout |
| **Crash Recovery** | Exponential backoff (5s to 60s) on disconnect |

## Quick Start

### 1. Install

```bash
bash "$CLAUDE_SKILL_DIR/scripts/install.sh"
```

The script will:
- Install Python dependencies (`dingtalk_stream`, `websockets`)
- Prompt for your DingTalk App Key & Secret (or read from env)
- Generate `config.json`
- Create `data/` directory for conversation state
- Optionally create a macOS LaunchAgent for 24/7 operation

### 2. Configure

Set credentials via **environment variables** (recommended):

```bash
export DINGTALK_APP_KEY="your_app_key"
export DINGTALK_APP_SECRET="your_app_secret"
export DINGTALK_WORKDIR="/path/to/your/project"  # optional
```

Or edit `config.json` in the skill directory (see `config.example.json`).

### 3. Get Conversation ID

The bot needs a conversation ID to send messages. Two ways:

**Auto (recommended):** Start the Stream bot, then @mention it in a DingTalk group. The conv ID is saved automatically.

**Manual:** If you already have the `openConversationId` and `robotCode`:
```bash
mkdir -p "$CLAUDE_SKILL_DIR/data"
echo '{"openConversationId":"YOUR_ID","robotCode":"YOUR_ROBOT_CODE"}' > "$CLAUDE_SKILL_DIR/data/conv.json"
```

## Commands

### Send a message

```bash
# Markdown (default)
python3 "$CLAUDE_SKILL_DIR/src/send.py" "**Bold** message with markdown"

# With custom title
python3 "$CLAUDE_SKILL_DIR/src/send.py" --title "Alert" "Server is down!"

# Plain text
python3 "$CLAUDE_SKILL_DIR/src/send.py" --text "Plain text message"
```

### Start the Stream Bot

```bash
python3 "$CLAUDE_SKILL_DIR/src/stream_bot.py"
```

The bot will:
1. Connect to DingTalk via Stream protocol
2. Listen for all @mentions in groups where the bot is added
3. Execute the message content via `claude -p "<message>" --continue`
4. Reply with the result as a markdown message

### Use as Python module

```python
import sys
sys.path.insert(0, "/path/to/dingtalk-bridge/src")
from send import send_markdown, send_text

send_markdown("Daily Report", "**Sent:** 50\n**Opened:** 18\n**Clicked:** 7")
send_text("Simple notification")
```

## Configuration Reference

| Config Key | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `app_key` | `DINGTALK_APP_KEY` | (required) | DingTalk App Key |
| `app_secret` | `DINGTALK_APP_SECRET` | (required) | DingTalk App Secret |
| `conv_file` | `DINGTALK_CONV_FILE` | `<skill>/data/conv.json` | Conversation metadata path |
| `workdir` | `DINGTALK_WORKDIR` | cwd | Working directory for claude CLI |
| `claude_bin` | `DINGTALK_CLAUDE_BIN` | `claude` | Path to claude binary |
| `max_reply` | `DINGTALK_MAX_REPLY` | `3000` | Max reply length (chars) |
| `keepalive` | `DINGTALK_KEEPALIVE` | `20` | WebSocket keepalive interval (seconds) |

## DingTalk App Setup (Prerequisites)

1. Go to [DingTalk Open Platform](https://open-dev.dingtalk.com/)
2. Create an **Enterprise Internal App** (企业内部应用)
3. Enable **Robot** capability (机器人)
4. Set message receive mode to **Stream** (Stream 模式)
5. Copy the App Key and App Secret
6. Add the bot to a group chat

## Running Tests

```bash
python3 "$CLAUDE_SKILL_DIR/tests/test_dingtalk.py"
```

## Architecture

```
dingtalk-bridge/
├── SKILL.md              # This file
├── config.example.json   # Example configuration
├── config.json           # Your config (gitignored)
├── data/
│   └── conv.json         # Auto-saved conversation metadata
├── src/
│   ├── __init__.py
│   ├── config.py         # Config loader (env > file > defaults)
│   ├── send.py           # Send messages (OpenAPI)
│   └── stream_bot.py     # Stream bot (receive + execute + reply)
├── scripts/
│   └── install.sh        # One-command setup
└── tests/
    └── test_dingtalk.py  # Regression tests
```
