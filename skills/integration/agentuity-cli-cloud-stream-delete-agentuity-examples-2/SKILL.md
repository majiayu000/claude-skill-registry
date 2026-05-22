---
name: agentuity-cli-cloud-stream-delete
description: Delete a stream by ID (soft delete). Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<id>"
metadata:
  command: "agentuity cloud stream delete"
  tags: "destructive deletes-resource slow requires-auth"
---

# Cloud Stream Delete

Delete a stream by ID (soft delete)

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud stream delete <id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<id>` | string | Yes | - |

## Examples

Delete a stream:

```bash
bunx @agentuity/cli stream delete stream-id-123
```

Delete stream (using alias):

```bash
bunx @agentuity/cli stream rm stream-id-456
```

Delete stream (using alias):

```bash
bunx @agentuity/cli stream del stream-id-789
```

## Output

Returns JSON object:

```json
{
  "id": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stream ID |
