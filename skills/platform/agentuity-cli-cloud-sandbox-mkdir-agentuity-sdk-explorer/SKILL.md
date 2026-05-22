---
name: agentuity-cli-cloud-sandbox-mkdir
description: Create a directory in a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> <path>"
metadata:
  command: "agentuity cloud sandbox mkdir"
  tags: "slow requires-auth"
---

# Cloud Sandbox Mkdir

Create a directory in a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox mkdir <sandboxId> <path> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<path>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--parents` | boolean | No | `false` | Create parent directories as needed |

## Examples

Create a directory in the sandbox:

```bash
bunx @agentuity/cli cloud sandbox mkdir sbx_abc123 /path/to/dir
```

Create nested directories recursively:

```bash
bunx @agentuity/cli cloud sandbox mkdir sbx_abc123 /path/to/nested/dir -p
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "path": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | - |
| `path` | string | - |
