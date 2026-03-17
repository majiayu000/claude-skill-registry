---
name: agentuity-cli-project-delete
description: Delete a project. Requires authentication. Use for project management operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[id]"
metadata:
  command: "agentuity project delete"
  tags: "destructive deletes-resource slow requires-auth"
---

# Project Delete

Delete a project

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity project delete [id] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<id>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | Yes | - | Skip confirmation prompts |

## Examples

Delete item:

```bash
bunx @agentuity/cli project delete
```

Delete item:

```bash
bunx @agentuity/cli project delete proj_abc123def456
```

Use confirm option:

```bash
bunx @agentuity/cli project delete proj_abc123def456 --confirm
```

Delete item:

```bash
bunx @agentuity/cli project rm proj_abc123def456
```

Delete item:

```bash
bunx @agentuity/cli --explain project delete proj_abc123def456
```

Delete item:

```bash
bunx @agentuity/cli --dry-run project delete proj_abc123def456
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "projectIds": "array",
  "count": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the deletion succeeded |
| `projectIds` | array | Deleted project IDs |
| `count` | number | Number of projects deleted |
