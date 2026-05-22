---
name: agentuity-cli-cloud-queue-sources-create
description: Create a source for a queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name>"
metadata:
  command: "agentuity cloud queue sources create"
  tags: "mutating creates-resource requires-auth"
---

# Cloud Queue Sources Create

Create a source for a queue

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue sources create <queue_name> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--name` | string | Yes | - | Source name |
| `--description` | string | Yes | - | Source description |
| `--auth-type` | string | No | `"none"` | Authentication type |
| `--auth-value` | string | Yes | - | Authentication value |

## Examples

Create a source with header authentication:

```bash
bunx @agentuity/cli cloud queue sources create my-queue --name webhook-1 --auth-type header --auth-value "X-API-Key:secret123"
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "queue_id": "string",
  "name": "string",
  "description": "unknown",
  "auth_type": "string",
  "enabled": "boolean",
  "url": "string",
  "request_count": "number",
  "success_count": "number",
  "failure_count": "number",
  "last_request_at": "unknown",
  "last_success_at": "unknown",
  "last_failure_at": "unknown",
  "last_failure_error": "unknown",
  "created_at": "string",
  "updated_at": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | - |
| `queue_id` | string | - |
| `name` | string | - |
| `description` | unknown | - |
| `auth_type` | string | - |
| `enabled` | boolean | - |
| `url` | string | - |
| `request_count` | number | - |
| `success_count` | number | - |
| `failure_count` | number | - |
| `last_request_at` | unknown | - |
| `last_success_at` | unknown | - |
| `last_failure_at` | unknown | - |
| `last_failure_error` | unknown | - |
| `created_at` | string | - |
| `updated_at` | string | - |
