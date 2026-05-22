---
name: agentuity-cli-cloud-queue-destinations-create
description: Create a webhook destination for a queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name>"
metadata:
  command: "agentuity cloud queue destinations create"
  tags: "mutating creates-resource requires-auth"
---

# Cloud Queue Destinations Create

Create a webhook destination for a queue

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue destinations create <queue_name> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--url` | string | Yes | - | Webhook URL |
| `--method` | string | No | `"POST"` | HTTP method (default: POST) |
| `--timeout` | number | Yes | - | Request timeout in milliseconds |

## Examples

Create a webhook destination:

```bash
bunx @agentuity/cli cloud queue destinations create my-queue --url https://example.com/webhook
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "queue_id": "string",
  "destination_type": "string",
  "config": "object",
  "enabled": "boolean",
  "stats": "object",
  "created_at": "string",
  "updated_at": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | - |
| `queue_id` | string | - |
| `destination_type` | string | - |
| `config` | object | - |
| `enabled` | boolean | - |
| `stats` | object | - |
| `created_at` | string | - |
| `updated_at` | string | - |
