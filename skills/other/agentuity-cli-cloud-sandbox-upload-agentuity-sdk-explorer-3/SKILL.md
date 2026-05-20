---
name: agentuity-cli-cloud-sandbox-upload
description: Upload a compressed archive to a sandbox and extract it. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> <archive>"
metadata:
  command: "agentuity cloud sandbox upload"
  tags: "slow requires-auth"
---

# Cloud Sandbox Upload

Upload a compressed archive to a sandbox and extract it

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox upload <sandboxId> <archive> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<archive>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--path` | string | Yes | - | Destination path in sandbox (defaults to root) |
| `--format` | string | Yes | - | Archive format (auto-detected if not specified) |

## Examples

Upload and extract a tar.gz archive to sandbox root:

```bash
bunx @agentuity/cli cloud sandbox upload sbx_abc123 ./archive.tar.gz
```

Upload and extract a zip archive to a specific directory:

```bash
bunx @agentuity/cli cloud sandbox upload sbx_abc123 ./archive.zip --path /subdir
```

Upload with explicit format specification:

```bash
bunx @agentuity/cli cloud sandbox upload sbx_abc123 ./archive.bin --format tar.gz
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "bytes": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | - |
| `bytes` | number | - |
