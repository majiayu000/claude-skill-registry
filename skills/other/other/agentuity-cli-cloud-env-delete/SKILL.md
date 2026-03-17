---
name: agentuity-cli-cloud-env-delete
description: Delete an environment variable. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<key>"
metadata:
  command: "agentuity cloud env delete"
  tags: "destructive deletes-resource slow requires-auth requires-project"
---

# Cloud Env Delete

Delete an environment variable

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud env delete <key>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<key>` | string | Yes | - |

## Examples

Delete item:

```bash
bunx @agentuity/cli env delete OLD_FEATURE_FLAG
```

Delete item:

```bash
bunx @agentuity/cli env rm PORT
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
| `key` | string | Environment variable key that was deleted |
| `path` | string | Local file path where env var was removed |
