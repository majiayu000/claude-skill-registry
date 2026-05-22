---
name: agentuity-cli-cloud-queue-dlq-list
description: List messages in the dead letter queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name>"
metadata:
  command: "agentuity cloud queue dlq list"
  tags: "read-only fast requires-auth"
---

# Cloud Queue Dlq List

List messages in the dead letter queue

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue dlq list <queue_name> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--limit` | number | Yes | - | Maximum number of messages to return |
| `--offset` | number | Yes | - | Offset for pagination |

## Examples

List DLQ messages:

```bash
bunx @agentuity/cli cloud queue dlq list my-queue
```

## Output

Returns JSON object:

```json
{
  "messages": "array",
  "total": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `messages` | array | - |
| `total` | number | - |
