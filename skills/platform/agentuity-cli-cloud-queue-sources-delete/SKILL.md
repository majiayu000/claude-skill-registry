---
name: agentuity-cli-cloud-queue-sources-delete
description: Delete a source from a queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name> <source_id>"
metadata:
  command: "agentuity cloud queue sources delete"
  tags: "mutating deletes-resource requires-auth"
---

# Cloud Queue Sources Delete

Delete a source from a queue

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue sources delete <queue_name> <source_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |
| `<source_id>` | string | Yes | - |

## Examples

Delete a source:

```bash
bunx @agentuity/cli cloud queue sources delete my-queue qsrc_abc123
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "queue_name": "string",
  "source_id": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | - |
| `queue_name` | string | - |
| `source_id` | string | - |
