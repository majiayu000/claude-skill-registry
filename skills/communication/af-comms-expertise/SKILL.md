---
name: af-comms-expertise
description: Use when sending notifications for project events like setup completion, deployments, or status updates. Covers Zulip (primary) and Slack (legacy) integration, channel/stream selection, message formatting, and notification triggers.

# AgentFlow documentation fields
title: Communications Expertise
created: 2025-12-10
updated: 2026-02-25
last_checked: 2026-02-25
tags: [skill, expertise, communications, zulip, slack, notifications]
parent: ../README.md
---

# Communications Expertise

## When to Use This Skill

Load this skill when you need to:
- Send notifications for project milestones
- Announce setup completion to project streams/channels
- Post deployment or release notices
- Share status updates with teams

## Quick Reference

AgentFlow uses **Zulip as the primary communication platform**. Slack is legacy (gated behind `SLACK_ENABLED=false` by default).

### Zulip (Primary)

Zulip notifications are sent via the Zulip API using bot credentials from Doppler:

| Parameter | Source |
|-----------|--------|
| `ZULIP_BOT_EMAIL` | Doppler (`agentview/prd`) |
| `ZULIP_API_KEY` | Doppler (`agentview/prd`) |
| `ZULIP_REALM` | Doppler (`agentview/prd`) |

**Sending a Zulip message:**
```bash
curl -s -X POST "$ZULIP_REALM/api/v1/messages" \
  -u "$ZULIP_BOT_EMAIL:$ZULIP_API_KEY" \
  -d "type=stream" \
  -d "to=engineering-team" \
  -d "topic=AgentFlow Updates" \
  --data-urlencode "content=Your message here"
```

### Slack (Legacy)

Slack MCP tools are available but gated behind `SLACK_ENABLED=true`. By default Slack is disabled.

**Available Slack MCP tools (legacy):**
- `mcp__slack__slack_list_channels` - List available channels
- `mcp__slack__slack_post_message` - Post to a channel
- `mcp__slack__slack_reply_to_thread` - Reply in a thread
- `mcp__slack__slack_get_channel_history` - Read recent messages

**Note:** Only use Slack MCP tools when `SLACK_ENABLED=true` is set and the agent is running in Slack-enabled mode.

## Message Templates

### Greenfield Setup Complete

```
Project setup complete!

**{Project Name}**
GitHub: https://github.com/{owner}/{repo}
Linear: https://linear.app/gaininsight/team/{KEY}
Worktree: /srv/worktrees/{repo}/develop

Ready for development. Use `start-work {repo} {ISSUE-ID}` to begin.
```

### Deployment Notice

```
Deployed to {environment}

**{Project Name}** v{version}
URL: {deployment-url}
Issues: {comma-separated issue IDs}

Changes:
- {Change 1}
- {Change 2}
```

### Status Update

```
Status Update: **{Project Name}**

Completed: {list}
In Progress: {list}
Blocked: {list if any}
```

## Workflow

### Sending a Zulip Notification (Primary)

1. **Determine the stream and topic:**
   - Use the project's configured Zulip stream (from project registry)
   - Use a descriptive topic (e.g., "Deployments", "Setup", "AgentFlow Updates")

2. **Post message:**
   ```bash
   curl -s -X POST "$ZULIP_REALM/api/v1/messages" \
     -u "$ZULIP_BOT_EMAIL:$ZULIP_API_KEY" \
     -d "type=stream" \
     -d "to={stream-name}" \
     -d "topic={topic}" \
     --data-urlencode "content={formatted message}"
   ```

3. **Handle errors:**
   - HTTP 401 -> Invalid bot credentials
   - HTTP 400 -> Invalid stream or missing parameters
   - Check `ZULIP_REALM`, `ZULIP_BOT_EMAIL`, `ZULIP_API_KEY` are set

### Sending a Slack Notification (Legacy)

Only when `SLACK_ENABLED=true`:

1. **Check channel access:**
   ```
   mcp__slack__slack_list_channels
   ```
   Look for `is_member: true`

2. **Post message:**
   ```
   mcp__slack__slack_post_message
   - channel_id: [from list]
   - text: [formatted message]
   ```

3. **Handle errors:**
   - `not_in_channel` -> Bot needs to be invited to channel
   - `channel_not_found` -> Invalid channel ID
   - `not_authed` -> Token issue

### Bot Invitation (Slack Legacy)

If bot isn't in a channel, instruct user:
> "Please invite the bot to #{channel} by typing `/invite @AgentFlow` in the channel"

## Integration Points

**Greenfield setup** (af-setup-process):
- After setup completion, optionally notify the project's Zulip stream
- Only if user provided a Zulip stream (or Slack channel for legacy) during setup

**Delivery phase** (af-delivery-process):
- Post deployment notices after successful releases
- Update on PR merges if configured

## Common Pitfalls

1. **Missing Zulip credentials** - Ensure `ZULIP_BOT_EMAIL`, `ZULIP_API_KEY`, `ZULIP_REALM` are available via Doppler
2. **Wrong stream name** - Verify the stream exists in Zulip before posting
3. **Slack not enabled** - Don't attempt Slack MCP tools unless `SLACK_ENABLED=true`
4. **Bot not in Slack channel** (legacy) - Must be invited before posting

## Key Principles

1. **Zulip is primary** - Use Zulip for all new notifications
2. **Slack is legacy** - Only use when explicitly enabled via `SLACK_ENABLED=true`
3. **Notifications are optional** - Don't block workflows on notification failures
4. **Keep messages concise** - Use templates, avoid walls of text
5. **Include links** - GitHub, Linear, deployment URLs
6. **Fail gracefully** - Log error, continue workflow
