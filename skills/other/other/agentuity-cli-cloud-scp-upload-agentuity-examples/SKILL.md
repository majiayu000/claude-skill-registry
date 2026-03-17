---
name: agentuity-cli-cloud-scp-upload
description: Upload a file using security copy. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<source> [destination]"
metadata:
  command: "agentuity cloud scp upload"
  tags: "mutating updates-resource slow requires-auth requires-deployment"
---

# Cloud Scp Upload

Upload a file using security copy

## Prerequisites

- Authenticated with `agentuity auth login`
- cloud deploy

## Usage

```bash
agentuity cloud scp upload <source> [destination] [options]
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

Upload to remote home directory:

```bash
bunx @agentuity/cli cloud scp upload ./config.json
```

Upload to specific path:

```bash
bunx @agentuity/cli cloud scp upload ./config.json /app/config.json
```

Upload to specific project:

```bash
bunx @agentuity/cli cloud scp upload ./config.json --identifier=proj_abc123xyz
```

Upload multiple files:

```bash
bunx @agentuity/cli cloud scp upload ./logs/*.log ~/logs/
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
| `success` | boolean | Whether upload succeeded |
| `source` | string | Local source path |
| `destination` | string | Remote destination path |
| `identifier` | string | Project or deployment identifier |
