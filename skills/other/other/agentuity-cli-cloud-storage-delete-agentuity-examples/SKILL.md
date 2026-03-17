---
name: agentuity-cli-cloud-storage-delete
description: Delete a storage resource or file. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name] [filename]"
metadata:
  command: "agentuity cloud storage delete"
  tags: "destructive deletes-resource slow requires-auth requires-deployment"
---

# Cloud Storage Delete

Delete a storage resource or file

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud storage delete [name] [filename] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |
| `<filename>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | Yes | - | Skip confirmation prompts |

## Examples

Delete a storage bucket:

```bash
bunx @agentuity/cli cloud storage delete my-bucket
```

Delete a file from a bucket:

```bash
bunx @agentuity/cli cloud storage rm my-bucket file.txt
```

Interactive selection to delete a bucket:

```bash
bunx @agentuity/cli cloud storage delete
```

Dry-run: show what would be deleted without making changes:

```bash
bunx @agentuity/cli --dry-run cloud storage delete my-bucket
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
| `name` | string | Deleted bucket or file name |
