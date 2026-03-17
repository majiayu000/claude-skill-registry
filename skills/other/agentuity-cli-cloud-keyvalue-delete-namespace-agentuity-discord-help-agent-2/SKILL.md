---
name: agentuity-cli-cloud-keyvalue-delete-namespace
description: Delete a keyvalue namespace and all its keys. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.110"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name> <confirm>"
metadata:
  command: "agentuity cloud keyvalue delete-namespace"
  tags: "destructive deletes-resource slow requires-auth requires-project"
---

# Cloud Keyvalue Delete-namespace

Delete a keyvalue namespace and all its keys

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue delete-namespace <name> <confirm>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |
| `<confirm>` | string | Yes | - |

## Examples

Delete staging namespace (interactive):

```bash
bunx @agentuity/cli kv delete-namespace staging
```

Delete cache without confirmation:

```bash
bunx @agentuity/cli kv rm-namespace cache --confirm
```

Force delete production:

```bash
bunx @agentuity/cli kv delete-namespace production --confirm
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "namespace": "string",
  "message": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the deletion succeeded |
| `namespace` | string | Deleted namespace name |
| `message` | string | Confirmation message |
