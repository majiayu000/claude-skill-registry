---
name: agentuity-cli-cloud-apikey-create
description: Create a new API key. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud apikey create"
  tags: "destructive creates-resource slow requires-auth"
---

# Cloud Apikey Create

Create a new API key

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud apikey create [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--name` | string | Yes | - | the name for the API key |
| `--expires-at` | string | Yes | - | expiration date as ISO 8601 (2025-12-31T23:59:59Z) or duration (1h, 2d, 30d, 1y) |
| `--confirm` | boolean | Yes | - | Skip confirmation prompts (required for non-TTY) |

## Examples

Create API key with 1 year expiration:

```bash
bunx @agentuity/cli cloud apikey create --name "My API Key" --expires-at 1y
```

Create API key with 30 day expiration:

```bash
bunx @agentuity/cli cloud apikey create --name "Short-lived Key" --expires-at 30d
```

Create API key with specific date and skip confirmation:

```bash
bunx @agentuity/cli cloud apikey create --name "Production Key" --expires-at 2026-01-01T00:00:00Z --confirm
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "value": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | the API key id |
| `value` | string | the API key value |
