---
name: agentuity-cli-cloud-queue-stats
description: View queue analytics and statistics. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name]"
metadata:
  command: "agentuity cloud queue stats"
  tags: "read-only requires-auth"
---

# Cloud Queue Stats

View queue analytics and statistics

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud queue stats [name] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--live` | boolean | No | `false` | Stream real-time stats |
| `--interval` | number | No | `5` | Refresh interval in seconds (for --live) |
| `--start` | string | Yes | - | Start time (ISO 8601) |
| `--end` | string | Yes | - | End time (ISO 8601) |
| `--granularity` | string | Yes | - | Time granularity |

## Examples

View org-level analytics for all queues:

```bash
bunx @agentuity/cli cloud queue stats
```

View detailed analytics for a specific queue:

```bash
bunx @agentuity/cli cloud queue stats --name my-queue
```

Stream real-time stats (Ctrl+C to exit):

```bash
bunx @agentuity/cli cloud queue stats --live
```

Stream queue stats every 10 seconds:

```bash
bunx @agentuity/cli cloud queue stats --name my-queue --live --interval 10
```
