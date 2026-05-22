---
name: agentuity-cli-cloud-vector-delete-namespace
description: Delete a vector namespace and all its vectors. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name>"
metadata:
  command: "agentuity cloud vector delete-namespace"
  tags: "destructive deletes-resource slow requires-auth"
---

# Cloud Vector Delete-namespace

Delete a vector namespace and all its vectors

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud vector delete-namespace <name> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | No | `false` | if true will not prompt for confirmation |

## Examples

Delete staging namespace (interactive):

```bash
bunx @agentuity/cli vector delete-namespace staging
```

Delete cache without confirmation:

```bash
bunx @agentuity/cli vector rm-namespace cache --confirm
```

Force delete old-data namespace:

```bash
bunx @agentuity/cli vector delete-namespace old-data --confirm
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
