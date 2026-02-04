---
name: telegram
description: Process Telegram messages via GramJS MTProto client. Read messages, generate AI drafts, save drafts, and create intro groups. Use when handling Telegram conversations or facilitating introductions.
---

# Telegram Skill

Process Telegram messages via GramJS MTProto client. Supports unread messages, specific users, message requests, and group creation for introductions.

**CRITICAL: NEVER SEND MESSAGES. Only save drafts.**

## Capabilities

| Capability | Description |
|------------|-------------|
| **Unread Mode** | Process N unread conversations |
| **User Mode** | Find specific person by username/name (any read state) |
| **Requests Mode** | Process message requests folder (non-contacts) |
| **Entity Context** | Load context from database for known contacts |
| **Draft Replies** | AI generates contextual reply drafts |
| **Save Drafts** | Save drafts to Telegram (no sending) |
| **Create Groups** | Create new groups and add members for introductions |
| **Dialog Cache** | Fast lookups via cached dialog IDs (~1s vs ~90s) |
| **Mark Unread** | Re-mark conversations as unread after processing |
| **History** | Save per-person history to vault `context/telegram/` |

## Workflows

- **`workflows/process-messages.md`** - Full workflow for reading/replying
- **`workflows/create-intro-group.md`** - Workflow for facilitating introductions

## Tools

| Script | Purpose |
|--------|---------|
| `scripts/telegram-gramjs.ts` | GramJS MTProto client - fetch messages, populate cache |
| `scripts/telegram-save-drafts.ts` | Save AI drafts to Telegram from work file |
| `scripts/save-telegram-draft.ts` | Quick helper to save one draft by username |
| `scripts/telegram-create-group.ts` | Create groups and add members for intros |

## Quick Reference

```bash
# Unread mode (default)
/cyber-telegram                    # 1 unread dialog
/cyber-telegram --count 3          # 3 unread dialogs

# User mode
/cyber-telegram --user "@username" # By username
/cyber-telegram --user "Name"      # By name

# Requests mode
/cyber-telegram --requests         # Message requests folder

# Modifiers
/cyber-telegram --dry-run          # Read only
/cyber-telegram --no-mark-unread   # Don't preserve unread state

# Create intro group
bun scripts/telegram-create-group.ts --dry-run --title "A <> B" --users "@user1,@user2"
bun scripts/telegram-create-group.ts --title "A <> B" --users "@user1,@user2" --draft "Intro message"
```

See workflow files for full documentation.

## Dialog Cache

Dialog cache (`~/.cybos/telegram/dialog-cache.json`) stores all dialog IDs with access hashes for fast lookups:
- Populated automatically during searches
- Used by `telegram-save-drafts.ts` to avoid fetching all dialogs
- ~1 second draft save vs ~90 seconds without cache

## Safety

Drafts only - never sends messages automatically. User reviews and sends manually in Telegram.
