---
name: agentuity-cli-cloud-secret-delete
description: Delete a secret. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<key>"
metadata:
  command: "agentuity cloud secret delete"
  tags: "destructive deletes-resource slow requires-auth requires-project"
---

# Cloud Secret Delete

Delete a secret

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud secret delete <key>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<key>` | string | Yes | - |

## Examples

Delete item:

```bash
bunx @agentuity/cli secret delete OLD_API_KEY
```

Delete item:

```bash
bunx @agentuity/cli secret rm DATABASE_URL
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
| `key` | string | Secret key name that was deleted |
| `path` | string | Local file path where secret was removed |
