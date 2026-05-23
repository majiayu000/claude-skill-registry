---
name: request-discord-approval
version: "2.0.0"
description: >
  Request human approval for a critical operation via Discord MCP server. Posts
  a message with reaction buttons and uses await_reaction to wait for response.
  Use for destructive or irreversible operations. Keywords: approval, Discord,
  human-in-the-loop, confirmation, dangerous operation, reactions.
metadata:
  domain: general
  category: notifications
  requires-approval: false
  confidence: 0.9
dependencies:
  mcp-servers:
    - discord-mcp-server
  skills: []
  tools: []
execution:
  timeout: 300s  # 5 minutes default
  retries: 1
  backoff: none
---

# Request Discord Approval

Request human approval via Discord using the MCP server's reaction capabilities.

## When to Use

- Operation requires human review before execution
- Destructive or irreversible operations
- High-impact changes in production
- Keywords: approve, confirm, human, review, dangerous

## Prerequisites

Before applying this skill, verify:

- [ ] Operation genuinely requires human review
- [ ] DISCORD_MCP_URL is configured
- [ ] Approval channel exists
- [ ] Timeout duration is acceptable (default: 5 minutes)

## Input Schema

```json
{
  "action": "string - Description of the proposed action",
  "resource": "string - Target resource identifier",
  "namespace": "string - Optional Kubernetes namespace",
  "agent": "string - Name of the requesting agent",
  "reason": "string - Justification for the action",
  "channel_name": "string - Approval channel (default: kubani-alerts)",
  "timeout_seconds": "number - How long to wait (default: 300)"
}
```

## Actions

### 1. Format Approval Request

Build the approval embed with context:

```yaml
embed:
  color: 16753920  # Orange - attention required
  title: "🔐 Approval Required"
  description: $operation_description
  fields:
    - name: "Action"
      value: $proposed_action
      inline: false
    - name: "Resource"
      value: $target_resource
      inline: true
    - name: "Namespace"
      value: $namespace
      inline: true
    - name: "Requesting Agent"
      value: $agent_name
      inline: false
    - name: "Reason"
      value: $justification
      inline: false
  footer:
    text: "React with ✅ to approve or ❌ to reject"
  timestamp: $current_timestamp
```

### 2. Post Approval Request

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  embed: $approval_embed
timeout: 30s
store_result: message_result
```

### 3. Add Reaction Options

Add reaction buttons to the message:

```yaml
mcp_tool: discord-mcp-server/add_reaction
params:
  channel_id: $message_result.channel_id
  message_id: $message_result.message_id
  emoji: "✅"
---
mcp_tool: discord-mcp-server/add_reaction
params:
  channel_id: $message_result.channel_id
  message_id: $message_result.message_id
  emoji: "❌"
```

### 4. Wait for Reaction

Use the MCP server's await_reaction to wait for human response:

```yaml
mcp_tool: discord-mcp-server/await_reaction
params:
  channel_id: $message_result.channel_id
  message_id: $message_result.message_id
  valid_emojis: ["✅", "❌"]
  timeout_seconds: $timeout_seconds
timeout: $timeout_seconds + 10  # Buffer for network
on_timeout: return_timeout
```

### 5. Process Response

- If ✅ reaction received: return approved=true
- If ❌ reaction received: return approved=false
- If timeout: return approved=false with timeout reason

### 6. Post Result Notification

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  content: "$result_emoji **$result_status**: `$action` on `$resource`\n_Responded by: $responder_"
```

## Output Schema

```json
{
  "approved": "boolean - Whether the action was approved",
  "responder": "string - Username who responded (null if timeout)",
  "response_time_seconds": "number - Time to response",
  "emoji": "string - The emoji that was selected",
  "reason": "string - Human-readable result reason"
}
```

## Success Criteria

The skill succeeds when:

- [ ] Approval request posted successfully
- [ ] Human response received within timeout
- [ ] Response recorded with audit trail

## Failure Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Post failed | Return error, do not proceed |
| Timeout | Return approved=false, safe default |
| MCP server error | Return error, do not proceed |

**Important:** On ANY failure or timeout, default to NOT APPROVED for safety.

## Examples

### Example 1: Pod Deletion Approval

**Input:**
```json
{
  "action": "Delete Pod",
  "resource": "api-server-abc123",
  "namespace": "production",
  "agent": "remediator",
  "reason": "Pod stuck in CrashLoopBackOff for 30 minutes, restart required",
  "timeout_seconds": 300
}
```

**MCP Tool Calls:**
```yaml
# Step 1: Post message
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: kubani-alerts
  embed:
    title: "🔐 Approval Required"
    description: "The remediator agent is requesting approval for a critical action."
    color: 16753920
    fields:
      - name: "Action"
        value: "Delete Pod"
      - name: "Resource"
        value: "api-server-abc123"
        inline: true
      - name: "Namespace"
        value: "production"
        inline: true
      - name: "Requesting Agent"
        value: "remediator"
      - name: "Reason"
        value: "Pod stuck in CrashLoopBackOff for 30 minutes, restart required"
    footer:
      text: "React with ✅ to approve or ❌ to reject"

# Step 2: Add reactions
mcp_tool: discord-mcp-server/add_reaction
params:
  channel_id: "123456789"
  message_id: "987654321"
  emoji: "✅"

mcp_tool: discord-mcp-server/add_reaction
params:
  channel_id: "123456789"
  message_id: "987654321"
  emoji: "❌"

# Step 3: Wait for response
mcp_tool: discord-mcp-server/await_reaction
params:
  channel_id: "123456789"
  message_id: "987654321"
  valid_emojis: ["✅", "❌"]
  timeout_seconds: 300
```

**Output (Approved):**
```json
{
  "approved": true,
  "responder": "admin_user",
  "response_time_seconds": 45,
  "emoji": "✅",
  "reason": "Approved via Discord reaction"
}
```

**Output (Timeout):**
```json
{
  "approved": false,
  "responder": null,
  "response_time_seconds": 300,
  "emoji": null,
  "reason": "Approval request timed out after 300 seconds"
}
```

## Related Skills

- [send-discord-notification](../send-discord-notification/SKILL.md) - For non-blocking notifications

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-11 | Migrated to Discord MCP server with await_reaction |
| 1.0.0 | 2025-01-09 | Initial version with webhook + polling |
