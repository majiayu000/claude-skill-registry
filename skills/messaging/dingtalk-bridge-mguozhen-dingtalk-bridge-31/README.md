<p align="center">
  <img src="https://img.alicdn.com/imgextra/i3/O1CN01Kpgs1i1duSbfODzCm_!!6000000003797-2-tps-240-240.png" width="80" alt="DingTalk Bridge">
</p>

<h1 align="center">DingTalk Bridge</h1>

<p align="center">
  <strong>Connect any Claude Code agent to DingTalk group chat in 60 seconds.</strong>
</p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/setup-60s-brightgreen?style=flat-square" alt="60s Setup"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-blue?style=flat-square" alt="Agent Skills"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License"></a>
  <a href="https://code.claude.com"><img src="https://img.shields.io/badge/Claude%20Code-skill-8B5CF6?style=flat-square" alt="Claude Code Skill"></a>
  <img src="https://img.shields.io/badge/python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/tests-27%20passed-brightgreen?style=flat-square" alt="27 Tests Passed">
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#commands">Commands</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#faq">FAQ</a>
</p>

---

## What is this?

**DingTalk Bridge** is a [Claude Code skill](https://code.claude.com/docs/en/skills) that bridges your AI coding agent with [DingTalk](https://www.dingtalk.com/) (Alibaba's enterprise messaging platform). Once installed, your Claude Code agent can:

- **Send** rich Markdown or plain text messages to any DingTalk group
- **Receive** @mentions and auto-execute them via `claude -p`
- **Run 24/7** as a Stream bot with crash recovery and keepalive

Think of it as giving your Claude Code agent a DingTalk phone number.

## Features

| Feature | Description |
|---------|-------------|
| **Send Messages** | Markdown and plain text via DingTalk OpenAPI |
| **Stream Bot** | Persistent WebSocket listener for real-time @mention handling |
| **Auto-Execute** | Incoming messages run as Claude Code prompts, results posted back |
| **Crash Recovery** | Exponential backoff (5s to 60s) on disconnect, auto-restart via LaunchAgent |
| **20s Keepalive** | Custom WebSocket ping prevents DingTalk's 30-min timeout |
| **Zero Hardcoded Secrets** | Config via env vars or `config.json`, never in source code |
| **One-Command Install** | `bash install.sh` handles deps, credentials, and optional LaunchAgent |
| **27 Regression Tests** | Full test coverage with mocked API calls, no network required |

## Quick Start

### 1. Install the skill

```bash
# Clone into your Claude Code skills directory
git clone https://github.com/mguozhen/dingtalk-bridge.git ~/.claude/skills/dingtalk-bridge

# Run the installer
bash ~/.claude/skills/dingtalk-bridge/scripts/install.sh
```

The installer will:
- Install Python dependencies (`dingtalk_stream`, `websockets`)
- Prompt for your DingTalk App Key & Secret
- Generate `config.json` (chmod 600)
- Optionally create a macOS LaunchAgent for 24/7 operation

### 2. Prerequisites: Create a DingTalk App

1. Go to [DingTalk Open Platform](https://open-dev.dingtalk.com/)
2. Create an **Enterprise Internal App** (企业内部应用)
3. Enable **Robot** capability (机器人)
4. Set message receive mode to **Stream** (Stream 模式)
5. Copy the **App Key** and **App Secret**
6. Add the bot to a group chat

### 3. Start the bot

```bash
python3 ~/.claude/skills/dingtalk-bridge/src/stream_bot.py
```

@mention the bot in your group. It will auto-save the conversation ID and start responding.

### 4. Send messages from Claude Code

Once the skill is installed, Claude Code auto-discovers it. Just say:

> "Send a DingTalk message: today's build passed all tests"

Or use it programmatically:

```bash
python3 ~/.claude/skills/dingtalk-bridge/src/send.py "**Build Status**: All 142 tests passed"
```

## Commands

### CLI

```bash
# Send markdown message (default)
python3 src/send.py "**Bold** message with _markdown_"

# Send with custom title
python3 src/send.py --title "Deploy Alert" "Production deploy complete"

# Send plain text
python3 src/send.py --text "Simple notification"

# Start the Stream bot
python3 src/stream_bot.py
```

### Python Module

```python
from dingtalk_bridge.src.send import send_markdown, send_text

# Rich markdown
send_markdown("Daily Report", """
**Sent:** 50
**Opened:** 18 (36%)
**Clicked:** 7 (14%)
""")

# Plain text
send_text("Deployment complete.")
```

## Configuration

Config priority: **Environment Variables** > **config.json** > **Defaults**

| Config Key | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `app_key` | `DINGTALK_APP_KEY` | *(required)* | DingTalk App Key |
| `app_secret` | `DINGTALK_APP_SECRET` | *(required)* | DingTalk App Secret |
| `conv_file` | `DINGTALK_CONV_FILE` | `data/conv.json` | Conversation metadata path |
| `workdir` | `DINGTALK_WORKDIR` | cwd | Working directory for `claude` CLI |
| `claude_bin` | `DINGTALK_CLAUDE_BIN` | `claude` | Path to Claude binary |
| `max_reply` | `DINGTALK_MAX_REPLY` | `3000` | Max reply length (chars) |
| `keepalive` | `DINGTALK_KEEPALIVE` | `20` | WebSocket keepalive interval (sec) |

### Example: Environment Variables

```bash
export DINGTALK_APP_KEY="your_key_here"
export DINGTALK_APP_SECRET="your_secret_here"
export DINGTALK_WORKDIR="$HOME/my-project"
```

### Example: config.json

```json
{
  "app_key": "your_key_here",
  "app_secret": "your_secret_here",
  "workdir": "/home/user/my-project"
}
```

## Architecture

```
dingtalk-bridge/
├── SKILL.md                # Claude Code skill definition
├── README.md               # This file
├── LICENSE                  # MIT License
├── config.example.json     # Config template
├── marketplace.json        # Skill registry metadata
├── data/
│   └── conv.json           # Auto-saved conversation state
├── src/
│   ├── __init__.py
│   ├── config.py           # Config loader (env > file > defaults)
│   ├── send.py             # DingTalk OpenAPI messaging
│   └── stream_bot.py       # Stream bot (listen + execute + reply)
├── scripts/
│   └── install.sh          # One-command setup
└── tests/
    └── test_dingtalk.py    # 27 regression tests
```

### Message Flow

```
You (@mention bot in DingTalk group)
        |
        v
DingTalk Stream API (WebSocket)
        |
        v
stream_bot.py: BridgeHandler.process()
        |
        +-- save_conv_info() --> data/conv.json
        |
        +-- threading.Thread(execute_prompt)
                |
                +-- reply("Processing...") via webhook
                |
                +-- subprocess: claude -p "<your message>" --continue
                |
                +-- send_markdown("Done", result) via OpenAPI
                        |
                        v
                DingTalk Group (result displayed)
```

## Running Tests

```bash
python3 tests/test_dingtalk.py
```

```
test_env_var_takes_priority ... ok
test_file_config_fallback ... ok
test_require_raises_on_missing ... ok
test_send_markdown_payload ... ok
test_reply_via_webhook ... ok
test_execute_prompt_success ... ok
test_execute_prompt_timeout ... ok
test_handler_process_spawns_thread ... ok
test_no_hardcoded_credentials ... ok
...
----------------------------------------------------------------------
Ran 27 tests in 0.15s

OK
```

All tests run offline with mocked API calls. No DingTalk credentials required.

## FAQ

<details>
<summary><strong>How do I get the conversation ID?</strong></summary>

Start the Stream bot, then @mention it in any DingTalk group. The conversation ID is automatically saved to `data/conv.json`. You only need to do this once per group.
</details>

<details>
<summary><strong>Can I use this with multiple groups?</strong></summary>

The current implementation saves one conversation at a time. For multiple groups, you can manually set the `conv_file` config to different paths per group, or extend `send.py` to accept a conversation ID parameter.
</details>

<details>
<summary><strong>What happens if the bot crashes?</strong></summary>

The bot has built-in exponential backoff (5s to 60s) and will auto-reconnect. If you set up the LaunchAgent via `install.sh`, macOS will also restart the process if it exits.
</details>

<details>
<summary><strong>Does this work on Linux?</strong></summary>

Yes. The Python code is cross-platform. The LaunchAgent setup is macOS-only, but you can use systemd on Linux instead. A systemd unit file example:

```ini
[Unit]
Description=DingTalk Bridge Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/dingtalk-bridge/src/stream_bot.py
Restart=always
RestartSec=5
Environment=DINGTALK_APP_KEY=your_key
Environment=DINGTALK_APP_SECRET=your_secret
Environment=DINGTALK_WORKDIR=/path/to/project

[Install]
WantedBy=multi-user.target
```
</details>

<details>
<summary><strong>Is this an official Anthropic product?</strong></summary>

No. This is a community skill that follows the open <a href="https://agentskills.io">Agent Skills</a> specification. It works with Claude Code but is independently maintained.
</details>

## Contributing

PRs welcome. Please ensure all 27 tests pass before submitting:

```bash
python3 tests/test_dingtalk.py
```

## License

[MIT](LICENSE)

---

<p align="center">
  Built for <a href="https://code.claude.com">Claude Code</a> &bull; Powered by <a href="https://open.dingtalk.com">DingTalk Open Platform</a>
</p>
