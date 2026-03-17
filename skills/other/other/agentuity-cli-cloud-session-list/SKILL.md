---
name: agentuity-cli-cloud-session-list
description: List recent sessions. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud session list"
  tags: "read-only fast requires-auth"
---

# Cloud Session List

List recent sessions

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud session list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--count` | number | No | `10` | Number of sessions to list (1–100) |
| `--projectId` | string | Yes | - | Filter by project ID |
| `--deploymentId` | string | Yes | - | Filter by deployment ID |
| `--trigger` | string | Yes | - | Filter by trigger type (api, cron, webhook) |
| `--env` | string | Yes | - | Filter by environment |
| `--threadId` | string | Yes | - | Filter by thread ID |
| `--agentIdentifier` | string | Yes | - | Filter by agent identifier |
| `--devmode` | boolean | Yes | - | Filter by dev mode (true/false) |
| `--success` | boolean | Yes | - | Filter by success status (true/false) |
| `--startAfter` | string | Yes | - | Filter by start time after (ISO 8601) |
| `--startBefore` | string | Yes | - | Filter by start time before (ISO 8601) |

## Examples

List 10 most recent sessions:

```bash
bunx @agentuity/cli cloud session list
```

List 25 most recent sessions:

```bash
bunx @agentuity/cli cloud session list --count=25
```

Filter by project:

```bash
bunx @agentuity/cli cloud session list --project-id=proj_*
```

Filter by deployment:

```bash
bunx @agentuity/cli cloud session list --deployment-id=*
```

Only successful sessions:

```bash
bunx @agentuity/cli cloud session list --success=true
```

Only production sessions:

```bash
bunx @agentuity/cli cloud session list --devmode=false
```

Only API triggered sessions:

```bash
bunx @agentuity/cli cloud session list --trigger=api
```

Only production environment:

```bash
bunx @agentuity/cli cloud session list --env=production
```

## Output

Returns: `array`
