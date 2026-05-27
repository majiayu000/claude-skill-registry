---
name: bot-developer
description: Expert bot developer specializing in Discord, Telegram, Slack automation with deep knowledge of rate limiting, state machines, event sourcing, moderation systems, and conversational AI integration. Activate on 'Discord bot', 'Telegram bot', 'Slack bot', 'chat automation', 'moderation system'. NOT for web APIs (use backend-architect), general automation scripts (use python-pro), or frontend chat widgets (use frontend-developer).
allowed-tools: Read,Write,Edit,Bash,WebSearch,WebFetch
category: AI & Machine Learning
tags:
  - discord
  - telegram
  - slack
  - bots
  - automation
pairs-with:
  - skill: api-architect
    reason: Design robust bot backend APIs
  - skill: devops-automator
    reason: Deploy and scale bot infrastructure
---

# Bot Developer

Expert in building production-grade bots with proper architecture, state management, and scalability.

## Quick Start

```
User: "Build a Discord moderation bot with auto-mod"

Bot Developer:
1. Set up event-driven architecture (message broker + service layer)
2. Implement state machine for multi-turn mod flows
3. Add distributed rate limiting (Redis)
4. Create point-based moderation with decay
5. Configure auto-mod rules (spam, caps, links, words)
6. Deploy with proper logging and error handling
```

**Key principle**: Production bots need rate limiting, state management, and graceful degradation—not just command handlers.

## Core Capabilities

### 1. Platform Expertise

| Platform | Connection | Best For |
|----------|------------|----------|
| Discord | Gateway (WebSocket) | Gaming communities, large servers |
| Telegram | Webhook (production) | International, groups/channels |
| Slack | Socket Mode/Webhook | Workplace, integrations |

### 2. Production Architecture
- Event-driven design with message broker (Redis Streams / RabbitMQ)
- Service layer separation (User, Moderation, Economy, Integration)
- PostgreSQL + Redis + S3 data layer
- Cog-based modular structure

### 3. State Management
- Finite state machines for multi-turn conversations
- Timeout handling (auto-reset after inactivity)
- Race condition prevention
- Context preservation across turns

### 4. Rate Limiting
- Distributed limiter with Redis backend
- Adaptive limiter responding to API headers
- Per-user, per-guild, and global buckets
- Graceful degradation with retry-after info

### 5. Moderation System
- Point-based escalation (configurable thresholds)
- Automatic decay over time
- Auto-mod rules (spam, caps, links, banned words)
- Fuzzy matching to catch bypass attempts (l33t speak)
- Audit logging for compliance

## Escalation Thresholds

| Points | Action |
|--------|--------|
| 0-2 | No action |
| 3-5 | Mute |
| 6-9 | Kick |
| 10-14 | Temp Ban |
| 15+ | Permanent Ban |

## Auto-Mod Rules

| Rule | Detection Method |
|------|-----------------|
| Spam | Message frequency per sliding window |
| Caps | Character ratio (&gt;70% uppercase) |
| Links | URL regex + domain whitelist |
| Words | Dictionary + Levenshtein (85% threshold) |
| Mentions | @mention counting with variants |
| Invites | Discord invite regex + URL expansion |

## When to Use

**Use for:**
- Discord/Telegram/Slack bot development
- Moderation and auto-mod systems
- Multi-turn conversational flows
- Economy/XP/leveling systems
- Integration with external APIs

**Do NOT use for:**
- Web APIs without chat interface (use backend-architect)
- General automation scripts (use python-pro)
- Frontend chat widgets (use frontend-developer)
- AI/ML model integration alone (use ai-engineer)

## Anti-Patterns

### Anti-Pattern: Polling in Production
**What it looks like**: Using `bot.polling()` or long-polling for Telegram
**Why wrong**: Wastes resources, slower response, can't scale
**Instead**: Use webhooks with proper verification

### Anti-Pattern: No Rate Limiting
**What it looks like**: Sending API requests without throttling
**Why wrong**: Gets bot banned, triggers 429s, poor UX
**Instead**: Implement adaptive rate limiter respecting API headers

### Anti-Pattern: In-Memory State Only
**What it looks like**: Storing conversation state in Python dict
**Why wrong**: Lost on restart, can't scale to multiple instances
**Instead**: Redis for state, PostgreSQL for persistence

### Anti-Pattern: Blocking Event Handlers
**What it looks like**: Long-running operations in `on_message`
**Why wrong**: Blocks all other events, causes timeouts
**Instead**: Async tasks, message queue for heavy work

## Security Checklist

```
TOKEN SECURITY
├── Never commit tokens to git
├── Use environment variables or secret manager
├── Rotate tokens if exposed
└── Separate tokens for dev/staging/prod

PERMISSION CHECKS
├── Verify user permissions before action
├── Use platform's permission system
├── Check bot's permissions before attempting
└── Fail safely if permissions missing

INPUT VALIDATION
├── Sanitize all user input
├── Validate command arguments
├── Parameterized queries (no SQL injection)
└── Rate limit user-triggered actions
```

## Reference Files

- `references/architecture-patterns.md` - Event-driven architecture, state machines
- `references/rate-limiting.md` - Distributed and adaptive rate limiting
- `references/moderation-system.md` - Point-based moderation, auto-mod
- `references/platform-templates.md` - Discord.py, Telegram webhook templates, security

---

**Core insight**: Production bots fail from rate limiting and state bugs, not from bad command logic. Build infrastructure first.

**Use with**: ai-engineer (LLM integration) | backend-architect (API design) | deployment-engineer (hosting)
