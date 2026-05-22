---
name: agentuity-cli-cloud-sandbox-snapshot-get
description: Get snapshot details. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<snapshotId>"
metadata:
  command: "agentuity cloud sandbox snapshot get"
  tags: "slow requires-auth"
---

# Cloud Sandbox Snapshot Get

Get snapshot details

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox snapshot get <snapshotId>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<snapshotId>` | string | Yes | - |

## Examples

Get details for a snapshot:

```bash
bunx @agentuity/cli cloud sandbox snapshot get snp_abc123
```

## Output

Returns JSON object:

```json
{
  "snapshotId": "string",
  "tag": "unknown",
  "sizeBytes": "number",
  "fileCount": "number",
  "parentSnapshotId": "unknown",
  "createdAt": "string",
  "downloadUrl": "string",
  "files": "array",
  "sandboxes": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `snapshotId` | string | Snapshot ID |
| `tag` | unknown | Snapshot tag |
| `sizeBytes` | number | Snapshot size in bytes |
| `fileCount` | number | Number of files |
| `parentSnapshotId` | unknown | Parent snapshot ID |
| `createdAt` | string | Creation timestamp |
| `downloadUrl` | string | Presigned download URL |
| `files` | array | Files in snapshot |
| `sandboxes` | array | Attached sandboxes (idle or running) |
