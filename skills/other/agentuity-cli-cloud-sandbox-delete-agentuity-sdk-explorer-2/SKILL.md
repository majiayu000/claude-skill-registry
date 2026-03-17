---
name: agentuity-cli-cloud-sandbox-delete
description: Delete a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId>"
metadata:
  command: "agentuity cloud sandbox delete"
  tags: "destructive deletes-resource slow requires-auth"
---

# Cloud Sandbox Delete

Delete a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox delete <sandboxId> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | No | `false` | Skip confirmation prompt |

## Examples

Delete a sandbox:

```bash
bunx @agentuity/cli cloud sandbox delete abc123
```

Delete without confirmation prompt:

```bash
bunx @agentuity/cli cloud sandbox delete abc123 --confirm
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "sandboxId": "string",
  "durationMs": "number",
  "message": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `sandboxId` | string | Sandbox ID |
| `durationMs` | number | Operation duration in milliseconds |
| `message` | string | Status message |
