---
name: agentuity-cli-cloud-db-delete
description: Delete a database resource. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name]"
metadata:
  command: "agentuity cloud db delete"
  tags: "destructive deletes-resource slow requires-auth requires-deployment"
---

# Cloud Db Delete

Delete a database resource

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud db delete [name] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | Yes | - | Skip confirmation prompts |

## Examples

Delete item:

```bash
bunx @agentuity/cli cloud db delete my-database
```

Delete item:

```bash
bunx @agentuity/cli cloud db rm my-database
```

Delete item:

```bash
bunx @agentuity/cli cloud db delete
```

Delete item:

```bash
bunx @agentuity/cli --dry-run cloud db delete my-database
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "name": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether deletion succeeded |
| `name` | string | Deleted database name |
