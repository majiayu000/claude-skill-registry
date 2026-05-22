---
name: agentuity-cli-cloud-sandbox-runtime-list
description: List available sandbox runtimes. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud sandbox runtime list"
  tags: "read-only slow requires-auth"
---

# Cloud Sandbox Runtime List

List available sandbox runtimes

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox runtime list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--limit` | number | Yes | - | Maximum number of results |
| `--offset` | number | Yes | - | Offset for pagination |

## Examples

List all available runtimes:

```bash
bunx @agentuity/cli cloud sandbox runtime list
```

## Output

Returns JSON object:

```json
{
  "runtimes": "array",
  "total": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `runtimes` | array | List of runtimes |
| `total` | number | Total number of runtimes |
