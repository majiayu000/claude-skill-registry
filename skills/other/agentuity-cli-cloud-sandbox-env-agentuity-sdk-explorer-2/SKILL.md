---
name: agentuity-cli-cloud-sandbox-env
description: Set or delete environment variables on a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> [vars...]"
metadata:
  command: "agentuity cloud sandbox env"
  tags: "slow requires-auth"
---

# Cloud Sandbox Env

Set or delete environment variables on a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox env <sandboxId> [vars...] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<vars...>` | array | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--delete` | array | Yes | - | Environment variable names to delete |

## Examples

Set an environment variable:

```bash
bunx @agentuity/cli cloud sandbox env sbx_abc123 MY_VAR=value
```

Set multiple environment variables:

```bash
bunx @agentuity/cli cloud sandbox env sbx_abc123 VAR1=value1 VAR2=value2
```

Delete an environment variable:

```bash
bunx @agentuity/cli cloud sandbox env sbx_abc123 --delete MY_VAR
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "env": "object"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | - |
| `env` | object | - |
