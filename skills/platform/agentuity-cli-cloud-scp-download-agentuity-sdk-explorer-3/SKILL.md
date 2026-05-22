---
name: agentuity-cli-cloud-scp-download
description: Download a file using security copy. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<source> [destination]"
metadata:
  command: "agentuity cloud scp download"
  tags: "read-only slow requires-auth requires-deployment"
---

# Cloud Scp Download

Download a file using security copy

## Prerequisites

- Authenticated with `agentuity auth login`
- cloud deploy

## Usage

```bash
agentuity cloud scp download <source> [destination] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<source>` | string | Yes | - |
| `<destination>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--identifier` | string | Yes | - | The project or deployment id to use |

## Examples

Download to current directory:

```bash
bunx @agentuity/cli cloud scp download /var/log/app.log
```

Download to specific path:

```bash
bunx @agentuity/cli cloud scp download /var/log/app.log ./logs/
```

Download from specific project:

```bash
bunx @agentuity/cli cloud scp download /app/config.json --identifier=proj_abc123xyz
```

Download multiple files:

```bash
bunx @agentuity/cli cloud scp download ~/logs/*.log ./logs/
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "source": "string",
  "destination": "string",
  "identifier": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether download succeeded |
| `source` | string | Remote source path |
| `destination` | string | Local destination path |
| `identifier` | string | Project or deployment identifier |
