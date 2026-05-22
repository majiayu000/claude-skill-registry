---
name: agentuity-cli-cloud-queue-ack
description: Acknowledge a message (mark as processed). Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name> <message_id>"
metadata:
  command: "agentuity cloud queue ack"
  tags: "mutating updates-resource requires-auth"
---

# Cloud Queue Ack

Acknowledge a message (mark as processed)

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue ack <queue_name> <message_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |
| `<message_id>` | string | Yes | - |

## Examples

Acknowledge a message:

```bash
bunx @agentuity/cli cloud queue ack my-queue msg-123
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
