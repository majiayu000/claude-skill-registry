---
name: partiful
description: Access Partiful events, invites, and RSVPs via reverse-engineered API. Use when user asks about party invites, event RSVPs, or social event data.
---

# Partiful

Programmatic access to Partiful event data via Babashka.

## Quick Start

```bash
# List all RSVPs/invites
bb scripts/partiful.clj invites

# Get event details
bb scripts/partiful.clj event <event-id>

# Authenticate (opens browser)
bb scripts/partiful.clj auth
```

## Commands

| Command | Description |
|---------|-------------|
| `invites` | List events you're invited to with RSVP status |
| `events` | List events you're hosting |
| `mutuals` | List mutual connections |
| `event <id>` | Get full details for an event |
| `auth` | Authenticate via Playwright browser |

## Configuration

Set environment variables or store in `~/.partiful-config.edn`:

```bash
export PARTIFUL_AUTH_TOKEN="..."
export PARTIFUL_USER_ID="..."
export PARTIFUL_REFRESH_TOKEN="..."
export PARTIFUL_FIREBASE_API_KEY="..."  # Get from Partiful web app
```

## ACSet Schema

Category-theoretic event modeling with morphisms:

```
  Event <──host──── User
    ^                 ^
    │                 │
 event_of          invitee
    │                 │
    └─── Invite ─────┘
           ↓
         RSVP
```

See `scripts/partiful-acset.clj` for queries:
- `my-invited-events` - Events user is invited to
- `event-guests` - All guests for an event
- `event-rsvps` - RSVP statuses for event

## Cat# Integration

```
Trit: +1 (PLUS)
Color: #FF6B35 (warm/executor)
Triads: partiful(+1) + acsets(0) + calendar-acset(-1) = 0
```
