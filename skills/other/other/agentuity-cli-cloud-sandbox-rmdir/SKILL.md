---
name: agentuity-cli-cloud-sandbox-rmdir
description: Remove a directory from a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> <path>"
metadata:
  command: "agentuity cloud sandbox rmdir"
  tags: "slow requires-auth"
---

# Cloud Sandbox Rmdir

Remove a directory from a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox rmdir <sandboxId> <path> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<path>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--recursive` | boolean | No | `false` | Remove directory and all contents |

## Examples

Remove an empty directory from the sandbox:

```bash
bunx @agentuity/cli cloud sandbox rmdir sbx_abc123 /path/to/dir
```

Remove a directory and all its contents recursively:

```bash
bunx @agentuity/cli cloud sandbox rmdir sbx_abc123 /path/to/dir -r
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
