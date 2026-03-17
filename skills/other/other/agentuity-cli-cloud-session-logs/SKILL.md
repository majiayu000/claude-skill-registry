---
name: agentuity-cli-cloud-session-logs
description: Get logs for a specific session. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<session_id>"
metadata:
  command: "agentuity cloud session logs"
  tags: "read-only slow requires-auth"
---

# Cloud Session Logs

Get logs for a specific session

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud session logs <session_id> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<session_id>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--projectId` | string | Yes | - | Project ID (for display purposes) |
| `--deploymentId` | string | Yes | - | Deployment ID (for display purposes) |
| `--timestamps` | boolean | No | `true` | Show timestamps in output |

## Examples

View logs for session:

```bash
bunx @agentuity/cli cloud session logs sess_abc123xyz
```

Hide timestamps:

```bash
bunx @agentuity/cli cloud session logs sess_abc123xyz --no-timestamps
```

## Output

Returns: `array`
