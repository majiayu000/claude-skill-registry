---
name: agentuity-cli-cloud-queue-create
description: Create a new queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_type>"
metadata:
  command: "agentuity cloud queue create"
  tags: "mutating creates-resource requires-auth"
---

# Cloud Queue Create

Create a new queue

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud queue create <queue_type> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_type>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--name` | string | Yes | - | Queue name (auto-generated if not provided) |
| `--description` | string | Yes | - | Queue description |
| `--ttl` | number | Yes | - | Default message TTL in seconds |
| `--visibilityTimeout` | number | Yes | - | Default visibility timeout in seconds (worker queues) |
| `--maxRetries` | number | Yes | - | Maximum retry attempts for failed messages |

## Examples

Create a worker queue named my-tasks:

```bash
bunx @agentuity/cli cloud queue create worker --name my-tasks
```

Create a pubsub queue with 24h TTL:

```bash
bunx @agentuity/cli cloud queue create pubsub --name events --ttl 86400
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "name": "string",
  "queue_type": "string",
  "created_at": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | - |
| `name` | string | - |
| `queue_type` | string | - |
| `created_at` | string | - |
