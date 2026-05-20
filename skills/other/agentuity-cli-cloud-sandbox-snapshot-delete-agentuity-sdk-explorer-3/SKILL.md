---
name: agentuity-cli-cloud-sandbox-snapshot-delete
description: Delete a snapshot. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<snapshotId>"
metadata:
  command: "agentuity cloud sandbox snapshot delete"
  tags: "destructive deletes-resource slow requires-auth"
---

# Cloud Sandbox Snapshot Delete

Delete a snapshot

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox snapshot delete <snapshotId> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<snapshotId>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | No | `false` | Skip confirmation prompt |

## Examples

Delete a snapshot:

```bash
bunx @agentuity/cli cloud sandbox snapshot delete snp_abc123
```

Delete without confirmation prompt:

```bash
bunx @agentuity/cli cloud sandbox snapshot rm snp_abc123 --confirm
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "snapshotId": "string",
  "message": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `snapshotId` | string | Deleted snapshot ID |
| `message` | string | Status message |
