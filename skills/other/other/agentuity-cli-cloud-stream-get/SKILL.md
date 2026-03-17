---
name: agentuity-cli-cloud-stream-get
description: Get detailed information about a specific stream. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<id>"
metadata:
  command: "agentuity cloud stream get"
  tags: "read-only slow requires-auth"
---

# Cloud Stream Get

Get detailed information about a specific stream

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud stream get <id> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<id>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--output` | string | Yes | - | download stream content to file |

## Examples

Get stream details:

```bash
bunx @agentuity/cli stream get stream-id-123
```

Get stream as JSON:

```bash
bunx @agentuity/cli stream get stream-id-123 --json
```

Download stream to file:

```bash
bunx @agentuity/cli stream get stream-id-123 --output stream.dat
```

Download stream (short flag):

```bash
bunx @agentuity/cli stream get stream-id-123 -o stream.dat
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "name": "string",
  "metadata": "object",
  "url": "string",
  "sizeBytes": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stream ID |
| `name` | string | Stream name |
| `metadata` | object | Stream metadata |
| `url` | string | Public URL |
| `sizeBytes` | number | Size in bytes |
