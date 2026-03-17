---
name: agentuity-cli-cloud-secret-get
description: Get a secret value. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<key>"
metadata:
  command: "agentuity cloud secret get"
  tags: "read-only fast requires-auth requires-project"
---

# Cloud Secret Get

Get a secret value

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud secret get <key> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<key>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--mask` | boolean | No | `true` | mask the value in output (default: true in TTY, false otherwise) |

## Examples

Get item details:

```bash
bunx @agentuity/cli secret get DATABASE_URL
```

Use no mask option:

```bash
bunx @agentuity/cli secret get STRIPE_SECRET_KEY --no-mask
```

## Output

Returns JSON object:

```json
{
  "key": "string",
  "value": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `key` | string | Secret key name |
| `value` | string | Secret value |
