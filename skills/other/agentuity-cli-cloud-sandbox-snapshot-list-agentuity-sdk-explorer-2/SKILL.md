---
name: agentuity-cli-cloud-sandbox-snapshot-list
description: List snapshots. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud sandbox snapshot list"
  tags: "slow requires-auth"
---

# Cloud Sandbox Snapshot List

List snapshots

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox snapshot list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--sandbox` | string | Yes | - | Filter by sandbox ID |
| `--limit` | number | Yes | - | Maximum number of results |
| `--offset` | number | Yes | - | Offset for pagination |

## Examples

List all snapshots:

```bash
bunx @agentuity/cli cloud sandbox snapshot list
```

List snapshots for a specific sandbox:

```bash
bunx @agentuity/cli cloud sandbox snapshot list --sandbox sbx_abc123
```

## Output

Returns JSON object:

```json
{
  "snapshots": "array",
  "total": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `snapshots` | array | List of snapshots |
| `total` | number | Total number of snapshots |
