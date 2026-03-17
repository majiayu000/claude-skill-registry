---
name: agentuity-cli-cloud-sandbox-run
description: "Run a one-shot command in a sandbox (creates, executes, destroys). Requires authentication. Use for Agentuity cloud platform operations"
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<command...>"
metadata:
  command: "agentuity cloud sandbox run"
  tags: "slow requires-auth"
---

# Cloud Sandbox Run

Run a one-shot command in a sandbox (creates, executes, destroys)

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox run <command...> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<command...>` | array | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--memory` | string | Yes | - | Memory limit (e.g., "500Mi", "1Gi") |
| `--cpu` | string | Yes | - | CPU limit in millicores (e.g., "500m", "1000m") |
| `--disk` | string | Yes | - | Disk limit (e.g., "500Mi", "1Gi") |
| `--network` | boolean | No | `false` | Enable outbound network access |
| `--timeout` | string | Yes | - | Execution timeout (e.g., "5m", "1h") |
| `--env` | array | Yes | - | Environment variables (KEY=VALUE) |
| `--file` | array | Yes | - | Files to create in sandbox (sandbox-path:local-path) |
| `--timestamps` | boolean | No | `false` | Include timestamps in output (default: true) |
| `--snapshot` | string | Yes | - | Snapshot ID or tag to restore from |
| `--dependency` | array | Yes | - | Apt packages to install (can be specified multiple times) |

## Examples

Run a simple command:

```bash
bunx @agentuity/cli cloud sandbox run -- echo "hello world"
```

Run with resource limits:

```bash
bunx @agentuity/cli cloud sandbox run --memory 1Gi --cpu 1000m -- bun run index.ts
```

Run with network access enabled:

```bash
bunx @agentuity/cli cloud sandbox run --network -- curl https://api.example.com
```

## Output

Returns JSON object:

```json
{
  "sandboxId": "string",
  "exitCode": "number",
  "durationMs": "number",
  "output": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sandboxId` | string | Sandbox ID |
| `exitCode` | number | Exit code from the process |
| `durationMs` | number | Duration in milliseconds |
| `output` | string | Combined stdout/stderr output |
