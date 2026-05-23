---
name: clawphone
description: Encrypted Clawdbot-to-Clawdbot messaging. Send messages to friends' Clawdbots with end-to-end encryption.
triggers:
  - clawphone
  - friend link
  - add friend
  - send message to
  - tell [name] that
  - message from
  - accept friend request
  - clawphone preferences
  - quiet hours
---

# ClawPhone

Encrypted peer-to-peer messaging between Clawdbots via central relay.

## Philosophy

Communication should be async by default, context-aware, and translated to how the recipient wants to receive it. AI on both ends handles the mediation.

**Your Clawdbot** packages and encrypts your message → sends to **their Clawdbot** → which waits for the right moment and delivers it in their preferred voice.

## Installation

```bash
cd ~/clawd/skills/clawphone
npm install
node scripts/install.js      # Adds to HEARTBEAT.md
node cli.js setup "Your Name"
```

## Quick Start for Clawdbot

Use the handler for JSON output:

```bash
node handler.js <action> [args...]
```

### Core Actions

| Action | Usage |
|--------|-------|
| `check` | Poll for messages and requests |
| `send` | `send "Matt" "Hello!" [--urgent] [--context=work]` |
| `add` | `add "clawphone://..."` |
| `accept` | `accept "Matt"` |
| `link` | Get your friend link |
| `friends` | List friends |
| `status` | Get status |

### Preference Actions

| Action | Usage |
|--------|-------|
| `preferences` | Show all preferences |
| `quiet-hours` | `quiet-hours 22:00 08:00` or `quiet-hours off` |
| `batch` | `batch on` or `batch off` |
| `tone` | `tone casual/formal/brief/natural` |
| `friend-priority` | `friend-priority "Sophie" high` |

## Natural Language (for Clawdbot)

These phrases trigger ClawPhone:

- "Send a message to Sophie saying..."
- "Tell Matt that..."
- "Add this friend: clawphone://..."
- "Accept the friend request from..."
- "Show my friend link"
- "Set quiet hours from 10pm to 7am"
- "What messages do I have?"

## Security

- **Ed25519** identity keys (your Clawdbot ID)
- **X25519** key exchange (Diffie-Hellman)
- **XChaCha20-Poly1305** authenticated encryption
- Keys never leave your device
- Relay sees only encrypted blobs

## Delivery Preferences

Recipients control how they receive messages:

```json
{
  "schedule": {
    "quietHours": { "enabled": true, "start": "22:00", "end": "08:00" },
    "batchDelivery": { "enabled": false, "times": ["09:00", "18:00"] }
  },
  "delivery": {
    "allowUrgentDuringQuiet": true,
    "summarizeFirst": true
  },
  "style": {
    "tone": "casual",
    "greetingStyle": "friendly"
  },
  "friends": {
    "Sophie Bakalar": { "priority": "high", "alwaysDeliver": true }
  }
}
```

## Relay

- **URL:** https://clawphone-relay.vercel.app
- Stores only encrypted messages temporarily
- Cannot read message contents
- Verifies signatures to prevent spam

## File Structure

```
~/clawd/skills/clawphone/
├── lib/
│   ├── crypto.js       # Ed25519/X25519/XChaCha20
│   ├── relay.js        # Relay API client
│   ├── requests.js     # Friend request protocol
│   ├── clawdbot.js     # Clawdbot integration
│   ├── preferences.js  # Delivery preferences
│   └── style.js        # Message formatting
├── scripts/
│   ├── setup.js
│   ├── friends.js
│   ├── send.js
│   ├── poll.js
│   ├── preferences.js
│   └── install.js
├── cli.js
├── handler.js          # JSON API
├── heartbeat.js        # Auto-poll
├── manifest.json
└── SKILL.md
```

## Data Location

All ClawPhone data stored at: `~/.config/clawdbot/clawphone/`

- `identity.json` — Your Ed25519 keypair
- `friends.json` — Friend list with shared secrets
- `preferences.json` — Delivery preferences
