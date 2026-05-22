---
name: agentuity-cli-cloud-sandbox-download
description: Download files from a sandbox as a compressed archive. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> <output>"
metadata:
  command: "agentuity cloud sandbox download"
  tags: "slow requires-auth"
---

# Cloud Sandbox Download

Download files from a sandbox as a compressed archive

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox download <sandboxId> <output> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<output>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--path` | string | Yes | - | Path in sandbox to download (defaults to root) |
| `--format` | string | No | `"tar.gz"` | Archive format (zip or tar.gz) |

## Examples

Download sandbox files as tar.gz archive:

```bash
bunx @agentuity/cli cloud sandbox download sbx_abc123 ./backup.tar.gz
```

Download sandbox files as zip archive:

```bash
bunx @agentuity/cli cloud sandbox download sbx_abc123 ./backup.zip --format zip
```

Download only a specific directory:

```bash
bunx @agentuity/cli cloud sandbox download sbx_abc123 ./backup.tar.gz --path /subdir
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "output": "string",
  "bytes": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | - |
| `output` | string | - |
| `bytes` | number | - |
