---
name: agentuity-cli-cloud-queue-nack
description: Negative acknowledge a message (return to queue for retry). Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name> <message_id>"
metadata:
  command: "agentuity cloud queue nack"
  tags: "mutating updates-resource requires-auth"
---

# Cloud Queue Nack

Negative acknowledge a message (return to queue for retry)

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue nack <queue_name> <message_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |
| `<message_id>` | string | Yes | - |

## Examples

Return message to queue for retry:

```bash
bunx @agentuity/cli cloud queue nack my-queue msg-123
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "queue_name": "string",
  "message_id": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | - |
| `queue_name` | string | - |
| `message_id` | string | - |
