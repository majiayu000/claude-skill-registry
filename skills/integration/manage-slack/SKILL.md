---
name: manage-slack
description: Slack integration via CLI. Triggers on "send to slack", "post message", "slack notification", "dm user".
---

# Slack Integration

Use the `slack-cc` CLI tool for all Slack operations. All commands return JSON.

**Shared reference:** See [_shared/slack-integration/](../_shared/slack-integration/README.md) for:
- [CLI reference](../_shared/slack-integration/cli-reference.md) - Canonical commands
- [Error handling](../_shared/slack-integration/error-handling.md) - Warn and continue pattern

## Commands

### Sync (Required First)
```bash
npx tsx .claude/tools/slack-cc/src/index.ts sync
```
Fetches channels and members, caches locally. **Run once before other commands.**

### Send Message to Channel
```bash
npx tsx .claude/tools/slack-cc/src/index.ts send-message <channel> <message>

# Examples
npx tsx .claude/tools/slack-cc/src/index.ts send-message design-studio "Deployment complete!"
npx tsx .claude/tools/slack-cc/src/index.ts send-message "#prototype-v2-updates" "New feature shipped"

# Thread reply
npx tsx .claude/tools/slack-cc/src/index.ts send-message design-studio "Follow-up" --thread 1234567890.123456
```
**Options:** `--thread <ts>` - Reply in thread

### Send Direct Message
```bash
npx tsx .claude/tools/slack-cc/src/index.ts send-dm <user> <message>

# Examples
npx tsx .claude/tools/slack-cc/src/index.ts send-dm zeeshan "Design polish is complete!"
npx tsx .claude/tools/slack-cc/src/index.ts send-dm "Andy Rong" "Check out the new feature"
```

### List Channels
```bash
npx tsx .claude/tools/slack-cc/src/index.ts list-channels
npx tsx .claude/tools/slack-cc/src/index.ts list-channels --filter design
npx tsx .claude/tools/slack-cc/src/index.ts list-channels --limit 10
```

### List Members
```bash
npx tsx .claude/tools/slack-cc/src/index.ts list-members
npx tsx .claude/tools/slack-cc/src/index.ts list-members --filter zeeshan
npx tsx .claude/tools/slack-cc/src/index.ts list-members --limit 20
```

---

## Response Format

**Success:**
```json
{"success": true, "channel": "design-studio", "messageTs": "...", "permalink": "..."}
```

**Error:**
```json
{"success": false, "error": "Channel not found. Available: design-studio, ..."}
```

---

## Primary Channels

- `design-studio` - Design updates and reviews
- `prototype-v2-updates` - Feature and deployment notifications

---

## Usage Pattern

```bash
# 1. Check if a user exists
RESULT=$(npx tsx .claude/tools/slack-cc/src/index.ts list-members --filter zeeshan)

# 2. Send notification
npx tsx .claude/tools/slack-cc/src/index.ts send-dm zeeshan "DIS-307 design polish is complete!"

# 3. Or post to channel
npx tsx .claude/tools/slack-cc/src/index.ts send-message prototype-v2-updates "New feature deployed! See DIS-308"
```

---

## Error Handling

Slack updates are informational, not blocking. If sending fails:
1. Warn and continue
2. Log error for debugging
3. Don't block the primary workflow

```bash
RESULT=$(npx tsx .claude/tools/slack-cc/src/index.ts send-message design-studio "Update" 2>&1)

if echo "$RESULT" | grep -q '"success":true'; then
  echo "Message sent"
else
  echo "Warning: Slack notification failed. Continuing..."
fi
```
