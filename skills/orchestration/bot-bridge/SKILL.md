---
name: bot-bridge
description: Cross-gateway bot-to-bot communication between Cleber and Romário via HTTP API over Tailscale. Use when told to talk to the other bot, have a conversation with the other bot, ask the other bot something, or relay messages between bots. Also handles multi-round autonomous conversations.
---

# Bot Bridge 🌉

Talk to the other bot via HTTP API over Tailscale, with messages relayed to the Armada Lucas Telegram group so Lucas has full visibility.

## Async Mode (Default — Use This)

Fire-and-forget. Send the message, relay to Armada Lucas, return immediately. The other bot receives the message and is instructed to reply back using THEIR bridge script, creating an async conversation.

```bash
# Cleber asking Romário:
~/clawd/scripts/bot-bridge.sh romario "Hey, what are you working on?"

# Romário asking Cleber:
~/romario/scripts/bot-bridge.sh cleber "Hey, can you check something for me?"
```

**Why async?** The other bot may use tool calls (exec, browser, etc.) that take minutes. A synchronous call would time out waiting. Async lets each bot work at their own pace and reply when ready.

**Flow:**
1. Your message is relayed to Armada Lucas (via your Telegram bot)
2. Message is sent to the other bot's API (fire-and-forget)
3. The other bot processes it, then calls THEIR bridge script to reply
4. Their reply is relayed to Armada Lucas (via their Telegram bot)
5. You receive the reply in your session and can respond again

**When you receive a message via the bridge, ALWAYS reply using the bridge script** so the conversation stays visible in Armada Lucas.

## Sync Mode (Short Messages Only)

For quick exchanges where neither bot needs to run tools. Has a 120s timeout.

```bash
# Single sync exchange
~/scripts/bot-bridge.sh romario "Quick question: what port are you on?" --sync

# Multi-round sync (5 rounds)
~/scripts/bot-bridge.sh romario "Let's brainstorm" --sync 5
```

⚠️ Only use sync for simple text replies. If the other bot needs to run commands, use async.

## Network Details

| Bot | Tailscale IP | Port | Gateway Token |
|-----|-------------|------|---------------|
| Cleber 🤖 | 100.94.11.81 | 18789 | See TOOLS.md |
| Romário ⚽ | 100.127.240.60 | 18790 | See TOOLS.md |

Both gateways use `bind: tailnet` with token auth.

## When Lucas Says "Talk to Each Other"

1. Pick a topic from context or ask Lucas
2. Run async bridge: `~/scripts/bot-bridge.sh <target> "message"`
3. When the other bot replies via bridge, continue the conversation the same way
4. All messages appear in Armada Lucas for Lucas to follow

## Armada Lucas Group

- Group ID: `-1003768595045`
- Both bots relay via Telegram Bot API (`sendMessage`)
- `requireMention: false` — bots talk freely in this group
