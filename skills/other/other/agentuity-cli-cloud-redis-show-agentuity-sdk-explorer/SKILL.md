---
name: agentuity-cli-cloud-redis-show
description: Show Redis connection URL. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud redis show"
  tags: "read-only fast requires-auth"
---

# Cloud Redis Show

Show Redis connection URL

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud redis show [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--showCredentials` | boolean | Yes | - | Show credentials in plain text (default: masked in terminal, unmasked in JSON) |

## Examples

Show Redis connection URL:

```bash
bunx @agentuity/cli cloud redis show
```

Show Redis URL with credentials visible:

```bash
bunx @agentuity/cli cloud redis show --show-credentials
```

Show Redis URL as JSON:

```bash
bunx @agentuity/cli --json cloud redis show
```

## Output

Returns JSON object:

```json
{
  "url": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Redis connection URL |
