---
name: agentuity-cli-cloud-queue-list
description: List all queues. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud queue list"
  tags: "read-only fast requires-auth"
---

# Cloud Queue List

List all queues

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--limit` | number | Yes | - | Maximum number of queues to return |
| `--offset` | number | Yes | - | Offset for pagination |

## Examples

List all queues:

```bash
bunx @agentuity/cli cloud queue list
```

List all queues (alias):

```bash
bunx @agentuity/cli cloud queue ls
```

## Output

Returns JSON object:

```json
{
  "queues": "array",
  "total": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `queues` | array | - |
| `total` | number | - |
