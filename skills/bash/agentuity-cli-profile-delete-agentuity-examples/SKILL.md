---
name: agentuity-cli-profile-delete
description: Delete a configuration profile
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name]"
metadata:
  command: "agentuity profile delete"
  tags: "destructive deletes-resource fast"
---

# Profile Delete

Delete a configuration profile

## Usage

```bash
agentuity profile delete [name] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | Yes | - | Skip confirmation prompt |

## Examples

Delete item:

```bash
bunx @agentuity/cli profile delete staging
```

Use confirm option:

```bash
bunx @agentuity/cli profile delete old-dev --confirm
```

Delete item:

```bash
bunx @agentuity/cli profile delete
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
| `name` | string | Deleted profile name |
