---
name: agentuity-cli-cloud-apikey-delete
description: Delete an API key (soft delete). Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<id>"
metadata:
  command: "agentuity cloud apikey delete"
  tags: "destructive deletes-resource slow requires-auth"
---

# Cloud Apikey Delete

Delete an API key (soft delete)

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud apikey delete <id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<id>` | string | Yes | - |

## Examples

Delete item:

```bash
bunx @agentuity/cli cloud apikey delete <id>
```

Run <id> command:

```bash
bunx @agentuity/cli cloud apikey del <id>
```

Delete item:

```bash
bunx @agentuity/cli cloud apikey rm <id>
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "id": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `id` | string | API key id that was deleted |
