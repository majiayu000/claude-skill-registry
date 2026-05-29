---
name: discord-ops
description: >
  TOS-compliant Discord notification monitor. Watches YOUR Discord server for
  security content forwarded by researchers, matches keywords, and pushes to
  paper-writer/dogpile via webhooks. Persists to graph-memory for semantic search.
allowed-tools:
  - Bash
  - Read
  - Write
triggers:
  - discord
  - discord monitor
  - discord notifications
  - discord keywords
  - security discord
  - discord webhook
metadata:
  short-description: Discord keyword monitor with webhook + memory integration
---

# Discord Operations - Notification Monitor Model

**TOS-compliant** approach to Discord security intelligence gathering.

## The Key Insight

**OLD (Broken):** Try to search external servers where you're not admin → TOS violation, impossible

**NEW (Works):** Monitor YOUR OWN server for content forwarded by researchers → 100% compliant

## Architecture

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                   TOS-Compliant Discord Pipeline + Memory                      │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  External Sources              Your Server (Admin)            Consumers        │
│  ────────────────              ────────────────────            ─────────        │
│                                                                                │
│  ┌─────────────┐               ┌──────────────────┐                           │
│  │ Researchers │──DM/forward──▶│ #security-intel  │                           │
│  │ share       │               │                  │                           │
│  │ insights    │               │  Your Bot        │──webhook──▶ paper-writer  │
│  └─────────────┘               │  (keyword watch) │                           │
│                                │                  │──webhook──▶ dogpile       │
│  ┌─────────────┐               │  Keywords:       │                           │
│  │ Telegram    │──bridge──▶    │  CVE, DARPA,     │                           │
│  │ bridges     │  (social-     │  HTB, 0-day...   │                           │
│  └─────────────┘   bridge)     └────────┬─────────┘                           │
│                                         │                                      │
│                           ┌─────────────┼─────────────┐                       │
│                           ▼             ▼             ▼                        │
│                    ┌──────────┐  ┌──────────────┐  ┌────────────┐             │
│                    │ matches  │  │ graph-memory │  │  dogpile   │             │
│                    │ .jsonl   │  │  (ArangoDB)  │  │  search    │             │
│                    │ (local)  │  │   lessons    │  │            │             │
│                    └──────────┘  └──────┬───────┘  └─────┬──────┘             │
│                                         │                │                     │
│                                         └────────────────┘                     │
│                                         (semantic recall)                      │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Check setup
./run.sh setup

# 2. Add your Discord server to monitor
./run.sh guild add "Security Intel" 1234567890123456789

# 3. Add webhook for forwarding matches
./run.sh webhook add alerts "https://discord.com/api/webhooks/..."

# 4. Start monitoring
./run.sh monitor start --webhook alerts
```

## Commands

### `setup` - Check Configuration

```bash
./run.sh setup
```

Shows status of:
- Bot token (from env or clawdbot)
- discord.py library
- httpx for webhooks
- Current configuration

### `keywords` - Manage Watch Patterns

```bash
# List all keywords (regex patterns)
./run.sh keywords list

# Add a keyword pattern
./run.sh keywords add "CVE-2025-\d+"
./run.sh keywords add "supply.?chain"

# Remove a pattern
./run.sh keywords remove "HTB"

# Reset to defaults
./run.sh keywords reset
```

**Default Keywords:**
- Vulnerabilities: `CVE-\d{4}-\d+`, `0-?day`, `exploit`, `RCE`, `LPE`, `privesc`
- Programs: `DARPA`, `IARPA`, `BAA`, `grants?\.gov`
- Platforms: `HTB`, `TryHackMe`, `CTF`
- Threat Intel: `APT\d+`, `malware`, `ransomware`, `C2`, `cobalt.?strike`
- Techniques: `MITRE`, `ATT&CK`, `T\d{4}`

### `guild` - Manage Monitored Servers

```bash
# List monitored guilds
./run.sh guild list

# Add a guild to monitor
./run.sh guild add "My Server" 1234567890123456789

# Remove a guild
./run.sh guild remove "My Server"
```

### `webhook` - Manage Output Webhooks

```bash
# List webhooks
./run.sh webhook list

# Add a webhook
./run.sh webhook add alerts "https://discord.com/api/webhooks/..."
./run.sh webhook add paper-writer "http://localhost:8000/paperwriter/discord"

# Remove a webhook
./run.sh webhook remove alerts

# Test a webhook
./run.sh webhook test alerts
```

### `monitor` - Run the Monitor

```bash
# Check status
./run.sh monitor status

# Start monitoring (foreground)
./run.sh monitor start --webhook alerts

# Start in dry-run mode (log only, don't forward)
./run.sh monitor start --dry-run

# Stop the monitor
./run.sh monitor stop
```

### `matches` - View Logged Matches

```bash
# Show recent matches
./run.sh matches

# Show more matches
./run.sh matches --limit 50

# Filter by keyword
./run.sh matches --keyword CVE

# Output as JSON
./run.sh matches --json
```

### `memory` - Knowledge Graph Integration

```bash
# Check memory integration status
./run.sh memory status

# Search stored matches in memory
./run.sh memory search "CVE-2024"

# Search with JSON output
./run.sh memory search "ransomware" --json --k 20

# Ingest existing matches from log file to memory
./run.sh memory ingest --limit 100
```

**Auto-Persistence:**
The monitor automatically persists matches to memory by default:
```bash
# Start with memory persistence (default)
./run.sh monitor start --webhook alerts

# Start without memory persistence
./run.sh monitor start --webhook alerts --no-persist
```

## Webhook Payload Formats

### Discord Webhook (auto-detected by URL)

```json
{
  "embeds": [{
    "title": "Keyword Match: CVE-2024-1234, exploit",
    "description": "New RCE exploit for CVE-2024-1234...",
    "url": "https://discord.com/channels/...",
    "color": 5793266,
    "author": {"name": "researcher#1234"},
    "footer": {"text": "Security Intel #cve-alerts"},
    "timestamp": "2026-01-28T12:00:00Z"
  }]
}
```

### Generic Webhook (paper-writer/dogpile)

```json
{
  "source": "discord",
  "content": "New RCE exploit for CVE-2024-1234...",
  "author": "researcher#1234",
  "channel": "Security Intel/#cve-alerts",
  "url": "https://discord.com/channels/...",
  "keywords": ["CVE-2024-1234", "exploit"],
  "timestamp": "2026-01-28T12:00:00Z"
}
```

## Setup Your Security Intel Server

### Step 1: Create Server

Create a Discord server for aggregating security intel:
- `#cve-alerts` - CVE announcements
- `#research-feed` - General security research
- `#threat-intel` - APT/malware news
- `#darpa-baa` - Funding opportunities

### Step 2: Add Your Bot

1. Use the bot from clawdbot or create a new one
2. Required permissions: `Read Messages`, `Read Message History`, `View Channels`
3. Get guild ID: Server Settings → Widget → Server ID

### Step 3: Invite Researchers

- Researchers can forward content from other servers to your channels
- Or set up Telegram bridges (see social-bridge skill)
- Bot watches for keywords in YOUR server only

### Step 4: Configure Webhooks

Create webhooks in your destination channels or endpoints:
- Discord webhook for alerts channel
- HTTP webhook for paper-writer integration
- Generic webhook for ArangoDB logging

## Integration with paper-writer

```bash
# paper-writer endpoint receives Discord matches
POST /paperwriter/discord
{
  "source": "discord",
  "content": "...",
  "keywords": ["CVE-...", "exploit"],
  ...
}

# Gets auto-indexed alongside arXiv/SAM.gov pulls
```

## Integration with social-bridge

The social-bridge skill can forward Telegram content to your Discord server:

```
Telegram Public Channels → social-bridge → Your Discord → discord-ops → paper-writer
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Bot token | Yes (or in clawdbot .env) |
| `CLAWDBOT_DIR` | Path to clawdbot | No (default: ~/workspace/experiments/clawdbot) |

## Files

```
.pi/skills/discord-ops/
├── discord_ops.py    # Main CLI
├── run.sh            # Runner script
├── config.json       # Guilds and webhooks config
├── keywords.json     # Watched keyword patterns
├── matches.jsonl     # Logged keyword matches
└── monitor.pid       # PID file when running
```

## Why This Works

| Aspect | This Approach |
|--------|---------------|
| **TOS** | Compliant - monitoring YOUR server |
| **Admin access** | Only needed on YOUR server |
| **Real-time** | Yes - event-driven via Gateway |
| **Scalable** | Limited by webhook rate limits |
| **Reliable** | Uses official Discord API |

## Comparison with Old Approach

| Feature | Old (Search) | New (Monitor) |
|---------|--------------|---------------|
| Search external servers | Attempted | Not needed |
| Requires admin on target | Yes (impossible) | No |
| TOS compliant | No | Yes |
| Real-time | No | Yes |
| Works | No | Yes |
