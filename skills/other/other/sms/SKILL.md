---
name: sms
description: "Send, read, listen, respond, and manage SMS conversations via Telnyx and Twilio. Supports 8 phone numbers across both providers with auto-detection, conversation threading, MMS, real-time inbound listening, and soul-aware auto-reply. 8 Python scripts for SMS operations."
---

# SMS Skill

Send SMS/MMS, read inboxes, auto-reply as Claudius, and view conversation threads via Telnyx (2 numbers) and Twilio (6 numbers).

## When to Use This Skill

- Sending a text message to any phone number
- Reading recent SMS messages (inbox)
- Listening for real-time inbound messages (two-way SMS)
- Auto-replying to inbound SMS as Claudius (soul-aware responses)
- Viewing a conversation thread with a specific number
- Listing available phone numbers across providers
- Sending MMS with image attachments

## Prerequisites

Requires `requests` (`uv pip install --system requests`).

Credentials are loaded automatically:
- **Telnyx**: `TELNYX_API_KEY` env var, or falls back to `~/.claude.json` (already configured)
- **Twilio**: `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` env vars, or falls back to hardcoded defaults

## Quick Start

```bash
# Send a text
python3 ~/.claude/skills/sms/scripts/sms_send.py "+19175551234" "Hello from Claude"

# Read recent messages
python3 ~/.claude/skills/sms/scripts/sms_read.py -n 10

# View conversation with someone
python3 ~/.claude/skills/sms/scripts/sms_conversation.py "+19175551234"

# List all available numbers
python3 ~/.claude/skills/sms/scripts/sms_numbers.py

# Start real-time listener (background)
python3 ~/.claude/skills/sms/scripts/sms_listen.py --bg

# Check inbound messages
python3 ~/.claude/skills/sms/scripts/sms_inbox.py
```

---

## Available Scripts

### 1. sms_send.py — Send SMS/MMS

```bash
python3 ~/.claude/skills/sms/scripts/sms_send.py TO "MESSAGE" [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--from NUMBER` | Send from a specific number (auto-detects provider) |
| `--provider telnyx\|twilio` | Force a specific provider |
| `--media URL` | Attach media for MMS |

**Examples**:
```bash
# Send via Telnyx (default)
python3 ~/.claude/skills/sms/scripts/sms_send.py "+19175551234" "Meeting at 3pm"

# Send from a Twilio number
python3 ~/.claude/skills/sms/scripts/sms_send.py "+19175551234" "Hello" --from "+18508058037"

# Send MMS with image
python3 ~/.claude/skills/sms/scripts/sms_send.py "+19175551234" "Check this" --media "https://example.com/photo.jpg"
```

### 2. sms_read.py — Read Inbox

```bash
python3 ~/.claude/skills/sms/scripts/sms_read.py [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--to NUMBER` | Messages to a specific number |
| `--from-number NUMBER` | Messages from a specific sender |
| `--direction inbound\|outbound` | Filter by direction |
| `-n/--limit NUM` | Number of messages (default: 10) |
| `--provider telnyx\|twilio` | Query specific provider |
| `--all-providers` | Query both providers |

**Examples**:
```bash
# Read last 10 messages (Twilio recommended for reads)
python3 ~/.claude/skills/sms/scripts/sms_read.py -n 10 --provider twilio

# Messages to a specific number
python3 ~/.claude/skills/sms/scripts/sms_read.py --to "+18508058037" --provider twilio

# Only inbound messages
python3 ~/.claude/skills/sms/scripts/sms_read.py --direction inbound --provider twilio

# Query both providers
python3 ~/.claude/skills/sms/scripts/sms_read.py --all-providers -n 20
```

### 3. sms_conversation.py — View Conversation Thread

```bash
python3 ~/.claude/skills/sms/scripts/sms_conversation.py NUMBER [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `-n/--limit NUM` | Max messages per direction (default: 20) |
| `--our-number NUMBER` | Filter to a specific one of our numbers |
| `--provider telnyx\|twilio` | Query specific provider |
| `--all-providers` | Query both providers |

**Examples**:
```bash
# View conversation with a number
python3 ~/.claude/skills/sms/scripts/sms_conversation.py "+19175551234" --provider twilio

# Limit to last 10 messages per direction
python3 ~/.claude/skills/sms/scripts/sms_conversation.py "+19175551234" -n 10 --provider twilio

# Filter to a specific one of our numbers
python3 ~/.claude/skills/sms/scripts/sms_conversation.py "+19175551234" --our-number "+18508058037"
```

### 4. sms_numbers.py — List Available Numbers

```bash
python3 ~/.claude/skills/sms/scripts/sms_numbers.py [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--provider telnyx\|twilio` | Filter by provider |
| `--live` | Query APIs for live status (slower) |

**Examples**:
```bash
# List all 8 numbers
python3 ~/.claude/skills/sms/scripts/sms_numbers.py

# Twilio numbers only
python3 ~/.claude/skills/sms/scripts/sms_numbers.py --provider twilio

# Live API status check
python3 ~/.claude/skills/sms/scripts/sms_numbers.py --live
```

### 5. sms_listen.py — Real-Time Inbound Listener

Background daemon that polls Twilio for new inbound messages and runs a webhook server for Telnyx inbound. Messages are written to `data/inbox.jsonl`.

```bash
python3 ~/.claude/skills/sms/scripts/sms_listen.py [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--bg` | Run in background (daemonize) |
| `--stop` | Stop running listener |
| `--status` | Check if listener is running |
| `--interval N` | Twilio poll interval in seconds (default: 10) |
| `--numbers +1... +1...` | Twilio numbers to monitor (default: all 6) |
| `--webhook-port N` | Telnyx webhook port (default: 9147) |
| `--no-telnyx` | Disable Telnyx webhook server |
| `--no-twilio` | Disable Twilio polling |

**Examples**:
```bash
# Start listener in background
python3 ~/.claude/skills/sms/scripts/sms_listen.py --bg

# Check status
python3 ~/.claude/skills/sms/scripts/sms_listen.py --status

# Stop listener
python3 ~/.claude/skills/sms/scripts/sms_listen.py --stop

# Monitor only the Aldea production number, poll every 5s
python3 ~/.claude/skills/sms/scripts/sms_listen.py --bg --numbers +18557066006 --interval 5

# Telnyx webhook only (no Twilio polling)
python3 ~/.claude/skills/sms/scripts/sms_listen.py --bg --no-twilio
```

**Telnyx webhook setup**: Point your Telnyx Messaging Profile webhook URL to `http://localhost:9147/telnyx`. For remote access, use ngrok or similar tunnel.

### 6. Auto-Reply — Two Modes

#### Mode A: `/sms-respond` Slash Command (Interactive)

Process unhandled SMS using the **current Claude Code session** as the LLM. No subprocess needed—follows the same pattern as `/slack-respond`.

```
/sms-respond        # Process all unhandled messages
/sms-respond 2      # Process only message #2 from inbox
```

The slash command loads inbox, soul.md, and memory context dynamically, then walks through a 6-step cognitive pipeline (internal monologue → external dialogue → user model check → user model update → soul state check → soul state update). Replies are sent via `sms_send.py` and all memory layers are updated.

**Use this when**: You're in an active Claude Code session and want to reply to SMS.

#### Mode B: `sms_respond.py` Daemon (Standalone)

Standalone daemon for Mac Mini or headless deployment. Uses `claude -p` subprocess to generate responses. **Does not work from within a running Claude Code session** (subprocess nesting conflict).

```bash
python3 ~/.claude/skills/sms/scripts/sms_respond.py [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--daemon` | Loop continuously, polling inbox |
| `--bg` | Run daemon in background (requires `--daemon`) |
| `--status` | Check if responder daemon is running |
| `--stop` | Stop running responder daemon |
| `--interval N` | Poll interval in seconds (default: 5) |
| `--model MODEL` | Override LLM model (default: claude-sonnet-4-5-20250514) |
| `--no-soul` | Disable soul context (plain responses) |
| `--dry-run` | Process messages without sending replies |

**Examples**:
```bash
# Start auto-reply daemon in background (Mac Mini)
python3 ~/.claude/skills/sms/scripts/sms_respond.py --daemon --bg

# Check daemon status
python3 ~/.claude/skills/sms/scripts/sms_respond.py --status

# Stop daemon
python3 ~/.claude/skills/sms/scripts/sms_respond.py --stop
```

**Use this when**: Running headless on Mac Mini or outside Claude Code.

#### Shared Infrastructure

Both modes require `sms_listen.py` running to feed `inbox.jsonl`.

**Memory**: 3-tier SQLite at `data/sms_memory.db`:
- Working memory — per-conversation message history + cognitive outputs
- User models — per-phone-number personality profiles
- Soul memory — cross-conversation soul state

### 7. sms_inbox.py — Read Inbound Inbox

Read messages collected by `sms_listen.py`.

```bash
python3 ~/.claude/skills/sms/scripts/sms_inbox.py [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--all` | Show all messages (including handled) |
| `-n/--limit NUM` | Number of messages to show |
| `--from NUMBER` | Filter by sender number |
| `--provider telnyx\|twilio` | Filter by provider |
| `--mark-read ID` | Mark a specific message as handled |
| `--mark-all-read` | Mark all messages as handled |

**Examples**:
```bash
# Show unhandled messages
python3 ~/.claude/skills/sms/scripts/sms_inbox.py

# Show last 5 messages from a specific sender
python3 ~/.claude/skills/sms/scripts/sms_inbox.py --from "+15551234567" -n 5

# Mark all as read
python3 ~/.claude/skills/sms/scripts/sms_inbox.py --mark-all-read
```

---

## Configuration

### Provider Auto-Detection

When you use `--from`, the skill detects the provider by matching against known numbers:
- Telnyx numbers: `+18628026208`, `+18334843851`
- Twilio numbers: `+13205950420`, `+18557066006`, `+18559149834`, `+18776882519`, `+18665517616`, `+18778377603`, `+18665650327`, `+18667056747`, `+18445491928`

### Defaults

| Setting | Value |
|---------|-------|
| Default provider | Telnyx |
| Default Telnyx from | `+18628026208` |
| Default Twilio from | `+18557066006` (Claudius 855) |

Edit `_sms_utils.py` to change defaults.

### Local Message Log

All sent messages are automatically logged to `~/.claude/skills/sms/data/messages.jsonl` (JSONL format). This enables:
- **Telnyx conversation history**: Since Telnyx is send-only (no REST API for reading messages), the local log provides the only record of Telnyx messages.
- **Offline message browsing**: Read/conversation scripts automatically fall back to the local log when Telnyx API returns 404.
- **Per-number history**: Filter by any phone number to see all correspondences.

The log grows with each sent message. To reset, delete `data/messages.jsonl`.

### Known Limitations

- **Telnyx is send-only**: Telnyx has no `GET /v2/messages` endpoint — message receiving is webhook-based only. Sent messages are tracked via the local log. For full read/conversation capability, use `--provider twilio` or `--all-providers`.

---

## Phone Number Reference

### Telnyx
| Number | Type | Label | Reserved |
|--------|------|-------|----------|
| `+18628026208` | Longcode | Primary (default) | Aldea / Dr. Shefali |
| `+18334843851` | Toll-free | Secondary | Aldea (dev/backup) |

### Twilio (9 numbers — verified live 2026-03-03)
| Number | Type | Label | Reserved |
|--------|------|-------|----------|
| `+13205950420` | Local | Claudius 320 | Claudius (broken—needs 10DLC registration) |
| `+18557066006` | Toll-free | Claudius 855 | Claudius (2-way) |
| `+18559149834` | Toll-free | 855 number | Available |
| `+18776882519` | Local | 877 number | Available |
| `+18665517616` | Local | 866 number | Available |
| `+18778377603` | Local | 877-837 number | Available |
| `+18665650327` | Local | 866-565 number | Available |
| `+18667056747` | Local | 866-705 number | Available |
| `+18445491928` | Local | 844 number | Available |
