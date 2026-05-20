---
name: agentuity-cli-cloud-stream-list
description: List recent streams with optional filtering. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud stream list"
  tags: "read-only slow requires-auth"
---

# Cloud Stream List

List recent streams with optional filtering

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud stream list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--size` | number | Yes | - | maximum number of streams to return (default: 100) |
| `--offset` | number | Yes | - | number of streams to skip for pagination |
| `--name` | string | Yes | - | filter by stream name |
| `--metadata` | string | Yes | - | filter by metadata (format: key=value or key1=value1,key2=value2) |

## Examples

List all streams:

```bash
bunx @agentuity/cli cloud stream list
```

List 50 most recent streams:

```bash
bunx @agentuity/cli cloud stream ls --size 50
```

Filter by name:

```bash
bunx @agentuity/cli cloud stream list --name agent-logs
```

Filter by metadata:

```bash
bunx @agentuity/cli cloud stream list --metadata type=export
```

Output as JSON:

```bash
bunx @agentuity/cli cloud stream ls --json
```

## Output

Returns JSON object:

```json
{
  "streams": "array",
  "total": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `streams` | array | List of streams |
| `total` | number | Total count of matching streams |
