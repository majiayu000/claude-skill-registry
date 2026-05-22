---
name: agentuity-cli-cloud-sandbox-snapshot-tag
description: Add or update a tag on a snapshot. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<snapshotId> [tag]"
metadata:
  command: "agentuity cloud sandbox snapshot tag"
  tags: "slow requires-auth"
---

# Cloud Sandbox Snapshot Tag

Add or update a tag on a snapshot

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox snapshot tag <snapshotId> [tag] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<snapshotId>` | string | Yes | - |
| `<tag>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--clear` | boolean | Yes | - | Remove the tag from the snapshot |

## Examples

Tag a snapshot as "latest":

```bash
bunx @agentuity/cli cloud sandbox snapshot tag snp_abc123 latest
```

Remove a tag from a snapshot:

```bash
bunx @agentuity/cli cloud sandbox snapshot tag snp_abc123 --clear
```

## Output

Returns JSON object:

```json
{
  "snapshotId": "string",
  "tag": "unknown"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `snapshotId` | string | Snapshot ID |
| `tag` | unknown | New tag |
