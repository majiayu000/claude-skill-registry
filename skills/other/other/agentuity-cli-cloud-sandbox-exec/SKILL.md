---
name: agentuity-cli-cloud-sandbox-exec
description: Execute a command in a running sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId> <command...>"
metadata:
  command: "agentuity cloud sandbox exec"
  tags: "slow requires-auth"
---

# Cloud Sandbox Exec

Execute a command in a running sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox exec <sandboxId> <command...> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |
| `<command...>` | array | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--timeout` | string | Yes | - | Execution timeout (e.g., "5m", "1h") |
| `--timestamps` | boolean | No | `false` | Include timestamps in output (default: false) |

## Examples

Execute a command in a sandbox:

```bash
bunx @agentuity/cli cloud sandbox exec abc123 -- echo "hello"
```

Execute with timeout:

```bash
bunx @agentuity/cli cloud sandbox exec abc123 --timeout 5m -- bun run build
```

## Output

Returns JSON object:

```json
{
  "executionId": "string",
  "status": "string",
  "exitCode": "number",
  "durationMs": "number",
  "output": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `executionId` | string | Unique execution identifier |
| `status` | string | Execution status |
| `exitCode` | number | Exit code (if completed) |
| `durationMs` | number | Duration in milliseconds (if completed) |
| `output` | string | Combined stdout/stderr output |
