---
name: agentuity-cli-cloud-queue-resume
description: Resume message delivery for a paused queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name>"
metadata:
  command: "agentuity cloud queue resume"
  tags: "mutating updates-resource requires-auth"
---

# Cloud Queue Resume

Resume message delivery for a paused queue

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue resume <name>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |

## Examples

Resume a paused queue:

```bash
bunx @agentuity/cli cloud queue resume my-queue
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "name": "string",
  "description": "unknown",
  "queue_type": "string",
  "default_ttl_seconds": "unknown",
  "default_visibility_timeout_seconds": "number",
  "default_max_retries": "number",
  "default_retry_backoff_ms": "number",
  "default_retry_max_backoff_ms": "number",
  "default_retry_multiplier": "number",
  "max_in_flight_per_client": "number",
  "next_offset": "number",
  "message_count": "number",
  "dlq_count": "number",
  "created_at": "string",
  "updated_at": "string",
  "paused_at": "unknown",
  "retention_seconds": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | - |
| `name` | string | - |
| `description` | unknown | - |
| `queue_type` | string | - |
| `default_ttl_seconds` | unknown | - |
| `default_visibility_timeout_seconds` | number | - |
| `default_max_retries` | number | - |
| `default_retry_backoff_ms` | number | - |
| `default_retry_max_backoff_ms` | number | - |
| `default_retry_multiplier` | number | - |
| `max_in_flight_per_client` | number | - |
| `next_offset` | number | - |
| `message_count` | number | - |
| `dlq_count` | number | - |
| `created_at` | string | - |
| `updated_at` | string | - |
| `paused_at` | unknown | - |
| `retention_seconds` | number | - |
