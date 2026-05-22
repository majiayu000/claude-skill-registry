---
name: agentuity-cli-cloud-thread-get
description: Get details about a specific thread. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<thread_id>"
metadata:
  command: "agentuity cloud thread get"
  tags: "read-only fast requires-auth"
---

# Cloud Thread Get

Get details about a specific thread

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud thread get <thread_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<thread_id>` | string | Yes | - |

## Examples

Get a thread by ID:

```bash
bunx @agentuity/cli cloud thread get thrd_abc123xyz
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "created_at": "string",
  "updated_at": "string",
  "deleted": "boolean",
  "deleted_at": "unknown",
  "deleted_by": "unknown",
  "org_id": "string",
  "project_id": "string",
  "user_data": "unknown"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Thread ID |
| `created_at` | string | Creation timestamp |
| `updated_at` | string | Update timestamp |
| `deleted` | boolean | Deleted status |
| `deleted_at` | unknown | Deletion timestamp |
| `deleted_by` | unknown | Deleted by |
| `org_id` | string | Organization ID |
| `project_id` | string | Project ID |
| `user_data` | unknown | User data as JSON |
