---
name: social-bridge
description: >
  Aggregate security content from Telegram public channels and X/Twitter accounts,
  forward to Discord webhooks, and persist to graph-memory. Uses Telethon (MTProto)
  for Telegram, surf browser automation for X, and Discord webhooks for delivery.
allowed-tools:
  - Bash
  - Read
  - Write
triggers:
  - telegram
  - telegram channel
  - security telegram
  - x scrape
  - twitter scrape
  - social media aggregator
  - security feeds
  - aggregate feeds
  - forward to discord
metadata:
  short-description: Telegram/X aggregator with Discord + memory integration
---

# Social Bridge - Security Content Aggregator

Aggregate security research content from multiple social platforms, forward to your Discord server, and persist to the knowledge graph for semantic search.

## Data Sources

| Platform | Method | Auth Required | Can Read Public |
|----------|--------|---------------|-----------------|
| **Telegram** | Telethon (MTProto) | API ID + phone | Yes |
| **X/Twitter** | surf browser automation | Logged-in browser | Yes |
| **Discord** | Webhooks | Webhook URL | N/A (output only) |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Social Bridge Aggregator + Memory Integration             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │  Telegram   │    │  X/Twitter  │    │   RSS/Web   │                     │
│  │  (Telethon) │    │   (surf)    │    │  (future)   │                     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                     │
│         │                  │                  │                             │
│         └──────────────────┼──────────────────┘                             │
│                            ▼                                                │
│                   ┌─────────────────┐                                       │
│                   │   Aggregator    │                                       │
│                   │ (dedupe, filter)│                                       │
│                   └────────┬────────┘                                       │
│                            │                                                │
│         ┌──────────────────┼───────────────────┐                           │
│         ▼                  ▼                   ▼                            │
│   ┌──────────┐       ┌──────────┐       ┌────────────────┐                 │
│   │ Discord  │       │  JSON    │       │  graph-memory  │                 │
│   │ Webhook  │       │  Export  │       │   (ArangoDB)   │                 │
│   └──────────┘       └──────────┘       └───────┬────────┘                 │
│                                                 │                           │
│                                                 ▼                           │
│                                         ┌──────────────┐                   │
│                                         │   Dogpile    │                   │
│                                         │ (search/recall)│                 │
│                                         └──────────────┘                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Setup (one-time)
./run.sh setup

# Add sources
./run.sh telegram add "@vaborivs"           # Telegram channel
./run.sh x add "malaborwaretechblog"        # X/Twitter account

# Add Discord webhook for forwarding
./run.sh webhook add "security" "https://discord.com/api/webhooks/..."

# Fetch latest content
./run.sh fetch --all

# Forward to Discord
./run.sh forward --webhook security --hours 24
```

## Commands

### `setup` - Initial Configuration

```bash
# Interactive setup wizard
./run.sh setup

# This will:
# 1. Check/configure Telegram API credentials
# 2. Check surf browser setup
# 3. Configure Discord webhook
```

### `telegram` - Telegram Channel Management

```bash
# Add a public channel to monitor
./run.sh telegram add "@channel_name"
./run.sh telegram add "https://t.me/channel_name"

# List monitored channels
./run.sh telegram list

# Remove a channel
./run.sh telegram remove "@channel_name"

# Fetch messages from all channels
./run.sh telegram fetch --limit 50

# Fetch from specific channel
./run.sh telegram fetch "@channel_name" --limit 100
```

### `x` - X/Twitter Account Management

```bash
# Add an account to monitor
./run.sh x add "username"

# List monitored accounts
./run.sh x list

# Remove an account
./run.sh x remove "username"

# Fetch tweets (uses surf browser automation)
./run.sh x fetch --limit 50

# Fetch from specific account
./run.sh x fetch "username" --limit 100
```

### `webhook` - Discord Webhook Management

```bash
# Add a webhook
./run.sh webhook add "name" "https://discord.com/api/webhooks/..."

# List webhooks
./run.sh webhook list

# Remove a webhook
./run.sh webhook remove "name"

# Test a webhook
./run.sh webhook test "name"
```

### `fetch` - Fetch Content

```bash
# Fetch from all sources
./run.sh fetch --all

# Fetch only Telegram
./run.sh fetch --telegram

# Fetch only X/Twitter
./run.sh fetch --x

# With time filter
./run.sh fetch --all --hours 24

# Output as JSON
./run.sh fetch --all --json
```

### `forward` - Forward to Discord

```bash
# Forward recent content to Discord
./run.sh forward --webhook security --hours 24

# Forward with keyword filter
./run.sh forward --webhook security --filter "CVE,0day,exploit"

# Dry run (show what would be sent)
./run.sh forward --webhook security --dry-run
```

### `memory` - Knowledge Graph Integration

```bash
# Check memory integration status
./run.sh memory status

# Ingest all content to memory (fetch + persist)
./run.sh memory ingest --hours 24

# Ingest only Telegram
./run.sh memory ingest --telegram --hours 24

# Search stored social intel
./run.sh memory search "CVE-2024"

# Search with JSON output
./run.sh memory search "malware analysis" --json --k 20
```

**Auto-Fetch with Persistence:**
```bash
# Fetch and persist in one command
./run.sh fetch --all --persist

# Telegram fetch with persistence
./run.sh telegram fetch --persist
```

### `aggregate` - Scheduled Aggregation

```bash
# Run aggregation (fetch + forward)
./run.sh aggregate --webhook security

# Schedule hourly aggregation
./run.sh aggregate schedule --cron "0 * * * *" --webhook security

# View scheduled jobs
./run.sh aggregate status
```

## Pre-configured Security Channels

### Telegram Channels

| Channel | Focus |
|---------|-------|
| @vaborivs | Vulnerability research |
| @cikitech | Malware/threats |
| @TheHackersNews | Security news |
| @exploitin | Exploit announcements |
| @bugcrowd | Bug bounty |
| @CISAgov | CISA alerts |

### X/Twitter Accounts

| Account | Focus |
|---------|-------|
| malwaretechblog | Malware analysis |
| kloswonsecurity | Security news |
| SwiftOnSecurity | Security humor + insights |
| 0xdea | Vulnerability research |
| thegrugq | OpSec, threat intel |

## Telegram Setup (One-time)

1. Get API credentials at https://my.telegram.org/apps
2. Save to environment:
   ```bash
   export TELEGRAM_API_ID="your_api_id"
   export TELEGRAM_API_HASH="your_api_hash"
   ```
3. First run will prompt for phone number + code
4. Session file created at `~/.social-bridge/telegram.session`

## X/Twitter Setup (One-time)

1. Ensure surf-cli is installed and working:
   ```bash
   surf tab.list  # Should show browser tabs
   ```
2. Log into X/Twitter in your browser
3. social-bridge uses surf to scrape while logged in

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_API_ID` | Telegram API ID | For Telegram |
| `TELEGRAM_API_HASH` | Telegram API hash | For Telegram |
| `DISCORD_WEBHOOK_URL` | Default Discord webhook | For forwarding |

## Integration with Memory (graph-memory)

Social-bridge persists content to the `social_intel` scope in ArangoDB via the memory skill.

### Auto-Tagging

Posts are automatically tagged with security keywords:
- `cve` - CVE identifiers (CVE-2024-XXXX)
- `apt` - APT groups (APT29, APT41)
- `darpa` - DARPA/IARPA/BAA mentions
- `0day` - Zero-day references
- `exploit` - Exploit/RCE/LPE mentions
- `malware` - Malware/ransomware mentions
- `ctf` - CTF/HTB/TryHackMe
- `mitre` - MITRE ATT&CK references
- `c2` - C2/Cobalt Strike
- `ioc` - IOC/indicator mentions

### Memory Schema

Posts are stored as lessons with:
```json
{
  "problem": "[TELEGRAM] @vxunderground: New ransomware variant...",
  "solution": {
    "content": "Full post content...",
    "url": "https://t.me/vxunderground/12345",
    "author": "vx-underground",
    "timestamp": "2026-01-28T12:00:00Z",
    "platform": "telegram",
    "source": "vxunderground",
    "metadata": {"views": 5000, "forwards": 120}
  },
  "scope": "social_intel",
  "tags": ["telegram", "source:vxunderground", "malware", "ransomware"]
}
```

## Integration with Dogpile

Dogpile can query stored social intel via the memory skill:

```bash
# Dogpile searches memory automatically
dogpile search "CVE-2024-1234" --preset vulnerability_research

# Memory recall returns stored social intel
./run.sh memory search "ransomware variant"
```

**Pipeline:**
```
social-bridge fetch --persist → memory (ArangoDB) → dogpile recall
```

## Data Storage

Content is cached locally for deduplication:

```
~/.social-bridge/
├── config.json          # Sources and webhooks
├── telegram.session     # Telegram session (DO NOT SHARE)
├── cache/
│   ├── telegram/        # Cached Telegram messages
│   └── x/               # Cached X tweets
└── logs/
    └── aggregate.log    # Aggregation history
```

## Rate Limits & Best Practices

| Platform | Recommendation |
|----------|----------------|
| Telegram | Max 50 channels, 100 msgs/channel/hour |
| X/Twitter | Max 20 accounts, 50 tweets/account/hour |
| Discord | Max 30 messages/minute per webhook |

## Example: Security Feed Aggregator

```bash
# One-time setup
./run.sh setup
./run.sh telegram add "@vaborivs" "@exploitin" "@CISAgov"
./run.sh x add "malwaretechblog" "SwiftOnSecurity"
./run.sh webhook add "security" "$DISCORD_WEBHOOK_URL"

# Schedule hourly aggregation
./run.sh aggregate schedule --cron "0 * * * *" --webhook security

# Manual fetch when needed
./run.sh fetch --all --hours 1
./run.sh forward --webhook security --filter "CVE,0day,critical"
```
