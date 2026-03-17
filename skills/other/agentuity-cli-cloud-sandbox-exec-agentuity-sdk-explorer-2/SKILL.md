---
name: agentuity-cli-cloud-sandbox-execution-get
description: Get information about a specific execution. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<executionId>"
metadata:
  command: "agentuity cloud sandbox execution get"
  tags: "read-only fast requires-auth"
---

# Cloud Sandbox Execution Get

Get information about a specific execution

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox execution get <executionId>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<executionId>` | string | Yes | - |

## Examples

Get execution information:

```bash
bunx @agentuity/cli cloud sandbox execution get exec_abc123
```

## Output

Returns JSON object:

```json
{
  "executionId": "string",
  "sandboxId": "string",
  "status": "string",
  "command": "array",
  "exitCode": "number",
  "durationMs": "number",
  "startedAt": "string",
  "completedAt": "string",
  "error": "string",
  "stdoutStreamUrl": "string",
  "stderrStreamUrl": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `executionId` | string | Execution ID |
| `sandboxId` | string | Sandbox ID |
| `status` | string | Current status |
| `command` | array | Command that was executed |
| `exitCode` | number | Exit code |
| `durationMs` | number | Duration in milliseconds |
| `startedAt` | string | Start timestamp |
| `completedAt` | string | Completion timestamp |
| `error` | string | Error message if failed |
| `stdoutStreamUrl` | string | URL to stream stdout |
| `stderrStreamUrl` | string | URL to stream stderr |
