---
name: agentuity-cli-cloud-secret-set
description: Set a secret. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<key> <value>"
metadata:
  command: "agentuity cloud secret set"
  tags: "mutating updates-resource slow requires-auth requires-project"
---

# Cloud Secret Set

Set a secret

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud secret set <key> <value>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<key>` | string | Yes | - |
| `<value>` | string | Yes | - |

## Examples

Set the DATABASE_URL environment secret:

```bash
bunx @agentuity/cli secret set DATABASE_URL "postgres://user:pass@host:5432/db"
```

Set the STRIPE_SECRET_KEY environment secret:

```bash
bunx @agentuity/cli secret set STRIPE_SECRET_KEY "sk_live_..."
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "key": "string",
  "path": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `key` | string | Secret key name |
| `path` | string | Local file path where secret was saved |
