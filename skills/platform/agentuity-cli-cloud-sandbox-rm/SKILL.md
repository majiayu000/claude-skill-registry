---
name: agentuity-cli-cloud-sandbox-rm
description: Remove a file from a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> <path>"
metadata:
  command: "agentuity cloud sandbox rm"
  tags: "slow requires-auth"
---

# Cloud Sandbox Rm

Remove a file from a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox rm <sandboxId> <path>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<path>` | string | Yes | - |

## Examples

Remove a file from the sandbox:

```bash
bunx @agentuity/cli cloud sandbox rm sbx_abc123 /path/to/file.txt
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
